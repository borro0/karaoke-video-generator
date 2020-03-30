import shutil
import pytest

from karaoke.style_editor import StyleEditor

@pytest.fixture
def video_edit_files(tmp_path):
    video_edit_folder = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/"

    src = video_edit_folder
    dest = tmp_path / "Video edit files"

    destination = shutil.copytree(src, dest)

    return destination

def test_single_lyric_file(video_edit_files):
    print(video_edit_files)
    style_editor = StyleEditor()
    style_editor.try_update_lyric_file(f"{video_edit_files}/Lyric files", "Crazy On You - Heart")
    assert 0

def test_all_lyric_files(video_edit_files):
    print(video_edit_files)
    style_editor = StyleEditor()
    style_editor.update_all_lyric_files(f"{video_edit_files}/Lyric files")
    assert 0

def test_print_regex_replace_tuples():
    style_editor = StyleEditor()
    regex_replace_pairs = []
    regex_replace_pairs.append(("hello", "world"))
    regex_replace_pairs.append(("how", "you do"))
    style_editor.print_regex_replace_tuples(regex_replace_pairs)