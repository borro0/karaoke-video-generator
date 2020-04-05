from prettytable import PrettyTable
import os

lyric_layout_path = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Lyric layouts"


def is_file_using_encoding(file, possible_encoding):
    try:
        with open(file, 'r', encoding=possible_encoding) as f:
            f.readlines()
            return True
    except UnicodeDecodeError:
        print(f"Could not read this file: {file} as {possible_encoding}")
        return False


def read_file_with_encoding(file, target_encoding):
    with open(file, 'r', encoding=target_encoding) as f:
        return f.readlines()


def read_all_lines_of_file_or_exit(file):
    encodings = ["utf-8", "utf-16"]
    for encoding in encodings:
        if is_file_using_encoding(file, encoding):
            return read_file_with_encoding(file, encoding)

    print(f"Coudl not read this file: {file}")
    exit(-1)


def get_max_line_length_file(file):
    lines = read_all_lines_of_file_or_exit(file)
    longest_line = 0
    for line in lines:
        if len(line) > longest_line:
            longest_line = len(line)
    return longest_line


pretty_table = PrettyTable()
pretty_table.field_names = ["Song", "Longest line"]

for filename in os.listdir(lyric_layout_path):
    if filename.endswith(".txt"):
        longest_line = get_max_line_length_file(f"{lyric_layout_path}/{filename}")
        if (longest_line > 63):
            pretty_table.add_row([filename, longest_line])
    
print(pretty_table)