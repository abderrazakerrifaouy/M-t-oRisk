from sqlalchemy import Column, String, Float, Integer, ForeignKey
from src.loading.database import Base


class Risk(Base):
    __tablename__ = "risk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meteo_id = Column(Integer, ForeignKey("meteo.id"), nullable=False)
    risk_score = Column(Float, nullable=True)
    niveau = Column(String(255), nullable=True)