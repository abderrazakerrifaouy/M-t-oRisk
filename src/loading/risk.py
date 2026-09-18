from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.loading.database import Base


class Risk(Base):
    __tablename__ = "risk"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meteo_id: Mapped[int] = mapped_column(Integer, ForeignKey("meteo.id"), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=True)
    niveau: Mapped[str] = mapped_column(String(255), nullable=True)