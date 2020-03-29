import shutil

from karaoke.style_editor import StyleEditor

@pytest.fixture
def video_edit_files(tmp_path):
    video_edit_folder = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files"

    src = tmp_path
    dest = video_edit_folder

    destination = shutil.copytree(src, dest)   

    print(destination)

def test_video_edit_files(video_edit_files):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("test")
    assert p.read_text() == "test"
    assert len(list(tmp_path.iterdir())) == 1
    assert 0

def test_print_regex_replace_tuples():
    style_editor = StyleEditor()
    regex_replace_pairs = []
    regex_replace_pairs.append(("hello", "world"))
    regex_replace_pairs.append(("how", "you do"))
    style_editor.print_regex_replace_tuples(regex_replace_pairs)