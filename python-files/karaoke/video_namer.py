import click
import re
import os
from pathlib import Path

DEFAULT_PROJECT_DIRECTORY = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/projects"

@click.command()
@click.argument('nr-of-videos', type=int)
@click.argument('target-directory', type=click.Path(exists=True))
@click.option("-p", "--project-directory", default=DEFAULT_PROJECT_DIRECTORY, type=click.Path(exists=True), help=(
    f"Directory which contains all the projects. Default project directory: {DEFAULT_PROJECT_DIRECTORY}"))
@click.option("-s", "--start-index", default=0, type=int, help=("Index of first video"))
@click.option("-n", "--nr-of-videos", type=int, help=("Number of videos to render"))
def rename_videos(project_directory, target_directory, start_index, nr_of_videos):
    """
    This program updates the output of a batch render or Youtube Movie Maker to use the
    proper project names. It requires a 'project directory' to get all the project names,
    and a 'target directory' to update the target files with the proper names.
    Specifiy the number of videos you want to rename.
    """

    if not (nr_of_videos):
        print("Please provide target directory and number of videos")
        exit(-1)

    target_directory = Path(target_directory)
    project_directory = Path(project_directory)

    video_namer = VideoNamer(target_directory, project_directory)
    video_namer.rename_videos(start_index, nr_of_videos)


class VideoNamer(object):
    def __init__(self, video_directory, project_directory):
        self.video_directory = Path(video_directory)
        self.project_directory = project_directory

    def rename_videos(self, start_idx, nr_of_videos):
        all_video_names = os.listdir(self.project_directory)
        all_video_names = [v for v in all_video_names if v.endswith('.rzmmpj')]
        end_idx = start_idx + nr_of_videos
        video_names = all_video_names[start_idx:end_idx]
        print(video_names, start_idx, nr_of_videos)
        video_names_mp4 = [m.replace('.rzmmpj', '.mp4') for m in video_names]

        for idx, video in enumerate(video_names_mp4):
            print(f"{self.video_directory}/Target {idx}.mp4")
            os.rename(self.video_directory / f"Target {idx}.mp4", self.video_directory / video)

if __name__ == '__main__':
    rename_videos()