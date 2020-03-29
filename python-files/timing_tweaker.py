from xml.dom import minidom
from pathlib import Path
import click
import re

@click.command()
@click.argument("title")
@click.argument("artist")
@click.option("-d", "--delay", type=float, help="delay defined in seconds (for example: 1.45 or -0.5)")
def tweak_lyric_file(title, artist, delay):
    """
    This program changes the timing of a lyric file.
    Give a delay to change the timing of all text lines.
    Give a negative delay to speed up all lyrics.
    """
    lyricfile = f"C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files/Lyric files/{title} - {artist}.rzlrc"

    replace_times_regex(lyricfile, delay)

    # remove_invalid_xml(lyricfile)
    # replace_times_xml(lyricfile, delay)

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


def replace_times_xml(lyricfile, delay):
    DOMTree = minidom.parse(lyricfile)
    collection = DOMTree.documentElement
  
    items = collection.getElementsByTagName("item")
    for item in items:

        if item.hasAttribute("dStartTime"):
            time = float(item.getAttribute("dStartTime"))
            new_time = time + delay
            print(time)
            print("corrected time: ", new_time)
            item.setAttribute("dStartTime", f"{new_time}")

        if item.hasAttribute("dEndTime"):
            time = float(item.getAttribute("dEndTime"))
            new_time = time + delay
            print(time)
            print("corrected time: ", new_time)
            item.setAttribute("dEndTime", f"{new_time}")

     
    with open(lyricfile, 'wb') as outFile:
        outFile.write(DOMTree.toxml('utf-16-le'))   

def remove_invalid_xml(lyricfile):
    linelist = []
    with open(lyricfile, 'r', encoding='utf-16-le') as f:
        print("Reading txt file")
        linelist = f.readlines()
    
    print("replacing invalid xml")
    linelist[1] = re.sub(r' 3D[^"]+"[^"]+"', "", linelist[1]) #not the best regex, but gets the job done
    
    print("write changes back to file")
    with open(lyricfile, 'w', encoding='utf-16-le') as f:
        f.writelines(linelist)

if __name__ == '__main__':
    tweak_lyric_file()