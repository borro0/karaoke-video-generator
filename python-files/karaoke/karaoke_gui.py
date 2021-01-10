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
        sg.Checkbox('Shuffle', default=False, key="-SHUFFLE-")
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

window = sg.Window("LRKB Supermachinehackcomputer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            playlist_name = values["-FILE LIST-"][0]
        except IndexError:
            continue
        print(playlist_name)
        karaoke = Karaoke()  # Create new karaoke instance every time
        if karaoke.has_valid_config():
            if karaoke.not_allowed_to_alter_csv_file() or True:
                sg.popup("We cannot edit the tracklist csv file! Please close any program which has opened this file")
            else:
                karaoke.play_playlist(playlist_name, shuffle=values["-SHUFFLE-"])

    if event == "-VIDEO FOLDER-":
        folder = values["-VIDEO FOLDER-"]
        print(folder)
        karaoke.set_video_directory(folder)

    if event == "-TRACKLIST FILE-":
        tracklist_file = values["-TRACKLIST FILE-"]
        print(tracklist_file)
        karaoke.set_tracklist_file(tracklist_file)
        if karaoke.has_valid_config():
            karaoke = Karaoke()  # Create new karaoke instance every time
            playlists = karaoke.get_all_playlists()
            print(playlists)
            window["-FILE LIST-"].update(playlists)

window.close()
