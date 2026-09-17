import pandas as pd


class Merging:
    def __init__(self, cities_df, weather_df):
        self.cities_df = cities_df
        self.weather_df = weather_df

    def merge(self):
        self.cities_df = self.cities_df[['city' , 'country'] ]
        merged_df = pd.concat([self.cities_df, self.weather_df], axis=1)
        return merged_df