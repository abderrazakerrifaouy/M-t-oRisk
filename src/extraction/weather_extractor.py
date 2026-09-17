class WeatherExtractor:

    def __init__(self, api_client):
        self.api_client = api_client

    def extract(self, cities):
        latitudes = ",".join(
            cities["lat"].values.astype(str)
        )

        longitude = ','.join(
            cities['lng'].values.astype(str)
        )

        params = {
            "latitude": latitudes,
            "longitude":longitude ,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "weather_code"
            ],
            "timezone": "Africa/Casablanca"
        }

        data = self.api_client.get(params)

        return data
