import streamlit as st
import pandas as pd
import plotly.express as px

from src.loading.database import SessionLocal
from src.loading.city import City
from src.loading.meteo import Meteo
from src.loading.risk import Risk


st.set_page_config(page_title="Dashboard Météo & Risques - Maroc", layout="wide")



@st.cache_data(ttl=300)
def load_data():
    session = SessionLocal()
    try:
        query = (
            session.query(
                City.city,
                City.country,
                Meteo.date,
                Meteo.temperature_max,
                Meteo.temperature_min,
                Meteo.precipitation,
                Meteo.precipitation_probability,
                Meteo.wind_speed_max,
                Meteo.wind_gusts_max,
                Meteo.Categorie_temperature,
                Meteo.Categorie_precipitation,
                Meteo.Categorie_wind,
                Risk.risk_score,
                Risk.niveau,
            )
            .join(Meteo, Meteo.city_id == City.id)
            .join(Risk, Risk.meteo_id == Meteo.id)
        )
        rows = query.all()
        df = pd.DataFrame(rows, columns=[
            "city", "country", "date", "temperature_max", "temperature_min",
            "precipitation", "precipitation_probability", "wind_speed_max",
            "wind_gusts_max", "categorie_temperature", "categorie_precipitation",
            "categorie_wind", "risk_score", "niveau",
        ])
        df["date"] = pd.to_datetime(df["date"])
        return df
    finally:
        session.close()


df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible. Lancez d'abord le pipeline ETL (extraction → transformation → loading).")
    st.stop()



st.sidebar.header("Filtres")

villes = sorted(df["city"].unique())
selected_villes = st.sidebar.multiselect("Ville(s)", villes, default=villes)

min_date, max_date = df["date"].min().date(), df["date"].max().date()
selected_range = st.sidebar.date_input(
    "Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

niveaux = sorted(df["niveau"].dropna().unique())
selected_niveaux = st.sidebar.multiselect("Niveau de risque", niveaux, default=niveaux)

if isinstance(selected_range, tuple) and len(selected_range) == 2:
    start_date, end_date = selected_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    (df["city"].isin(selected_villes))
    & (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
    & (df["niveau"].isin(selected_niveaux))
]

st.sidebar.markdown(f"**{len(filtered_df)}** lignes après filtrage")
if len(selected_villes) > 15:
    st.sidebar.warning("Beaucoup de villes sélectionnées — certains graphiques se limitent au Top 10.")



st.title("Dashboard Météo & Risques — Maroc")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de villes", filtered_df["city"].nunique())
col2.metric(
    "Température maximale",
    f"{filtered_df['temperature_max'].max():.1f} °C" if not filtered_df.empty else "N/A",
)
col3.metric(
    "Précipitation maximale",
    f"{filtered_df['precipitation'].max():.1f} mm" if not filtered_df.empty else "N/A",
)
col4.metric(
    "Risque moyen global",
    f"{filtered_df['risk_score'].mean():.1f}" if not filtered_df.empty else "N/A",
)

st.divider()

if filtered_df.empty:
    st.info("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()



st.subheader("Top 10 des villes les plus chaudes")
top_temp = (
    filtered_df.sort_values("temperature_max", ascending=False)
    .drop_duplicates(subset="city")
    .head(10)
)
temp_fig = px.bar(
    top_temp.sort_values("temperature_max"),
    x="temperature_max", y="city", orientation="h",
    color="temperature_max", color_continuous_scale="OrRd",
    hover_data=["date"],
    labels={"temperature_max": "Température max (°C)", "city": "Ville"},
)
st.plotly_chart(temp_fig, use_container_width=True)


st.subheader("Top 10 des villes les plus arrosées")
top_precip = (
    filtered_df.sort_values("precipitation", ascending=False)
    .drop_duplicates(subset="city")
    .head(10)
)
precip_fig = px.bar(
    top_precip.sort_values("precipitation"),
    x="precipitation", y="city", orientation="h",
    color="precipitation", color_continuous_scale="Blues",
    hover_data=["date", "precipitation_probability"],
    labels={"precipitation": "Précipitation (mm)", "city": "Ville"},
)
st.plotly_chart(precip_fig, use_container_width=True)



st.subheader("Top 10 des villes à risque moyen le plus élevé")
avg_risk_all = (
    filtered_df.groupby("city", as_index=False)["risk_score"]
    .mean()
    .sort_values("risk_score", ascending=False)
)
top_avg_risk = avg_risk_all.head(10)
avg_risk_fig = px.bar(
    top_avg_risk.sort_values("risk_score"),
    x="risk_score", y="city", orientation="h",
    color="risk_score", color_continuous_scale="Reds",
    labels={"risk_score": "Risque moyen", "city": "Ville"},
)
st.plotly_chart(avg_risk_fig, use_container_width=True)



st.subheader("Risque maximal par période (toutes villes confondues)")
risk_by_date = (
    filtered_df.groupby("date", as_index=False)["risk_score"]
    .max()
    .sort_values("date")
)
risk_time_fig = px.line(
    risk_by_date, x="date", y="risk_score", markers=True,
    labels={"risk_score": "Risque max", "date": "Date"},
)
st.plotly_chart(risk_time_fig, use_container_width=True)



st.subheader("Jour le plus risqué par ville")
idx = filtered_df.groupby("city")["risk_score"].idxmax()
max_risk_per_city = (
    filtered_df.loc[idx, ["city", "date", "risk_score", "niveau"]]
    .sort_values("risk_score", ascending=False)
)
st.dataframe(max_risk_per_city, use_container_width=True, hide_index=True)



st.subheader("Évolution du risque dans le temps")
if len(selected_villes) <= 8:
    villes_a_afficher = selected_villes
else:
    villes_a_afficher = avg_risk_all.head(5)["city"].tolist()
    st.caption(f"Affichage limité aux 5 villes les plus à risque : {', '.join(villes_a_afficher)}")

evolution_df = filtered_df[filtered_df["city"].isin(villes_a_afficher)].sort_values("date")
evolution_fig = px.line(
    evolution_df, x="date", y="risk_score", color="city", markers=True,
    labels={"risk_score": "Score de risque", "date": "Date"},
)
st.plotly_chart(evolution_fig, use_container_width=True)


st.subheader("Répartition des niveaux de risque")
niveau_counts = filtered_df["niveau"].value_counts().reset_index()
niveau_counts.columns = ["niveau", "count"]
niveau_fig = px.pie(
    niveau_counts, names="niveau", values="count", color="niveau",
    color_discrete_map={"Faible": "green", "Modérée": "orange", "Élevé": "red"},
)
st.plotly_chart(niveau_fig, use_container_width=True)


st.divider()
st.subheader("Données détaillées")
st.dataframe(
    filtered_df.sort_values(["city", "date"]),
    use_container_width=True,
    hide_index=True,
)