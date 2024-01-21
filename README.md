# pyfilemanager

*Easy to use file search and file path management in python.*


## Installation

```sh
pip install pyfilemanager
```

## Usage

### Quickstart

```python
from pyfilemanager import FileManager
fm = FileManager(r'C:\videos')
fm.add('canon', '*Camera.avi', include='canon')
video_list = fm['video']
```

### Long version
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

1. Initialize the file manager.
   ```python
   fm = FileManager(r'C:\videos', exclude_hidden=True)
   ```
2. Add files based on different inclusion and exclusion criteria. Use the include parameter to keep file paths that contain **all** of the supplied strings *anywhere* in the file path. Use the exclude parameter to disregard file paths that contain **any** of the supplied string anywhere in the file path.
   ```python
    fm.add('canon', '*Camera.avi', include='canon')
    # file path must contain canon

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
    ```
3. Retrieve file paths using a dict-like convention.
   ```python
    canon_videos = fm['canon']
    all_videos = fm['videos']
    ```
4. Add and retrieve in one line of code. 
   ```python
   fm.add('canon', '*Camera.avi', include='canon')['canon']
   # Note that the method returns the instance of the FileManager object. 
   ```
5. Retrieve all the added keys using fm.**get_tags**()
   ```python
   fm.get_tags()
   # returns a tuple ('canon', 'sony42', 'videos', 'panasonic', 'notes')
   ```
6. Retrieve paths of all the added files.
   ```python
   fm.all_files
   ```
7. Get a report of the number of files, and the occupied space.
   ```python
    fm.report()
    ```

## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

[Praneeth Namburi](https://praneethnamburi.com)

Project Link: [https://github.com/praneethnamburi/pyfilemanager](https://github.com/praneethnamburi/pyfilemanager)


## Acknowledgments

This tool was developed as part of the ImmersionToolbox initiative at the MIT.nano Immersion Lab, and thanks to NCSOFT for supporting this initiative.

