import os
import configparser
from pathlib import Path


class ConfigManager:
    """
    This class manages storing and reading of configurations.
    A config file is maintained in the current working directory of the program
    """

    DEFAULT_CONFIG_FILE = Path.home() / "Documents" / "supermachinehackcomputer" / "config.ini"

    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        self.config_file = config_file
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        except FileNotFoundError:
            print("couldn't make parent dir for", self.config_file)
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        self.config.read(self.config_file)

    def has_valid_config(self):
        self.read_config()
        video_dir = self.get_config('PATHS', 'video_directory')
        tracklist = self.get_config('PATHS', 'tracklist_file')

        print("Checking config")
        print(video_dir, "exists:", os.path.exists(video_dir))
        print(tracklist, "exists:", os.path.exists(tracklist))
        print(tracklist, "is csv:", tracklist.endswith('.csv'))

        return os.path.exists(video_dir) and os.path.exists(tracklist) and tracklist.endswith('.csv')

    def get_config(self, config_category, config_name):
        self.read_config()
        try:
            config = self.config[config_category][config_name]
        except KeyError:
            config = ""
        return config

    def set_config(self, config_category, config_name, value):
        self.read_config()

        if config_category not in self.config:
            self.config[config_category] = {}

        self.config[config_category][config_name] = value
        with open(self.config_file, "w") as f:
            self.config.write(f)
