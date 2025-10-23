import streamlit as st

# ============================================================
# HEADER
# ============================================================
def mostra_header():
    st.title("🌱 Soil Carbon Calculator B")
    st.caption("Stima dello stoccaggio di carbonio nel suolo in base alle colture annuali")


# ============================================================
# SELEZIONE O AGGIUNTA TERRENO (senza rerun)
# ============================================================
def seleziona_o_aggiungi_terreno():
    if "terreni" not in st.session_state:
        st.session_state["terreni"] = {}

    st.markdown("## 🧭 Gestione terreni")

    # Mostra terreni già registrati
    if st.session_state["terreni"]:
        terreni = list(st.session_state["terreni"].keys())
        terreno_selezionato = st.selectbox("Seleziona un terreno", terreni)
    else:
        st.info("Nessun terreno registrato.")
        terreno_selezionato = None

    # Espandi sezione per aggiungere nuovo terreno
    with st.expander("➕ Aggiungi nuovo terreno"):
        nome = st.text_input("Nome del terreno")
        superficie = st.number_input("Superficie (ha)", min_value=0.1, step=0.1)

        if st.button("Salva terreno"):
            if not nome:
                st.error("Inserisci un nome per il terreno.")
            elif nome in st.session_state["terreni"]:
                st.warning("Questo terreno esiste già.")
            else:
                st.session_state["terreni"][nome] = {
                    "superficie": superficie,
                    "annate": {}
                }
                st.success(f"Terreno '{nome}' aggiunto correttamente ✅")

    # Elimina terreno
    if st.session_state["terreni"]:
        with st.expander("🗑️ Elimina terreno"):
            terreno_da_eliminare = st.selectbox("Seleziona il terreno da eliminare",
                                                list(st.session_state["terreni"].keys()))
            if st.button("Elimina terreno"):
                del st.session_state["terreni"][terreno_da_eliminare]
                st.warning(f"Terreno '{terreno_da_eliminare}' eliminato ❌")

    # Se non è selezionato nulla ma ci sono terreni, restituisci il primo
    if not terreno_selezionato and st.session_state["terreni"]:
        terreno_selezionato = list(st.session_state["terreni"].keys())[0]

    return terreno_selezionato


# ============================================================
# SELEZIONE ANNO
# ============================================================
def seleziona_anno():
    anni = list(range(1950, 2026))
    anni.reverse()
    anno = st.selectbox("📅 Seleziona l'anno", anni)
    return anno


# ============================================================
# FORM COLTURE
# ============================================================
def form_coltura(num, dati_annata):
    st.markdown(f"#### Coltura {num}")

    colture_disponibili = [
        "Nessuna",
        "Frumento tenero da granella",
        "Frumento trinciato",
        "Mais da granella",
        "Mais trinciato",
        "Sorgo da granella",
        "Sorgo trinciato",
        "Orzo",
        "Soia",
        "Erba medica",
        "Erbaio misto",
        "Loietto",
        "Colza",
        "Pisello proteico",
        "Girasole"
    ]

    coltura = st.selectbox(f"Coltura {num}", colture_disponibili, key=f"coltura_{num}")
    resa = st.number_input(f"Resa raccolta (t/ha) – Coltura {num}", min_value=0.0, step=0.1, key=f"resa_{num}")

    # Salva in session_state
    dati_annata[f"coltura_{num}"] = coltura
    dati_annata[f"resa_{num}"] = resa

    resa = st.number_input(f"Resa (t/ha) per coltura {numero}", min_value=0.0, key=f"resa_{numero}")
    dati_annata[f"coltura_{numero}"] = nome
    dati_annata[f"resa_{numero}"] = resa
