from csv_manager import CsvManager
from mpv_manager import MpvManger
from config_manager import ConfigManager

import os

VIDEO_DIRECTORY = r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'
TRACKLIST_FILE = r'D:\Documents\karaoke-video-generator\python-files\tests\csv_files\tracklist + bpm.csv'


class Karaoke:
    """
    This class is basically the main class.
    It uses all other classes to execute commands inserted from the ui
    If it has a valid config, it will start
    If it does not have a valid config
    """

    def __init__(self, video_dir=VIDEO_DIRECTORY, tracklist=TRACKLIST_FILE):
        self.config_manager = ConfigManager()
        
        if self. config_manager.has_valid_config():
            print("Valid config file is detected")
            video_dir = self.config_manager.get_config('PATHS', 'video_directory')
            tracklist = self.config_manager.get_config('PATHS', 'tracklist_file')
            self.setup(video_dir, tracklist)
        else:
            print("No valid config file is found")

    def has_valid_config(self):
        return self.config_manager.has_valid_config()

    def get_video_dir(self):
        return self.config_manager.get_config('PATHS', 'video_directory')
    
    def set_video_dir(self, video_dir):
        return self.config_manager.set_config('PATHS', 'video_directory', video_dir)

    def get_tracklist_file(self):
        return self.config_manager.get_config('PATHS', 'tracklist_file')

    def set_tracklist_file(self, tracklist_file):
        return self.config_manager.set_config('PATHS', 'tracklist_file', tracklist_file)

    def setup(self, video_dir, tracklist):
        # setup csv manager
        self.csv_manager = CsvManager(tracklist)

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
    if karaoke.has_valid_config():
        karaoke.test()
