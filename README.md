# Remate Grupo Chung — chungo.tech

Catálogo de liquidación por cambio de oficina. Página estática, sin backend.

- `site/items.json` — **aquí se edita todo**: inventario, precios, estatus, paquetes y textos de configuración.
- `site/index.html` — plantilla de la página (HTML, CSS y JS en un solo archivo). Diseño: navy y dorado del logo, Barlow Condensed para títulos y precios, fuente del sistema para lo demás; claro/oscuro automático, contraste ≥ 4.5:1, controles de 44 px, visor de fotos con `<dialog>`. Los precios son fijos y no dependen de fechas.
- `site/fotos/` — fotos por clave (`MOB-xx.jpg`).
- `site/logo.png` — logo de la barra superior (se incrusta en el HTML).
- `site/build.py` — genera `docs/`.
- `docs/` — lo que sirve GitHub Pages en chungo.tech. **No se edita a mano.**

## Actualizar (ej. marcar algo vendido)

```sh
# 1. editar site/items.json  →  "status": "vendido"
python3 site/build.py
git add -A docs site && git commit -m "MOB-17 vendido" && git push
```

Pages se actualiza en ~1 minuto. `build.py` también avisa si algún artículo referencia una foto que no existe.

## Diseño responsive

La plantilla es móvil primero y se adapta al ancho disponible sin depender de tamaños de dispositivo concretos:

- Los márgenes laterales, el espacio entre secciones y los encabezados usan valores fluidos.
- El catálogo pasa de una a dos columnas cuando cada tarjeta conserva un ancho útil; en pantallas mayores aumenta a tarjetas de 240 px como mínimo.
- Las tarjetas usan *container queries* para compactar tipografía solo cuando su propio ancho lo requiere.
- Los filtros se desplazan horizontalmente, los botones conservan un área táctil mínima de 44 px y los textos largos se parten sin provocar desplazamiento horizontal.
- La barra superior reduce logo y separación en pantallas de hasta 359 px para mantener visible el contador y el acceso a WhatsApp.

Al cambiar estilos en `site/index.html`, vuelve a ejecutar `python3 site/build.py`: `docs/index.html` es el archivo servido y debe viajar en el mismo commit.

## `items.json`

### `config`

| Campo | Uso |
|---|---|
| `whatsapp` | Número con lada de país, sin `+` (`528331881215`). Todos los botones abren `wa.me` con un mensaje ya escrito. |
| `telefono` | Se muestra como link `tel:` en "Cómo funciona", para quien no usa WhatsApp. |
| `direccion` | Texto de la dirección. |
| `mapa` | URL de Google Maps; la dirección se vuelve link en el hero y en "Ver y recoger". |
| `historia` | Línea humana bajo el título del hero (por qué se vende, qué pasa con el despacho). Si se deja vacía, no se muestra. |

### `items[]`

| Campo | Uso |
|---|---|
| `id` | Clave que ve el comprador y que llega en el mensaje de WhatsApp (`MOB-21`). |
| `nombre`, `cat`, `estado`, `nota` | Textos de la tarjeta. `cat` debe ser una de: `mobiliario`, `sillas`, `computo`, `clima`, `electro`, `gratis`. |
| `precio` | Precio de venta sin IVA, sin factura, en pesos enteros y múltiplos de $100. `0` = gratis con cualquier compra. |
| `nuevo` | Opcional. Precio aproximado nuevo; se muestra tachado como referencia ("Nuevo cuesta ~$12,000"). |
| `unidades` | Si es > 1 se muestra "N disponibles" y el precio lleva "c/u". |
| `instalado` | `true` muestra la etiqueta "Instalado · tú lo desmontas". |
| `status` | `disponible` / `apartado` / `vendido`. Apartado cambia el botón a "Preguntar si se libera"; vendido muestra una cruz y etiqueta rojas, tacha el precio y quita el botón. |
| `foto` | Clave del archivo en `site/fotos/` sin extensión. Sin foto, la tarjeta ofrece pedirla por WhatsApp. |

| `fotosExtras` | Opcional. Lista de claves de fotos adicionales; aparecen como miniaturas y se abren en el visor. |

### `lotes[]`

`{ "nombre", "detalle", "lista", "precio" }` — `lista` es la suma comprando por separado; `precio` el del paquete. Aparecen en la sección "Paquetes"; tienen precios fijos sin IVA y sin factura. Al cambiar precios individuales, actualiza también `lista` para que coincida con la suma de los artículos del paquete.

## Qué hace `build.py`

1. Incrusta `items.json` y `logo.png` en `docs/index.html` y fija `updated` a la fecha de hoy.
2. Copia a `docs/fotos/` solo las fotos que usa el catálogo y borra las que ya no.

El HTML pesa ~65 KB; cada foto carga aparte con `loading="lazy"`.

Los importes se convirtieron de los precios anteriores con IVA (16%) a precios sin IVA y se redondearon hacia arriba a la centena: `ceil(precio_anterior / 1.16 / 100) * 100`. Los importes sin IVA que ya son múltiplos de $100 no suben otra centena. Esta conversión se aplicó una sola vez; `build.py` utiliza directamente los precios guardados.
