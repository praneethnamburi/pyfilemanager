import os
import fnmatch
from pathlib import Path

class FileManager:
    """
    Easy to use file search and file path management. Useful for managing files in not-so-obviously organized folders.

    Usage: 
        TL;DR
        from pyFileManager import FileManager
        video_list = FileManager(r'C:\videos').add('video', '*.avi', include=['sony', 'panasonic'], exclude='canon')['video']

        Long version
        Consider the following file structure in C:\videos directory
        C:\videos
        -- sony
           -- 142Camera.avi
           -- 143Camera.avi
           -- notes.txt
        -- panasonic
           -- 151Camera.avi
           -- 152Camera.avi
           -- notes.txt
        -- panasonic2
           -- 201Camera.avi
           -- 202.mp4
        -- canon
           -- 51Camera.avi
           -- 40Camera.avi
           -- notes.txt
        -- notes
           -- notes1.txt
           -- notes2.txt
        1. Initialize the file manager
            fm = FileManager(r'C:\videos')
        2. Add files of different types with different inclusion and exclusion criteria
            fm.add('video', '*Camera.avi', include=['sony', 'panasonic'], exclude='canon')
            fm.add('video', '*.mp4', include='panasonic') # to include 202.mp4 in the panasonic2 folder
            fm.add('canon', '*Camera.avi', include='canon')
            fm.add('notes', 'notes*.txt')
        3. Retrieve the file list
            canon_videos = fm['canon']
            other_videos = fm['video']
        4. Generate a report for the different file types (number of files, and space occupied)
            fm.report()
    """
    def __init__(self, base_dir, exclude_hidden=True):
        assert isinstance(base_dir, str)
        self.base_dir = os.path.realpath(base_dir)
        self._files = {}
        self._filters = {}
        self._inclusions = {}
        self._exclusions = {}
        assert isinstance(exclude_hidden, bool)
        self._exclude_hidden = exclude_hidden
    
    def add(self, type_name, pattern_list, include=None, exclude=None, exclude_hidden=None):
        """
        Add a type of file with a given filter.
        e.g. fm.add('video', '*Camera*.avi')
        """
        if exclude_hidden is None: # None means not specified. In this case, set it to the global default.
            exclude_hidden = self._exclude_hidden
        if isinstance(pattern_list, str):
            pattern_list = [pattern_list]
        self._files[type_name] = []
        for pattern in pattern_list:
            self._files[type_name] += self._find(pattern, path=self.base_dir, exclude_hidden=exclude_hidden)
        self._filters[type_name] = pattern_list
        self._inclusions[type_name] = []
        self._exclusions[type_name] = []

        if include is not None:
            if isinstance(include, str):
                self._include(type_name, include)
            else:
                assert isinstance(include, (list, tuple))
                for inc_str in include:
                    assert isinstance(inc_str, str)
                    self._include(type_name, inc_str)
        
        if exclude is not None:
            if isinstance(exclude, str):
                self._exclude(type_name, exclude)
            else:
                assert isinstance(exclude, (list, tuple))
                for exc_str in exclude:
                    assert isinstance(exc_str, str)
                    self._exclude(type_name, exc_str)
        
        return self # for chaining commands

    def _include(self, type_name, inclusion_string):
        """
        Include a set of files from the list. Useful for choosing files in specific sub-folders.
        Use this functionality using the add method.
        """
        assert type_name in self._files
        self._files[type_name] = [fn for fn in self._files[type_name] if inclusion_string in fn]
        self._inclusions[type_name].append(inclusion_string)

    def _exclude(self, type_name, exclusion_string):
        """
        Exclude a set of files from the list. Useful for ignoring files in specific sub-folders.
        Use this functionality using the add method.
        """
        assert type_name in self._files
        self._files[type_name] = [fn for fn in self._files[type_name] if exclusion_string not in fn]
        self._exclusions[type_name].append(exclusion_string)

    def __getitem__(self, key):
        if key in self._files:
            return self._files[key]
        all_files = self.all_files
        stem_to_path = {Path(x).stem:x for x in all_files}
        # full-stem search
        if key in stem_to_path:
            return stem_to_path[key]
        # loose search - full path contains
        return [x for x in all_files if key in x]
        
    
    def types(self):
        return self._files.keys()

    @property
    def all_files(self):
        ret = []
        for ftype in self.types():
            ret += self[ftype]
        return ret

    def report(self, units='MB'):
        for file_type, file_list in self._files.items():
            fs = sum(list(self._file_size(file_list, units=units).values()))
            print(str(len(file_list)) + ' ' + file_type + ' files taking up {:4.3f} '.format(fs) + units)
    
    @staticmethod
    def _find(pattern, path=None, exclude_hidden=True):
        "Example: find('*.txt', '/path/to/dir')"
        if path is None:
            path = os.getcwd()
        
        # this bit is from stack overflow
        result = []
        for root, _, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))

        if exclude_hidden:
            return [r for r in result if not (r.split(os.sep)[-1].startswith('~$') or r.split(os.sep)[-1].startswith('.'))]
        return result
    
    @staticmethod
    def _file_size(file_list, units='MB'):
        """
        Returns files sizes in descending order (default: megabytes)
        """
        div = {'B':1, 'KB':1024, 'MB':1024**2, 'GB':1024**3, 'TB':1024**4}
        if isinstance(file_list, str):
            file_list = [file_list]
        assert isinstance(file_list, list)
        size_mb = {os.path.getsize(f)/div[units]:f for f in file_list} # {size: file_name}
        size_list = list(size_mb.keys())
        size_list.sort(reverse=True)
        return {size_mb[s]:s for s in size_list} # {file_name : size}
    