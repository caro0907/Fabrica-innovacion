# CONTEXTO · 17 de octubre de 2026 (v2, noche) — Revisión regulatoria lista y prototipo v5: la app del arquitecto

> El contexto anterior está en `historial-contextos/CONTEXTO-2026-10-17-v1.md`.

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
| Prototipo editable (v4) | Artefacto de diseño "Personal Wealth Architect · Prototipo": https://claude.ai/artifact/9MVrnadPTUq5rhxkSjFxAR (v5: fila nueva de 8 pantallas de app sobre las 17 de v4; copia en `diseno/prototipo/`, v3 en `diseno/versiones-anteriores/`) |

## 2. Lo trabajado en esta sesión
- **Experto financiero:** revisó los textos sensibles del prototipo v3 y creó `regulatorio.md` v1: 27 ajustes de texto (7 de prioridad alta), catálogo de lo que se puede decir (plan antes que producto, beneficios, condiciones, advertencias, lo que la IA nunca dice, reglas de cálculo), mandatos viables hoy, retiro informado, escenarios restrictivos regulatorios y 11 preguntas para validar con personas.
- **Hallazgos principales:** la Circular Externa 14 de 2025 de la Superintendencia Financiera ya regula la asesoría con herramientas tecnológicas y permite tratar los portafolios estandarizados de pensión voluntaria como productos simples masivos (el riesgo de la asesoría automatizada baja de alto a medio); información y recomendación deben verse distintas; las cifras tributarias del prototipo cuadran, pero tres textos eran inexactos (retiro antes de tiempo, "no declaras renta", retención por nómina); la reforma pensional rige desde el 1 de abril de 2027 (sentencia C-264 de 2026); la Ley 2300 de 2023 fija horario y frecuencia de contacto; en modo servicio se puede informar del Mecanismo de Protección al Cesante.
- `empresa/beneficios-tributarios.md` pasó a v2 con lo verificado.
- Se leyeron como contexto los 9 archivos de la carpeta de Drive de la fábrica.
- **Diseñador:** prototipo v4 fiel a la definición del concepto: Juliana empieza por su plan (pantalla nueva), el colchón de Laura es un paso del plan y no un producto, el asesor entra por regla cuando la decisión lo pide, marcas de información o recomendación y pantalla nueva "Cómo funciona tu arquitecto". Aplicados los ajustes regulatorios a las pantallas.
- **Diseñador:** benchmark de experiencia (`diseno/benchmark-experiencia.md`) y prototipo v5, la app del arquitecto: inicio con patrimonio y plan, revisión periódica, metas, simulador, propuesta, patrimonio y tu equipo con consultora con nombre.

## 3. Decisiones tomadas (no se revisitan)
- **Aprobado por Carolina (17 de octubre):** el colchón es un paso del plan fuera de los productos de la entidad; el asesor certificado entra por regla cuando la decisión lo pide (por ejemplo, el aporte voluntario a la pensión obligatoria).
- **La experiencia principal es la app como hogar del plan, no el chat** (observación de Carolina sobre v4).
- Solo datos públicos o simulados en el repositorio y en los entregables. Los documentos internos de Carolina se usan como contexto y viven solo en su Drive.
- Segmentos: renta masiva (hasta unos $6 millones) y renta media ($8 a $9 millones al mes). Foco: ahorro e inversión.
- Siempre evaluar beneficios tributarios como gancho, sin depender de ellos.
- Supuesto de trabajo: asesoría completamente automatizada (a validar con el Autorregulador del Mercado de Valores; ahora con base en la Circular Externa 14 de 2025).
- Principio: el plan primero, el producto después.

## 4. Pendientes, en orden
0. **Fábrica v2 lista (17 oct, noche):** revisor independiente, criterios vivos, activos, vigía semanal (lunes 6:56 a. m.) y métricas. Carolina debe guardar las mejoras de los cuatro especialistas. El revisor devolvió la v5 con 7 hallazgos que bloquean (`empresa/metricas.md`); el diseñador debe corregirlos y pasar la segunda ronda antes del desarrollo.
1. **Carolina:** revisar la v5 en el lienzo (dos filas superiores: "Tu primera reunión", el diagnóstico, y "La app del arquitecto"; ver `diseno/README.md`, sección 11 y `diseno/benchmark-experiencia.md`). Decidir si el consultor con nombre aplica a la renta masiva.
2. **Diseñador:** ajustar lo que Carolina observe en v5; luego preparar la prueba con usuarios sobre la app (no sobre el chat).
3. Prueba con 5 usuarios por segmento (plan en `diseno/README.md`).
4. **Estratega:** en la siguiente versión del concepto, cerrar el "a verificar" de la prima de diciembre (verificado) y bajar a medio el riesgo de la asesoría automatizada (control crítico #2), según `regulatorio.md` sección 10.
5. **Desarrollador:** MVP solo cuando Carolina apruebe el diseño.
6. **Experto financiero:** cerrar los cuatro puntos abiertos de `empresa/beneficios-tributarios.md` (tributación de los rendimientos, gravamen a los movimientos financieros, efecto de la reforma pensional en los aportes voluntarios a la pensión obligatoria, aportes del empleador).
7. Validar con personas (no con la fábrica) las 11 preguntas de `regulatorio.md`, sección 9; las 6 de prioridad alta antes de cualquier piloto real.
8. Actualizar la base de conocimiento en Drive a v2 después del deep dive del 23 de octubre.

## 5. Frase para retomar en una conversación nueva
"Retomemos la fábrica: lee CONTEXTO.md del repositorio caro0907/Fabrica-innovacion y empecemos por el pendiente 1."
