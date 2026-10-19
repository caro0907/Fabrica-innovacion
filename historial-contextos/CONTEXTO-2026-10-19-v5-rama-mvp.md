# CONTEXTO · 19 de octubre de 2026 (v5) — El MVP v1.1 pasó por dos rondas del revisor y está listo para que Carolina lo vea

> El contexto anterior está en `historial-contextos/CONTEXTO-2026-10-18-v4.md`.

## 0. Leer primero
- **Dónde está el MVP:** rama `mvp/personal-wealth-architect-v1` (código en `ideas/personal-wealth-architect/app/`, traspaso en `ideas/personal-wealth-architect/HANDOFF.md`). Para retomar: clonar el repositorio y cambiar a esa rama. Aún no está en `main` ni desplegado en Railway.
- La fábrica funciona: 5 especialistas guardados en la cuenta de Claude de Carolina, con sus mejoras al día el 18 de octubre (estratega, diseñador, experto financiero, revisor independiente y desarrollador), este repositorio como memoria y la carpeta de Drive "Fabrica de diseno y desarrollo".
- Todo especialista lee `empresa/forma-de-trabajo.md` (el documento de Carolina, v2) antes de empezar y pasa su lista de verificación (sección 6) antes de entregar.
- **La definición que manda en todo diseño** (palabras de Carolina): *"En la banca privada, un wealth architect es el asesor que diseña el plan completo del patrimonio de una persona a partir de sus metas de vida, y no a partir de los productos que vende. Hasta hoy era un servicio reservado a pocos. La IA permite ponerlo en el bolsillo de cada afiliado, y el asesor lo completa cuando la decisión lo pide."* Antes de entregar cualquier pantalla o texto, revisar que el plan va antes que el producto y que está claro cuándo entra el asesor (`regulatorio.md`, sección 1B).
- **Trabajo previo de Carolina:** síntesis en el Google Doc "BASE DE CONOCIMIENTO — Trabajo previo de Carolina" de la carpeta de Drive de la fábrica (https://docs.google.com/document/d/1At0uLPCUv8-b6u7XO4R8IBjPtuaNt8gRbeNzA5VmX8k/edit) y originales en la subcarpeta "Documentos arquitectura 2026 y vision 2027" (arquitectura 2026 v6, visión 2027 v9, pitch al comité v2, análisis de tendencias v3, Pronto Contextual v4.1). Se leen como contexto; no se copian a este repositorio.
- **Al retomar:** leer este archivo, preguntar a Carolina qué definió desde la última sesión y seguir con el pendiente 1. (Sigue pendiente su respuesta sobre el consultor con nombre, pendiente 2.)

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
| **MVP v1.1 (nuevo)** | Rama `mvp/personal-wealth-architect-v1`: `ideas/personal-wealth-architect/app/` y `HANDOFF.md` (sección 9: qué cambió) |
| **Revisiones del MVP (nuevo)** | `ideas/personal-wealth-architect/revisiones/2026-10-18-mvp-v1.md` (primera ronda) y `2026-10-19-mvp-v1.1.md` (segunda ronda y lo corregido después) |
| Criterios del revisor, métricas y verificador | `empresa/criterios-de-revision.md`, `empresa/metricas.md`, `empresa/activos/plantillas/verificar-prototipo.py` |

## 2. Lo trabajado en esta sesión (18 y 19 de octubre)
- **Desarrollador, MVP v1 (18 de octubre):** aplicación web con el motor determinista (restrictivos primero, el plan define lo elegible, priorización, compuertas de contacto, cinco campos), catálogo de lo que se puede decir como datos versionados con su control, redactor con Claude Haiku 5.5 apagado por defecto, registro de cada interacción, mandatos, vistas del consultor y del motor, y modo servicio de Andrés. La reforma pensional es un dato versionado, como pidió la vigía.
- **Primera ronda (18 de octubre):** el revisor y el experto financiero, como agentes aparte, devolvieron el MVP: 4 hallazgos que bloqueaban y 10 de prioridad alta. Las cifras cuadraban; fallaban coherencia de textos, consentimientos, idoneidad y el permiso del salario.
- **Desarrollador, MVP v1.1 (19 de octubre):** corrigió los 14 y casi todos los de prioridad media y baja. Lo más visible: el permiso del salario es opcional y, sin él, ninguna pantalla muestra cifras del salario; la regla "Prima con rumbo" se ofrece después de aprobar, desmarcada, con tope de $1.000.000 y sus condiciones a la vista; la recomendación es un portafolio del fondo de pensiones voluntarias; la hija de Laura es beneficiaria por ley y lo que falta es registrarla en su grupo familiar; nada viene marcado por defecto; los festivos de 2026 cuentan (el 15 de junio es festivo).
- **Segunda ronda (19 de octubre, la última):** el revisor confirmó resueltos 12 de los 14 y devolvió 2 en caminos que la demostración no recorre (otra prioridad distinta de la casa y deuda cara; retirar el permiso después de aprobar). Se corrigieron después, sin tercera ronda, con pruebas de caminos alternos. 74 pruebas y 29 pantallas sin problemas.
- **Cifras de Laura en el MVP:** pensión estimada $1,83 M (el prototipo decía $2,3 M: el MVP lleva a la cuenta individual el 11,5% de la cotización); salud del plan 585 el 1 de junio, 668 al registrar a su hija, 693 al aprobar y 735 con la regla; probablemente debe declarar renta (por $100.400).
- **Fábrica:** criterios nuevos A7, B12, C10 y C11; dos filas nuevas en `empresa/metricas.md`. Se trajo a la rama del MVP lo que estaba en `main` (radar y experto financiero v5).

## 3. Decisiones tomadas (no se revisitan)
- **Aprobado por Carolina (18 de octubre): el diseño v5.2 "quedó perfecto".** Es la base del desarrollo; no se rediseña sin una observación nueva de ella.
- **Aprobado por Carolina (17 de octubre):** el colchón es un paso del plan fuera de los productos de la entidad; el asesor certificado entra por regla cuando la decisión lo pide (por ejemplo, el aporte voluntario a la pensión obligatoria).
- **La experiencia principal es la app como hogar del plan, no el chat** (observación de Carolina sobre v4).
- Solo datos públicos o simulados en el repositorio y en los entregables. Los documentos internos de Carolina se usan como contexto y viven solo en su Drive.
- Segmentos: renta masiva (hasta unos $6 millones) y renta media ($8 a $9 millones al mes). Foco: ahorro e inversión.
- Siempre evaluar beneficios tributarios como gancho, sin depender de ellos.
- Supuesto de trabajo: asesoría completamente automatizada (a validar con el Autorregulador del Mercado de Valores; ahora con base en la Circular Externa 14 de 2025).
- Principio: el plan primero, el producto después.

## 4. Pendientes, en orden
1. **Carolina (siguiente paso):** revisar el MVP v1.1 (`HANDOFF.md`, sección 9, y `revisiones/2026-10-19-mvp-v1.1.md`), en especial las cifras que cambiaron frente al prototipo y lo corregido sin tercera ronda. Si aprueba: unir la rama a `main` y desplegar en Railway (pasos en `HANDOFF.md`, sección 2). Si corrige algo que el revisor no vio, se agrega un criterio y se registra como "detectado por Carolina".
2. **Carolina:** decidir si el consultor con nombre aplica a la renta masiva o solo a la renta media (el MVP puede dejarlo como una opción configurable mientras tanto).
3. **Experto financiero:** validar si el retiro de pensión voluntaria para una segunda vivienda conserva el beneficio; cerrar los cuatro puntos abiertos de `empresa/beneficios-tributarios.md`.
4. **Diseñador (cuando el MVP lo necesite):** vistas de Daniela y de los equipos comercial, remoto y de servicio, y la pantalla "Mis documentos" (ahí irían la recomendación y los consentimientos que hoy solo quedan en el registro).
4b. **Jurídico (fuera de la fábrica):** pregunta 12 de `regulatorio.md` (¿una administradora de pensiones puede recomendar un fondo de inversión colectiva?). Mientras tanto, el MVP recomienda un portafolio de pensiones voluntarias.
5. Prueba con 5 usuarios por segmento (plan en `diseno/README.md`, sección 12.4), idealmente sobre el MVP.
6. **Estratega:** en la siguiente versión del concepto, cerrar el "a verificar" de la prima de diciembre y bajar a medio el riesgo de la asesoría automatizada, según `regulatorio.md` sección 10.
7. Validar con personas (no con la fábrica) las 11 preguntas de `regulatorio.md`, sección 9; las 6 de prioridad alta antes de cualquier piloto real.
8. Actualizar la base de conocimiento en Drive a v2 después del deep dive del 23 de octubre.

## 5. Frase para retomar en una conversación nueva
"Retomemos la fábrica: lee CONTEXTO.md del repositorio caro0907/Fabrica-innovacion (rama mvp/personal-wealth-architect-v1) y sigamos con el pendiente 1."
