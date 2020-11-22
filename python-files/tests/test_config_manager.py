import pytest
import shutil
import os

from karaoke.config_manager import ConfigManager


@pytest.fixture
def tmp_test_files(tmp_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_files_folder = f"{dir_path}/test_files"

    src = test_files_folder
    dest = tmp_path / "test_files"

    destination = shutil.copytree(src, dest)

    return destination


def test_get_default_values(tmp_test_files):
    config_manager = ConfigManager(f"{tmp_test_files}/config.ini")

    video_dir = config_manager.get_config('PATHS', 'video_directory')
    assert video_dir == r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'

    tracklist_file = config_manager.get_config('PATHS', 'tracklist')
    assert tracklist_file == r'D:\Documents\karaoke-video-generator\python-files\tests\test_files\tracklist + bpm.csv'


def test_is_no_config_file_available(tmp_test_files):
    config_manager = ConfigManager()
    assert config_manager.has_valid_config() is False


def test_has_valid_config(tmp_test_files):
    config_manager = ConfigManager(f"{tmp_test_files}/config.ini")
    assert config_manager.has_valid_config() is True


def test_is_no_config_file_available(tmp_test_files):
    config_file = f"{tmp_test_files}/test.ini"
    config_manager = ConfigManager(config_file)

    test_dir = r'C:\Test'
    test_tracklist = r'C:\Test\tracklist.csv'
    config_manager.set_config('PATHS', 'video_directory', test_dir)
    config_manager.set_config('PATHS', 'tracklist', test_tracklist)

    actual_dir = config_manager.get_config('PATHS', 'video_directory')
    assert actual_dir == test_dir

    actual_tracklist = config_manager.get_config('PATHS', 'tracklist')
    assert actual_tracklist == test_tracklist
