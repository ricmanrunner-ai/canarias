#!/usr/bin/env python3
"""Obtiene coordenadas de cada sitio con Nominatim (OpenStreetMap).

- Lee data/sitios.csv.
- Usa la consulta de CONSULTAS (o el nombre del sitio si no hay) + la isla.
- Valida que el punto caiga dentro de la caja de su isla.
- Conserva las coordenadas ya guardadas en data/coordenadas.csv (solo busca las nuevas),
  así puedes corregir una a mano y no se pisa.

Uso:  python3 scripts/geocodificar.py
"""
import csv
import json
import pathlib
import time
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIOS = RAIZ / "data" / "sitios.csv"
SALIDA = RAIZ / "data" / "coordenadas.csv"

# (lon_min, lat_min, lon_max, lat_max)
CAJAS = {
    "Tenerife": (-16.95, 27.98, -16.10, 28.60),
    "Gran Canaria": (-15.86, 27.72, -15.35, 28.20),
    "Lanzarote": (-13.90, 28.82, -13.40, 29.25),
    "La Graciosa": (-13.56, 29.20, -13.46, 29.30),
    "Fuerteventura": (-14.55, 28.02, -13.80, 28.78),
    "La Palma": (-18.02, 28.44, -17.70, 28.88),
    "La Gomera": (-17.37, 28.00, -17.08, 28.23),
    "El Hierro": (-18.17, 27.62, -17.86, 27.86),
}

