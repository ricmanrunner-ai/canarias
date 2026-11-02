#!/usr/bin/env python3
"""Genera data/sitios.csv a partir de las tablas de islas/*.md.

Uso:  python3 scripts/generar_sitios.py
"""
import csv
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ISLAS = RAIZ / "islas"
SALIDA = RAIZ / "data" / "sitios.csv"


def filas(md: pathlib.Path):
    isla = re.sub(r"[#✅⬜]|visitada|pendiente", "", md.read_text(encoding="utf-8").splitlines()[0]).strip()
    for linea in md.read_text(encoding="utf-8").splitlines():
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) == 5 and celdas[0] in ("⬜", "✅"):
            check, sitio, tipo, prio, notas = celdas
            yield {
                "isla": isla,
                "sitio": sitio,
                "tipo": tipo,
                "prioridad": prio.count("⭐"),
                "visitado": "si" if check == "✅" else "no",
                "notas": notas,
            }


def main():
    todas = [f for md in sorted(ISLAS.glob("*.md")) for f in filas(md)]
    with SALIDA.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(todas[0].keys()))
        w.writeheader()
        w.writerows(todas)
    print(f"{len(todas)} sitios -> {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
