import pandas as pd


class RiskScore:

    @staticmethod
    def temperature_risk(
        temperature_max: float,
        temperature_min: float
    ):

        heat_risk = 0
        cold_risk = 0

        if temperature_max >= 45:
            heat_risk = 100

        elif temperature_max >= 40:
            heat_risk = 80

        elif temperature_max >= 35:
            heat_risk = 60

        elif temperature_max >= 30:
            heat_risk = 30

        if temperature_min <= 0:
            cold_risk = 100

        elif temperature_min <= 5:
            cold_risk = 75

        elif temperature_min <= 10:
            cold_risk = 50

        return max(heat_risk, cold_risk)


    @staticmethod
    def precipitation_risk(precipitation: float) :

        if precipitation == 0:
            return 0

        elif precipitation < 5:
            return 20

        elif precipitation < 20:
            return 50

        elif precipitation < 50:
            return 80

        else:
            return 100

    @staticmethod
    def wind_risk(wind_speed_max: float) :

        if wind_speed_max < 20:
            return 0

        elif wind_speed_max < 40:
            return 30

        elif wind_speed_max < 60:
            return 70

        else:
            return 100



    @staticmethod
    def gust_risk(wind_gusts_max: float) :

        if wind_gusts_max < 30:
            return 0

        elif wind_gusts_max < 50:
            return 30

        elif wind_gusts_max < 70:
            return 70

        else:
            return 100


    @staticmethod
    def weather_code_risk(weather_code: int):

        if weather_code == 0:
            return 0

        elif weather_code in [1, 2, 3]:
            return 5

        elif weather_code in [45, 48]:
            return 30

        elif weather_code in [51, 53, 55]:
            return 25

        elif weather_code in [56, 57]:
            return 50

        elif weather_code in [61, 63, 65]:
            return 55

        elif weather_code in [66, 67]:
            return 80

        elif weather_code in [71, 73, 75, 77]:
            return 70

        elif weather_code in [80, 81, 82]:
            return 65

        elif weather_code in [85, 86]:
            return 75

        elif weather_code == 95:
            return 90

        elif weather_code in [96, 99]:
            return 100

        return 0



    @staticmethod
    def calculate_risk_score_row(row: pd.Series) :

        temperature_score = RiskScore.temperature_risk(
            row["temperature_max"],
            row["temperature_min"]
        )

        precipitation_score = RiskScore.precipitation_risk(
            row["precipitation"]
        )

        probability_score = row["precipitation_probability"]

        wind_score = RiskScore.wind_risk(
            row["wind_speed_max"]
        )

        gust_score = RiskScore.gust_risk(
            row["wind_gusts_max"]
        )

        weather_score = RiskScore.weather_code_risk(
            int(row["weather_code"])
        )

        final_score = (
            temperature_score * 0.15
            + precipitation_score * 0.25
            + probability_score * 0.10
            + wind_score * 0.20
            + gust_score * 0.20
            + weather_score * 0.10
        )

        return final_score



    @staticmethod
    def calculate_risk_score(df):

        df["risk_score"] = df.apply(
            RiskScore.calculate_risk_score_row,
            axis=1
        )

        return df