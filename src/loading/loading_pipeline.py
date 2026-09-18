import pandas as pd
from src.loading.database import SessionLocal, create_tables
from src.loading.inserte import Inserter


class LoadingPipeline:
    def __init__(self, silver_path: str, session_factory=SessionLocal):
        self.silver_path = silver_path
        self.session_factory = session_factory

    def extract(self) -> pd.DataFrame:
        data = pd.read_csv(self.silver_path)
        return data

    def load(self, data: pd.DataFrame):
        inserter = Inserter(data=data, session_factory=self.session_factory)
        inserter.run()

    def run(self):
        create_tables()  
        data = self.extract()
        self.load(data)


