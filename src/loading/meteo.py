# meteo.py
from sqlalchemy import Column, String, Float, Integer, ForeignKey, UniqueConstraint
from src.loading.database import Base


class Meteo(Base):
    __tablename__ = "meteo"
    __table_args__ = (
        UniqueConstraint("city_id", "date", name="uq_city_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(String(255), nullable=False)
    temperature_max = Column(Float, nullable=True)
    temperature_min = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    precipitation_probability = Column(Float, nullable=True)
    wind_speed_max = Column(Float, nullable=True)
    wind_gusts_max = Column(Float, nullable=True)
    weather_code = Column(String(255), nullable=True)
    Categorie_temperature = Column(String(255), nullable=True)
    Categorie_precipitation = Column(String(255), nullable=True)
    Categorie_wind = Column(String(255), nullable=True)