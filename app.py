import streamlit as st
from modules import data, ui, calc
import pandas as pd

# ============================================================
# CONFIGURAZIONE BASE
# ============================================================
st.set_page_config(
    page_title="Soil Carbon Calculator B",
    page_icon="🌱",
    layout="centered"
)

# ============================================================
# INIZIALIZZAZIONE DATI
# ============================================================
data.inizializza()
data.carica_dati()

ui.mostra_header()

# ============================================================
# SELEZIONE O CREAZIONE TERRENO
# ============================================================
terreno_selezionato = ui.seleziona_o_aggiungi_terreno()
if not terreno_selezionato:
    st.stop()

# ============================================================
# SELEZIONE ANNO
# ============================================================
anno = ui.seleziona_anno()

# ============================================================
# INSERIMENTO COLTURE
# ============================================================
st.subheader(f"🌾 Dati colturali per {terreno_selezionato} ({anno})")

# Crea struttura se non esiste
if "annate" not in st.session_state["terreni"][terreno_selezionato]:
    st.session_state["terreni"][terreno_selezionato]["annate"] = {}
if str(anno) not in st.session_state["terreni"][terreno_selezionato]["annate"]:
    st.session_state["terreni"][terreno_selezionato]["annate"][str(anno)] = {}

dati_annata = st.session_state["terreni"][terreno_selezionato]["annate"][str(anno)]

# Form per due colture
ui.form_coltura(1, dati_annata)
ui.form_coltura(2, dati_annata)

# Salva i dati
data.salva_dati()

# ============================================================
# CALCOLO STABILITO
# ============================================================
st.markdown("---")
if st.button("🔍 Calcola stoccaggio di CO₂"):
    totale_CO2 = calc.calcola_stoccaggio_terreno(
        st.session_state["terreni"][terreno_selezionato],
        anno
    )

    st.success(f"Totale CO₂ stoccata: **{totale_CO2:.2f} tonnellate**")
    st.balloons()

    # Mostra tabella riepilogativa per tutti i terreni
    st.markdown("### 📊 Riepilogo generale")

    righe = []
    for nome, dati in st.session_state["terreni"].items():
        for a, dati_annata in dati["annate"].items():
            co2 = calc.calcola_stoccaggio_terreno(dati, a)
            righe.append({
                "Terreno": nome,
                "Anno": a,
                "Superficie (ha)": dati["superficie"],
                "CO₂ stoccata (t)": co2
            })

    if righe:
        df = pd.DataFrame(righe)
        st.dataframe(df)

        totale_generale = df["CO₂ stoccata (t)"].sum()
        st.markdown(f"**Totale complessivo:** 🌍 {totale_generale:.2f} tonnellate di CO₂")
    else:
        st.info("Nessun dato disponibile per il riepilogo.")
