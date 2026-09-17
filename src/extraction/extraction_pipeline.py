import pandas as pd
from src.extraction.cities_extractor import CitiesExtractor
from src.extraction.api_client import APIClient
from src.extraction.weather_extractor import WeatherExtractor

class ExtractionPipeline:
    
    def __init__(self, cities_file_path, api_base_url):
        self.cities_extractor = CitiesExtractor(cities_file_path)
        self.api_client = APIClient(api_base_url)
        self.weather_extractor = WeatherExtractor(self.api_client)

    def run(self):
        cities = self.cities_extractor.extract()
        data = self.weather_extractor.extract(cities)
        data_df = pd.DataFrame(data)
        data_df.to_json("data/bronze/weather_data.json", orient="records", indent=4)

