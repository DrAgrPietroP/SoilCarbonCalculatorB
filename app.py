import streamlit as st
from modules import data, ui, calc
import pandas as pd

# ============================================================
# CONFIGURAZIONE BASE
# ============================================================
st.set_page_config(
    page_title="Soil Carbon Calculator",
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
st.subheader(f"🌾 Dati colturali per
