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
| Metas y la más importante | Elegir metas y marcar la prioridad | `generar-primera-reunion.py` | `D2-Metas` |
| Metas con números | Cifra propuesta que la persona ajusta (cuota de la casa, pensión deseada) | `generar-primera-reunion.py` | `D2b-Numeros` |
| Tu vida y tu dinero hoy | Dependientes y su edad, vivienda, deudas, gastos, ahorros aquí y en otras entidades, seguro | `generar-primera-reunion.py` | `D3-Vida`, `D3b-Dinero` |
| Perfil de riesgo en pesos | Las seis preguntas a la vista, en hipotético | `generar-primera-reunion.py` | `D4-Riesgo` |
| Esto entendí de ti | Resumen con números para corregir antes del plan | `generar-primera-reunion.py` | `D5-Entendi` |
| Tu plan (primera vez) | Patrimonio, pensión con supuestos, metas con origen, salud del plan y el orden del plan | `generar-primera-reunion.py` | `H-TuPlan` |
| Inicio del hogar del plan | Patrimonio, salud del plan con advertencia, nota del asesor, metas | `generar-app-del-plan.py` → `inicio()` | `H-Inicio`, `H-InicioJuliana` |
| Salud del plan | Seis pilares; el puntaje es su promedio | `pilares()` | `H-Pilares` |
| Revisión periódica | Para quien vuelve: cómo vas, qué cambió, lo que propongo (sin nombrar productos) y lo que no | `revision()` | `H-Revision` |
| Recomendación | Paso del plan + producto con porqué, riesgo en pesos, costo, condición, alternativas y medio verificable; regla al confirmar | `decision()` | `H-Decision`, `H-DecisionJuliana` |
| Mis reglas | Mandato con sus siete campos, pausar y cancelar | `reglas()` | `H-Reglas` |
| Plan de vida y calendario | Ancla con "Ver supuestos", metas, sugerencias, fechas del año | `plan()` | `H-Plan` |
| Meta con simulador | "¿Y si separas cada mes…?" con escenario bueno y malo | `generar-app-del-plan.py` | `H-Meta` |
| Patrimonio | Ocho dimensiones con su origen | `patrimonio()` | `H-Patrimonio` |
| Tu equipo, perfil y reglamento | Consultor con nombre y agenda, perfil, reglas, cómo funciona | `equipo()`, `perfil()`, `como_funciona()` | `H-Equipo`, `H-Perfil`, `H-ComoFunciona` |
| Pregunta (superficie secundaria) | El chat responde y lleva al plan | `chat()` | `H-Chat` |

Los componentes comunes (colores, etiquetas de información, recomendación y origen, navegación por persona con `tabbar(activa, persona)`, `ask_bar(persona)`, primera reunión, deslizadores y opciones) están en `plantillas/pantallas_asesoria.py`. Cada función recibe la persona: la persona secundaria lleva su nombre como sufijo en los archivos.

**Antes del revisor:** `python3 plantillas/verificar-prototipo.py <carpeta> --entradas <pantallas de entrada> --personas <sufijos> --internas <prefijos> --visual` revisa enlaces muertos, recorridos que cruzan de persona o abren vistas internas, pantallas huérfanas, marcadores sin llenar, siglas, contenido que no cabe y elementos tocables de menos de 44 px. Debe dar 0 que bloquean.
Uso: `python3 generar-primera-reunion.py <carpeta>/project` y `python3 generar-app-del-plan.py <carpeta>/project` escriben las pantallas en esa carpeta (se ejecutan desde `plantillas/`).
