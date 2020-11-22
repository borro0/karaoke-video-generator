import PySimpleGUI as sg

from karaoke import Karaoke

karaoke = Karaoke()
if karaoke.has_valid_config():
    playlists = karaoke.get_all_playlists()
else:
    playlists = []

video_folder = karaoke.get_video_directory()
tracklist_file = karaoke.get_tracklist_file()

file_list_column = [
    [
        sg.Text("Video Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-VIDEO FOLDER-", default_text=video_folder),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Tracklist file"),
        sg.In(size=(25, 1), enable_events=True, key="-TRACKLIST FILE-", default_text=tracklist_file),
        sg.FileBrowse(),
    ],
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
    if event == "-VIDEO FOLDER-":
        folder = values["-VIDEO FOLDER-"]
        print(folder)
        karaoke.set_video_directory(folder)
    if event == "-TRACKLIST FILE-":
        tracklist_file = values["-TRACKLIST FILE-"]
        print(tracklist_file)
        karaoke.set_tracklist_file(tracklist_file)
        if karaoke.has_valid_config():
            playlists = karaoke.get_all_playlists()
            window["-FILE LIST-"].update(playlists)

window.close()
