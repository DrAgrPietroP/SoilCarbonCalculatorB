# modules/ui.py
import streamlit as st
from modules.data import aggiungi_terreno, rimuovi_terreno

def mostra_header():
    """
    Mostra il titolo e l'intestazione principale dell'app
    """
    st.title("🌱 Soil Carbon Calculator")
    st.markdown(
        """
        ### Calcolo dello stoccaggio annuale di CO₂ nel suolo agricolo  
        Inserisci i dati delle tue colture e scopri quanto carbonio stai immagazzinando.
        """
    )
    st.markdown("---")


def seleziona_o_aggiungi_terreno():
    """
    Interfaccia per scegliere o aggiungere un nuovo terreno
    """
    st.subheader("🗺️ Gestione terreni")

    # Mostra elenco terreni esistenti
    terreni = st.session_state.get("terreni", {})
    lista_terreni = list(terreni.keys())

    terreno_selezionato = None
    if lista_terreni:
        terreno_selezionato = st.selectbox("Seleziona un terreno esistente:", lista_terreni)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Rimuovi terreno selezionato"):
                rimuovi_terreno(terreno_selezionato)
                st.rerun()

    else:
        st.info("Nessun terreno presente. Aggiungine uno nuovo 👇")

    st.markdown("---")
    st.subheader("➕ Aggiungi nuovo terreno")

    with st.form("aggiungi_terreno_form", clear_on_submit=True):
        nuovo_nome = st.text_input("Nome del nuovo terreno")
        superficie = st.number_input("Superficie (ha)", min_value=0.1, step=0.1)
        aggiungi = st.form_submit_button("Aggiungi terreno")

        if aggiungi:
            aggiungi_terreno(nuovo_nome, superficie)
            st.rerun()

    st.markdown("---")
    return terreno_selezionato


def s