# Consulta que mejor representa el punto de cada sitio (punto de inicio de la ruta, pueblo, etc.)
CONSULTAS = {
    "El Sabinar y Ermita de los Reyes": "Ermita de Nuestra Señora de los Reyes, El Pinar",
    "Camino de Jinama": "Mirador de Jinama",
    "Camino de la Virgen": "Ermita de Nuestra Señora de los Reyes, El Pinar",
    "Mar de Las Calmas y Tacorón": "Tacorón",
    "Volcán de Tanganasoga y Hoya del Morcillo": "Hoya del Morcillo",
    "Charco Azul, Charco Manso y La Maceta": "La Maceta, Frontera",
    "Pozo de las Calcosas": "Pozo de las Calcosas",
    "Arenas Blancas y Faro de Orchilla": "Faro de Orchilla",
    "Sabinosa y Pozo de la Salud": "Sabinosa",
    "Roque de la Bonanza y Las Playas": "Roque de la Bonanza",
    "Árbol Garoé": "Garoé",
    "Mirador de la Peña / de Isora / de Las Playas": "Mirador de la Peña, Valverde",
    "La Restinga": "La Restinga",
    "Cofete y Villa Winter": "Cofete",
    "Barranco de las Peñitas y Ermita de la Peña": "Vega de Río Palmas",
    "Ajuy y sus cuevas": "Ajuy",
    "Puertito de los Molinos": "Los Molinos, Puerto del Rosario",
    "Majanicho": "Majanicho",
    "Lajares": "Lajares",
    "Playa de Esquinzo y Playa del Águila (El Cotillo)": "Playa de Esquinzo, El Cotillo",
    "Pozo Negro y Poblado de la Atalayita": "Pozo Negro",
    "Playa de Garcey y Playa del Viejo Rey": "Playa del Viejo Rey",
    "Ecomuseo La Alcogida (Tefía)": "Tefía",
    "Montaña de Tindaya": "Montaña de Tindaya",
    "Montaña de Cardón": "Montaña Cardón",
    "Las Playitas y Gran Tarajal": "Las Playitas",
    "Isla de Lobos": "Isla de Lobos",
    "Dunas de Corralejo": "Parque Natural de Corralejo",
    "Acusa Seca y Acusa Verde": "Acusa Seca",
    "Risco Caído y las montañas sagradas": "Risco Caído, Artenara",
    "Roque Bentayga": "Roque Bentayga",
    "El Carrizal de Tejeda → Presa del Parralillo": "El Carrizal, Tejeda",
    "Fortaleza de Ansite (Santa Lucía)": "La Fortaleza, Santa Lucía de Tirajana",
    "Cenobio de Valerón": "Cenobio de Valerón",
    "Cuatro Puertas (Telde)": "Cuatro Puertas, Telde",
    "Barranco de Azuaje": "Barranco de Azuaje",
    "Los Tilos de Moya": "Los Tilos, Moya",
    "Temisas y Agüimes": "Temisas",
    "Guayadeque": "Barranco de Guayadeque",
    "Fataga y su barranco": "Fataga",
    "Presa de Chira y Soria": "Presa de Chira",
    "El Hornillo (Agaete)": "El Hornillo, Agaete",
    "El Risco de Agaete y Playa de El Risco": "El Risco, Agaete",
    "Playa de Güigüí": "Playa de Güi-Güi",
    "Tamadaba y Faneque": "Pinar de Tamadaba",
    "Sardina del Norte (Gáldar)": "Sardina, Gáldar",
    "Playa del Cabrón (Arinaga)": "Playa del Cabrón",
    "Pozo Izquierdo": "Pozo Izquierdo",
    "Atalaya de Santa Brígida": "La Atalaya, Santa Brígida",
    "Vegueta, mercado y Las Canteras": "Vegueta, Las Palmas de Gran Canaria",
    "Cueva Pintada de Gáldar": "Cueva Pintada, Gáldar",
    "Roque Nublo": "Roque Nublo",
    "La Fortaleza de Chipude": "La Fortaleza, Vallehermoso",
    "El Cercado": "El Cercado, Vallehermoso",
    "Las Hayas – Casa Efigenia": "Las Hayas, Valle Gran Rey",
    "Garajonay por el Contadero → El Cedro": "El Cedro, Hermigua",
    "Imada": "Imada",
    "Taguluche y Arure": "Arure",
    "Playa de La Caleta (Hermigua)": "Playa de la Caleta, Hermigua",
    "Vallehermoso y Roque Cano": "Roque Cano",
    "Agulo y Mirador de Abrante": "Agulo",
    "Ermita de Guadalupe (Puntallana)": "Ermita de Nuestra Señora de Guadalupe, San Sebastián de La Gomera",
    "Los Órganos en barco": "Los Órganos, Vallehermoso",
    "Montaña Bermeja y Playa de Las Conchas": "Playa de las Conchas, La Graciosa",
    "Playa Lambra": "Playa Lambra",
    "Pedro Barba": "Pedro Barba",
    "Playa de La Cocina y Montaña Amarilla": "Montaña Amarilla, La Graciosa",
    "Playa Francesa": "Playa Francesa",
    "Caleta de Sebo de noche": "Caleta de Sebo",
    "Snorkel en la Reserva Marina del Archipiélago Chinijo": "Caleta de Sebo",
    "Poris de Candelaria (Tijarafe)": "Porís de Candelaria",
    "Ruta de los Dragos de Las Tricias (Garafía)": "Las Tricias",
    "Santo Domingo de Garafía y su puerto": "Santo Domingo de Garafía",
    "Caldera de Taburiente desde Los Brecitos": "Los Brecitos",
    "Ruta de los Volcanes (Cumbre Vieja)": "Refugio El Pilar",
    "Marcos y Cordero → Los Tilos": "Los Tilos, San Andrés y Sauces",
    "Volcán Tajogaite (2021)": "Tajogaite",
    "Roque de los Muchachos de noche": "Roque de los Muchachos",
    "Playa de Nogales (Puntallana)": "Playa de Nogales",
    "Puerto Espíndola y Charco Azul": "Puerto Espíndola",
    "La Fajana (Barlovento)": "La Fajana, Barlovento",
    "El Time y Mirador de El Time": "Mirador de El Time",
    "Puerto de Puntagorda y almendros en flor": "Puntagorda",
    "Pino de la Virgen y El Paso": "El Paso, La Palma",
    "Santa Cruz de La Palma": "Santa Cruz de La Palma",
    "Salinas de Fuencaliente": "Salinas de Fuencaliente",
    "Camino de los Gracioseros → Playa del Risco": "Playa del Risco, Haría",
    "Tenesar": "Tenesar",
    "Volcán del Cuervo y Montaña Colorada": "Volcán del Cuervo",
    "Rutas guiadas de Timanfaya (Tremesana / Litoral)": "Centro de Visitantes Mancha Blanca",
    "Volcán de la Corona y Ye": "Ye, Haría",
    "Caleta de Famara": "Caleta de Famara",
    "Charco del Palo": "Charco del Palo",
    "Arrieta y Punta Mujeres": "Arrieta",
    "Caletón Blanco y Playa de la Cantería (Órzola)": "Caletón Blanco",
    "Los Valles y Ermita de las Nieves": "Ermita de las Nieves, Teguise",
    "Haría y Máguez": "Haría",
    "Femés": "Femés",
    "Masdache y La Geria por pistas": "Masdache",
    "Playa de Janubio y Salinas": "Salinas de Janubio",
    "Playa del Paso / Caletas de Papagayo de punta a punta": "Playa de Papagayo",
    "Jameos del Agua / Mirador del Río / Fundación Manrique": "Jameos del Agua",
    "Chamorga → Faro de Anaga → Roque Bermejo": "Chamorga",
    "Afur → Playa de Tamadite": "Afur",
    "Taganana y El Draguillo": "Taganana",
    "Teno Alto (Los Bailaderos)": "Teno Alto",
    "Masca": "Masca",
    "Paisaje Lunar (Vilaflor)": "Paisaje Lunar, Vilaflor",
    "Teide al amanecer o con permiso nocturno": "Refugio de Altavista",
    "Sombra del Teide desde Guajara": "Alto de Guajara",
    "Chinyero y Arguayo": "Arguayo",
    "Charco del Viento (La Guancha)": "Charco del Viento",
    "Charco de la Laja (San Juan de la Rambla)": "Charco de la Laja",
    "Rambla de Castro y Playa de El Bollullo": "Rambla de Castro",
    "Punta del Hidalgo y Roque de los Dos Hermanos": "Punta del Hidalgo",
    "Chinamada": "Chinamada",
    "Malpaís de Güímar": "Malpaís de Güímar",
    "Lagunas de Erjos": "Charcas de Erjos",
    "Playa de La Tejita y Montaña Roja": "Playa de La Tejita",
    "Punta de Teno": "Faro de Teno",
    "La Laguna de noche": "San Cristóbal de La Laguna",
    "Mercado de Nuestra Señora de África (Santa Cruz)": "Mercado de Nuestra Señora de África",
}

