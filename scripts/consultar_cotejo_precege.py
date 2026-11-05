"""Consulta pequeña del inventario PRECEGE; no modifica el catálogo."""
import argparse
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "precege-cotejo-inventario.json"


def normalizar(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto.casefold())
                   if not unicodedata.combining(c))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--resumen", action="store_true")
    group.add_argument("--buscar")
    parser.add_argument("--limite", type=int, default=20)
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    sections = ("expresiones_binomiales", "nombres_con_saltos_o_fragmentos",
                "nombres_comunes_o_rotulos", "referencias_anatomicas", "cola_previa")
    if args.resumen:
        print(json.dumps({"base_catalogo": data["base_catalogo"],
                          "archivos": len(data["fuentes"]),
                          "paginas": sum(f["paginas"] for f in data["fuentes"]),
                          **{k: len(data[k]) for k in sections}}, ensure_ascii=False, indent=2))
        return
    term = normalizar(args.buscar)
    found = []
    for section in sections:
        for row in data[section]:
            if term in normalizar(json.dumps(row, ensure_ascii=False)):
                found.append({"seccion": section, **row})
    print(json.dumps({"total": len(found), "resultados": found[:max(0, args.limite)]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
