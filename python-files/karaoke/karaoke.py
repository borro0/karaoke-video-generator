from csv_manager import CsvManager
from mpv_manager import MpvManger

import os

VIDEO_DIRECTORY = r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'


def main():
    current_file_directory = os.path.dirname(os.path.realpath(__file__))
    tracklist_csv_file = f"{current_file_directory}/../tests/csv_files/tracklist + bpm.csv"
    print("Going for tracklist ", tracklist_csv_file)
    csv_manager = CsvManager(tracklist_csv_file)
    mpv_manager = MpvManger(song_completed_callback, VIDEO_DIRECTORY)

    playlist = csv_manager.generate_red_playlist()
    mpv_manager.play_playlist(playlist)


def song_completed_callback(song):
    print(song, " is finished playing")


if __name__ == '__main__':
    main()
