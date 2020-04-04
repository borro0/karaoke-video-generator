import shutil
import pytest
import os
import filecmp

from karaoke.style_editor import StyleEditor


@pytest.fixture
def video_edit_files(tmp_path):
    video_edit_folder = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/"

    src = video_edit_folder
    dest = tmp_path / "Video edit files"

    destination = shutil.copytree(src, dest)

    return destination

@pytest.fixture
def project_lyric_files(tmp_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    src = f"{dir_path}/test-project-lyric-files"

    dest = tmp_path / "test-project-lyric-files"

    destination = shutil.copytree(src, dest)

    return destination

def test_single_lyric_file(project_lyric_files):
    print(project_lyric_files)
    style_editor = StyleEditor()

    filename_to_test = "A Horse With No Name - America (38pt - 160line)"
    filepath_to_test = f"{project_lyric_files}/{filename_to_test}.rzlrc"

    style_editor.try_update_lyric_file(project_lyric_files, filename_to_test)

    filepath_actual = f"{project_lyric_files}/A Horse With No Name - America (32pt - 150line).rzlrc"
    assert filecmp.cmp(filepath_to_test, filepath_actual)

# def test_all_lyric_files(video_edit_files):
#     print(video_edit_files)
#     style_editor = StyleEditor()
#     style_editor.update_all_lyric_files(f"{video_edit_files}/Lyric files")
#     assert 0