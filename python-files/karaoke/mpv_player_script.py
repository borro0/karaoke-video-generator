# For this to work on windows, pip install python-mpv, and add 'mpv.net' folder to PATH
import mpv

print("Creating MPV object")
player = mpv.MPV()
print("Play anarchy")
player.play(r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos\Anarchy In The UK - Sex Pistols.mp4')
print("Wait for playback")
player.wait_for_playback()