from pathlib import Path
import pytest
from pyfilemanager import FileManager

@pytest.fixture(scope='session', autouse=True)
def initialize_folder_structure(tmp_path_factory):
    root_dir_files = tmp_path_factory.getbasetemp()
    folder_structure = {
        'sony': ['142Camera.avi', '143Camera.avi', 'notes.txt'], 
        'panasonic': ['151Camera.avi', '143Camera.avi', 'notes.txt'], 
        'panasonic2': ['201Camera.avi', '202.mp4'],
        'canon': ['51Camera.avi', '40Camera.avi', 'notes.txt'], 
        'notes': ['notes1.txt', 'notes2.txt']
        }
    for folder_name, file_names in folder_structure.items():
        this_folder = root_dir_files / folder_name
        this_folder.mkdir()
        for file_name in file_names:
            (this_folder / file_name).touch()

def _relative_paths(file_list:list) -> set:
    return {'/'.join(Path(x).parts[-2:]) for x in file_list}

def test_folder_initializer(tmp_path_factory):
    """Make sure initialize_folder_structure is working properly"""
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('abc', '*.*')
    assert len(fm.all_files) == 13


def test_add_special(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add()
    assert fm.add() is fm
    assert len(fm.all_files) == 13
    assert fm.get_tags() == ['all']
    fm.remove('all')
    assert len(fm.all_files) == 0
    fm.add('*.*')
    assert len(fm.all_files) == 13
    assert fm.get_tags() == ['all']
    fm.add('*.avi')
    assert fm.get_tags() == ['all', 'avi']
    assert len(fm['avi']) == 7
    with pytest.raises(AssertionError):
        fm.add('*.a?2')

def test_add_pattern(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('mp4', '*.mp4') # pattern: str
    assert len(fm['mp4']) == 1
    fm.add('videos', ['*.avi', '*.mp4']) # pattern: list
    assert len(fm['videos']) == 8

def test_add_include_str(tmp_path_factory):
    """FileManager.add (include:str=)"""
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('canon', '*Camera.avi', include='canon')
    assert _relative_paths(fm['canon']) == {'canon/40Camera.avi', 'canon/51Camera.avi'}

def test_add_include_list(tmp_path_factory):
    """FileManager.add (include:list=)"""
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('sony42', '*Camera.avi', include=['sony', '42']) # file path must contain sony AND 42
    assert _relative_paths(fm['sony42']) == {'sony/142Camera.avi'}

def test_add_exclude_str(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('panasonic', '*.avi', include='panasonic', exclude='panasonic2')
    assert _relative_paths(fm['panasonic']) == {'panasonic/151Camera.avi', 'panasonic/143Camera.avi'}

def test_tag_overwrite(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('notes', 'notes*.txt')
    assert len(fm['notes']) == 5
    fm.add('notes', 'notes*.txt', include='notes\\notes')
    assert _relative_paths(fm['notes']) == {'notes/notes2.txt', 'notes/notes1.txt'}
    fm.add('notes2', 'notes*.txt', exclude=['sony', 'panasonic', 'panasonic2', 'canon'])
    assert _relative_paths(fm['notes2']) == {'notes/notes2.txt', 'notes/notes1.txt'}

def test_getitem(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('canon', '*Camera.avi', include='canon')
    fm.add('videos', ['*.avi', '*.mp4'])
    fm.add('notes', 'notes*.txt')
    # Retrieve using special characters
    assert _relative_paths(fm['*notes?.txt']) == {'notes/notes1.txt', 'notes/notes2.txt'}
    # Retrieve by the tag 'canon'
    assert _relative_paths(fm['canon']) == {'canon/40Camera.avi', 'canon/51Camera.avi'}
    # When a tag is not found, retrieve file paths by an exact match to the file stem.
    assert _relative_paths(fm['143Camera']) == {'panasonic/143Camera.avi', 'sony/143Camera.avi'}
    # If the key doesn't match a tag or a stem of a filename, do a loose-search to retrieve all entries where the tag is anywhere in the full path.
    assert _relative_paths(fm['20']) == {'panasonic2/201Camera.avi', 'panasonic2/202.mp4'}

def test_get_tags(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('canon', '*Camera.avi', include='canon')
    assert fm.get_tags() == ['canon']
    fm.add('notes', 'notes*.txt')
    assert fm.get_tags() == ['canon', 'notes']
    fm.add('notes', 'notes*.txt', include='notes\\notes')
    assert fm.get_tags() == ['canon', 'notes']

def test_all_files(tmp_path_factory):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('videos', ['*.avi', '*.mp4'])
    fm.add('notes', 'notes*.txt')
    assert len(fm.all_files) == 13
    fm.add('canon', '*Camera.avi', include='canon')
    assert len(fm.all_files) == 13 # test that all_files is returning unique values
    assert len(fm['videos'] + fm['notes'] + fm['canon']) == 15

def test_report(tmp_path_factory, capsys):
    fm = FileManager(tmp_path_factory.getbasetemp())
    fm.add('canon', '*Camera.avi', include='canon')
    fm.add('sony42', '*Camera.avi', include=['sony', '42'])
    fm.add('videos', ['*.avi', '*.mp4'])
    fm.add('panasonic', '*.avi', include='panasonic', exclude='panasonic2')
    fm.add('notes', 'notes*.txt', include='notes\\notes')
    fm.report()
    captured = capsys.readouterr()
    assert [' '.join(x.split(' ')[:2]) for x in captured.out.splitlines()] == ['2 canon', '1 sony42', '8 videos', '2 panasonic', '2 notes']
    # assert captured.out == '2 canon files taking up 0.000 MB\n1 sony42 files taking up 0.000 MB\n8 videos files taking up 0.000 MB\n2 panasonic files taking up 0.000 MB\n2 notes files taking up 0.000 MB\n'
