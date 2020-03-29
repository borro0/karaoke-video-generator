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

    style_editor = StyleEditor()

    if (default):
        print("Updating style of all files in the default folder")
        style_editor.update_all_lyric_files(lyric_file_folder)
        style_editor.update_all_project_files(project_file_folder)
    elif(filename):
        print(f"Updating style of specific file: {filename}")
        style_editor.try_update_lyric_file(lyric_file_folder, filename)
        style_editor.try_update_project_file(project_file_folder, filename)
    else:
        print("No options are given!")
        exit(-1)


class StyleEditor(object):
    def update_all_lyric_files(self, lyric_file_folder):
        for filename in os.listdir(lyric_file_folder):
            if filename.endswith(".rzlrc"):
                self.update_lyric_file(lyric_file_folder, filename)

    def update_lyric_file(self, folder, filename):
        print(f"Updating lyric file: {filename}")

        regex_replace_tuples = []
        regex_replace_tuples.append("nLineInterval=\"[^\"]*\" nInner", "nLineInterval=\"160\" nInner")

        self.apply_regex_replace_to_file(f"{folder}/{filename}", regex_replace_tuples)

    def apply_regex_replace_to_file(self, filename, regex_replace_tuples):
        print("Converting file from utf-8 to utf-16")
        self.convert_file_from_utf8_to_utf16(filename)

        print("reading all lines of file")
        linelist = self.read_all_lines_of_file(filename)
        print("lines read", len(linelist))

        self.print_regex_replace_tuples(regex_replace_tuples)

        linelist[:] = [self.apply_regex_tuples_to_line(line, regex_replace_tuples) for line in linelist]

        print("write changes back to file")
        self.write_lines_back_to_file(linelist, filename)

    def convert_file_from_utf8_to_utf16(self, filename):
        try:
            content = ''
            with open(filename, 'r', encoding="utf-8") as f:
                content = f.read()
            with open(filename, 'w', encoding="utf-16") as f:
                f.write(content)
        except UnicodeDecodeError:
            print("File is probably already utf-16")

    def read_all_lines_of_file(self, filename):
        with open(filename, 'r', encoding='utf-16-le') as f:
            return f.readlines()

    def print_regex_replace_tuples(self, regex_replace_tuples):
        for regex_replace_tuple in regex_replace_tuples:
            print(f"regex: {regex_replace_tuple[0]}")
            print(f"replacement: {regex_replace_tuple[1]}")

    def apply_regex_tuples_to_line(self, line, regex_replace_tuples):
        for regex_replace_tuple in regex_replace_tuples:
            line = self.apply_regex_tuple_to_line(line, regex_replace_tuple)
        return line

    def apply_regex_tuple_to_line(self, line, regex_tuple):
        result = self.can_regex_be_replaced_in_line(line, regex_tuple)
        if result:
            print(f"found a match: {result}")
            line = self.replace_regex_in_line(line, regex_tuple)
        return line

    def can_regex_be_replaced_in_line(self, line, regex_tuple):
        regex = self.regex_replace_tuple[0]
        self.replacement = self.regex_replace_tuple[1]
        return re.search(regex, line)

    def replace_regex_in_line(self, line, regex_tuple):
        regex = self.regex_replace_tuple[0]
        replacement = self.regex_replace_tuple[1]
        return re.sub(regex, replacement, line)

    def update_all_project_files(self, project_file_folder):
        for filename in os.listdir(project_file_folder):
            if filename.endswith(".rzmmpj"):
                self.update_project_file(project_file_folder, filename)

    def write_lines_back_to_file(self, linelist, filename):
        with open(filename, 'w', encoding='utf-16-le') as f:
            f.writelines(linelist)

    def update_project_file(self, folder, filename):
        if not os.path.exists(f"{folder}/{filename}"):
            print(f"file doesn't exists! {folder}/{filename}")
            exit(-1)
        print(f"Updating project file: {filename}")

    def try_update_lyric_file(self, lyric_file_folder, filename):
        lyric_filename = f"{filename}.rzlrc"
        self.exit_progam_if_file_does_not_exist(lyric_file_folder, lyric_filename)
        self.update_lyric_file(lyric_file_folder, lyric_filename)

    def try_update_project_file(self, project_file_folder, filename):
        project_filename = f"{filename}.rzmmpj"
        self.exit_progam_if_file_does_not_exist(project_file_folder, project_filename)
        self.update_project_file(project_file_folder, project_filename)

    def exit_progam_if_file_does_not_exist(self, folder, filename):
        if not os.path.exists(f"{folder}/{filename}"):
            print(f"file doesn't exists! {folder}/{filename}")
            exit(-1)


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