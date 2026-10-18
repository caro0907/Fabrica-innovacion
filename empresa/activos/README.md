# Activos de la fábrica: lo que el próximo proyecto no tiene que rehacer

**v1 · 17 de octubre de 2026.** Salen del Personal Wealth Architect, ya revisados por Carolina. Todo especialista los usa antes de crear algo desde cero; si un activo no sirve, se mejora aquí y queda para todos.

| Activo | Archivo | Quién lo usa |
|---|---|---|
| Sistema de diseño (colores, tipografías, tamaños, componentes) | `tokens.json` y la sección 1 de este archivo | Diseñador, desarrollador |
| Plantillas de pantallas de asesoría | `plantillas/` y la sección 2 | Diseñador |
| Catálogo regulatorio base | `catalogo-regulatorio-base.md` | Experto financiero, diseñador, desarrollador |
| Criterios de revisión | `../criterios-de-revision.md` | Revisor y todos los especialistas |

## 1. Sistema de diseño: "despacho del asesor"
Una sensación de banca privada cercana: fondo marfil, tinta verde oscura, acción verde, acentos en oro y ámbar. Tres tipografías con roles fijos: **Bricolage Grotesque** para títulos y cifras, **Newsreader** solo para lo que "escribe el asesor" (notas, revisiones, propuestas) y **Plus Jakarta Sans** para todo lo demás. Valores en `tokens.json`.

**Componentes que se repiten:**
- **Tarjeta de patrimonio** (fondo tinta): total, desglose y salud del plan en un anillo.
- **Nota del arquitecto** (fondo blanco, título en Newsreader, etiqueta "Información de tu plan"): qué cambió y una sola acción.
- **Tarjeta de meta** con porcentaje, barra y estado (en camino, requiere atención, por empezar, completo).
- **Etiquetas** "Información de tu plan" (verde) y "Recomendación profesional" (ámbar) en el encabezado de cada pantalla.
- **Bloque "paso del plan · no es un producto"** (verde suave) separado del bloque de recomendación.
- **Riesgo en pesos** (ámbar suave): "En un mal año podría bajar unos $…".
- **Equipo visible**: avatares del arquitecto y del consultor con nombre; agenda de 15 minutos.
- **Barra de pestañas**: Inicio · Mi plan · Patrimonio · Tu equipo. El chat es una barra secundaria ("Pregúntale algo a tu arquitecto"), nunca una pestaña principal.

**Reglas:** botones de al menos 44 px; texto de cuerpo nunca más claro que `texto-secundario`; sin degradados, emojis ni bordes laterales de color; datos ficticios marcados en cada recorrido.

## 2. Plantillas de pantallas
Los generadores de `plantillas/` producen las pantallas del lienzo de diseño (archivos `.dc.html`) con datos de ejemplo; se copian, se cambian los datos y se ejecutan. Las pantallas resultantes del primer proyecto están en `ideas/personal-wealth-architect/diseno/prototipo/`.

| Patrón | Para qué sirve | Generador | Ejemplo |
|---|---|---|---|
| Primera reunión: lo que ya sabemos | Abrir el diagnóstico sin preguntar lo que la entidad ya sabe | `generar-primera-reunion.py` | `D1-Bienvenida` |
| Metas | Elegir metas y plazo de la principal | `generar-primera-reunion.py` | `D2-Metas` |
| Tu vida hoy | Dependientes, vivienda, gastos con deslizador, deudas | `generar-primera-reunion.py` | `D3-Vida` |
| Perfil de riesgo en pesos | Seis preguntas, una por criterio de la norma de asesoría | `generar-primera-reunion.py` | `D4-Riesgo` |
| Esto entendí de ti | Resumen para corregir antes del plan | `generar-primera-reunion.py` | `D5-Entendi` |
| Inicio del hogar del plan | Patrimonio, salud del plan, nota del asesor, metas, equipo | `generar-app-del-plan.py` | `H-Inicio`, `H-InicioJuliana` |
| Revisión periódica | La carta del banquero privado: cómo vas, qué cambió, lo que propongo y lo que no | `generar-app-del-plan.py` | `H-Revision` |
| Plan de vida y calendario del dinero | Ancla, metas con estado, fechas del año | `generar-app-del-plan.py` | `H-Plan` |
| Meta con simulador | "¿Y si separas cada mes…?" | `generar-app-del-plan.py` | `H-Meta` |
| Propuesta | Paso del plan + recomendación, porqué, riesgo, costo, consultor a un toque | `generar-app-del-plan.py` | `H-Decision` |
| Patrimonio | Todo lo tuyo con lo que sabemos, nos contaste y falta | `generar-app-del-plan.py` | `H-Patrimonio` |
| Tu equipo | Consultor con nombre, arquitecto digital y cuándo entra el humano | `generar-app-del-plan.py` | `H-Equipo` |

Uso: `python3 generar-app-del-plan.py <carpeta>/project` escribe las pantallas en esa carpeta.
