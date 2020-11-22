import os
import configparser


class ConfigManager:
    """
    This class manages storing and reading of configurations.
    A config file is maintained in the current working directory of the program
    """

    def __init__(self, config_file=f"{os.getcwd()}/config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        self.config.read(self.config_file)

    def has_valid_config(self):
        self.read_config()
        video_dir = self.get_config('PATHS', 'video_directory')
        tracklist = self.get_config('PATHS', 'tracklist')

        return os.path.exists(video_dir) and os.path.exists(tracklist)

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
