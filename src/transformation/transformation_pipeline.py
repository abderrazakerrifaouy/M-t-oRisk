import pandas as pd
from src.transformation.merging import Merging 
from src.transformation.weather_transformer import WeatherTransformer
from src.transformation.standardize_types import StandardizeTypes
from src.transformation.dataQualityChecker import DataQualityChecker
from src.transformation.category import Category
from src.transformation.risk_score import RiskScore
from src.transformation.niveau import Niveau
from src.exceptions import TransformationError


class TransformationPipeline:
    def __init__(self, cities_file_path, weather_file_path):
        try:
            self.cities_df = pd.read_csv(cities_file_path)
            self.weather_df = pd.read_json(weather_file_path, orient='records')
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as exc:
            raise TransformationError(
                "Unable to read transformation input files"
            ) from exc
        self.merging = Merging(self.cities_df, self.weather_df)

    def run(self):
        try:
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

            if cleaned_df.empty:
                raise TransformationError("Transformation produced no rows")

            cleaned_df.to_csv("data/silver/cleaned_data.csv", index=False)
        except TransformationError:
            raise
        except (KeyError, TypeError, ValueError, OSError) as exc:
            raise TransformationError("Weather data transformation failed") from exc




