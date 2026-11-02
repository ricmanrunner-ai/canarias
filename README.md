# 🌋 Canarias — mi guía personal

Repositorio para tener analizados los sitios de las Islas Canarias, isla por isla, y saber cómo llegar desde **Madrid (MAD)**, **Santander (SDR)** y **Bilbao (BIO)**.

## Estado

| Isla | Visitada | Aeropuerto(s) | Directo desde MAD | SDR | BIO | Ficha |
|---|---|---|---|---|---|---|
| Tenerife | ✅ | TFN (Norte) · TFS (Sur) | ✅ | ✅ | ✅ | [tenerife.md](islas/tenerife.md) |
| Lanzarote | ✅ | ACE | ✅ | ✅ (Binter, mar/sáb) | ⚠️ | [lanzarote.md](islas/lanzarote.md) |
| Gran Canaria | ⬜ | LPA | ✅ | ✅ | ✅ | [gran-canaria.md](islas/gran-canaria.md) |
| Fuerteventura | ⬜ | FUE | ✅ | ❌ | ⚠️ | [fuerteventura.md](islas/fuerteventura.md) |
| La Palma | ⬜ | SPC | ✅ | ❌ | ❌ | [la-palma.md](islas/la-palma.md) |
| La Gomera | ⬜ | GMZ (+ ferry) | ❌ | ❌ | ❌ | [la-gomera.md](islas/la-gomera.md) |
| El Hierro | ⬜ | VDE (+ ferry) | ❌ | ❌ | ❌ | [el-hierro.md](islas/el-hierro.md) |
| La Graciosa | ⬜ | — (ferry desde Órzola) | ❌ | ❌ | ❌ | [la-graciosa.md](islas/la-graciosa.md) |

✅ directo confirmado · ⚠️ estacional / sin confirmar · ❌ sin directo (escala o ferry)

Detalle completo en **[vuelos.md](vuelos.md)** y en bruto en [`data/vuelos.csv`](data/vuelos.csv).

## 🗺️ Mapa y web

- **Web:** https://claude.ai/artifact/3ZDAnfxZBMq21Vd1M9GReF (privada; se comparte desde su menú *Share*). Incluye el mapa del archipiélago con los 122 sitios, filtros por isla, ambiente y prioridad, buscador, vuelos desde MAD/SDR/BIO y un enlace a Google Maps en cada sitio.
- **Mapa para el móvil:** [`mapa/canarias.kml`](mapa/canarias.kml). Impórtalo en [Google My Maps](https://www.google.com/maps/d/) (*Crear mapa → Importar*) y aparecerá en la app de Google Maps, en *Guardados → Mapas*. Tiene una carpeta por isla y los pines coloreados por ambiente. También funciona con Organic Maps y Maps.me, que permiten usarlo sin conexión.

Para regenerar ambos después de editar una ficha:

```bash
python3 scripts/generar_sitios.py    # fichas → data/sitios.csv
python3 scripts/geocodificar.py      # solo busca coordenadas de sitios nuevos
python3 scripts/generar_mapa.py      # → mapa/canarias.kml y web/index.html
```

Si un pin cae mal, corrige `lat`/`lon` en `data/coordenadas.csv`, pon `manual` en `fuente` y vuelve a generar.

## Estilo de viaje

Este repositorio no es una guía para turistas de pulsera. Las reglas que sigue:
- **Prioriza los sitios 🔥 (joya local) y 🌿 (tranquilo).** Los 👥 aparecen solo si de verdad merecen la pena, siempre con el truco para evitar a la gente (madrugar, entrar por otro lado, ir a pie).
- **Dormir en pueblos:** casas rurales, casas-cueva o cascos históricos. Nunca en complejos de costa.
- **Comer donde come la gente local:** guachinches, bodegones, ventas, cofradías de pescadores y mercados.
- **Ir a fiestas de pueblo:** romerías, bajadas y carnavales locales. Cada ficha tiene su calendario.
- Cada ficha tiene una lista de **zonas a evitar**.

## Estructura

```
README.md          ← esto
vuelos.md          ← matriz de vuelos + cómo llegar a las islas sin directo
mis-viajes.md      ← diario de viajes y lista de deseos
islas/*.md         ← una ficha por isla: sitios con ambiente y prioridad, dónde dormir, comer, fiestas, qué evitar
data/vuelos.csv    ← datos de rutas (para filtrar / actualizar)
data/sitios.csv    ← todos los sitios en una tabla (se genera con scripts/generar_sitios.py)
data/coordenadas.csv ← lat/lon de cada sitio (OpenStreetMap + correcciones manuales)
data/islas.geojson ← contornos de las islas (OpenStreetMap, simplificados)
mapa/canarias.kml  ← mapa para Google My Maps / Organic Maps
web/               ← plantilla.html (fuente) e index.html (generada)
scripts/           ← generar_sitios.py, geocodificar.py, generar_mapa.py
```

## Cómo usarlo

- Marca un sitio como visitado cambiando `⬜` por `✅` en la ficha de la isla y regenera la tabla con `python3 scripts/generar_sitios.py`.
- **Prioridad** de cada sitio: ⭐⭐⭐ imprescindible · ⭐⭐ muy recomendable · ⭐ si hay tiempo.
- Los vuelos cambian cada temporada (verano: finales de marzo–octubre; invierno: finales de octubre–marzo). Revisa `vuelos.md` antes de cada viaje y actualiza la columna `ultima_revision`.

## Próximo viaje sugerido

Con dos islas ya hechas, el salto natural es **Gran Canaria**: tiene directo desde los tres aeropuertos, es la isla con más variedad (dunas, cumbres, pueblos, ciudad) y desde ahí Binter enlaza con cualquier otra isla. Después, **La Palma** o **La Gomera** para el lado verde y salvaje (ver propuestas en [mis-viajes.md](mis-viajes.md)).
