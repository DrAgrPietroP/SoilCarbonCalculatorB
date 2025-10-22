# modules/data.py
import os
import json
import streamlit as st

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fields.json")

def inizializza():
    """
    Inizializza lo stato dei terreni nello session_state se non presente
    """
    if "terreni" not in st.session_state:
        st.session_state["terreni"] = {}
    if "nuovo_terreno_temp" not in st.session_state:
        st.session_state["nuovo_terreno_temp"] = {"nome": "", "superficie": 0.0}


def carica_dati():
    """
    Carica i dati persistenti dal file JSON
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                st.session_state["terreni"] = json.load(f)
            except Exception:
                st.session_state["terreni"] = {}
    else:
        st.session_state["terreni"] = {}


def salva_dati():
    """
    Salva lo stato dei terreni in JSON
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["terreni"], f, indent=4, ensure_ascii=False)


def aggiungi_terreno(nuovo_nome, superficie):
    """
    Aggiunge un nuovo terreno se il nome non esiste già
    """
    if nuovo_nome.strip() == "":
        st.warning("Inserire un nome valido per il terreno.")
        return False
    if nuovo_nome in st.session_state["terreni"]:
        st.warning("Il terreno esiste già!")
        return False
    st.session_state["terreni"][nuovo_nome] = {"superficie": superficie, "annate": {}}
    salva_dati()
    st.success(f"Terreno '{nuovo_nome}' aggiunto!")
    return True


def rimuovi_terreno(nome_terreno):
    """
    Rimuove un terreno dal session_state e dal file JSON
    """
    if nome_terreno in st.session_state["terreni"]:
        del st.session_state["terreni"][nome_terreno]
        salva_dati()
        st.success(f"Terreno '{nome_terreno}' rimosso!")
        return True
    else:
        st.warning(f"Terreno '{nome_terreno}' non trovato.")
        return False
