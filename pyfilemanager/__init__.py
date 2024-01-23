from __future__ import annotations

import os
import fnmatch
from pathlib import Path
from typing import Union


class FileManager:
    """
    Easy to use file search and file path management.
    Add files using different inclusion and exclusion criteria under a 'tag'.
    Provides dictionary-like access to file-paths where the tags serve as keys.
    Useful for managing files in not-so-obviously organized folders.

    Args:
        base_dir (str): base directory for file search
        exclude_hidden (bool, optional): excludes hidden files when True. Defaults to True.

    Attributes:
        base_dir (str): base directory for file search

        _files (dict): {Tag: List of file paths}
        _filters (dict): {Tag: pattern list}
        _inclusions (dict): {Tag: inclusion criteria}
        _exclusions (dict): {Tag: exclusion criteria}
    
    IGNORE:
    Methods:
        add: Add files based on different inclusion and exclusion criteria.
        get_tags: Return a list of tags created using the add method.
        report: Print a report summarizing the size occupied by files under each tag.
        remove: Remove file paths stored under a given tag. May not be very useful.
        __getitem__: overloaded.

        _find: Core method for finding files based on os.walk and fnmatch.
        _include, _exclude: Utilities used by the add method.
    IGNORE
    """    
    def __init__(self, base_dir: str, exclude_hidden: bool=True):
        assert isinstance(base_dir, str)
        self.base_dir = os.path.realpath(base_dir)
        self._files = {}
        self._filters = {}
        self._inclusions = {}
        self._exclusions = {}
        assert isinstance(exclude_hidden, bool)
        self._exclude_hidden = exclude_hidden
    
    def add(self, tag: str, pattern_list: Union[str,list], include: Union[str,list]=None, exclude: Union[str,list]=None, exclude_hidden: bool=None) -> FileManager:
        """Add files based on different inclusion and exclusion criteria.

        Example:
            ``fm.add('video', '*Camera*.avi')``

        Args:
            tag (str): e.g. 'video_files'
            pattern_list (Union[str,list]): e.g. '*.avi', ['*.avi', '*.mp4']
            include (Union[str,list], optional): Keep file paths that contain **all** of the supplied strings *anywhere* in the file path. Defaults to None.
            exclude (Union[str,list], optional): Disregard file paths that contain **any** of the supplied string anywhere in the file path. Defaults to None.
            exclude_hidden (bool, optional): Set the state for excluding hidden files. Defaults to the value of _exclude_hidden attribute, which defaults to True.

        Returns:
            FileManager: Returns self. Useful for chaining commands.
        """
        if exclude_hidden is None: # None means not specified. In this case, set it to the global default.
            exclude_hidden = self._exclude_hidden
        
        if isinstance(pattern_list, str):
            pattern_list = [pattern_list]
        
        self._files[tag] = []
        
        for pattern in pattern_list:
            self._files[tag] += self._find(pattern, path=self.base_dir, exclude_hidden=exclude_hidden)
        
        self._filters[tag] = pattern_list
        self._inclusions[tag] = []
        self._exclusions[tag] = []

        if include is not None:
            if isinstance(include, str):
                self._include(tag, include)
            else:
                assert isinstance(include, (list, tuple))
                for inc_str in include:
                    assert isinstance(inc_str, str)
                    self._include(tag, inc_str)
        
        if exclude is not None:
            if isinstance(exclude, str):
                self._exclude(tag, exclude)
            else:
                assert isinstance(exclude, (list, tuple))
                for exc_str in exclude:
                    assert isinstance(exc_str, str)
                    self._exclude(tag, exc_str)
        
        return self # for chaining commands
    
    def remove(self, tag: str) -> None:
        """Remove file paths stored under the given tag.

        Args:
            tag (str): A tag created when using the add method.

        Raises:
            ValueError: If an unknown tag is supplied.
        """
        if tag in self._files:
            del self._files[tag]
        else:
            raise ValueError(f'Unknown type {tag}')

    def _include(self, tag: str, inclusion_string: str) -> None:
        """Include a set of files from the list. Useful for choosing files in specific sub-folders.
        Use this functionality using the add method.

        Args:
            tag (str): A tag created when using the add method.
            inclusion_string (str): File paths containing this string anywhere in the path will be kept.
        """        
        assert tag in self._files
        self._files[tag] = [fn for fn in self._files[tag] if inclusion_string in fn]
        self._inclusions[tag].append(inclusion_string)

    def _exclude(self, tag: str, exclusion_string: str):
        """Exclude a set of files from the list. Useful for ignoring files in specific sub-folders.
        Use this functionality using the add method.

        Args:
            tag (str): A tag created when using the add method.
            exclusion_string (str): File paths containing this string anywhere in the path will be removed.
        """
        assert tag in self._files
        self._files[tag] = [fn for fn in self._files[tag] if exclusion_string not in fn]
        self._exclusions[tag].append(exclusion_string)

    def __getitem__(self, key: str) -> list:
        """Retrieve file paths based on - 

            (1) tag
            (2) exact match for the 'stem' of the file
            (3) key is anywhere in the path 

            Try (2) only if (1) doesn't return any results, and try (3) only if (2) doesn't return any results.

        Args:
            key (str): Either a tag, filename, or partial match.

        Returns:
            list: List of file paths.
        """        
        # (1) by tag
        if key in self._files:
            return self._files[key]
        
        # (2) full-stem search
        all_files = self.all_files
        stem_to_path = {Path(x).stem:[] for x in all_files} # in case there are multiiple files with the same 'stem'
        for file_name in all_files:
            stem_to_path[Path(file_name).stem].append(file_name)
        if key in stem_to_path:
            return stem_to_path[key]
        
        # (3) loose search - full path contains
        return self._unique_sorted([x for x in all_files if key in x])
        
    
    def get_tags(self) -> list:
        """Return a list of tags created using the add method.

        Returns:
            list: List of tags.
        """        
        return list(self._files.keys())

    @property
    def all_files(self) -> list:
        """Return a list of all files managed by the filemanager. Remove duplicates.

        Returns:
            list: List of file paths
        """
        ret = []
        for ftype in self.get_tags():
            ret += self[ftype]
        return self._unique_sorted(ret)

    def report(self, units: str='MB') -> None:
        """Print a report summarizing the size occupied by files under each tag.

        Args:
            units (str, optional): One of ('B', 'KB', 'MB', 'GB', 'TB). B is for bytes. Defaults to 'MB'.
        """        
        for file_type, file_list in self._files.items():
            fs = sum(list(self._file_size(file_list, units=units).values()))
            print(str(len(file_list)) + ' ' + file_type + ' files taking up {:4.3f} '.format(fs) + units)
    
    @staticmethod
    def _find(pattern: str, path: str=None, exclude_hidden: bool=True) -> list:
        """Core method for finding files based on ``os.walk`` and ``fnmatch``.

        Example:
            ``FileManager._find('*.txt', '/path/to/dir')``

        Args:
            pattern (str): Input for fnmatch.
            path (str, optional): Search for files in this path. Defaults to the results of os.getcwd().
            exclude_hidden (bool, optional): Whether to include filenames of hidden files. Defaults to True.

        Returns:
            list: List of file names.
        """
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
    def _file_size(file_list: list, units: str='MB') -> dict:
        """Returns files sizes in descending order (default: megabytes). Used by the report method.

        Args:
            file_list (list): list of file names
            units (str, optional): One of ('B', 'KB', 'MB', 'GB', 'TB). B is for bytes. Defaults to 'MB'.

        Returns:
            dict: {file_name : size}
        """
        div = {'B':1, 'KB':1024, 'MB':1024**2, 'GB':1024**3, 'TB':1024**4}
        if isinstance(file_list, str):
            file_list = [file_list]
        assert isinstance(file_list, list)
        size_mb = {os.path.getsize(f)/div[units]:f for f in file_list} # {size: file_name}
        size_list = list(size_mb.keys())
        size_list.sort(reverse=True)
        return {size_mb[s]:s for s in size_list} # {file_name : size}
    
    @staticmethod
    def _unique_sorted(file_list: list) -> list:
        """Utility to return a sorted list of unique items in the input list.

        Args:
            file_list (list): Expected to be a list of strings (file names).

        Returns:
            list: List of unique elements (file names).
        """        
        ret = list(set(file_list))
        ret.sort()
        return ret
    