import csv
import tempfile
import os
import datetime


class CsvManager:
    "This class manages the reading of the CSV file, used as database to store all songs"

    def __init__(self, csv_file_location):
        self.dict = self.read_csv_file(csv_file_location)

    def read_csv_file(self, csv_file_location):
        with open(csv_file_location, mode='r') as csv_file:
            rowsReader = csv.DictReader(csv_file)
            dict = {}
            first_line = True
            for row in rowsReader:
                if first_line:
                    first_line = False
                else:
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
        formatted_date = date.strftime("%d-%m-%Y")
        print(formatted_date)
        # lookup row
        # see if current date column exists
        if formatted_date not in self.dict[track]:
            self.insert_date_column(formatted_date)

        self.dict[track][formatted_date] = "TRUE"


        # store in row

        # update csv file
        pass

    def insert_date_column(self, date):
        for row in self.dict.values():
            self.dict[row['Track']].update({date: "FALSE"})

    @staticmethod
    def get_title_from_song(song):
        return song.split(" - ")[0]
