#!/usr/bin/env python3
"""Genera el mapa y la web a partir de los datos del repositorio.

Salidas:
  mapa/canarias.kml   ← importable en Google My Maps / Organic Maps / Maps.me
  web/index.html      ← web autocontenida (plantilla web/plantilla.html + datos)

Uso:  python3 scripts/generar_sitios.py && python3 scripts/generar_mapa.py
"""
import csv
import json
import pathlib
import re
from xml.sax.saxutils import escape

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
ORDEN = ["Tenerife", "Gran Canaria", "Lanzarote", "La Graciosa", "Fuerteventura", "La Palma", "La Gomera", "El Hierro"]
FICHAS = {"Tenerife": "tenerife", "Gran Canaria": "gran-canaria", "Lanzarote": "lanzarote", "La Graciosa": "la-graciosa",
          "Fuerteventura": "fuerteventura", "La Palma": "la-palma", "La Gomera": "la-gomera", "El Hierro": "el-hierro"}
AEROPUERTO_ISLA = {"TFN": "Tenerife", "TFS": "Tenerife", "LPA": "Gran Canaria", "ACE": "Lanzarote",
                   "FUE": "Fuerteventura", "SPC": "La Palma", "GMZ": "La Gomera", "VDE": "El Hierro"}
COLOR_KML = {"joya local": "ff1d4fd9", "tranquilo": "ff4d8a2e", "concurrido": "ff8a8a8a"}  # aabbggrr


def leer(nombre):
    return list(csv.DictReader((DATA / nombre).open(encoding="utf-8")))


def limpiar_md(t):
    return re.sub(r"\*\*|\[([^\]]+)\]\([^)]+\)", lambda m: m.group(1) or "", t).strip()


def ficha(isla):
    """Saca de la ficha .md las líneas de contexto: llegar/aeropuerto, dónde dormir, evitar, carácter."""
    txt = (RAIZ / "islas" / f"{FICHAS[isla]}.md").read_text(encoding="utf-8")
    info = {"visitada": "✅ visitada" in txt.splitlines()[0]}
    for clave, patron in {
        "llegar": r"^\*\*(?:Aeropuertos?|Llegar):\*\*\s*(.+)$",
        "dormir": r"^\*\*Dónde dormir:\*\*\s*(.+)$",
        "caracter": r"^\*\*Carácter:\*\*\s*(.+)$",
        "truco": r"^\*\*Truco:\*\*\s*(.+)$",
        "evitar": r"^- \*\*Evitar:\*\*\s*(.+)$",
        "comer": r"^- \*\*Comer:\*\*\s*(.+)$",
        "fiestas": r"^- \*\*Fiestas:\*\*\s*(.+)$",
    }.items():
        m = re.search(patron, txt, re.M)
        if m:
            info[clave] = limpiar_md(m.group(1))
    return info


def vuelos_por_isla(vuelos):
    """Resume para cada isla y origen (MAD/SDR/BIO): directo / por confirmar / escala."""
    rango = {"confirmado": 3, "verificar": 2}
    res = {i: {o: {"estado": "escala", "detalle": []} for o in ("MAD", "SDR", "BIO")} for i in ORDEN}
    for v in vuelos:
        isla, o = AEROPUERTO_ISLA.get(v["destino"]), v["origen"]
        if not isla or o not in ("MAD", "SDR", "BIO") or v["estado"] not in rango:
            continue
        r = res[isla][o]
        r["detalle"].append(f'{v["destino"]}: {v["aerolineas"]} ({v["frecuencia"]})')
        nuevo = "directo" if v["estado"] == "confirmado" else "por confirmar"
        if r["estado"] == "escala" or (r["estado"] == "por confirmar" and nuevo == "directo"):
            r["estado"] = nuevo
    for o in ("MAD", "SDR", "BIO"):  # La Graciosa = volar a Lanzarote + ferry
        res["La Graciosa"][o] = {"estado": "ferry", "detalle": ["Vuelo a ACE + ferry Órzola → Caleta de Sebo"]}
    return res


def kml(sitios):
    partes = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Canarias fuera de ruta</name>']
    for amb, col in COLOR_KML.items():
        partes.append(f'<Style id="{amb.replace(" ", "-")}"><IconStyle><color>{col}</color>'
                      '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>'
                      '</IconStyle></Style>')
    for isla in ORDEN:
        partes.append(f"<Folder><name>{escape(isla)}</name>")
        for s in (x for x in sitios if x["isla"] == isla):
            estrellas = "★" * int(s["prioridad"])
            desc = f'{s["tipo"]} · {s["ambiente"]} · {estrellas}' + (" · ✅ visitado" if s["visitado"] == "si" else "")
            desc += f'\n\n{s["notas"]}'
            partes.append(f'<Placemark><name>{escape(s["sitio"])}</name>'
                          f'<description>{escape(desc)}</description>'
                          f'<styleUrl>#{s["ambiente"].replace(" ", "-")}</styleUrl>'
                          f'<Point><coordinates>{s["lon"]},{s["lat"]},0</coordinates></Point></Placemark>')
        partes.append("</Folder>")
    partes.append("</Document></kml>")
    return "\n".join(partes)


def main():
    coords = {c["sitio"]: c for c in leer("coordenadas.csv")}
    sitios = []
    for s in leer("sitios.csv"):
        c = coords.get(s["sitio"])
        if not c or not c["lat"]:
            print("Sin coordenadas (ejecuta scripts/geocodificar.py):", s["sitio"])
            continue
        sitios.append({**s, "lat": float(c["lat"]), "lon": float(c["lon"])})

    (RAIZ / "mapa").mkdir(exist_ok=True)
    (RAIZ / "mapa" / "canarias.kml").write_text(kml(sitios), encoding="utf-8")

    datos = {
        "sitios": [{k: s[k] for k in ("isla", "sitio", "tipo", "ambiente", "visitado", "notas", "lat", "lon")}
                   | {"prioridad": int(s["prioridad"])} for s in sitios],
        "islas": {i: ficha(i) for i in ORDEN},
        "vuelos": vuelos_por_isla(leer("vuelos.csv")),
        "contornos": json.loads((DATA / "islas.geojson").read_text(encoding="utf-8")),
        "revision": max(v["ultima_revision"] for v in leer("vuelos.csv")),
    }
    plantilla = (RAIZ / "web" / "plantilla.html").read_text(encoding="utf-8")
    html = plantilla.replace("/*__DATOS__*/null", json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    (RAIZ / "web" / "index.html").write_text(html, encoding="utf-8")
    print(f"{len(sitios)} sitios → mapa/canarias.kml y web/index.html")


if __name__ == "__main__":
    main()
