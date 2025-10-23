import streamlit as st
import pandas as pd
import json
import os

# ============================================================
# CONFIGURAZIONE APP
# ============================================================
st.set_page_config(page_title="Soil Carbon Calculator B", layout="wide")
DATA_FILE = "dati_utenti.json"

# ============================================================
# FUNZIONI DI GESTIONE DATI
# ============================================================
def carica_dati():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salva_dati(dati):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=2)

# ============================================================
# SEZIONE 1: LOGIN / REGISTRAZIONE
# ============================================================
st.sidebar.header("🔒 Accesso utente")
dati_utenti = carica_dati()

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")
azione = st.sidebar.radio("Azione", ["Login", "Registrati"])
pulsante = st.sidebar.button("Conferma")

if "utente_corrente" not in st.session_state:
    st.session_state["utente_corrente"] = None

if pulsante:
    if azione == "Registrati":
        if email in dati_utenti:
            st.sidebar.error("❌ Email già registrata")
        elif email.strip() == "" or password.strip() == "":
            st.sidebar.warning("⚠️ Inserisci email e password valide")
        else:
            dati_utenti[email] = {"password": password, "terreni": {}}
            salva_dati(dati_utenti)
            st.sidebar.success("✅ Registrazione completata. Ora fai login.")
    else:  # Login
        if email in dati_utenti and dati_utenti[email]["password"] == password:
            st.session_state["utente_corrente"] = email
            st.sidebar.success(f"✅ Login effettuato: {email}")
        else:
            st.sidebar.error("❌ Email o password errati")

if st.session_state["utente_corrente"] is None:
    st.stop()

utente = st.session_state["utente_corrente"]

# ============================================================
# SEZIONE 2: CARICAMENTO DATI UTENTE
# ============================================================
if utente not in dati_utenti:
    dati_utenti[utente] = {"password": password, "terreni": {}}

if "terreni" not in st.session_state:
    st.session_state["terreni"] = dati_utenti[utente]["terreni"]

# ============================================================
# SEZIONE 3: HEADER
# ============================================================
st.title("🌱 Soil Carbon Calculator B")
st.caption(f"Utente: {utente} – Stima dello stoccaggio annuo di carbonio nel suolo")

# ============================================================
# SEZIONE 4: SCELTA ANNO
# ============================================================
st.subheader("📅 Seleziona l'anno")
anni = list(range(1950, 2026))
anno = st.selectbox("Anno", anni, index=len(anni)-1)

# ============================================================
# SEZIONE 5: GESTIONE TERRENI
# ============================================================
st.subheader("🌍 Gestione dei terreni")
col1, col2 = st.columns([3,1])

with col1:
    if st.session_state["terreni"]:
        terreno_selezionato = st.selectbox(
            "Seleziona un terreno",
            list(st.session_state["terreni"].keys())
        )
    else:
        terreno_selezionato = None

with col2:
    nuovo_nome = st.text_input("Nome nuovo terreno")
    nuova_sup = st.number_input("Superficie (ha)", min_value=0.1, step=0.1, key="sup_new")
    if st.button("➕ Aggiungi terreno"):
        if nuovo_nome.strip() == "":
            st.warning("⚠️ Inserisci un nome valido")
        elif nuovo_nome in st.session_state["terreni"]:
            st.warning("⚠️ Terreno già esistente")
        else:
            st.session_state["terreni"][nuovo_nome] = {"superficie": nuova_sup, "annate": {}}
            st.success(f"✅ Terreno '{nuovo_nome}' aggiunto")
            salva_dati({**dati_utenti, utente: {"password": dati_utenti[utente]["password"], "terreni": st.session_state["terreni"]}})
            st.rerun()

if terreno_selezionato:
    terreno_dati = st.session_state["terreni"][terreno_selezionato]

    if st.button("🗑️ Rimuovi terreno"):
        del st.session_state["terreni"][terreno_selezionato]
        st.success(f"Terreno '{terreno_selezionato}' rimosso")
        salva_dati({**dati_utenti, utente: {"password": dati_utenti[utente]["password"], "terreni": st.session_state["terreni"]}})
        st.rerun()

    # ============================================================
    # SEZIONE 6: DATI COLTURALI
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

    for i in [1,2]:
        st.markdown(f"**Coltura {i}**")
        coltura = st.selectbox(f"Coltura {i}", colture_possibili, key=f"coltura_{i}_{terreno_selezionato}_{anno}")
        resa = st.number_input(f"Resa (t/ha) coltura {i}", min_value=0.0, step=0.1, key=f"resa_{i}_{terreno_selezionato}_{anno}")
        terreno_dati["annate"][anno][f"coltura_{i}"] = coltura
        terreno_dati["annate"][anno][f"resa_{i}"] = resa

    # ============================================================
    # SEZIONE 7: CALCOLO CO2
    # ============================================================
    st.markdown("---")
    if st.button("🔍 Calcola stoccaggio di CO₂"):
        superficie = terreno_dati["superficie"]
        dati_annata = terreno_dati["annate"][anno]

        totale_co2 = 0
        for i in [1,2]:
            resa = dati_annata.get(f"resa_{i}",0)
            if resa>0:
                totale_co2 += resa*superficie*0.45*3.67

        st.success(f"✅ Calcolo completato! CO₂ stimata: **{totale_co2:.2f} t**")

        # ============================================================
        # RIEPILOGO GENERALE
        # ============================================================
        righe=[]
        for nome, dati in st.session_state["terreni"].items():
            for a, annata in dati["annate"].items():
                co2 = 0
                for i in [1,2]:
                    resa = annata.get(f"resa_{i}",0)
                    co2 += resa*dati["superficie"]*0.45*3.67
                righe.append({"Terreno":nome, "Anno":a,"Superficie(ha)":dati["superficie"],"CO₂ stimata(t)":co2})

        if righe:
            df=pd.DataFrame(righe)
            st.dataframe(df,use_container_width=True)
            totale=df["CO₂ stimata(t)"].sum()
            st.markdown(f"**Totale complessivo:** 🌍 {totale:.2f} t CO₂")

        # Salva dati persistenti
        salva_dati({**dati_utenti, utente: {"password": dati_utenti[utente]["password"], "terreni": st.session_state["terreni"]}})

    # ============================================================
    # SEZIONE 8: ESPORTAZIONE CSV
    # ============================================================
    if st.session_state["terreni"]:
        export_rows = []
        for nome, dati in st.session_state["terreni"].items():
            for a, annata in dati["annate"].items():
                row = {
                    "Terreno": nome,
                    "Anno": a,
                    "Superficie (ha)": dati["superficie"]
                }
                for i in [1,2]:
                    row[f"Coltura {i}"] = annata.get(f"coltura_{i}", "")
                    row[f"Resa {i} (t/ha)"] = annata.get(f"resa_{i}", 0)
                    if annata.get(f"resa_{i}",0) > 0:
                        row[f"CO₂ {i} (t)"] = annata.get(f"resa_{i}",0)*dati["superficie"]*0.45*3.67
                    else:
                        row[f"CO₂ {i} (t)"] = 0
                row["CO₂ totale (t)"] = row["CO₂ 1 (t)"] + row["CO₂ 2 (t)"]
                export_rows.append(row)

        if export_rows:
            df_export = pd.DataFrame(export_rows)
            csv = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Esporta dati terreni in CSV",
                data=csv,
                file_name=f"{utente}_terreni.csv",
                mime="text/csv"
            )

