
def run_extraction():
    from src.extraction.extraction_pipeline import ExtractionPipeline
    pipeline = ExtractionPipeline("data/bronze/ma.csv", "https://api.open-meteo.com/v1/forecast")
    pipeline.run()


def run_transformation():
    from src.transformation.transformation_pipeline import TransformationPipeline
    pipeline = TransformationPipeline("data/bronze/ma.csv", "data/bronze/weather_data.json")
    pipeline.run()


def run_loading():
    from src.loading.loading_pipeline import LoadingPipeline
    pipeline = LoadingPipeline(silver_path="data/silver/cleaned_data.csv")
    pipeline.run()

run_extraction()
run_transformation()
run_loading()