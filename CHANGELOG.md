# Change Log
All notable changes to this project will be documented in this file.

## [1.1.0] - 2024-02-22

### Added
Depth-based search support for files and directories. Useful for working with files in the top level directory.

```python
FileManager(base_dir).add_by_depth()['*annotations*.json']
# To retrieve annotation json files in base_dir and not with any of the files in the sub-directories.

FileManager(base_dir).add()['*annotations*.json']
# To retrieve annotation json file paths in the base directory and all the sub-directories.
```

### Changed
1. When `exclude_hidden` is set to `True` (default), a folder called *#recycle* will now be ignored. This is to exclude the contents of the recycle bin on network attached storage devices such as a synology NAS.

2. Refactored the core function `pyfilemanager.find`
   
## [1.0.0] - 2024-01-26

First major release after thorough testing, 100% coverage, and formatting.

### Added
More flexibility in the FileManager.add method. When called without any arguments, all the files in the base directory are stored in the FileManager object.

## [0.1.1] - 2024-01-21

Initial release
