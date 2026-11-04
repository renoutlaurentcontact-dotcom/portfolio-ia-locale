#!/usr/bin/env python3
"""Recalcul arithmétique des mesures Qwen transcrites d'un rapport fourni.

Développement réalisé par un agent logiciel sous la supervision de Laurent Renout.
Bibliothèque standard uniquement. Aucun benchmark, accès réseau ou accès au P910.
Les données sont une transcription du rapport, pas les journaux originaux.

Usage : python recalculer_mesures.py [--json]
Le fichier de données est résolu relativement à ce script, quel que soit le cwd.
"""

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path
from statistics import median


DATA_PATH = Path(__file__).resolve().parent / "mesures_transcrites.json"


def charger_donnees():
    """Préserver les décimales écrites dans le JSON lors des calculs."""
    with DATA_PATH.open(encoding="utf-8") as source:
        return json.load(source, parse_float=Decimal)


def gain_pct(reference, finale):
    """Variation relative descriptive, sans attribution causale supplémentaire."""
    if reference <= 0:
        raise ValueError("La valeur de référence doit être strictement positive.")
    with localcontext() as contexte:
        contexte.prec = 40
        return (finale - reference) / reference * Decimal(100)


def recalculer(donnees):
    """Produire les médianes et gains de chaque comparaison sans les mélanger."""
    colocation = donnees["campagne_colocation"]
    generation_colocation = colocation["generation"]
    off = median(generation_colocation["off_valeurs_arrondies"])
    split22 = median(generation_colocation["split22_valeurs_arrondies"])
    off_precise = generation_colocation["mediane_off_plus_precise_rapportee"]
    split22_precise = generation_colocation["mediane_split22_plus_precise_rapportee"]
    lecture_colocation = colocation["lecture_contexte"]

    mtp = donnees["campagne_mtp_ubatch"]
    generation_mtp = mtp["generation"]
    mediane_b1 = median(generation_mtp["b1_ubatch64"])
    mediane_b2 = median(generation_mtp["b2_ubatch64"])
    moyenne_medianes = (mediane_b1 + mediane_b2) / Decimal(2)
    reference_mtp = generation_mtp["reference_ubatch32_rapportee"]

    lectures_mtp = []
    for lecture in mtp["lectures_contexte"]:
        reference = lecture["reference_ubatch32_rapportee"]
        finale = lecture["finale_ubatch64_rapportee"]
        lectures_mtp.append({
            "tokens_entree": lecture["tokens_entree"],
            "unite_debit": lecture["unite"],
            "reference_ubatch32_rapportee": reference,
            "finale_ubatch64_rapportee": finale,
            "gain_descriptif_pct": gain_pct(reference, finale),
        })

    return {
        "provenance": donnees["provenance"],
        "calcul": "Arithmétique décimale sur les valeurs transcrites uniquement.",
        "campagne_colocation": {
            "section_source": colocation["section_source"],
            "generation": {
                "unite_debit": generation_colocation["unite"],
                "mediane_off_series_arrondies": off,
                "mediane_split22_series_arrondies": split22,
                "gain_depuis_series_arrondies_pct": gain_pct(off, split22),
                "mediane_off_plus_precise_rapportee": off_precise,
                "mediane_split22_plus_precise_rapportee": split22_precise,
                "gain_depuis_medianes_plus_precises_rapportees_pct": gain_pct(
                    off_precise, split22_precise
                ),
            },
            "lecture_contexte": {
                "tokens_entree": lecture_colocation["tokens_entree"],
                "tokens_cache": lecture_colocation["tokens_cache"],
                "unite_debit": lecture_colocation["unite"],
                "mediane_off_rapportee": lecture_colocation["mediane_off_rapportee"],
                "mediane_split22_rapportee": lecture_colocation["mediane_split22_rapportee"],
                "gain_descriptif_pct": gain_pct(
                    lecture_colocation["mediane_off_rapportee"],
                    lecture_colocation["mediane_split22_rapportee"],
                ),
                "portee": lecture_colocation["portee"],
            },
        },
        "campagne_mtp_ubatch": {
            "section_source": mtp["section_source"],
            "generation": {
                "unite_debit": generation_mtp["unite"],
                "mediane_b1_ubatch64": mediane_b1,
                "mediane_b2_ubatch64": mediane_b2,
                "moyenne_des_deux_medianes": moyenne_medianes,
                "moyenne_arrondie_10_decimales": moyenne_medianes.quantize(
                    Decimal("0.0000000001"), rounding=ROUND_HALF_UP
                ),
                "agregation": generation_mtp["agregation"],
                "reference_ubatch32_rapportee": reference_mtp,
                "gain_ubatch32_vers64_pct": gain_pct(reference_mtp, moyenne_medianes),
            },
            "lectures_contexte": lectures_mtp,
        },
        "limites": donnees["limites"],
    }


