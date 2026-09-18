import pandas as pd
from src.transformation.merging import Merging 
from src.transformation.weather_transformer import WeatherTransformer
from src.transformation.standardize_types import StandardizeTypes
from src.transformation.dataQualityChecker import DataQualityChecker
from src.transformation.category import Category
from src.transformation.risk_score import RiskScore
from src.transformation.niveau import Niveau


class TransformationPipeline:
    def __init__(self, cities_file_path, weather_file_path):
        self.cities_df = pd.read_csv(cities_file_path)
        self.weather_df = pd.read_json(weather_file_path, orient='records')
        self.merging = Merging(self.cities_df, self.weather_df)

    def run(self):

        merged_df = self.merging.merge()

        transformed_df = WeatherTransformer.transform(merged_df)

        standardized_df = StandardizeTypes.standardize(transformed_df)

        data_quality_checker = DataQualityChecker(standardized_df)

        data_quality_checker.float_values()

        data_quality_checker.check_temperature()

        data_quality_checker.check_precipitation()

        data_quality_checker.fixed_missing_values()

        data_quality_checker.delete_duplicates()

        cleaned_df = data_quality_checker.get_dataframe()

        cleaned_df = Category.add_Categories_temp(cleaned_df)

        cleaned_df = Category.add_Categories_prec(cleaned_df)

        cleaned_df = Category.add_Categories_wind(cleaned_df)

        cleaned_df = RiskScore.calculate_risk_score(cleaned_df)

        cleaned_df = Niveau.add_niveau(cleaned_df)
        
        cleaned_df.to_csv('data/silver/cleaned_data.csv', index=False)




