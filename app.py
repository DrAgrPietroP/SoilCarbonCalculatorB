import streamlit as st
import json
import os

# === CONFIGURAZIONE INIZIALE ===
st.set_page_config(page_title="Soil Carbon Calculator", layout="wide")

# === INIZIALIZZAZIONE SESSION STATE ===
if "terreni" not in st.session_state:
    st.session_state["terreni"] = {}

# === FUNZIONI DI SUPPORTO ===
def salva_dati():
    with open("data/fields.json", "w") as f:
        json.dump(st.session_state["terreni"], f, indent=4)

def carica_dati():
    if os.path.exists("data/fields.json"):
        with open("data/fields.json", "r") as f:
            st.session_state["terreni"] = json.load(f)
    else:
        st.session_state["terreni"] = {}

# === CARICA DATI SALVATI ===
carica_dati()

# === INTERFACCIA ===
st.title("🌱 Soil Carbon Calculator B")
st.write("Calcolatore semplificato di stoccaggio annuale di carbonio nel suolo")

# Scelta dell'anno
import datetime
anno_corrente = datetime.date.today().year
anni = list(range(1950, anno_corrente + 1))
anno_selezionato = st.selectbox("Anno di riferimento", anni, index=len(anni)-1)

# Scelta o creazione del terreno
st.subheader("Gestione Terreni")
terreni = list(st.session_state["terreni"].keys())
col1, col2 = st.columns([3, 1])

with col1:
    terreno_selezionato = st.selectbox("Seleziona un terreno", [""] + terreni)

with col2:
    if st.button("+ Aggiungi nuovo terreno"):
        nuovo = st.text_input("Nome nuovo terreno:", key="nuovo_terreno_nome")
        if nuovo:
            st.session_state["terreni"][nuovo] = {"superficie": 0, "annate": {}}
            salva_dati()
            st.success(f"Terreno '{nuovo}' aggiunto!")

if terreno_selezionato:
    superficie = st.number_input(
        "Superficie (ha)",
        min_value=0.0, step=0.1,
        value=st.session_state["terreni"][terreno_selezionato].get("superficie", 0.0)
    )
    st.session_state["terreni"][terreno_selezionato]["superficie"] = superficie

    st.subheader("Colture dell'anno")
    colture = ["Nessuna", "Mais da granella", "Mais trinciato", "Frumento", "Sorgo da granella", "Sorgo trinciato", "Erba medica", "Loietto", "Soia"]
    col1, col2 = st.columns(2)
    coltura1 = col1.selectbox("Coltura 1", colture)
    resa1 = col1.number_input("Resa Coltura 1 (t/ha)", min_value=0.0, step=0.1)

    coltura2 = col2.selectbox("Coltura 2", coltures)
    resa2 = col2.number_input("Resa Coltura 2 (t/ha)", min_value=0.0, step=0.1)

    if st.button("💾 Salva anno"):
        st.session_state["terreni"][terreno_selezionato]["annate"][str(anno_selezionato)] = {
            "coltura1": {"nome": coltura1, "resa": resa1},
            "coltura2": {"nome": coltura2, "resa": resa2}
        }
        salva_dati()
        st.success("Dati salvati correttamente!")

    # Visualizza tabella di riepilogo
    st.subheader("📊 Riepilogo terreni")
    totale_asporti = 0
    for nome, dati in st.session_state["t]()_
