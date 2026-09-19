import pandas as pd
from datetime import date, timedelta
from src.loading.city import City
from src.loading.meteo import Meteo
from src.loading.risk import Risk
from src.exceptions import LoadingError


class Inserter:
    def __init__(self, data: pd.DataFrame, session_factory):
        self.data = data
        self.session_factory = session_factory

    def get_or_create_city(self, session, row):
        city_obj = (
            session.query(City)
            .filter_by(city=row["city"], country=row["country"])
            .first()
        )
        if city_obj is None:
            city_obj = City(
                city=row["city"],
                country=row["country"],
                latitude=row["latitude"],
                longitude=row["longitude"],
            )
            session.add(city_obj)
            session.flush()
        return city_obj

    def upsert_meteo(self, session, row, city_id):
        meteo_obj = (
            session.query(Meteo)
            .filter_by(city_id=city_id, date=str(row["date"]))
            .first()
        )
        fields = dict(
            temperature_max=row.get("temperature_max"),
            temperature_min=row.get("temperature_min"),
            precipitation=row.get("precipitation"),
            precipitation_probability=row.get("precipitation_probability"),
            wind_speed_max=row.get("wind_speed_max"),
            wind_gusts_max=row.get("wind_gusts_max"),
            weather_code=str(row.get("weather_code")),
            Categorie_temperature=row.get("Categorie_temperature"),
            Categorie_precipitation=row.get("Categorie_precipitation"),
            Categorie_wind=row.get("Categorie_wind"),
        )

        if meteo_obj is None:
            meteo_obj = Meteo(city_id=city_id, date=str(row["date"]), **fields)
            session.add(meteo_obj)
        else:
            for key, value in fields.items():
                setattr(meteo_obj, key, value)

        session.flush()
        return meteo_obj

    def upsert_risk(self, session, row, meteo_id):
        risk_obj = session.query(Risk).filter_by(meteo_id=meteo_id).first()
        if risk_obj is None:
            risk_obj = Risk(
                meteo_id=meteo_id,
                risk_score=row.get("risk_score"),
                niveau=row.get("niveau_risque"),
            )
            session.add(risk_obj)
        else:
            risk_obj.risk_score = row.get("risk_score")
            risk_obj.niveau = row.get("niveau_risque")

    def cleanup_old_dates(self, session):
        today_str = date.today().isoformat()
        old_meteo = session.query(Meteo).filter(Meteo.date < today_str).all()
        for m in old_meteo:
            session.query(Risk).filter_by(meteo_id=m.id).delete()
            session.delete(m)

    def run(self):
        session = self.session_factory()
        try:
            for _, row in self.data.iterrows():
                city_obj = self.get_or_create_city(session, row)
                meteo_obj = self.upsert_meteo(session, row, city_obj.id)
                self.upsert_risk(session, row, meteo_obj.id)

            self.cleanup_old_dates(session)

            session.commit()
        except Exception as exc:
            session.rollback()
            raise LoadingError("Database transaction failed while loading weather data") from exc
        finally:
            session.close()