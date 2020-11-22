import pytest

@pytest.fixture
def tmp_test_files(tmp_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    test_files_folder = f"{dir_path}/test_files"

    src = test_files_folder
    dest = tmp_path / "test_files"

    destination = shutil.copytree(src, dest)

    return destination

# def test_is_config_file_available():
