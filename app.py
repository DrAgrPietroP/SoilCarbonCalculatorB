import streamlit as st
import pandas as pd
import json
import os

# ============================================================
# SEZIONE 0: CONFIGURAZIONE APP
# ============================================================
st.set_page_config(page_title="Soil Carbon Calculator B", layout="wide")

DATA_FILE = "dati_utenti.json"

# ============================================================
# SEZIONE 1: LOGIN UTENTE
# ============================================================
st.sidebar.header("🔒 Login")

# Utenti demo per MVP
utenti_demo = {
    "pietro": "1234",
    "maria": "abcd"
}

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if "utente_corrente" not in st.session_state:
    st.session_state["utente_corrente"] = None

if login_button:
    if username in utenti_demo and utenti_demo[username] == password:
        st.session_state["utente_corrente"] = username
        st.success(f"✅ Login effettuato: {username}")
    else:
        st.error("❌ Username o password errati")

if st.session_state["utente_corrente"] is None:
    st.stop()  # blocca l'app fino al login

utente = st.session_state["utente_corrente"]

# ============================================================
# SEZIONE 2: CARICAMENTO DATI PERSISTENTI
# ============================================================
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        tutti_i_dati = json.load(f)
else:
    tutti_i_dati = {}

# Se l’utente non ha ancora dati, crea struttura vuota
if utente not in tutti_i_dati:
    tutti_i_dati[utente] = {"terreni": {}}

# Carica i terreni in session state
if "terreni" not in st.session_state:
    st.session_state["terreni"] = tutti_i_dati[utente]["terreni"]

# ============================================================
# SEZIONE 3: HEADER
# ============================================================
st.title("🌱 Soil Carbon Calculator B")
st.caption(f"Utente: {utente} – Stima dello stoccaggio annuo di carbonio nei suoli agricoli")

# ============================================================
# SEZIONE 4: SELEZIONE ANNO
# ============================================================
st.subheader("📅 Seleziona l'anno di riferimento")
anni = list(range(1950, 2026))
anno = st.selectbox("Anno", anni, index=len(anni)-1)

# ============================================================
# SEZIONE 5: GESTIONE TERRENI
# ============================================================
st.subheader("🌍 Gestione dei terreni")

col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state["terreni"]:
        terreno_selezionato = st.selectbox(
            "Seleziona un terreno esistente",
            list(st.session_state["terreni"].keys())
        )
   

