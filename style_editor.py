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

def update_project_file(folder, filename):
    if not os.path.exists(f"{folder}/{filename}"):
        print(f"file doesn't exists! {folder}/{filename}")
        exit(-1)
    print(f"Updating project file: {filename}")

def update_file(lyric_file_folder, project_file_folder, filename):
    update_lyric_file(lyric_file_folder,f"{filename}.rzlrc")
    update_project_file(project_file_folder,f"{filename}.rzmmpj")

def find_float(text):
    result = re.search('[0-9]+\.?[0-9]*', f"{text}")
    if result:
        original_value = float(result.group(0))
        return original_value

def add_to_attribute_value(line, attribute, add):
    result = re.search(f'{attribute}="[-+]?[0-9]*\.?[0-9]*"', line)
    if (result):
        matched_result = result.group(0) # matched something like dEndTime="34.34"
        old_value = find_float(matched_result)
        new_value = old_value + add
        line = re.sub(f'{attribute}="{old_value}"', f'{attribute}="{new_value}"', line)
    return line

def replace_times_regex(lyricfile, delay):
    linelist = []
    with open(lyricfile, 'r', encoding='utf-16-le') as f:
        print("Reading txt file")
        linelist = f.readlines()
    
    for i in range(len(linelist)):
        linelist[i] = add_to_attribute_value(linelist[i], 'dStartTime', delay)
        linelist[i] = add_to_attribute_value(linelist[i], 'dEndTime', delay)

    print("lines read", len(linelist))

    print("write changes back to file")
    with open(lyricfile, 'w', encoding='utf-16-le') as f:
        f.writelines(linelist)

if __name__ == '__main__':
    edit_style()