from csv_manager import CsvManager
from mpv_manager import MpvManger
import os

VIDEO_DIRECTORY = r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'
TRACKLIST_FILE = r'D:\Documents\karaoke-video-generator\python-files\tests\csv_files\tracklist + bpm.csv'


class Karaoke:
    """
    This class is basically the main class.
    It uses all other classes to execute commands inserted from the ui
    """

    def __init__(self, video_dir=VIDEO_DIRECTORY, tracklist_file=TRACKLIST_FILE):
        # setup csv manager
        self.csv_manager = CsvManager(tracklist_file)

        # setup mpv manager
        song_completed_callback = self.csv_manager.record_song_played
        self.mpv_manager = MpvManger(song_completed_callback, video_dir)

    def test(self):
        playlist = self.csv_manager.generate_red_playlist()
        self.mpv_manager.play_playlist(playlist)

    def get_all_playlists(self):
        return self.csv_manager.get_all_playlist_names()

    def play_playlist(self, playlist_name):
        playlist = self.csv_manager.get_playlist_by_name(playlist_name)
        self.mpv_manager.play_playlist(playlist)



if __name__ == '__main__':
    karaoke = Karaoke()
    karaoke.test()
