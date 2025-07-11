# energie_simulatie_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Energieverbruik Simulatie", layout="wide")
st.title("🏡 Simulatie energieverbruik op basis van thermostaatgedrag")

st.markdown("Pas de thermostaatinstellingen aan en zie het effect op het energieverbruik.")

# Invoer
col1, col2, col3 = st.columns(3)

with col1:
    woningtype = st.selectbox("Woningtype", ["Rijwoning", "Appartement", "Vrijstaand"])
with col2:
    isolatie = st.selectbox("Isolatieniveau", ["Slecht", "Matig", "Goed"])
with col3:
    oppervlakte = st.slider("Oppervlakte woning (m²)", 50, 300, 100)

gedrag = st.radio("Gedragstype", ["Zuinig", "Gemiddeld", "Royaal"], horizontal=True)

st.subheader("🌡️ Thermostaatinstellingen per uur")
temperaturen = []
cols = st.columns(6)
for i in range(24):
    with cols[i % 6]:
        t = st.slider(f"{i}:00", min_value=14, max_value=23, value=18)
        temperaturen.append(t)

# Simulatie starten
if st.button("🔍 Simuleer energieverbruik"):

    # Dummy buitentemperaturen voor een winterdag
    buitentemp = [3 if 8 <= h <= 20 else 0 for h in range(24)]

    # Factoren op basis van isolatie & gedrag
    isolatiefactor = {"Slecht": 1.5, "Matig": 1.0, "Goed": 0.6}[isolatie]
    gedragfactor = {"Zuinig": 0.9, "Gemiddeld": 1.0, "Royaal": 1.2}[gedrag]

    # Verbruik berekenen
    verbruik_per_uur = []
    for i in range(24):
        delta = max(0, temperaturen[i] - buitentemp[i])
        verbruik = delta * oppervlakte * 0.0005 * isolatiefactor * gedragfactor
        verbruik_per_uur.append(verbruik)

    totaal_kwh = sum(verbruik_per_uur)
    st.success(f"💡 Geschat dagelijks verbruik: **{totaal_kwh:.2f} kWh**")

    # Grafiek
    df = pd.DataFrame({
        "Uur": list(range(24)),
        "BinnenT (°C)": temperaturen,
        "BuitenT (°C)": buitentemp,
        "Verbruik (kWh)": verbruik_per_uur
    })

    st.line_chart(df.set_index("Uur")[["BinnenT (°C)", "BuitenT (°C)"]])
    st.bar_chart(df.set_index("Uur")[["Verbruik (kWh)"]])
