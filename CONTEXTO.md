# CONTEXTO · 17 de octubre de 2026 (v3, noche) — Prototipo v5.2 después de dos rondas del revisor independiente; listo para que Carolina lo revise

> El contexto anterior está en `historial-contextos/CONTEXTO-2026-10-17-v2.md`.

## 0. Leer primero
- La fábrica funciona: 4 especialistas guardados en la cuenta de Claude de Carolina (estratega, diseñador, desarrollador, experto financiero), este repositorio como memoria y la carpeta de Drive "Fabrica de diseno y desarrollo".
- Todo especialista lee `empresa/forma-de-trabajo.md` (el documento de Carolina, v2) antes de empezar y pasa su lista de verificación (sección 6) antes de entregar.
- **La definición que manda en todo diseño** (palabras de Carolina): *"En la banca privada, un wealth architect es el asesor que diseña el plan completo del patrimonio de una persona a partir de sus metas de vida, y no a partir de los productos que vende. Hasta hoy era un servicio reservado a pocos. La IA permite ponerlo en el bolsillo de cada afiliado, y el asesor lo completa cuando la decisión lo pide."* Antes de entregar cualquier pantalla o texto, revisar que el plan va antes que el producto y que está claro cuándo entra el asesor (`regulatorio.md`, sección 1B).
- **Trabajo previo de Carolina:** síntesis en el Google Doc "BASE DE CONOCIMIENTO — Trabajo previo de Carolina" de la carpeta de Drive de la fábrica (https://docs.google.com/document/d/1At0uLPCUv8-b6u7XO4R8IBjPtuaNt8gRbeNzA5VmX8k/edit) y originales en la subcarpeta "Documentos arquitectura 2026 y vision 2027" (arquitectura 2026 v6, visión 2027 v9, pitch al comité v2, análisis de tendencias v3, Pronto Contextual v4.1). Se leen como contexto; no se copian a este repositorio.
- **Al retomar:** leer este archivo, preguntar a Carolina qué definió desde la última sesión y seguir con el pendiente 1. (En la sesión del 17 de octubre en la noche se le preguntó y no alcanzó a responder antes de que se hiciera la revisión.)

## 1. Documentos vigentes
| Qué | Dónde |
|---|---|
| Manual de la fábrica | `README.md` |
| Forma de trabajo de Carolina (v2) | `empresa/forma-de-trabajo.md` (v1 en `empresa/versiones-anteriores/`) |
| Beneficios tributarios verificados (v2) | `empresa/beneficios-tributarios.md` (v1 en `empresa/versiones-anteriores/`) |
| Aprendizajes y mejoras a especialistas | `empresa/aprendizajes.md` |
| Respaldo de los 4 especialistas | `empresa/especialistas/` |
| Concepto PWA v5.1 | `ideas/personal-wealth-architect/concepto.md` |
| Brief v5.1 | `ideas/personal-wealth-architect/brief.md` |
| **Concepto regulatorio y catálogo de lo que se puede decir v1 (nuevo)** | `ideas/personal-wealth-architect/regulatorio.md` |
| 27 referentes y matriz | `ideas/personal-wealth-architect/referentes.md` |
| Diseño y copia del prototipo | `ideas/personal-wealth-architect/diseno/` |
| Prototipo editable (v5.2) | Artefacto de diseño "Personal Wealth Architect · Prototipo v5.2": https://claude.ai/artifact/9MVrnadPTUq5rhxkSjFxAR (38 pantallas en 4 filas: Laura el 1 de junio, Laura el 15 de junio, Juliana el 23 de noviembre y vistas internas; copia en `diseno/prototipo/`; v3, v5.0 y v5.1 en `diseno/versiones-anteriores/`) |
| Criterios del revisor, métricas y verificador | `empresa/criterios-de-revision.md`, `empresa/metricas.md`, `empresa/activos/plantillas/verificar-prototipo.py` |

## 2. Lo trabajado en esta sesión
- **Experto financiero:** revisó los textos sensibles del prototipo v3 y creó `regulatorio.md` v1: 27 ajustes de texto (7 de prioridad alta), catálogo de lo que se puede decir (plan antes que producto, beneficios, condiciones, advertencias, lo que la IA nunca dice, reglas de cálculo), mandatos viables hoy, retiro informado, escenarios restrictivos regulatorios y 11 preguntas para validar con personas.
- **Hallazgos principales:** la Circular Externa 14 de 2025 de la Superintendencia Financiera ya regula la asesoría con herramientas tecnológicas y permite tratar los portafolios estandarizados de pensión voluntaria como productos simples masivos (el riesgo de la asesoría automatizada baja de alto a medio); información y recomendación deben verse distintas; las cifras tributarias del prototipo cuadran, pero tres textos eran inexactos (retiro antes de tiempo, "no declaras renta", retención por nómina); la reforma pensional rige desde el 1 de abril de 2027 (sentencia C-264 de 2026); la Ley 2300 de 2023 fija horario y frecuencia de contacto; en modo servicio se puede informar del Mecanismo de Protección al Cesante.
- `empresa/beneficios-tributarios.md` pasó a v2 con lo verificado.
- Se leyeron como contexto los 9 archivos de la carpeta de Drive de la fábrica.
- **Diseñador:** prototipo v4 fiel a la definición del concepto: Juliana empieza por su plan (pantalla nueva), el colchón de Laura es un paso del plan y no un producto, el asesor entra por regla cuando la decisión lo pide, marcas de información o recomendación y pantalla nueva "Cómo funciona tu arquitecto". Aplicados los ajustes regulatorios a las pantallas.
- **Diseñador:** benchmark de experiencia (`diseno/benchmark-experiencia.md`) y prototipo v5, la app del arquitecto: inicio con patrimonio y plan, revisión periódica, metas, simulador, propuesta, patrimonio y tu equipo con consultora con nombre.
- **Fábrica v2 en uso:** el revisor independiente devolvió la v5 (7 que bloquean) y la v5.1 (2 que bloquean); el diseñador corrigió todo en v5.2 (`diseno/README.md`, sección 12). Nueva herramienta de verificación mecánica (enlaces, persona, momento, alturas, toques, marcadores, siglas) y componentes reutilizables en `empresa/activos/plantillas/`. Criterios nuevos B10, B11, C8, C9 y E4.

## 3. Decisiones tomadas (no se revisitan)
- **Aprobado por Carolina (17 de octubre):** el colchón es un paso del plan fuera de los productos de la entidad; el asesor certificado entra por regla cuando la decisión lo pide (por ejemplo, el aporte voluntario a la pensión obligatoria).
- **La experiencia principal es la app como hogar del plan, no el chat** (observación de Carolina sobre v4).
- Solo datos públicos o simulados en el repositorio y en los entregables. Los documentos internos de Carolina se usan como contexto y viven solo en su Drive.
- Segmentos: renta masiva (hasta unos $6 millones) y renta media ($8 a $9 millones al mes). Foco: ahorro e inversión.
- Siempre evaluar beneficios tributarios como gancho, sin depender de ellos.
- Supuesto de trabajo: asesoría completamente automatizada (a validar con el Autorregulador del Mercado de Valores; ahora con base en la Circular Externa 14 de 2025).
- Principio: el plan primero, el producto después.

## 4. Pendientes, en orden
0. **Carolina:** guardar las mejoras propuestas de los especialistas (diseñador y revisor en esta sesión; estratega, experto financiero y desarrollador desde la sesión anterior, si aún no se guardaron).
1. **Carolina:** revisar la v5.2 en el lienzo. Laura empieza en "Bienvenida", arriba a la izquierda; Juliana, en su inicio, en la tercera fila (`diseno/README.md`, sección 12). Decidir si el consultor con nombre aplica a la renta masiva. Lo que ella corrija y el revisor no vio se vuelve criterio nuevo.
2. **Diseñador:** ajustar lo que Carolina observe; luego vistas de Daniela y de los equipos comercial, remoto y de servicio, y la pantalla "Mis documentos".
3. Prueba con 5 usuarios por segmento (plan en `diseno/README.md`, sección 12.4).
4. **Experto financiero:** validar si el retiro de pensión voluntaria para una segunda vivienda conserva el beneficio; cerrar los cuatro puntos abiertos de `empresa/beneficios-tributarios.md`.
5. **Estratega:** en la siguiente versión del concepto, cerrar el "a verificar" de la prima de diciembre y bajar a medio el riesgo de la asesoría automatizada, según `regulatorio.md` sección 10.
6. **Desarrollador:** MVP solo cuando Carolina apruebe el diseño.
7. Validar con personas (no con la fábrica) las 11 preguntas de `regulatorio.md`, sección 9; las 6 de prioridad alta antes de cualquier piloto real.
8. Actualizar la base de conocimiento en Drive a v2 después del deep dive del 23 de octubre.

## 5. Frase para retomar en una conversación nueva
"Retomemos la fábrica: lee CONTEXTO.md del repositorio caro0907/Fabrica-innovacion y empecemos por el pendiente 1."
