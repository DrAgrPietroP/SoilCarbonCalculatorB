import streamlit as st
import json
import os

# ============================================================
# COSTANTI
# ============================================================
DATA_FILE = "terreni_dati.json"


# ============================================================
# INIZIALIZZA SESSION STATE
# ============================================================
def inizializza():
    if "terreni" not in st.session_state:
        st.session_state["terreni"] = {}


# ============================================================
# CARICA I DATI DAL FILE LOCALE (persistenza)
# ============================================================
def carica_dati():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state["terreni"] = json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Errore nel caricamento dei dati: {e}")
    else:
        st.session_state["terreni"] = {}


# ============================================================
# SALVA I DATI SU FILE LOCALE
# ============================================================
def salva_dati():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state["terreni"], f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"❌ Errore nel salvataggio dei dati: {e}")
