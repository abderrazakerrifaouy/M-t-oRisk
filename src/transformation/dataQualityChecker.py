import pandas as pd


class DataQualityChecker:

    def __init__(self, df):
        self.df = df

    def fixed_missing_values(self):

        self.df.fillna(
            self.df.mean(numeric_only=True),
            inplace=True
        )

        self.check_temperature()
        self.check_precipitation()
 

    def delete_duplicates(self):

        duplicates = self.df[
            self.df.duplicated()
        ]

        self.df = self.df.drop_duplicates()

        return duplicates

    def check_temperature(self):

        mask = (
            self.df["temperature_max"]
            < self.df["temperature_min"]
        )
        
        max_temp = self.df.loc[
            mask,
            "temperature_max"
        ].copy()

        self.df.loc[
            mask,
            "temperature_max"
        ] = self.df.loc[
            mask,
            "temperature_min"
        ]

        self.df.loc[
            mask,
            "temperature_min"
        ] = max_temp

    def check_precipitation(self):

        mask = self.df["precipitation"] < 0

        self.df.loc[
            mask,
            "precipitation"
        ] = 0
        
    def float_values(self):
        self.df["precipitation"] = self.df["precipitation"].round(2)

        

    def get_dataframe(self):

        return self.df