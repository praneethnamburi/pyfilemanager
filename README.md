# pyfilemanager

[![src](https://img.shields.io/badge/src-github-blue)](https://github.com/praneethnamburi/pyfilemanager)
[![PyPI - Version](https://img.shields.io/pypi/v/pyfilemanager.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pyfilemanager/)
[![Documentation Status](https://readthedocs.org/projects/pyfilemanager/badge/?version=latest)](https://pyfilemanager.readthedocs.io)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/praneethnamburi/pyfilemanager/main/LICENSE)


*Easy to use file search and file path management in python.*


## Installation

`pyfilemanager` can be installed through pip or conda.

```sh
pip install pyfilemanager

# or

conda install conda-forge::pyfilemanager
```

## Quickstart

```python
from pyfilemanager import FileManager

# one-liner to retrieve videos in the canon folder
canon_videos = FileManager(r'C:\videos').add()['canon/*Camera.avi']

# or, work with tags
fm.add('canon', '*Camera.avi', include='canon')
canon_videos = fm['canon']
```

## Usage
Consider the following directory structure

```
C:\videos
├── sony
│   ├── 142Camera.avi
│   ├── 143Camera.avi
│   ├── notes.txt
├── panasonic
│   ├── 151Camera.avi
│   ├── 143Camera.avi
│   ├── notes.txt
├── panasonic2
│   ├── 201Camera.avi
│   ├── 202.mp4
├── canon
│   ├── 51Camera.avi
│   ├── 40Camera.avi
│   ├── notes.txt
├── notes
│   ├── notes1.txt
│   ├── notes2.txt
```

0. Import the FileManager class.
   ```python
   from pyfilemanager import FileManager
   ```
1. Initialize the file manager.
   ```python
   fm = FileManager(r'C:\videos', exclude_hidden=True)
   ```
2. Add files based on different inclusion and exclusion criteria. Use the include parameter to keep file paths that contain **all** of the supplied strings *anywhere* in the file path. Use the exclude parameter to disregard file paths that contain **any** of the supplied string anywhere in the file path.
   ```python
    fm.add()
    # add all files in the directory under the tag 'all'
    # achieves the same result as fm.add('all') and fm.add('*.*')

    fm.add('*.avi')
    # add all files with extension .avi under the tag 'avi'
    # this is short for fm.add('avi', '*.avi'), and only works for patterns that start with *.

    fm.add('canon', '*Camera.avi', include='canon')
    # include=canon means that file path must contain canon

    fm.add('sony42', '*Camera.avi', include=['sony', '42'])
    # file path must contain sony AND 42
    # grabs one file - sony\142Camera.avi
    
    fm.add('videos', ['*.avi', '*.mp4'])
    # add multiple conditions by supplying them as a list or tuple
    
    fm.add('panasonic', '*.avi', include='panasonic', exclude='panasonic2')
    # grab videos in the panasonic folder
    
    fm.add('notes', 'notes*.txt')
    # grab all notes

    fm.add('notes', 'notes*.txt', include='notes\\notes')
    # grab notes from the notes folder
    # this will overwrite the previous notes entry

    fm.add('notes', 'notes*.txt', exclude=['sony', 'panasonic', 'panasonic2', 'canon'])
    # achieves the same result as the previous line

    fm.add_by_depth(max_depth=1)
    # creates the tags 'files0' and 'files1' (new in v1.1)
    # files0 tag will contain paths for files in the base directory (0 entries)
    # files1 tag will contain paths for files in the immediate sub-directories (13 entries)
    ```
3. Retrieve file paths using a dict-like convention.
   ```python
    fm['canon']
    # Retrieve by the tag 'canon'
    # Returns canon/40Camera.avi and canon/51Camera.avi

    fm['143Camera']
    # When a tag is not found, retrieve file paths by an exact match to the file stem.
    # Returns panasonic/143Camera.avi and sony/143Camera.avi

    fm['20']
    # If the key doesn't match a tag or a stem of a filename, do a loose-search to retrieve all entries where the tag is anywhere in the full path.
    # Returns panasonic2/201Camera.avi and panasonic2/202.mp4

    fm['notes?.txt']
    # Search for files using special chracters *, ?, !, [] specified in fnmatch
    # Returns notes/notes1.txt and notes/notes2.txt
    ```
4. Add and retrieve in one line of code. 
   ```python
   fm.add('canon', '*Camera.avi', include='canon')['canon']
   # Note that the method returns the instance of the FileManager object. 
   ```
5. Retrieve all the added keys using fm.**get_tags**()
   ```python
   fm.get_tags()
   # returns a list ['canon', 'sony42', 'videos', 'panasonic', 'notes']
   ```
6. Retrieve paths of all the added files.
   ```python
   fm.all_files
   ```
7. Get a report of the number of files, and the occupied space.
   ```python
    fm.report()
    ```
    ```console
    2 canon files taking up 0.000 MB
    1 sony42 files taking up 0.000 MB
    8 videos files taking up 0.000 MB
    2 panasonic files taking up 0.000 MB
    5 txt files taking up 0.000 MB
    ```

## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

[Praneeth Namburi](https://praneethnamburi.com)

Project Link: [https://github.com/praneethnamburi/pyfilemanager](https://github.com/praneethnamburi/pyfilemanager)


## Acknowledgments

This tool was developed as part of the ImmersionToolbox initiative at the [MIT.nano Immersion Lab](https://immersion.mit.edu). Thanks to NCSOFT for supporting this initiative.
