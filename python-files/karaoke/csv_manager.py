import csv
import tempfile
import os
import datetime
import random

class CsvManager:
    "This class manages the reading of the CSV file, used as database to store all songs"

    DATE_FORMAT = "%d-%m-%Y"
    FALSE_CSV_FIELD_CONTENT_STRING = ""
    TRUE_CSV_FIELD_CONTENT_STRING = "x"

    def __init__(self, csv_file_location):
        self.csv_file_location = csv_file_location
        self.dict = self.read_csv_file(csv_file_location)

    def read_csv_file(self, csv_file_location):
        with open(csv_file_location, mode='r') as csv_file:
            rowsReader = csv.DictReader(csv_file)
            dict = {}
            for row in rowsReader:
                dict[row['Track']] = row
            return dict

    def get_all_rows(self):
        return self.dict.values()

    def print_csv_file(self, csv_file_location):
        line_count = 0
        for row in self.get_all_rows():
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            self.print_row(row)
            line_count += 1
        print(f'Processed {line_count} lines.')

    @staticmethod
    def print_row(row):
        print(f'{row["Track"]}\t\t\t {row["Artist"]}.')

    def generate_red_playlist(self):
        return self.generate_playlist_by_difficulty("red")

    def generate_yellow_playlist(self):
        return self.generate_playlist_by_difficulty("yellow")

    def generate_green_playlist(self):
        return self.generate_playlist_by_difficulty("green")

    def generate_playlist_by_difficulty(self, difficulty_name):
        selected_rows = []
        difficulty_char = self.convert_difficulty_name_to_single_char(difficulty_name)
        for row in self.get_all_rows():
            if row["Extra aandacht"] == difficulty_char:
                video_name = self.convert_row_into_video_name(row)
                selected_rows.append(video_name)
                self.print_row(row)
        return selected_rows

    @staticmethod
    def convert_difficulty_name_to_single_char(difficulty_name):
        difficulty_dict = {
            "green": "g",
            "yellow": "v",
            "red": "o"
        }
        return difficulty_dict[difficulty_name]

    def convert_row_into_video_name(self, row):
        return f"{row['Track']} - {row['Artist']}.mp4"

    def get_playlist_by_name(self, name, shuffle=False):
        playlist = []
        if self.is_playlist_name_a_difficulty(name):
            playlist = self.generate_playlist_by_difficulty(name)
        else:
            for row in self.get_all_rows():
                if row[name] == self.TRUE_CSV_FIELD_CONTENT_STRING:
                    video_name = self.convert_row_into_video_name(row)
                    playlist.append(video_name)
        
        if shuffle:
            random.shuffle(playlist)
        
        return playlist

    @staticmethod
    def is_playlist_name_a_difficulty(name):
        return name in ["green", "yellow", "red"]

    @staticmethod
    def store_playlist_to_file(playlist):
        fd, filename = tempfile.mkstemp(suffix='.txt', text=True)
        with os.fdopen(fd, 'w') as f:
            f.writelines('\n'.join(playlist))
        return filename

    def record_song_played(self, song, date=datetime.date.today()):
        """
        Put record in csv file that song is played.
        If there exists a column of current day, set field to TRUE.
        If such a column does not exist yet, create one.
        """
        track = self.get_title_from_song(song)
        print("Insert ", track)
        formatted_date = self.convert_date_to_string(date)
        if formatted_date not in self.dict[track]:
            print("No column exists for ", formatted_date, " creating one now.")
            self.insert_date_column(formatted_date)

        self.dict[track][formatted_date] = self.TRUE_CSV_FIELD_CONTENT_STRING
        self.write_changes_to_csv_file()

    @staticmethod
    def get_title_from_song(song):
        return song.split(" - ")[0]

    def convert_date_to_string(self, date):
        date = date.strftime(self.DATE_FORMAT)
        date_withouth_leading_zeros = date.lstrip("0").replace(" 0", " ").replace("-0", "-")
        return date_withouth_leading_zeros

    def insert_date_column(self, date):
        for row in self.get_all_rows():
            self.dict[row['Track']].update({date: self.FALSE_CSV_FIELD_CONTENT_STRING})

        self.reorder_columns()

    def reorder_columns(self):
        fieldnames = self.get_field_names()
        sorted_fieldnames = self.sort_fieldnames(fieldnames)

        new_dict = {}
        for row in self.get_all_rows():
            new_row = {}
            for fieldname in sorted_fieldnames:
                new_row[fieldname] = row[fieldname]
            new_dict[row['Track']] = new_row

        self.dict = new_dict

    def sort_fieldnames(self, fieldnames):
        date_list = []
        non_date_list = []
        for fieldname in fieldnames:
            if self.is_date(fieldname):
                date_list.append(fieldname)
            else:
                non_date_list.append(fieldname)

        sorted_date_list = self.sort_dates(date_list)
        complete_list = non_date_list + sorted_date_list
        return complete_list

    def sort_dates(self, dates):
        dates.sort(key=lambda date: datetime.datetime.strptime(date, self.DATE_FORMAT))
        dates.reverse()
        return dates

    def is_date(self, date):
        try:
            datetime.datetime.strptime(date, self.DATE_FORMAT)
            return True
        except ValueError:
            print(date, "is not a date")
            return False

    def write_changes_to_csv_file(self):
        fieldnames = self.get_field_names()

        with open(self.csv_file_location, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator=os.linesep)
            writer.writeheader()
            for row in self.get_all_rows():
                writer.writerow(row)

    def get_field_names(self):
        first_row = list(self.get_all_rows())[0]
        keys_or_first_row = first_row.keys()
        return list(keys_or_first_row)

    def get_all_playlist_names(self):
        field_names = self.get_field_names()
        field_names = self.remove_pre_defined_non_playlist_fields(field_names)
        field_names = self.remove_dates_from_field_names(field_names)
        field_names = field_names + self.get_all_colored_playlists_names()
        print(field_names)
        return field_names

    def remove_pre_defined_non_playlist_fields(self, field_names):
        non_playlist_fields = ["Track", "Artist", "Selectie", "Date Added",
                               "BPM", "Extra aandacht", "Shuffle?", "Actief", "Video"]
        for field in non_playlist_fields:
            try:
                field_names.remove(field)
            except ValueError:
                print("Tried to remove ", field, " from list, but it was not a member of list")
        return field_names

    def remove_dates_from_field_names(self, field_names):
        for item in list(field_names):
            if self.is_date(item):
                field_names.remove(item)
        return field_names

    def get_all_colored_playlists_names(self):
        return ["red", "yellow", "green"]

    def not_allowed_to_alter_csv_file(self):
        try:
            with open(self.csv_file_location, "w"):
                return False
        except PermissionError:
            print("Not allowed to alter csv file")
            return True
