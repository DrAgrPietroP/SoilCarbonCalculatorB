import streamlit as st
import pandas as pd

# ============================================================
# IMPOSTAZIONI INIZIALI
# ============================================================
st.set_page_config(page_title="Soil Carbon Calculator B", layout="wide")

if "terreni" not in st.session_state:
    st.session_state["terreni"] = {}

st.title("🌱 Soil Carbon Calculator B")
st.caption("Stima dello stoccaggio annuo di carbonio nel suolo agricolo.")


# ============================================================
# SEZIONE: SCELTA DELL’ANNO
# ============================================================
st.subheader("📅 Seleziona l'anno di riferimento")
anni = list(range(1950, 2026))
anno = st.selectbox("Anno", anni, index=len(anni)-1)


# ============================================================
# SEZIONE: GESTIONE TERRENI
# ============================================================
st.subheader("🌍 Gestione dei terreni")

col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state["terreni"]:
        terreno_selezionato = st.selectbox(
            "Seleziona un terreno esistente",
            list(st.session_state["terreni"].keys())
        )
    else:
        terreno_selezionato = None

with col2:
    nuovo_nome = st.text_input("Nome nuovo terreno")
    nuova_superficie = st.number_input("Superficie (ha)", min_value=0.1, step=0.1, key="sup_new")
    if st.button("➕ Aggiungi terreno"):
        if nuovo_nome.strip() == "":
            st.warning("⚠️ Inserisci un nome valido per il terreno.")
        elif nuovo_nome in st.session_state["terreni"]:
            st.warning("⚠️ Esiste già un terreno con questo nome.")
        else:
            st.session_state["terreni"][nuovo_nome] = {"superficie": nuova_superficie, "annate": {}}
            st.success(f"✅ Terreno '{nuovo_nome}' aggiunto con successo!")
            st.rerun()

if terreno_selezionato:
    terreno_dati = st.session_state["terreni"][terreno_selezionato]

    if st.button("🗑️ Rimuovi terreno selezionato"):
        del st.session_state["terreni"][terreno_selezionato]
        st.success(f"Terreno '{terreno_selezionato}' rimosso.")
        st.rerun()

    # ============================================================
    # SEZIONE DATI COLTURALI
    # ============================================================
    st.subheader(f"🌾 Dati colturali per {terreno_selezionato} ({anno})")

    if "annate" not in terreno_dati:
        terreno_dati["annate"] = {}

    if anno not in terreno_dati["annate"]:
        terreno_dati["annate"][anno] = {}

    colture_possibili = [
        "Nessuna",
        "Mais da granella", "Mais trinciato",
        "Frumento tenero", "Frumento duro", "Frumento trinciato",
        "Sorgo da granella", "Sorgo trinciato",
        "Orzo", "Avena", "Triticale", "Segale",
        "Soia", "Erba medica", "Loietto", "Erbaio misto"
    ]

    for i in [1, 2]:
        st.markdown(f"**Coltura {i}**")
        coltura = st.selectbox(
            f"Coltura {i}",
            colture_possibili,
            key=f"coltura_{i}_{terreno_selezionato}_{anno}"
        )
        resa = st.number_input(
            f"Resa (t/ha) per coltura {i}",
            min_value=0.0,
            step=0.1,
            key=f"resa_{i}_{terreno_selezionato}_{anno}"
        )

        terreno_dati["annate"][anno][f"coltura_{i}"] = coltura
        terreno_dati["annate"][anno][f"resa_{i}"] = resa


    # ============================================================
    # CALCOLO STIMATO DELLA CO2
    # ============================================================
    st.markdown("---")

    if st.button("🔍 Calcola stoccaggio di CO₂"):
        superficie = terreno_dati["superficie"]
        dati_annata = terreno_dati["annate"][anno]

        totale_carbonio = 0
        for i in [1, 2]:
            resa = dati_annata.get(f"resa_{i}", 0)
            if resa > 0:
                carbonio = resa * superficie * 0.45 * 3.67
                totale_carbonio += carbonio

        st.success(f"✅ Calcolo completato! CO₂ stimata: **{totale_carbonio:.2f} tonnellate**")

        st.markdown("### 📊 Riepilogo generale")

        righe = []
        for nome, dati in st.session_state["terreni"].items():
            for a, annata in dati["annate"].items():
                co2 = 0
                for i in [1, 2]:
                    resa = annata.get(f"resa_{i}", 0)
                    co2 += resa * dati["superficie"] * 0.45 * 3.67
                righe.append({
                    "Terreno": nome,
                    "Anno": a,
                    "Superficie (ha)": dati["superficie"],
                    "CO₂ stimata (t)": co2
                })

        if righe:
            df = pd.DataFrame(righe)
            st.dataframe(df, use_container_width=True)
            totale = df["CO₂ stimata (t)"].sum()
            st.markdown(f"**Totale complessivo:** 🌍 {totale:.2f} tonnellate di CO₂")
