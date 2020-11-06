import mpv


class MpvManger:
    """ This class handles the playing of videos with MPV player """

    def __init__(self, song_completed_callback, video_directory):
        # This callback is called when song has played completely to store in csv file
        self.song_completed_callback = song_completed_callback
        self.video_directory = video_directory
        self.player = mpv.MPV()

    def play_playlist(self, playlist):
        player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)

        print("appending list: ", playlist)
        for song in playlist:
            player.playlist_append(f"{self.video_directory}/{song}")

        player.playlist_pos = 0

        @player.property_observer('percent-pos')
        def eof_observer(_name, value):
            print("current pos: ", value)

        @player.property_observer('eof-reached')
        def eof_observer(_name, value):
            # Here, _value is either None if nothing is playing or a float containing
            # fractional seconds since the beginning of the file.
            print(f"eof reached {_name} {value} !")

            pos = player._get_property('percent-pos')
            print("current pos: ", pos)

        while True:
            # To modify the playlist, use player.playlist_{append,clear,move,remove}. player.playlist is read-only
            print("calling playlist next")
            # player.playlist_next()
            print("waiting for playback")
            player.wait_for_playback()
            eof_reached = player._get_property('eof-reached')
            print("eof-reached: ", eof_reached)
        # self.song_completed_callback(song)

    
