import streamlit as st

def mostra_header():
    st.title("🌱 Soil Carbon Calculator B")
    st.caption("Calcola lo stoccaggio di carbonio nel suolo, campo per campo.")

def seleziona_o_aggiungi_terreno():
    st.subheader("🏡 Gestione terreni")

    terreni = list(st.session_state["terreni"].keys())
    terreno_selezionato = st.selectbox("Seleziona terreno", [""] + terreni)

    with st.expander("➕ Aggiungi nuovo terreno"):
        nome = st.text_input("Nome terreno")
        superficie = st.number_input("Superficie (ha)", min_value=0.1, value=1.0)
        if st.button("Salva terreno"):
            if nome:
                st.session_state["terreni"][nome] = {"superficie": superficie, "annate": {}}
                st.success(f"Terreno '{nome}' aggiunto!")
                st.experimental_rerun()

    if terreno_selezionato and st.button("🗑️ Elimina terreno"):
        del st.session_state["terreni"][terreno_selezionato]
        st.success("Terreno eliminato!")
        st.experimental_rerun()

    return terreno_selezionato

def seleziona_anno():
    import datetime
    anno_corrente = datetime.date.today().year
    anni = list(range(1950, anno_corrente + 1))
    return st.selectbox("📅 Seleziona anno", reversed(anni))

def form_coltura(numero, dati_annata):
    st.markdown(f"**Coltura {numero}**")
    colture = [
        "Nessuna", "Grano tenero", "Grano duro", "Mais da granella",
        "Mais trinciato", "Sorgo da granella", "Sorgo trinciato",
        "Orzo", "Avena", "Erba medica", "Loietto", "Fieno misto"
    ]
    nome = st.selectbox(f"Coltura {numero}", colture, key=f"coltura_{numero}")
    resa = st.number_input(f"Resa (t/ha) per coltura {numero}", min_value=0.0, key=f"resa_{numero}")
    dati_annata[f"coltura_{numero}"] = nome
    dati_annata[f"resa_{numero}"] = resa
