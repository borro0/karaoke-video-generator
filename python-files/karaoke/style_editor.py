from pathlib import Path
import click
import re
import os

DEFAULT_DIRECTORY = "C:/Users/boris/Google Drive/Live Karaoke Band/Lyric-videos/Video edit files"

@click.command()
@click.option("-d", "--directory", default=DEFAULT_DIRECTORY, help=(
    "All files this directory should be updated."))
@click.option("-f", "--filename", help=(
    "Update a only specific file. Give the complete filename of target file,"
    "it will be searched in the default directory"))
def edit_style(directory, filename):
    """
    This program updates video-edit files to the style defined in this file.
    All files in the (default) directory can be updated, or a single-specific file.
    The directory should have the following structure:
    root
    --Lyric files
    ----song1.rzlrc
    ----song2.rzlrc
    ----etc...
    --projects
    ----song1.rzmmpj
    ----song2.rzmmpj
    ----etc...
    """

    lyric_file_directory = f"{directory}/Lyric files"
    project_file_directory = f"{directory}/projects"

    style_editor = StyleEditor()

    if(filename):
        print(f"Updating style of specific file: {filename}")
        style_editor.try_update_lyric_file(lyric_file_directory, filename)
        style_editor.try_update_project_file(project_file_directory, filename)
    else:
        print("Updating style of all files in the directory")
        style_editor.update_all_lyric_files(lyric_file_directory)
        style_editor.update_all_project_files(project_file_directory)


class StyleEditor(object):
    def update_all_lyric_files(self, lyric_file_directory):
        for filename in os.listdir(lyric_file_directory):
            if filename.endswith(".rzlrc"):
                self.update_lyric_file(lyric_file_directory, filename)

    def update_lyric_file(self, directory, filename):
        print(f"Updating lyric file: {filename}")

        regex_replace_tuples = []
        regex_replace_tuples = regex_replace_tuples + [(" nLineInterval=\"[^\"]*\" ", " nLineInterval=\"150\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" lfHeight=\"[^\"]*\" ", " lfHeight=\"32\" ")]

        self.apply_regex_replace_to_file(f"{directory}/{filename}", regex_replace_tuples)

    def apply_regex_replace_to_file(self, filepath, regex_replace_tuples):
        print("Converting file from utf-8 to utf-16")
        self.convert_file_from_utf8_to_utf16(filepath)

        print("reading all lines of file")
        linelist = self.read_all_lines_of_file(filepath)
        print("lines read", len(linelist))

        self.print_regex_replace_tuples(regex_replace_tuples)

        linelist[:] = [self.apply_regex_tuples_to_line(line, regex_replace_tuples) for line in linelist]

        print("write changes back to file")
        self.write_lines_back_to_file(linelist, filepath)

    def convert_file_from_utf8_to_utf16(self, filepath):
        try:
            content = ''
            with open(filepath, 'r', encoding="utf-8") as f:
                content = f.read()
            with open(filepath, 'w', encoding="utf-16") as f:
                f.write(content)
        except UnicodeDecodeError:
            print("File is probably already utf-16")

    def read_all_lines_of_file(self, filepath):
        with open(filepath, 'r', encoding='utf-16-le') as f:
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
        regex = regex_tuple[0]
        self.replacement = regex_tuple[1]
        return re.search(regex, line)

    def replace_regex_in_line(self, line, regex_tuple):
        regex = regex_tuple[0]
        replacement = regex_tuple[1]
        return re.sub(regex, replacement, line)

    def write_lines_back_to_file(self, linelist, filepath):
        with open(filepath, 'w', encoding='utf-16-le') as f:
            f.writelines(linelist)

    def update_all_project_files(self, project_file_directory):
        for filename in os.listdir(project_file_directory):
            if filename.endswith(".rzmmpj"):
                self.update_project_file(project_file_directory, filename)

    def update_project_file(self, directory, filename):
        print(f"Updating project file: {filename}")

        regex_replace_tuples = []
        regex_replace_tuples = regex_replace_tuples + [(" eVResolution=\"[^\"]*\" ", " eVResolution=\"1\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" lBitRate=\"[^\"]*\" ", " lBitRate=\"2000\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" lFrameHeight=\"[^\"]*\" ", " lFrameHeight=\"720\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" lFrameWidth=\"[^\"]*\" ", " lFrameWidth=\"1280\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" vensettingIndex=\"[^\"]*\" ", " vensettingIndex=\"2\" ")]
        regex_replace_tuples = regex_replace_tuples + [(" nIndex=\"[^\"]*\"  nMp4P", " nIndex=\"2\" nMp4P")]
        regex_replace_tuples = regex_replace_tuples + [(" TitlelfHeight=\"[^\"]*\" ", " TitlelfHeight=\"2\" ")]
        

        self.apply_regex_replace_to_file(f"{directory}/{filename}", regex_replace_tuples)

    def try_update_lyric_file(self, lyric_file_directory, filename):
        lyric_filename = f"{filename}.rzlrc"
        self.exit_progam_if_file_does_not_exist(lyric_file_directory, lyric_filename)
        self.update_lyric_file(lyric_file_directory, lyric_filename)

    def try_update_project_file(self, project_file_directory, filename):
        project_filename = f"{filename}.rzmmpj"
        self.exit_progam_if_file_does_not_exist(project_file_directory, project_filename)
        self.update_project_file(project_file_directory, project_filename)

    def exit_progam_if_file_does_not_exist(self, directory, filename):
        if not os.path.exists(f"{directory}/{filename}"):
            print(f"file doesn't exists! {directory}/{filename}")
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
