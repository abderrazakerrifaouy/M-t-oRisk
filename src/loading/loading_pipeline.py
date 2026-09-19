import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from src.loading.database import SessionLocal, create_tables
from src.loading.inserte import Inserter
from src.exceptions import LoadingError


class LoadingPipeline:
    def __init__(self, silver_path: str, session_factory=SessionLocal):
        self.silver_path = silver_path
        self.session_factory = session_factory

    def extract(self) -> pd.DataFrame:
        try:
            data = pd.read_csv(self.silver_path)
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
            raise LoadingError(
                f"Unable to read transformed data: {self.silver_path}"
            ) from exc

        if data.empty:
            raise LoadingError("Transformed data contains no rows")
        return data

    def load(self, data: pd.DataFrame):
        inserter = Inserter(data=data, session_factory=self.session_factory)
        inserter.run()

    def run(self):
        try:
            create_tables()
            data = self.extract()
            self.load(data)
        except LoadingError:
            raise
        except (OSError, RuntimeError, ValueError, SQLAlchemyError) as exc:
            raise LoadingError("Loading data into PostgreSQL failed") from exc


