def get_harvest_index(coltura):
    hi = {
        "Grano tenero": 0.45,
        "Grano duro": 0.45,
        "Mais da granella": 0.50,
        "Mais trinciato": 0.35,
        "Sorgo da granella": 0.48,
        "Sorgo trinciato": 0.35,
        "Orzo": 0.45,
        "Avena": 0.40,
        "Erba medica": 0.30,
        "Loietto": 0.30,
        "Fieno misto": 0.30,
        "Nessuna": 0
    }
    return hi.get(coltura, 0.4)

def calcola_stoccaggio_terreno(terreno, anno):
    superficie = terreno["superficie"]
    annata = terreno["annate"].get(str(anno), {})
    totale_c = 0

    for i in [1, 2]:
        coltura = annata.get(f"coltura_{i}", "Nessuna")
        resa = annata.get(f"resa_{i}", 0)
        if coltura != "Nessuna" and resa > 0:
            HI = get_harvest_index(coltura)
            residui = resa * ((1 - HI) / HI)
            c_stoccato = residui * superficie * 0.45 * 3.67
            totale_c += c_stoccato

    return totale_c
