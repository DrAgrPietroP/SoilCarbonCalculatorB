import streamlit as st
from modules import data

# ============================================================
# HEADER
# ============================================================

def mostra_header():
    st.title("🌱 Soil Carbon Calculator B")
    st.caption("Strumento per stimare lo stoccaggio annuo di carbonio nel suolo.")


# ============================================================
# SELEZIONE O AGGIUNTA TERRENO
# ============================================================

def seleziona_o_aggiungi_terreno():
    terreni = st.session_state["terreni"]

    col1, col2 = st.columns([3, 1])

    with col1:
        if terreni:
            terreno_selezionato = st.selectbox(
                "Seleziona un terreno esistente",
                list(terreni.keys()),
                key="terreno_select"
            )
        else:
            terreno_selezionato = None

    with col2:
        if st.button("➕ Aggiungi nuovo terreno"):
            with st.form("nuovo_terreno"):
                st.subheader("🧩 Nuovo terreno")
                nome = st.text_input("Nome del terreno")
                superficie = st.number_input("Superficie (ha)", min_value=0.1, step=0.1)
                conferma = st.form_submit_button("Salva terreno")

                if conferma:
                    if nome.strip() == "":
                        st.warning("⚠️ Inserisci un nome valido per il terreno.")
                    elif nome in terreni:
                        st.warning("⚠️ Esiste già un terreno con questo nome.")
                    else:
                        st.session_state["terreni"][nome] = {"superficie": superficie, "annate": {}}
                        st.success(f"✅ Terreno '{nome}' aggiunto con successo!")
                        st.rerun()

    # possibilità di rimuovere terreno
    if terreni:
        if st.button("🗑️ Rimuovi terreno selezionato"):
            if terreno_selezionato:
                del st.session_state["terreni"][terreno_selezionato]
                st.success(f"Terreno '{terreno_selezionato}' rimosso.")
                st.rerun()

    return terreno_selezionato


# ============================================================
# FORM INSERIMENTO DATI COLTURA
# ============================================================

def form_coltura(numero, terreno_dati, anno):
    """
    Form per inserire i dati di una coltura (coltura 1 o coltura 2)
    """
    colture_possibili = [
        "Nessuna",
        "Mais da granella", "Mais trinciato",
        "Frumento tenero", "Frumento duro", "Frumento trinciato",
        "Sorgo da granella", "Sorgo trinciato",
        "Orzo", "Avena", "Triticale", "Segale",
        "Soia", "Erba medica", "Loietto", "Erbaio misto"
    ]

    terreno_nome = None
    for nome, t in st.session_state["terreni"].items():
        if t == terreno_dati:
            terreno_nome = nome
            break

    # Crea la chiave se non esiste
    if "annate" not in terreno_dati:
        terreno_dati["annate"] = {}
    if anno not in terreno_dati["annate"]:
        terreno_dati["annate"][anno] = {}

    dati_annata = terreno_dati["annate"][anno]

    with st.container():
        coltura = st.selectbox(
            f"Coltura {numero}",
            colture_possibili,
            key=f"coltura_{numero}_{terreno_nome}_{anno}"
        )

        resa = st.number_input(
            f"Resa (t/ha) coltura {numero}",
            min_value=0.0,
            step=0.1,
            key=f"resa_{numero}_{terreno_nome}_{anno}"
        )

        # Salva nel dizionario di sessione
        dati_annata[f"coltura_{numero}"] = coltura
        dati_annata[f"resa_{numero}"] = resa

