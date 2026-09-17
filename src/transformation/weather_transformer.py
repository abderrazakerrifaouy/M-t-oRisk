import pandas as pd
from abc import ABC, abstractmethod


class WeatherTransformer:

    @staticmethod
    def transform(df):
        base = df[
            ["city",
             "country",
            "latitude",
            "longitude"]
        ].copy()

        daily = pd.json_normalize(df["daily"])
        
        daily = daily.apply(
            lambda column: column.explode()
        )
        daily = daily.reset_index(drop=True)

        base = base.loc[
            base.index.repeat(
                df["daily"].str["time"].str.len()
            )
        ].reset_index(drop=True)

        result = pd.concat(
            [base, daily],
            axis=1
        )

        result = result.rename(
            columns={
                "time": "date",
                "temperature_2m_max": "temperature_max",
                "temperature_2m_min": "temperature_min",
                "precipitation_sum": "precipitation",
                "precipitation_probability_max": "precipitation_probability",
                "wind_speed_10m_max": "wind_speed_max",
                "wind_gusts_10m_max": "wind_gusts_max"
            }
        )


        return result