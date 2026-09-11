# Remate Grupo Chung — chungo.tech

Catálogo de liquidación por cierre de oficina. Página estática, sin backend.

- `site/items.json` — inventario, precios, estatus (`disponible` / `apartado` / `vendido`), fases de descuento y paquetes. **Aquí se edita todo.**
- `site/index.html` — plantilla de la página.
- `site/fotos/` — fotos por clave (MOB-xx.jpg).
- `site/build.py` — genera `docs/index.html` con fotos y datos incrustados.
- `docs/` — lo que sirve GitHub Pages en chungo.tech.

## Actualizar (ej. marcar algo vendido)

```sh
# 1. editar site/items.json  →  "status": "vendido"
python3 site/build.py
git commit -am "MOB-17 vendido" && git push
```

Pages se actualiza en ~1 minuto.
