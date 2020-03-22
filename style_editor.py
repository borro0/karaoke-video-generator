from pathlib import Path
import click
import re
import os

@click.command()
@click.option("-d", "--default", is_flag=True, help="All files in the default folder should be updated")
@click.option("-f", "--filename", help="Update a specific file. Give the complete filename of target file, it will be searced in the default folder")
def edit_style(default, filename):
    """
    This program updates video-edit files to the style defined in this file.
    All files in the default folder can be updated, or a single-specific file.
    """

    default_folder = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files"
    lyric_file_folder = f"{default_folder}/Lyric files"
    project_file_folder = f"{default_folder}/projects"

    if (default):
        print("Updating style of all files in the default folder")
        update_all_files(lyric_file_folder, project_file_folder)
    elif(filename):
        print(f"Updating style of specific file: {filename}")
        update_file(lyric_file_folder, project_file_folder, filename)
    else:
        print("No options are given!")
        exit(-1)

def update_all_files(lyric_file_folder, project_file_folder):
    # update all lyric files
    for filename in os.listdir(lyric_file_folder):
        if filename.endswith(".rzlrc"):
            update_lyric_file(lyric_file_folder, filename)

    # update all projects
    for filename in os.listdir(project_file_folder):
        if filename.endswith(".rzmmpj"):
            update_project_file(project_file_folder, filename)

def update_lyric_file(folder, filename):
    if not os.path.exists(f"{folder}/{filename}"):
        print(f"file doesn't exists! {folder}/{filename}")
        exit(-1)
    print(f"Updating lyric file: {filename}")

    pattern_replace_tuples = []
    pattern_replace_tuples.append("nLineInterval=\"[^\"]*\" nInner", "nLineInterval=\"160\" nInner")

    convert_file(f"{folder}/{filename}", pattern_replace_tuples)

def update_project_file(folder, filename):
    if not os.path.exists(f"{folder}/{filename}"):
        print(f"file doesn't exists! {folder}/{filename}")
        exit(-1)
    print(f"Updating project file: {filename}")

def update_file(lyric_file_folder, project_file_folder, filename):
    update_lyric_file(lyric_file_folder,f"{filename}.rzlrc")
    update_project_file(project_file_folder,f"{filename}.rzmmpj")

def convert_file_to_utf16(filename):
    print("Converting file from utf-8 to utf-16")
    content = ''
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            content = f.read()
        with open(filename, 'w', encoding="utf-16") as f:
            f.write(content)
    except UnicodeDecodeError:
        print("File is probably already utf-16")

def convert_file(filename, pattern_replace_tuples):

    convert_file_to_utf16(filename)

    linelist = []
    with open(filename, 'r', encoding='utf-16-le') as f:
        linelist = f.readlines()

    for pattern_replace_tuple in pattern_replace_tuples:
        print(f"pattern: {pattern_replace_tuple[0]}")
        print(f"replacement: {pattern_replace_tuple[1]}")
    
    for i in range(len(linelist)):
        for pattern_replace_tuple in pattern_replace_tuples:
            pattern = pattern_replace_tuple[0]
            replacement = pattern_replace_tuple[1]
            result = re.search(pattern, linelist[i])
            if result:
                print(f"found a match at line {i}: {result}")
                linelist[i] = re.sub(pattern, replacement, linelist[i])

    print("lines read", len(linelist))

    print("write changes back to file")
    with open(filename, 'w', encoding='utf-16-le') as f:
        f.writelines(linelist)


def sandbox():
    test_string = "<para nStartLine=\"1\" nAlign=\"0\" nAngle=\"0\" nLineInterval=\"80\" nInnerAlign=\"1\" nScrollDirection=\"0\" nGradient=\"5\" dAppears=\"0.5\"/>"
    result = re.search("nLineInterval=\"[^\"]*\" nInner", test_string)
    print(result)


if __name__ == '__main__':
    DEBUG = False
    if DEBUG:
        sandbox()
    else:
        edit_style()