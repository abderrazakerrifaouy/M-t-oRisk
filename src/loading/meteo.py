# meteo.py
from sqlalchemy import String, Float, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.loading.database import Base


class Meteo(Base):
    __tablename__ = "meteo"
    __table_args__ = (
        UniqueConstraint("city_id", "date", name="uq_city_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"), nullable=False)
    date: Mapped[str] = mapped_column(String(255), nullable=False)
    temperature_max: Mapped[float] = mapped_column(Float, nullable=True)
    temperature_min: Mapped[float] = mapped_column(Float, nullable=True)
    precipitation: Mapped[float] = mapped_column(Float, nullable=True)
    precipitation_probability: Mapped[float] = mapped_column(Float, nullable=True)
    wind_speed_max: Mapped[float] = mapped_column(Float, nullable=True)
    wind_gusts_max: Mapped[float] = mapped_column(Float, nullable=True)
    weather_code: Mapped[str] = mapped_column(String(255), nullable=True)
    Categorie_temperature: Mapped[str] = mapped_column(String(255), nullable=True)
    Categorie_precipitation: Mapped[str] = mapped_column(String(255), nullable=True)
    Categorie_wind: Mapped[str] = mapped_column(String(255), nullable=True)