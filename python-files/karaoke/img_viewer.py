# img_viewer.py

import PySimpleGUI as sg
import os.path

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Select playlist"),
    ],
    [
        sg.Listbox(
            values=["playlist1", "playlist2"], enable_events=True, size=(40, 20), key="-FILE LIST-"
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
        try:
            print(values["-FILE LIST-"][0])
        except:
            pass

window.close()