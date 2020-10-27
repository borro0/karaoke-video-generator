import csv


class CsvManager:
    "This class manages the reading of the CSV file, used as database to store all songs"
    def __init__(self, csv_file_location):
        self.rows = self.read_csv_file(csv_file_location)

    def read_csv_file(self, csv_file_location):
        with open(csv_file_location, mode='r') as csv_file:
            rowsReader = csv.DictReader(csv_file)
            rows = []
            first_line = True
            for row in rowsReader:
                if first_line:
                    first_line = False
                else:
                    rows.append(row)
            return rows

    def print_csv_file(self, csv_file_location):
        line_count = 0
        for row in self.rows:
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
        for row in self.rows:
            if row["Extra aandacht"] == difficulty:
                video_name = self.convert_row_into_video_name(row)
                selected_rows.append(video_name)
        return selected_rows
    
    def convert_row_into_video_name(self, row):
        return f"{row['Track']} - {row['Artist']}.mp4"