ISLA_TEXTO = {"La Graciosa": "Lanzarote", "Lanzarote": "Lanzarote"}


def dentro(isla, lat, lon):
    x0, y0, x1, y1 = CAJAS[isla]
    return x0 <= lon <= x1 and y0 <= lat <= y1


def buscar(consulta, isla):
    x0, y0, x1, y1 = CAJAS[isla]
    for q in (f"{consulta}, {ISLA_TEXTO.get(isla, isla)}", consulta):
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
            {"q": q, "format": "json", "limit": 5, "viewbox": f"{x0},{y1},{x1},{y0}", "bounded": 1}
        )
        req = urllib.request.Request(url, headers={"User-Agent": "canarias-guia-personal/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.load(r)
        time.sleep(1.1)  # política de uso de Nominatim: 1 petición/segundo
        for hit in res:
            lat, lon = float(hit["lat"]), float(hit["lon"])
            if dentro(isla, lat, lon):
                return lat, lon, hit["display_name"]
    return None


def main():
    previas = {}
    if SALIDA.exists():
        previas = {r["sitio"]: r for r in csv.DictReader(SALIDA.open(encoding="utf-8"))}
    filas, fallos = [], []
    for s in csv.DictReader(SITIOS.open(encoding="utf-8")):
        if s["sitio"] in previas and previas[s["sitio"]]["lat"]:
            filas.append(previas[s["sitio"]])
            continue
        consulta = CONSULTAS.get(s["sitio"], s["sitio"])
        hit = buscar(consulta, s["isla"])
        if hit:
            lat, lon, nombre = hit
            filas.append({"isla": s["isla"], "sitio": s["sitio"], "lat": f"{lat:.5f}", "lon": f"{lon:.5f}",
                          "fuente": "osm", "osm": nombre})
        else:
            fallos.append(s["sitio"])
            filas.append({"isla": s["isla"], "sitio": s["sitio"], "lat": "", "lon": "", "fuente": "", "osm": ""})
        print(("OK " if hit else "-- ") + s["isla"] + " | " + s["sitio"] + (" -> " + hit[2][:70] if hit else ""))
    with SALIDA.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["isla", "sitio", "lat", "lon", "fuente", "osm"])
        w.writeheader()
        w.writerows(filas)
    print(f"\n{len(filas) - len(fallos)}/{len(filas)} con coordenadas. Sin encontrar: {fallos}")


if __name__ == "__main__":
    main()
