from sqlalchemy import Numeric, cast, func, desc
from sqlalchemy.orm import Session

from src.loading.city import City
from src.loading.meteo import Meteo
from src.loading.risk import Risk


class QueryRunner:
    def __init__(self, session: Session):
        self.session = session

    def top_temperatures(self, limit: int = 10):
        return (
            self.session.query(
                City.city, City.country, Meteo.date, Meteo.temperature_max
            )
            .join(Meteo, Meteo.city_id == City.id)
            .order_by(desc(Meteo.temperature_max))
            .limit(limit)
            .all()
        )

    def top_precipitations(self, limit: int = 10):
        return (
            self.session.query(
                City.city, City.country, Meteo.date,
                Meteo.precipitation, Meteo.precipitation_probability
            )
            .join(Meteo, Meteo.city_id == City.id)
            .order_by(desc(Meteo.precipitation))
            .limit(limit)
            .all()
        )

    def average_risk_by_city(self):
        return (
            self.session.query(
                City.city, City.country,
                func.round( cast(func.avg(Risk.risk_score), Numeric),
                    2
                ).label("risque_moyen")
            )
            .join(Meteo, Meteo.city_id == City.id)
            .join(Risk, Risk.meteo_id == Meteo.id)
            .group_by(City.city, City.country)
            .order_by(desc("risque_moyen"))
            .all()
        )

    def max_risk_by_period(self, limit: int = 10):
        return (
            self.session.query(
                Meteo.date,
                func.max(Risk.risk_score).label("risque_max")
            )
            .join(Risk, Risk.meteo_id == Meteo.id)
            .group_by(Meteo.date)
            .order_by(desc("risque_max"))
            .limit(limit)
            .all()
        )

    def max_risk_per_city(self):
        subquery = (
            self.session.query(
                City.id.label("city_id"),
                func.max(Risk.risk_score).label("max_risk")
            )
            .join(Meteo, Meteo.city_id == City.id)
            .join(Risk, Risk.meteo_id == Meteo.id)
            .group_by(City.id)
            .subquery()
        )

        return (
            self.session.query(
                City.city, City.country, Meteo.date, Risk.risk_score, Risk.niveau
            )
            .join(Meteo, Meteo.city_id == City.id)
            .join(Risk, Risk.meteo_id == Meteo.id)
            .join(
                subquery,
                (subquery.c.city_id == City.id)
                & (subquery.c.max_risk == Risk.risk_score),
            )
            .all()
        )

    def global_stats(self):
        nb_villes = self.session.query(func.count(City.id)).scalar()
        temp_max = self.session.query(func.max(Meteo.temperature_max)).scalar()
        precip_max = self.session.query(func.max(Meteo.precipitation)).scalar()
        return {
            "nombre_villes": nb_villes,
            "temperature_maximale": temp_max,
            "precipitation_maximale": precip_max,
        }

    def risk_distribution_by_city(self):
        return (
            self.session.query(
                City.city, Risk.niveau, func.count(Risk.id).label("nombre_jours")
            )
            .join(Meteo, Meteo.city_id == City.id)
            .join(Risk, Risk.meteo_id == Meteo.id)
            .group_by(City.city, Risk.niveau)
            .order_by(City.city, desc("nombre_jours"))
            .all()
        )