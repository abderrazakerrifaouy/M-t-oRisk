from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "abderrazak",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
}


def run_extraction(**context):
    from src.extraction.extraction_pipeline import ExtractionPipeline
    pipeline = ExtractionPipeline("data/bronze/ma.csv", "https://api.open-meteo.com/v1/forecast")
    pipeline.run()


def run_transformation(**context):
    from src.transformation.transformation_pipeline import TransformationPipeline
    pipeline = TransformationPipeline("data/bronze/ma.csv", "data/bronze/weather_data.json")
    pipeline.run()


def run_loading(**context):
    from src.loading.loading_pipeline import LoadingPipeline
    pipeline = LoadingPipeline(silver_path="data/silver/cleaned_data.csv")
    pipeline.run()


def refresh_dashboard_cache(**context):
    """
    Streamlit @st.cache_data kay refreshi wa7dou b TTL,
    hna ghi log conditionnel bach ntbeto executé (webhook/notification mstaqbaliya).
    """
    print("[Airflow] Données rafraîchies dans PostgreSQL - dashboard mis à jour au prochain TTL.")


with DAG(
    dag_id="meteo_risk_pipeline",
    description="Pipeline ETL complet : extraction API -> transformation -> loading PostgreSQL",
    default_args=default_args,
    schedule_interval="@daily",       
    start_date=datetime(2026, 9, 18),
    catchup=False,
    tags=["meteo", "etl", "m-t-orisk"],
) as dag:

    extraction_task = PythonOperator(
        task_id="extraction",
        python_callable=run_extraction,
    )

    transformation_task = PythonOperator(
        task_id="transformation",
        python_callable=run_transformation,
    )

    loading_task = PythonOperator(
        task_id="loading",
        python_callable=run_loading,
    )

    refresh_task = PythonOperator(
        task_id="refresh_dashboard",
        python_callable=refresh_dashboard_cache,
    )

    extraction_task >> transformation_task >> loading_task >> refresh_task