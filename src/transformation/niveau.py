import pandas as pd


class Niveau:

    @staticmethod
    def get_niveau(risk_score: float) -> str:

        if risk_score < 25:
            return "Faible"

        elif risk_score < 50:
            return "Modérée"

        elif risk_score < 75:
            return "Forte"

        else:
            return "Très forte"

    @staticmethod
    def add_niveau(df: pd.DataFrame) -> pd.DataFrame:

        df["niveau_risque"] = df["risk_score"].apply(
            Niveau.get_niveau
        )

        return df