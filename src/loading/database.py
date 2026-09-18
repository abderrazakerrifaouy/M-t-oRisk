from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg2://abderrazak:abderrazak@localhost:5432/mtoRisk"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass

def create_tables():
    from src.loading.city import City
    from src.loading.meteo import Meteo
    from src.loading.risk import Risk

    Base.metadata.create_all(bind=engine)