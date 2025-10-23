import streamlit as st
import pandas as pd
from modules import data, ui, calc

# ============================================================
# CONFIGURAZIONE INIZIALE APP
# ============================================================

st.set_page_config(
    page_title="Soil Carbon Calculator B",
    page_icon="🌱",
    layout="wide"
)

# Inizializza la sessione se non esiste
if "terreni" not in st.session_state:
    st.session_state["terreni"] = {}

# ============================================================
# HEADER E TITOLO
# ============================================================

st.title("🌱 Soil Carbon Calculator B")
st.caption("Calcola l’accumulo di carbonio nei suoli agricoli in base alle colture e alle rese.")


# ============================================================
# SELEZIONE ANNO
# ============================================================

st.subheader("📅 Selezione anno")
anni_possibili = list(range(1950, 2026))
anno = st.selectbox("Anno di riferimento", anni_possibili, index=len(anni_possibili)-1)


# ============================================================
# GESTIONE TERRENI
# ============================================================

st.subheader("🌾 Gestione terreni")

terreno_selezionato = ui.seleziona_o_aggiungi_terreno()

if terreno_selezionato:
    terreno_dati = st.session_state["terreni"][terreno_selezionato]

    st.markdown(f"**Superficie:** {terreno_dati['superficie']} ha")

    # Sezione per le due colture annuali
    st.divider()
    st.subheader(f"🧮 Dati colturali per {terreno_selezionato} - Anno {anno}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Coltura 1**")
        ui.form_coltura(1, terreno_dati, anno)
    with col2:
        st.markdown("**Coltura 2**")
        ui.form_coltura(2, terreno_dati, anno)

    st.divider()


    # ============================================================
    # CALCOLO DELLO STOCCAGGIO
    # ============================================================

    if st.button("🔍 Calcola stoccaggio di CO₂"):
        totale_CO2 = calc.calcola_stoccaggio_terreno(terreno_dati, anno)

        st.success(f"✅ Calcolo completato con successo! CO₂ stoccata: **{totale_CO2:.2f} tonnellate**")

        progress_text = "Elaborazione completata..."
        st.progress(100, text=progress_text)

        # Tabella riepilogativa per tutti i terreni
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
            st.dataframe(df, use_container_width=True)

            totale_generale = df["CO₂ stoccata (t)"].sum()
            st.markdown(f"**Totale complessivo:** 🌍 {totale_generale:.2f} tonnellate di CO₂")
        else:
            st.info("Nessun dato disponibile per il riepilogo.")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption("🧠 Progetto di agronomia digitale - MVP SoilCarbonCalculatorB © 2025")

