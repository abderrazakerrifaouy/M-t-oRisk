from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://abderrazak:abderrazak@postgres:5432/mtoRisk"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


Base = declarative_base()

def create_tables():
    from src.loading.city import City
    from src.loading.meteo import Meteo
    from src.loading.risk import Risk

    Base.metadata.create_all(bind=engine)