import pandas as pd


class CitiesExtractor:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        df = pd.read_csv(self.file_path)

        cities = df[["city", "lat", "lng"]].copy()

        return cities