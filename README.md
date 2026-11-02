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

## Estructura

```
README.md          ← esto
vuelos.md          ← matriz de vuelos + cómo llegar a las islas sin directo
mis-viajes.md      ← diario de viajes y lista de deseos
islas/*.md         ← una ficha por isla: zonas, sitios, playas, rutas, comer, consejos
data/vuelos.csv    ← datos de rutas (para filtrar / actualizar)
data/sitios.csv    ← todos los sitios en una tabla (se genera con scripts/generar_sitios.py)
scripts/           ← utilidades
```

## Cómo usarlo

- Marca un sitio como visitado cambiando `⬜` por `✅` en la ficha de la isla y regenera la tabla con `python3 scripts/generar_sitios.py`.
- **Prioridad** de cada sitio: ⭐⭐⭐ imprescindible · ⭐⭐ muy recomendable · ⭐ si hay tiempo.
- Los vuelos cambian cada temporada (verano: finales de marzo–octubre; invierno: finales de octubre–marzo). Revisa `vuelos.md` antes de cada viaje y actualiza la columna `ultima_revision`.

## Próximo viaje sugerido

Con dos islas ya hechas, el salto natural es **Gran Canaria**: tiene directo desde los tres aeropuertos, es la isla con más variedad (dunas, cumbres, pueblos, ciudad) y desde ahí Binter enlaza con cualquier otra isla. Después, **La Palma** o **La Gomera** para el lado verde y salvaje (ver propuestas en [mis-viajes.md](mis-viajes.md)).
