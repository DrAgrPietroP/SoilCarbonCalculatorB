import streamlit as st
import json
import os

def inizializza():
    if "terreni" not in st.session_state:
        st.session_state["terreni"] = {}

def carica_dati():
    if os.path.exists("terreni.json"):
        with open("terreni.json", "r") as f:
            st.session_state["terreni"] = json.load(f)

def salva_dati():
    with open("terreni.json", "w") as f:
        json.dump(st.session_state["terreni"], f, indent=4)

