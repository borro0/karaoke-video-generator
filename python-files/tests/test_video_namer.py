import shutil
import pytest
import os
import filecmp

from karaoke.video_namer import VideoNamer

def create_rendered_videos_folder(tmp_path, video_names):
    rendered_files_folder = tmp_path
    dir_list = os.listdir(rendered_files_folder)

    for idx, video in enumerate(video_names):
        with open(rendered_files_folder / f"Target {idx}.mp4", 'w') as fp:
            fp.write(video)
    
    dir_list = os.listdir(rendered_files_folder)

    return rendered_files_folder

@pytest.fixture
def projects_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    projects_dir = f"{dir_path}/projects"

    return projects_dir

@pytest.fixture
def video_names(projects_dir):
    video_names = os.listdir(projects_dir)
    video_names = [v for v in video_names if v.endswith('.rzmmpj')]
    return video_names

# @pytest.mark.parametrize("start_idx, end_idx", [(0, 36), (36, 55), (55, 100)])
# def test_first_videos(tmp_path, video_names, projects_dir, start_idx, end_idx):
#     print("start of test", start_idx, end_idx)
#     video_names = video_names[start_idx:end_idx]
#     create_rendered_videos_folder(tmp_path, video_names)
#     print(tmp_path)

#     video_namer = VideoNamer(tmp_path, projects_dir)
#     video_namer.rename_videos(start_idx, len(video_names))

#     video_names_mp4 = [m.replace('.rzmmpj', '.mp4') for m in video_names]

#     assert os.listdir(tmp_path) == video_names_mp4
