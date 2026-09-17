import pandas as pd
import sqlalchemy as sa


class DatabaseLoader:
    engine = sa.create_engine(
        "postgresql+psycopg2://abderrazak:abderrazak@localhost:5432/m-toRisk"
    )
    def __init__(self):
        self.verify_connection()

    def verify_connection(self):
        try:
            with self.engine.connect() as connection:
                print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")