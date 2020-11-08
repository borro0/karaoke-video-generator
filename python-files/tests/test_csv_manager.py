import pytest
import os
import filecmp
import shutil
import datetime

from karaoke.csv_manager import CsvManager
# Execute test with: pytest -s -k "csv_manager"


@pytest.fixture
def basic_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = f"{dir_path}/csv_files/basic.csv"

    return csv_file


@pytest.fixture
def tracklist_bpm_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = f"{dir_path}/csv_files/tracklist + bpm.csv"

    return csv_file


def get_playlist_filename(color):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/csv_files/{color}_playlist.txt"


def read_playlist(color):
    file = get_playlist_filename(color)
    with open(file) as f:
        content_list = f.read().splitlines()

    return content_list


@pytest.fixture
def yellow_playlist():
    return read_playlist("yellow")


@pytest.fixture
def red_playlist():
    return read_playlist("red")


@pytest.fixture
def green_playlist():
    return read_playlist("green")


def compare_two_lists(list1, list2):
    list1.sort()
    list2.sort()
    return list1 == list2


@pytest.fixture
def tmp_csv_files(tmp_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_files_folder = f"{dir_path}/csv_files"

    src = csv_files_folder
    dest = tmp_path / "csv_files"

    destination = shutil.copytree(src, dest)

    return destination


def test_print_csv_file(tracklist_bpm_file):
    print("Csv file used for the: ", tracklist_bpm_file)
    csv_manager = CsvManager(tracklist_bpm_file)
    csv_manager.print_csv_file(tracklist_bpm_file)


def test_generate_red_playlist(tracklist_bpm_file, red_playlist):
    csv_manager = CsvManager(tracklist_bpm_file)
    red_playlist_read = csv_manager.generate_red_playlist()

    assert compare_two_lists(red_playlist, red_playlist_read)


def test_generate_yellow_playlist(tracklist_bpm_file, yellow_playlist):
    csv_manager = CsvManager(tracklist_bpm_file)
    yellow_playlist_read = csv_manager.generate_yellow_playlist()

    assert compare_two_lists(yellow_playlist, yellow_playlist_read)


def test_generate_green_playlist(tracklist_bpm_file, green_playlist):
    csv_manager = CsvManager(tracklist_bpm_file)
    green_playlist_read = csv_manager.generate_green_playlist()

    assert compare_two_lists(green_playlist, green_playlist_read)


def test_store_playlist_to_file(green_playlist):
    green_playlist_file_expected = get_playlist_filename("green")
    generated_playlist_actual = CsvManager.store_playlist_to_file(green_playlist)

    assert filecmp.cmp(green_playlist_file_expected, generated_playlist_actual)


def test_get_title_from_song():
    song = "More Than A Feeling - Boston.mp4"
    assert CsvManager.get_title_from_song(song) == "More Than A Feeling"


# def test_record_song_played(tmp_csv_files, green_playlist, red_playlist):
#     actual_csv_file = f"{tmp_csv_files}/tracklist + bpm.csv"
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     target_csv_file = f"{dir_path}/csv_files/tracklist + bpm target.csv"
#     csv_manager = CsvManager(actual_csv_file)
#     # insert various songs, with various dates
#     for song in green_playlist:
#         csv_manager.record_song_played(song, date=datetime.date(2020, 11, 22))

#     for song in red_playlist:
#         csv_manager.record_song_played(song, date=datetime.date(2020, 11, 22))

#     # compare with expected file
#     assert filecmp.cmp(actual_csv_file, target_csv_file)