def decimal_vers_json(valeur):
    """Émettre des nombres JSON ; l'affichage JSON utilise la précision des floats."""
    if isinstance(valeur, Decimal):
        return float(valeur)
    raise TypeError(f"Type non sérialisable : {type(valeur).__name__}")


def nombre(valeur, decimales=10, signe=False):
    precision = Decimal(1).scaleb(-decimales)
    arrondi = valeur.quantize(precision, rounding=ROUND_HALF_UP)
    return format(arrondi, "+f" if signe else "f").replace(".", ",")


def afficher_texte(resultats):
    provenance = resultats["provenance"]
    print("RECALCUL DE VALEURS TRANSCRITES — aucun benchmark")
    print(provenance["document"])
    print(f"Audit rapporté : {provenance['date_audit_rapporte']} ; "
          f"mise en fichier : {provenance['date_mise_en_fichier']}.")
    print(provenance["nature"])
    print(provenance["portee_recalcul"])

    tg = resultats["campagne_colocation"]["generation"]
    print("\nColocation — génération (tokens/s)")
    print("Médianes des séries arrondies : "
          f"OFF {nombre(tg['mediane_off_series_arrondies'], 3)} ; "
          f"split22 {nombre(tg['mediane_split22_series_arrondies'], 3)}.")
    print("Gain sur ces séries arrondies : "
          f"{nombre(tg['gain_depuis_series_arrondies_pct'], signe=True)} %.")
    print("Médianes plus précises rapportées : "
          f"OFF {nombre(tg['mediane_off_plus_precise_rapportee'])} ; "
          f"split22 {nombre(tg['mediane_split22_plus_precise_rapportee'])}.")
    print("Gain sur ces médianes plus précises rapportées : "
          f"{nombre(tg['gain_depuis_medianes_plus_precises_rapportees_pct'], signe=True)} %.")

    pp = resultats["campagne_colocation"]["lecture_contexte"]
    print(f"\nColocation — lecture de {pp['tokens_entree']} tokens "
          f"(cache {pp['tokens_cache']}, débits en tokens/s)")
    print(f"{nombre(pp['mediane_off_rapportee'], 3)} → "
          f"{nombre(pp['mediane_split22_rapportee'], 3)} ; "
          f"gain descriptif {nombre(pp['gain_descriptif_pct'], 4, signe=True)} %.")
    print(pp["portee"])

    mtp = resultats["campagne_mtp_ubatch"]["generation"]
    print("\nMTP — génération (tokens/s)")
    print(f"Médiane B1 : {nombre(mtp['mediane_b1_ubatch64'])} ; "
          f"médiane B2 : {nombre(mtp['mediane_b2_ubatch64'])}.")
    print("Moyenne des deux médianes : "
          f"{nombre(mtp['moyenne_des_deux_medianes'])}.")
    print("UB32 → UB64, comparaison propre à ce réglage : "
          f"{nombre(mtp['reference_ubatch32_rapportee'])} → "
          f"{nombre(mtp['moyenne_des_deux_medianes'])} ; "
          f"{nombre(mtp['gain_ubatch32_vers64_pct'], 7, signe=True)} %.")

    print("\nMTP — lecture du contexte (tokens/s, séparée de la génération)")
    for pp in resultats["campagne_mtp_ubatch"]["lectures_contexte"]:
        print(f"{pp['tokens_entree']} tokens : "
              f"{nombre(pp['reference_ubatch32_rapportee'], 6)} → "
              f"{nombre(pp['finale_ubatch64_rapportee'], 6)} ; "
              f"gain descriptif {nombre(pp['gain_descriptif_pct'], 5, signe=True)} %.")

    print("\nPortée et limites")
    for limite in resultats["limites"]:
        print(f"- {limite}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Émettre un rapport JSON sur stdout.")
    arguments = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    resultats = recalculer(charger_donnees())
    if arguments.json:
        print(json.dumps(resultats, ensure_ascii=False, indent=2,
                         default=decimal_vers_json, allow_nan=False))
    else:
        afficher_texte(resultats)


if __name__ == "__main__":
    main()
