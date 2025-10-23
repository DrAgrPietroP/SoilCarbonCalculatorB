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
# CONFIGURAZIONE ADMIN
# ============================================================
ADMIN_EMAIL = "ADMIN"
ADMIN_PASSWORD = "Pi3tr0"  # Password admin

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
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Logout
if st.sidebar.button("🔓 Logout"):
    st.session_state["utente_corrente"] = None
    st.session_state["is_admin"] = False
    st.experimental_rerun()

# Login / Registrazione
if pulsante:
    if azione == "Registrati":
        if email in dati_utenti or email == ADMIN_EMAIL:
            st.sidebar.error("❌ Email già registrata")
        elif email.strip() == "" or password.strip() == "":
            st.sidebar.warning("⚠️ Inserisci email e password valide")
        else:
            dati_utenti[email] = {"password": password, "terreni": {}}
            salva_dati(dati_utenti)
            st.sidebar.success("✅ Registrazione completata. Ora fai login.")
    else:  # Login
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state["utente_corrente"] = email
            st.session_state["is_admin"] = True
            st.sidebar.success(f"✅ Login Admin effettuato")
        elif email in dati_utenti and dati_utenti[email]["password"] == password:
            st.session_state["utente_corrente"] = email
            st.session_state["is_admin"] = False
            st.sidebar.success(f"✅ Login effettuato: {email}")
        else:
            st.sidebar.error("❌ Email o password errati")

if st.session_state["utente_corrente"] is None:
    st.stop()

utente = st.session_state["utente_corrente"]
is_admin = st.session_state["is_admin"]

# ============================================================
# SEZIONE 2: CARICAMENTO DATI UTENTE
# ============================================================
if not is_admin:
    if utente not in dati_utenti:
        dati_utenti[utente] = {"password": password, "terreni": {}}
    if "terreni" not in st.session_state:
        st.session_state["terreni"] = dati_utenti[utente]["terreni"]

# ============================================================
# SEZIONE 3: HEADER
# ============================================================
st.title("🌱 Soil Carbon Calculator B")
st.caption(f"Utente: {utente}")

# ============================================================
# SEZIONE ADMIN
# ============================================================
if is_admin:
    st.subheader("🛠️ Pannello Admin")
    for email_user, info in dati_utenti.items():
        st.markdown(f"**📧 Email:** {email_user}")
        terreni = info.get("terreni", {})
        if terreni:
            for nome, dati in terreni.items():
                st.write(f"- Terreno: {nome}, Superficie: {dati['superficie']} ha")
                for anno, annata in dati.get("annate", {}).items():
                    st.write(f"  - Anno: {anno}")
                    for i in [1,2]:
                        coltura = annata.get(f"coltura_{i}", "")
                        resa = annata.get(f"resa_{i}", 0)
                        if coltura != "Nessuna" and coltura != "":
                            co2 = resa*dati["superficie"]*0.45*3.67
                            st.write(f"    - Coltura {i}: {coltura}, Resa: {resa} t/ha, CO₂ stimata: {co2:.2f} t")
        else:
            st.write("  Nessun terreno registrato")
        st.markdown("---")
    
    # Export CSV globale
    export_rows = []
    for email_user, info in dati_utenti.items():
        for nome, dati in info.get("terreni", {}).items():
            for anno, annata in dati.get("annate", {}).items():
                row = {"Email": email_user, "Terreno": nome, "Anno": anno, "Superficie (ha)": dati["superficie"]}
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
            label="📥 Esporta tutti i dati utenti in CSV",
            data=csv,
            file_name="tutti_utenti_terreni.csv",
            mime="text/csv"
        )
    st.stop()

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

# ============================================================
# SEZIONE 6: DATI COLTURALI, CALCOLO CO₂ E CSV
# ============================================================
if terreno_selezionato:
    terreno_dati = st.session_state["terreni"][terreno_selezionato]

    if st.button("🗑️ Rimuovi terreno"):
        del st.session_state["terreni"][terreno_selezionato]
        st.success(f"Terreno '{terreno_selezionato}' rimosso")
        salva_dati({**dati_utenti, utente: {"password": dati_utenti[utente]["password"], "terreni": st.session_state["terreni"]}})
        st.rerun()

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
        "Soia", "Erba medica",

