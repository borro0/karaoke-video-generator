import mpv


class MpvManger:
    """ This class handles the playing of videos with MPV player """

    def __init__(self, song_completed_callback, video_directory):
        # This callback is called when song has played completely to store in csv file
        self.song_completed_callback = song_completed_callback
        self.video_directory = video_directory

    def play_playlist(self, playlist):
        for song in playlist:
            print("I'm playing the following song: ", song)
            song_completed_callback(song)
