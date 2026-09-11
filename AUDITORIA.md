# Revisión del catálogo — 11 de septiembre de 2026

Resultado: verificaciones locales satisfactorias antes de publicar.

- Catálogo: 30 artículos; MOB-29, MOB-30 y MOB-31 eliminados.
- Precios: IVA retirado y redondeo hacia arriba a centenas, sin centavos. Verificados contra los importes anteriores; comprobada la separación de IVA en el inventario PDF. Paquetes y notas de piezas sueltas actualizados; sumas por separado recalculadas.
- Fechas: eliminados calendario, cuenta regresiva y descuentos automáticos. Conservadas las fechas de compra y garantía de las computadoras como información del producto.
- Responsive: Chromium, anchos de 320, 360, 390, 420, 600, 768, 1024 y 1440 px, en modo claro y oscuro. Sin desbordamiento horizontal de página ni tarjetas; botones y filtros de al menos 44 × 44 px.
- Accesibilidad: cuatro análisis con axe-core (390 y 1440 px, claro y oscuro), reglas WCAG 2 A/AA y 2.1 AA, sin infracciones detectadas. Visor de fotos probado con apertura y cierre mediante Escape.
- Funcionalidad: siete filtros, 30 precios mostrados y sus enlaces de WhatsApp comprobados; 28 fotos responden correctamente y se decodifican en el navegador. Sin errores JavaScript.
- Revisión visual de capturas móviles y de escritorio. Las dos computadoras conservan su aviso previo para pedir una foto por WhatsApp.
- Publicación: HTML regenerado con `python3 site/build.py`; sitio estático de aproximadamente 716 KB incluyendo fotos, con carga diferida de imágenes y HTTPS configurado en GitHub Pages.

Las pruebas responsive son emulación de tamaños en Chromium, no pruebas en teléfonos físicos. La auditoría automática es esencial, no una certificación integral de accesibilidad ni una medición de rendimiento en redes móviles reales.

## Actualización: fotos y vendido destacado

- Conmutador conservado con cruz roja, etiqueta roja «VENDIDO», borde rojo y precio tachado; sin botón de compra.
- Agregadas cuatro fotos para PC-01 y PC-02, incluidas vistas adicionales en miniaturas. Los 30 artículos tienen foto principal; 32 archivos de imagen en total.
- Corregido el contenedor de fotos verticales para mantener su proporción cuadrada en las tarjetas.
- Repetidas las 16 combinaciones de ancho/tema y cuatro auditorías axe-core: sin fallos. Comprobados enlaces de compra de disponibles, filtros, imágenes y apertura/cierre con Escape de las fotos adicionales; sin errores JavaScript.
- Las fotografías originales se conservan sin retoques. Se aclara que computadora y monitor se venden por separado.
