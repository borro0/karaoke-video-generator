from xml.dom import minidom
from pathlib import Path
import click

@click.command()
@click.argument("title")
@click.argument("artist")
@click.argument("bpm_filename")
@click.option("-f", "--force", is_flag=True, help="This flag allows to override existing files")
def generate_project_and_lyric(title, artist, bpm_filename, force):
    """This program generates new Youtube Movie Make Projects and Lyrics recording based on an existing project / lyric recording."""

    audiofile = f"C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/clicktrack shizzle/{bpm_filename}.mp3"
    lyricfile = f"C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/Lyric files/{title} - {artist}.rzlrc"
    projectfile = f"C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/projects/{title} - {artist}.rzmmpj"
    txtfile = f"C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Lyric layouts/{title} - {artist}.txt"

    generate_project_file(title, artist, audiofile, projectfile, lyricfile, force)
    convert_txt_file_to_utf16(txtfile)
    add_end_to_last_line(txtfile)
    generate_lyric_file(audiofile, txtfile, lyricfile, force)

def generate_project_file(title, artist, audiofile, projectfile, lyricfile, force):

    # Open XML document using minidom parser
    DOMTree = minidom.parse("Video edit files/projects/Africa - Toto.rzmmpj")
    collection = DOMTree.documentElement

    # Get all the lines in the project
    lines = collection.getElementsByTagName("line")

    # Print name of each line.
    for line in lines:
        if line.hasAttribute("szLineName"):
            if line.getAttribute("szLineName") == "Audio 0":
                set_audio_or_lyric_path(DOMTree, line, audiofile)
            if line.getAttribute("szLineName") == "Text 0":
                set_audio_or_lyric_path(DOMTree, line, lyricfile)
            if line.getAttribute("szLineName") == "Text 1":
                set_title_page(DOMTree, line, title, artist)
    
    if Path(projectfile).exists() and not force:
        print(f"File already exists!: {projectfile}")
        exit()

    with open(projectfile, 'wb') as outFile:
        outFile.write(DOMTree.toxml('utf-8'))

def add_end_to_last_line(txtfile):
    linelist = []
    with open(txtfile, 'r', encoding="utf-16") as f:
        print("Reading txt file")
        linelist = f.readlines()
    
    print("Number of lines: ", len(linelist))
    last_line = linelist[-1]
    print(f"last line: {last_line}")
    if last_line == "{end}":
        print("No need to insert end")
        return
    elif last_line == "(end)":
        print("So we got an (end), replace with {end}")
        linelist[-1] = "{end}"
    else:
        print("No end detected, write add {end}")
        linelist.append("{end}")

    print("write changes back to file")
    with open(txtfile, 'w', encoding="utf-16") as f:
        f.writelines(linelist)

def convert_txt_file_to_utf16(txtfile):
    print("Converting file from utf-8 to utf-16")
    content = ''
    try:
        with open(txtfile, 'r', encoding="utf-8") as f:
            content = f.read()
        with open(txtfile, 'w', encoding="utf-16") as f:
            f.write(content)
    except UnicodeDecodeError:
        print("File is probably already utf-16")

def generate_lyric_file(audiofile, txtfile, lyricfile, force):
    # open template
    DOMTree = minidom.parse("Video edit files/Lyric files/Venus - Schocking Blue.rzlrc")
    collection = DOMTree.documentElement

    # set proper .txt file
    if collection.hasAttribute("Text"):
        print("So we got the attribute Text")
        print(collection.getAttribute("Text"))
        print("We convert it to the new value")
        collection.setAttribute("Text", txtfile)
        print(collection.getAttribute("Text"))
    
    # set proper bpm file
    mediafile = collection.getElementsByTagName("mediafile")[0]
    print(f"current mediafile: {mediafile.firstChild.data}")
    mediafile.replaceChild(DOMTree.createTextNode(audiofile), mediafile.firstChild)
    print(f"new mediafile: {mediafile.firstChild.data}")

    # remove any recorded lines
    for node in collection.childNodes:
        if node.nodeName == "item":
            collection.removeChild(node)

    if Path(lyricfile).exists() and not force:
        print(f"File already exists!: {lyricfile}")
        exit()

    with open(lyricfile, 'wb') as outFile:
        outFile.write(DOMTree.toxml('utf-8'))


def set_audio_or_lyric_path(tree, line, path):
    subline = line.getElementsByTagName("item")[0]
    source = subline.getElementsByTagName("source")[0]
    print(source.firstChild.data)
    print("replacing this with ", path)
    source.replaceChild(tree.createTextNode(path), source.firstChild)
    print("new value")
    print(source.firstChild.data)

def merge_title_artist(title, artist):
    return f"{title}\n-\n{artist}"

def set_title_page(tree, line, title, artist):
    subline = line.getElementsByTagName("item")[0]
    text = subline.getElementsByTagName("text")[0]
    print(text.firstChild.data)
    new_text = merge_title_artist(title, artist)
    print("replacing this with ", new_text)
    text.replaceChild(tree.createTextNode(new_text), text.firstChild)
    print("new value")
    print(text.firstChild.data)
    
if __name__ == '__main__':
    generate_project_and_lyric()