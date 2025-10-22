# modules/calc.py
def stima_residui(coltura, resa_t_ha):
    """
    Calcola i residui lasciati in campo basandosi sull'harvest index
    (percentuale raccolta / totale biomassa).
    Ritorna residui t/ha.
    """
    # harvest index medi per coltura
    hi = {
        "Mais da granella": 0.55,
        "Mais trinciato": 0.50,
        "Frumento": 0.60,
        "Sorgo da granella": 0.55,
        "Sorgo trinciato": 0.50,
        "Erba medica": 0.40,
        "Loietto": 0.45,
        "Soia": 0.55,
        "Nessuna": 1.0
    }
    indice = hi.get(coltura, 0.55)
    residui = resa_t_ha * (1 - indice) / indice if indice != 0 else 0
    return residui


def stima_carbonio(residui_t_ha):
    """
    Converte i residui in carbonio stoccato (t C/ha) e poi in CO2 equivalente.
    Frazione di carbonio stimata = 0.45, moltiplicatore CO2/C = 3.67
    """
    C = residui_t_ha * 0.45
    CO2eq = C * 3.67
    return CO2eq


def calcola_stoccaggio_terreno(dati_terreno, anno):
    """
    Calcola lo stoccaggio totale di CO2 per un terreno in un anno.
    Somma le due colture se presenti.
    """
    annate = dati_terreno.get("annate", {})
    annata = annate.get(str(anno), {})
    superficie = dati_terreno.get("superficie", 0)
    totale_CO2 = 0.0

    for coltura in ["coltura1", "coltura2"]:
        dati_coltura = annata.get(coltura, {})
        nome = dati_coltura.get("nome", "Nessuna")
        resa = dati_coltura.get("resa", 0)
        residui = stima_residui(nome, resa)
        co2 = stima_carbonio(residui) * superficie
        totale_CO2 += co2

    return totale_CO2
