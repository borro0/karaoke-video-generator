import mpv


class Song:
    """ This class represents a song played in MPV """

    def __init__(self):
        self.name = ""
        self.percentage_played = 0

    def isSongPlayed(self):
        return self.percentage_played > 80.0


class MpvManger:
    """ This class handles the playing of videos with MPV player """

    def __init__(self, song_completed_callback, video_directory):
        # This callback is called when song has played completely to store in csv file
        self.song_completed_callback = song_completed_callback
        self.video_directory = video_directory
        self.player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
        self.current_song = Song()

        @self.player.property_observer('percent-pos')
        def percent_pos_observer(_name, value):
            if value is None:
                self.current_song.percentage_played = 0
            else:
                self.current_song.percentage_played = value

    def play_playlist(self, playlist):
        print("appending list: ", playlist)
        for song in playlist:
            self.player.playlist_append(f"{self.video_directory}/{song}")

        self.player.playlist_pos = 0
        while self.player.playlist_pos is not None:
            song = playlist[self.player.playlist_pos]
            self.current_song.name = song
            print(song)

            self.player._set_property('pause', True)
            self.player.wait_for_playback()

            if self.current_song.isSongPlayed():
                self.song_completed_callback(song)
