# pyfilemanager

*Easy to use file search and file path management in python.*


## Installation

```sh
pip install pyfilemanager
```

## Usage

### Quickstart

```python
from pyFileManager import FileManager
video_list = FileManager(r'C:\videos').add('video', '*.avi', include=['sony', 'panasonic'], exclude='canon')['video']
```

### Long version
Consider the following file structure in C:\videos directory

```
C:\videos
├── sony
│   ├── 142Camera.avi
│   ├── 143Camera.avi
│   ├── notes.txt
├── panasonic
│   ├── 151camera.avi
│   ├── 143camera.avi
│   ├── notes.txt
├── panasonic2
│   ├── 201camera.avi
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
   fm = FileManager(r'C:\videos')
   ```
2. Add files of different types with different inclusion and exclusion criteria.
   ```python
    fm.add('video', '*Camera.avi', include=['sony', 'panasonic'], exclude='canon')
    fm.add('video', '*.mp4', include='panasonic') # to include 202.mp4 in the panasonic2 folder
    fm.add('canon', '*Camera.avi', include='canon')
    fm.add('notes', 'notes*.txt')
    ```
3. Retrieve the file list.
   ```python
    canon_videos = fm['canon']
    other_videos = fm['video']
    ```
4. Generate a report for the different file types (number of files, and space occupied).
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

