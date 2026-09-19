import pandas as pd

from src.exceptions import ExtractionError


class CitiesExtractor:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        try:
            df = pd.read_csv(self.file_path)
            required_columns = {"city", "lat", "lng"}
            missing_columns = required_columns.difference(df.columns)
            if missing_columns:
                raise ExtractionError(
                    f"Cities file is missing columns: {sorted(missing_columns)}"
                )

            cities = df[["city", "lat", "lng"]].copy()
            if cities.empty:
                raise ExtractionError("Cities file contains no cities")

            return cities
        except ExtractionError:
            raise
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
            raise ExtractionError(
                f"Unable to read cities file: {self.file_path}"
            ) from exc
        except (TypeError, ValueError) as exc:
            raise ExtractionError(
                f"Invalid values in cities file: {self.file_path}"
            ) from exc