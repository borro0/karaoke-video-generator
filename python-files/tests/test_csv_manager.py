import pytest
import os
import filecmp
import tempfile

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
