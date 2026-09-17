import pandas as pd
from abc import ABC, abstractmethod



class StandardizeTypes:

    @staticmethod
    def standardize(df):
        df["date"] = pd.to_datetime(df["date"])
        df["temperature_max"] = df["temperature_max"].astype(float)
        df["temperature_min"] = df["temperature_min"].astype(float)
        df["precipitation"] = df["precipitation"].astype(float)
        df["precipitation_probability"] = df["precipitation_probability"].astype(float)
        df["wind_speed_max"] = df["wind_speed_max"].astype(float)
        df["wind_gusts_max"] = df["wind_gusts_max"].astype(float)

        return df