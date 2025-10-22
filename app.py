# app.py
import streamlit as st
import json
import os
import datetime

# Importa moduli (assicurati che modules/calc.py e modules/report.py esistano)
try:
    from modules.calc import calcola_totale_stoccaggio
    from modules.report import genera_csv, genera_pdf
except Exception:
    # Fallback se i moduli non sono presenti: definizioni semplici per evitare crash
    def calcola_totale_stoccaggio(dati_terreno, anno):
        # somma grezza: per ogni coltura resa * coeff * superficie
        coeff = {
            "Mais da granella": 0.35,
            "Mais trinciato": 0.25,
            "Frumento": 0.30,
            "Sorgo da granella": 0.32,
            "Sorgo trinciato": 0.28,
            "Erba medica": 0.40,
            "Loietto": 0.25,
            "Soia": 0.20,
            "Nessuna": 0.00
        }
        superficie = dati_terreno.get("superficie", 0)
        totale = 0.0
        annata = dati_terreno.get("annate", {}).get(str(anno), {})
        for entry in annata.values():
            nome = entry.get("nome", "Nessuna")
            resa = entry.get("resa", 0)
            fatt = coeff.get(nome, 0.25)
            totale += resa * fatt * superficie
        return totale

    def genera_csv(terreni, anno):
        import csv
        from io import StringIO
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Terreno", "Superficie (ha)", "CO2 stoccata (t)"])
        for nome, dati in terreni.items():
            stocc = calcola_totale_stoccaggio(dati, anno)
            writer.writerow([nome, dati.get("superficie", 0), round(stocc, 3)])
        return output.getvalue()

    def genera_pdf(terreni, anno, totale):
        # semplice fallback: crea un file txt rinominato .pdf (compatibilità minima)
        fname = f"report_CO2_{anno}.pdf"
        with open(fname, "w") as f:
            f.write(f"Report CO2 anno {anno}\n\n")
            for nome, dati in terreni.items():
                stocc = calcola_totale_stoccaggio(dati, anno)
                f.write(f"{nome}: {stocc:.3f} t\n")
            f.write(f"\nTotale: {totale:.3f} t\n")
        return fname

# Configurazione pagina
st.set_page_config(page_title="Soil Carbon Calculator B", layout="wide")

# Inizializzazione stato
if "terreni" not in st.session_state:
    st.session_state["terreni"] = {}

# Funzioni: salva e carica
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fields.json")

def salva_dati():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["terreni"], f, indent=4, ensure_ascii=False)

def carica_dati():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                st.session_state["terreni"] = json.load(f)
            except Exception:
                st.session_state["terreni"] = {}
    else:
        st.session_state["terreni"] = {}

carica_dati()

# Titolo
st.title("🌱 Soil Carbon Calculator B")
st.caption("Calcolo semplificato di stoccaggio annuale di carbonio nel suolo")

# Selezione anno
anno_corrente = datetime.date.today().year
anni = list(range(1950, anno_corrente + 1))
anno_selezionato = st.selectbox("Anno di riferimento", anni, index=len(anni)-1)

# Gestione terreni
st.subheader("Gestione Terreni")
terreni = list(st.session_state["terreni"].keys())

col1, col2 = st.columns([3, 1])
with col1:
    terreno_sel = st.selectbox("Seleziona un terreno", [""] + terreni)
with col2:
    if st.button("+ Aggiungi nuovo terreno"):
        # popup per nome nuovo terreno
        nuovo = st.text_input("Nome nuovo terreno:", key="nuovo_terreno_nome")
        superficie_tmp = st.number_input("Superficie (ha)", min_value=0.1, step=0.1, key="nuovo_terreno_sup")
        if nuovo:
            st.session_state["terreni"][nuovo] = {"superficie": superficie_tmp, "annate": {}}
            salva_dati()
            st.success(f"Terreno '{nuovo}' aggiunto!")
            st.experimental_rerun()

# Se è selezionato un terreno
if terreno_sel:
    # assicurati che il terreno esista nella struttura
    if terreno_sel not in st.session_state["terreni"]:
        st.session_state["terreni"][terreno_sel] = {"superficie": 0, "annate": {}}

    dati_terreno = st.session_state["terreni"][terreno_sel]

    superficie = st.number_input(
        "Superficie (ha)",
        min_value=0.0,
        step=0.1,
        value=dati_terreno.get("superficie", 0.0),
        key=f"sup_{terreno_sel}"
    )
    st.session_state["terreni"][terreno_sel]["superficie"] = superficie

    st.subheader("Colture dell'anno")
    colture = [
        "Nessuna", "Mais da granella", "Mais trinciato", "Frumento",
        "Sorgo da granella", "Sorgo trinciato", "Erba medica",
        "Loietto", "Soia"
    ]

    colA, colB = st.columns(2)
    with colA:
        coltura1 = st.selectbox("Coltura 1", colture, key=f"col1_{terreno_sel}")
        resa1 = st.number_input("Resa Coltura 1 (t/ha)", min_value=0.0, step=0.1, key=f"resa1_{terreno_sel}")
    with colB:
        coltura2 = st.selectbox("Coltura 2", colture, key=f"col2_{terreno_sel}")
        resa2 = st.number_input("Resa Coltura 2 (t/ha)", min_value=0.0, step=0.1, key=f"resa2_{terreno_sel}")

    if st.button("💾 Salva anno", key=f"save_{terreno_sel}"):
        annate = st.session_state["terreni"][terreno_sel].setdefault("annate", {})
        annate[str(anno_selezionato)] = {
            "coltura1": {"nome": coltura1, "resa": resa1},
            "coltura2": {"nome": coltura2, "resa": resa2}
        }
        salva_dati()
        st.success("Dati salvati correttamente!")

# Riepilogo e calcoli
st.subheader("📊 Riepilogo terreni")
totale = 0.0
tabella = []

for nome, dati in st.session_state["terreni"].items():
    stoccaggio = calcola_totale_stoccaggio(dati, anno_selezionato)
    superficie = dati.get("superficie", 0)
    tabella.append({
        "Terreno": nome,
        "Superficie (ha)": superficie,
        "CO₂ stimata (t)": round(stoccaggio, 3)
    })
    st.write(f"**{nome}** — Superficie: {superficie} ha — CO₂ stimata: {stoccaggio:.3f} t")
    totale += stoccaggio

st.success(f"Totale CO₂ stoccata: **{totale:.3f} t**")

# Tabella riepilogativa (pandas)
try:
    import pandas as pd
    if tabella:
        df = pd.DataFrame(tabella)
        st.dataframe(df, use_container_width=True)
except Exception:
    pass

# Report: CSV / PDF
st.subheader("📑 Esporta report")
colx, coly = st.columns(2)
if colx.button("⬇️ Scarica CSV"):
    csv_data = genera_csv(st.session_state["terreni"], anno_selezionato)
    st.download_button(label="Scarica CSV", data=csv_data, file_name=f"report_CO2_{anno_selezionato}.csv", mime="text/csv")

if coly.button("📄 Genera PDF"):
    fname = genera_pdf(st.session_state["terreni"], anno_selezionato, totale)
    # invia il file come download se esiste
    if os.path.exists(fname):
        with open(fname, "rb") as f:
            st.download_button(label="Scarica PDF", data=f, file_name=fname, mime="application/pdf")
    else:
        st.error("Errore nella generazione del PDF.")
