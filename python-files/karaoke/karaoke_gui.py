import PySimpleGUI as sg

from karaoke import Karaoke

VIDEO_DIRECTORY = r'C:\Users\boris\Google Drive\Live Karaoke Band\Lyric-videos\rendered videos'
TRACKLIST_FILE = r'D:\Documents\karaoke-video-generator\python-files\tests\csv_files\tracklist + bpm.csv'

karaoke = Karaoke()
playlists = karaoke.get_all_playlists()


file_list_column = [
    [
        sg.Text("Select playlist"),
    ],
    [
        sg.Listbox(
            values=playlists, enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
    ]
]

window = sg.Window("Image Viewer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        playlist_name = values["-FILE LIST-"][0]
        print(playlist_name)
        karaoke = Karaoke()  # Create new karaoke instance every time
        karaoke.play_playlist(playlist_name)

window.close()
