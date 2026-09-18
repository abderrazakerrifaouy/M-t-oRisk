import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from src.loading.database import SessionLocal
from src.loading.city import City
from src.loading.meteo import Meteo
from src.loading.risk import Risk


st.set_page_config(page_title="Dashboard Météo & Risques - Maroc", layout="wide")


# ---------------------------------------------------------
# Connexion & chargement des données
# ---------------------------------------------------------
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
        df = pd.DataFrame(query.all(), columns=[
            "city", "country", "date", "temperature_max", "temperature_min",
            "precipitation", "precipitation_probability", "wind_speed_max",
            "wind_gusts_max", "categorie_temperature", "categorie_precipitation",
            "categorie_wind", "risk_score", "niveau"
        ])
        df["date"] = pd.to_datetime(df["date"])
        return df
    finally:
        session.close()


df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible dans la base. Lancez d'abord le pipeline ETL.")
    st.stop()


# ---------------------------------------------------------
# Sidebar - Filtres
# ---------------------------------------------------------
st.sidebar.header("🔎 Filtres")

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

# Application des filtres
if isinstance(selected_range, tuple) and len(selected_range) == 2:
    start_date, end_date = selected_range
else:
    start_date, end_date = min_date, max_date

filtered_df = df[
    (df["city"].isin(selected_villes)) &
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date) &
    (df["niveau"].isin(selected_niveaux))
]

st.sidebar.markdown(f"**{len(filtered_df)}** lignes après filtrage")


# ---------------------------------------------------------
# Titre + KPIs globaux
# ---------------------------------------------------------
st.title("🌦️ Dashboard Météo & Risques — Maroc")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de villes", filtered_df["city"].nunique())
col2.metric("Température max", f"{filtered_df['temperature_max'].max():.1f} °C" if not filtered_df.empty else "N/A")
col3.metric("Précipitation max", f"{filtered_df['precipitation'].max():.1f} mm" if not filtered_df.empty else "N/A")
col4.metric("Risque moyen", f"{filtered_df['risk_score'].mean():.1f}" if not filtered_df.empty else "N/A")

st.divider()


# ---------------------------------------------------------
# 1) Températures les plus élevées par ville
# ---------------------------------------------------------
st.subheader("🌡️ Températures maximales par ville")
temp_fig = px.bar(
    filtered_df.sort_values("temperature_max", ascending=False),
    x="city", y="temperature_max", color="city",
    hover_data=["date"],
    labels={"temperature_max": "Température max (°C)", "city": "Ville"},
)
st.plotly_chart(temp_fig, use_container_width=True)


# ---------------------------------------------------------
# 2) Précipitations les plus fortes par ville
# ---------------------------------------------------------
st.subheader("🌧️ Précipitations par ville")
precip_fig = px.bar(
    filtered_df.sort_values("precipitation", ascending=False),
    x="city", y="precipitation", color="city",
    hover_data=["date", "precipitation_probability"],
    labels={"precipitation": "Précipitation (mm)", "city": "Ville"},
)
st.plotly_chart(precip_fig, use_container_width=True)


# ---------------------------------------------------------
# 3) Risque moyen par ville
# ---------------------------------------------------------
st.subheader("⚠️ Risque moyen par ville")
avg_risk = (
    filtered_df.groupby("city", as_index=False)["risk_score"]
    .mean()
    .sort_values("risk_score", ascending=False)
)
avg_risk_fig = px.bar(
    avg_risk, x="city", y="risk_score", color="risk_score",
    color_continuous_scale="Reds",
    labels={"risk_score": "Risque moyen", "city": "Ville"},
)
st.plotly_chart(avg_risk_fig, use_container_width=True)


# ---------------------------------------------------------
# 4) Évolution du risque dans le temps (par période)
# ---------------------------------------------------------
st.subheader("📅 Évolution du risque par période")
risk_time_fig = px.line(
    filtered_df.sort_values("date"),
    x="date", y="risk_score", color="city",
    markers=True,
    labels={"risk_score": "Score de risque", "date": "Date"},
)
st.plotly_chart(risk_time_fig, use_container_width=True)


# ---------------------------------------------------------
# 5) Répartition des niveaux de risque
# ---------------------------------------------------------
st.subheader("📊 Répartition des niveaux de risque")
niveau_counts = filtered_df["niveau"].value_counts().reset_index()
niveau_counts.columns = ["niveau", "count"]
niveau_fig = px.pie(
    niveau_counts, names="niveau", values="count",
    color="niveau",
    color_discrete_map={"Faible": "green", "Modérée": "orange", "Élevé": "red"},
)
st.plotly_chart(niveau_fig, use_container_width=True)


# ---------------------------------------------------------
# 6) Pour chaque ville, jour le plus à risque
# ---------------------------------------------------------
st.subheader("🏙️ Jour le plus risqué par ville")
idx = filtered_df.groupby("city")["risk_score"].idxmax()
max_risk_per_city = filtered_df.loc[idx, ["city", "date", "risk_score", "niveau"]].sort_values(
    "risk_score", ascending=False
)
st.dataframe(max_risk_per_city, use_container_width=True, hide_index=True)


# ---------------------------------------------------------
# Table détaillée (données filtrées)
# ---------------------------------------------------------
st.divider()
st.subheader("📋 Données détaillées")
st.dataframe(filtered_df.sort_values(["city", "date"]), use_container_width=True, hide_index=True)