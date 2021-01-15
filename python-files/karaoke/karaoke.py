from csv_manager import CsvManager
from mpv_manager import MpvManger
from config_manager import ConfigManager


class Karaoke:
    """
    This class is basically the main class.
    It uses all other classes to execute commands inserted from the ui
    If it has a valid config, it will start
    If it does not have a valid config
    """

    def __init__(self):
        self.config_manager = ConfigManager()

        if self.config_manager.has_valid_config():
            print("Valid config file is detected")
            self.setup()
        else:
            print("No valid config file is found")

    def has_valid_config(self):
        if not self.config_manager.has_valid_config():
            print("Invalid config")
            return False
        if not self.csv_manager.is_csv_valid():
            print("Invalid tracklist")
            return False
        
        return True

    def get_video_directory(self):
        return self.config_manager.get_config('PATHS', 'video_directory')

    def set_video_directory(self, video_dir):
        return self.config_manager.set_config('PATHS', 'video_directory', video_dir)

    def get_tracklist_file(self):
        return self.config_manager.get_config('PATHS', 'tracklist_file')

    def set_tracklist_file(self, tracklist_file):
        return self.config_manager.set_config('PATHS', 'tracklist_file', tracklist_file)

    def setup(self):
        self.setup_csv_file_manager()
        self.setup_mpv_manager()

    def setup_csv_file_manager(self):
        tracklist = self.config_manager.get_config('PATHS', 'tracklist_file')
        self.csv_manager = CsvManager(tracklist)

    def setup_mpv_manager(self):
        video_dir = self.config_manager.get_config('PATHS', 'video_directory')
        song_completed_callback = self.csv_manager.record_song_played
        self.mpv_manager = MpvManger(song_completed_callback, video_dir)

    def test(self):
        playlist = self.csv_manager.generate_red_playlist()
        self.mpv_manager.play_playlist(playlist)

    def get_all_playlists(self):
        try:
            playlists = self.csv_manager.get_all_playlist_names()
        except AttributeError:
            playlists = []
        return playlists

    def play_playlist(self, playlist_name, shuffle=False):
        playlist = self.csv_manager.get_playlist_by_name(playlist_name, shuffle)
        self.mpv_manager.play_playlist(playlist)

    def allowed_to_alter_csv_file(self):
        return self.csv_manager.allowed_to_alter_csv_file()


if __name__ == '__main__':
    karaoke = Karaoke()
    if karaoke.has_valid_config():
        karaoke.test()
