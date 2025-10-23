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
