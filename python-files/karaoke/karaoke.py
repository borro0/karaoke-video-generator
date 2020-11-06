from csv_manager import CsvManager
from mpv_manager import MpvManger

import os

VIDEO_DIRECTORY = r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'


def main():
    csv_manager = CsvManager(os.path.join(os.path.curdir, '..', 'tests', 'csv_files', 'tracklist + bmp.csv'))
    mpv_manager = MpvManger(song_completed_callback, VIDEO_DIRECTORY)

    green_playlist = csv_manager.generate_green_playlist()
    mpv_manager.play_playlist(green_playlist)


def song_completed_callback(song):
    print(song, " is finished playing")

if __name__ == '__main__':
    main()