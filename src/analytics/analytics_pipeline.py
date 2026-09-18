from src.loading.database import SessionLocal
from src.analytics.queries import QueryRunner


class AnalyticsPipeline:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def run(self):
        session = self.session_factory()
        try:
            runner = QueryRunner(session)

            print("\n🌡️ Top températures :")
            for row in runner.top_temperatures():
                print(row)

            print("\n🌧️ Top précipitations :")
            for row in runner.top_precipitations():
                print(row)

            print("\n⚠️ Risque moyen par ville :")
            for row in runner.average_risk_by_city():
                print(row)

            print("\n📅 Périodes à risque maximal :")
            for row in runner.max_risk_by_period():
                print(row)

            print("\n🏙️ Risque max par ville :")
            for row in runner.max_risk_per_city():
                print(row)

            print("\n📊 Statistiques globales :")
            print(runner.global_stats())

        finally:
            session.close()


