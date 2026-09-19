from src.loading.database import SessionLocal
from src.analytics.queries import QueryRunner
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions import AnalyticsError


class AnalyticsPipeline:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def run(self):
        try:
            session = self.session_factory()
            runner = QueryRunner(session)

            print("\nTop températures :")
            for row in runner.top_temperatures():
                print(row)

            print("\nTop précipitations :")
            for row in runner.top_precipitations():
                print(row)

            print("\nRisque moyen par ville :")
            for row in runner.average_risk_by_city():
                print(row)

            print("\nPériodes à risque maximal :")
            for row in runner.max_risk_by_period():
                print(row)

            print("\nRisque max par ville :")
            for row in runner.max_risk_per_city():
                print(row)

            print("\nStatistiques globales :")
            print(runner.global_stats())

        except SQLAlchemyError as exc:
            raise AnalyticsError("Analytics queries failed") from exc
        except SQLAlchemyError as exc:
            raise AnalyticsError("Analytics queries failed") from exc
        finally:
            if "session" in locals():
                session.close()


