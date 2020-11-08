import csv
import tempfile
import os
import datetime


class CsvManager:
    "This class manages the reading of the CSV file, used as database to store all songs"

    DATE_FORMAT = "%d-%m-%Y"

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

    def print_csv_file(self, csv_file_location):
        line_count = 0
        for row in self.dict.values():
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'{row["Track"]}\t\t\t {row["Artist"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')

    def generate_red_playlist(self):
        return self.generate_playlist_by_difficulty("o")

    def generate_yellow_playlist(self):
        return self.generate_playlist_by_difficulty("v")

    def generate_green_playlist(self):
        return self.generate_playlist_by_difficulty("g")

    def generate_playlist_by_difficulty(self, difficulty):
        selected_rows = []
        for row in self.dict.values():
            if row["Video"] == "FALSE":
                continue
            if row["Extra aandacht"] == difficulty:
                video_name = self.convert_row_into_video_name(row)
                selected_rows.append(video_name)
        return selected_rows

    def convert_row_into_video_name(self, row):
        return f"{row['Track']} - {row['Artist']}.mp4"

    @staticmethod
    def store_playlist_to_file(playlist):
        fd, filename = tempfile.mkstemp(suffix='.txt', text=True)
        with os.fdopen(fd, 'w') as f:
            f.writelines('\n'.join(playlist))
        return filename

    def record_song_played(self, song, date=datetime.date.today()):
        track = self.get_title_from_song(song)
        formatted_date = date.strftime(self.DATE_FORMAT)
        print("formatted_date ", formatted_date)
        # lookup row
        # see if current date column exists
        if formatted_date not in self.dict[track]:
            self.insert_date_column(formatted_date)

        # store in row
        self.dict[track][formatted_date] = "TRUE"

        # update csv file
        self.write_to_csv_file()

    def insert_date_column(self, date):
        for row in self.dict.values():
            self.dict[row['Track']].update({date: "FALSE"})

        self.reorder_columns()

    def reorder_columns(self):
        fieldnames = self.get_field_names()
        sorted_fieldnames = self.sort_fieldnames(fieldnames)

        new_dict = {}
        for row in self.dict.values():
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
            return False

    def write_to_csv_file(self):
        fieldnames = self.get_field_names()
        print("fieldnames: ", fieldnames)

        with open(self.csv_file_location, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.dict.values():
                writer.writerow(row)

    def get_field_names(self):
        first_row = list(self.dict.values())[0]
        keys_or_first_row = first_row.keys()
        return list(keys_or_first_row)

    @staticmethod
    def get_title_from_song(song):
        return song.split(" - ")[0]
