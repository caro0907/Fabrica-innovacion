# Aprendizajes de la fábrica

Al cerrar cada proyecto, registra qué funcionó, qué no y qué mejora proponer a los especialistas.

## Plantilla
### <idea> — <fecha>
- Qué funcionó:
- Qué no funcionó:
- Mejora propuesta a un especialista (cuál y qué cambia):

### Personal Wealth Architect · diseño v1 · 17 de octubre de 2026
- **Qué funcionó:** la profundidad de la investigación (27 referentes, matriz de piezas), el cálculo tributario por segmento, el calendario del dinero colombiano y los mandatos como diferenciales, y el prototipo navegable en un lienzo de diseño.
- **Qué no funcionó:**
  1. Un mecanismo (el "siguiente peso" y la prima) se volvió el producto, y el concepto dejó de ser un Personal Wealth Architect integral.
  2. La pensión salió del centro, cuando para una AFP es el ancla del plan de vida.
  3. El estratega no partió del trabajo previo de Carolina (su visión, su motor de decisión, su journey de 8 fases y sus OKR), que ya estaba en sus conversaciones.
  4. Faltaba una tesis de negocio explícita: llevar la asesoría integral de los grandes patrimonios a las rentas medias y masivas.
  5. Faltaban el diseño por objetivos y el motor de recomendación detrás de la experiencia.
- **Mejoras aplicadas a los especialistas:**
  - **Estratega:** sección "Fidelidad al concepto" (partir del trabajo previo de Carolina; el concepto manda y los mecanismos lo sirven; tesis de negocio con métrica), "diseño por objetivos y motor" como estándar, y nuevas preguntas de autoevaluación.
  - **Diseñador:** arquitectura de información del concepto completo antes de los flujos, el recorrido de la relación antes que la transacción, vistas internas (motor y consultor), autocrítica contra las promesas y revisión de textos sensibles por el experto financiero.

### Personal Wealth Architect · concepto v5 · 17 de octubre de 2026
- **Qué pasó:** Carolina compartió como contexto su trabajo previo (visión, arquitectura, análisis de referentes y tendencias, pitch). Se extrajo su método en `empresa/forma-de-trabajo.md`, solo en términos genéricos.
- **Qué faltaba en la fábrica:** leer cada fuente con su sesgo, las tres preguntas para decidir qué entra, el "tipo de respuesta" de cada necesidad, la primera versión visible pronto, y patrones de gobierno (restrictivos primero, cuatro poblaciones, catálogo de lo que se puede decir, reglas de la conversación, freno de servicio, niveles de control de los mandatos, lo que no hará nunca).
- **Qué cambió en el concepto:** arquitectura en cuatro capas, puntaje de 6 pilares con la pensión y la protección adentro, mandatos con nivel de control, sección 4C y H11.
- **Mejoras a los especialistas:** los cuatro leen `forma-de-trabajo.md`; el estratega suma el método y dos preguntas de autoevaluación; el diseñador, los patrones de relación visibles en el prototipo; el desarrollador, los patrones de motor y gobierno; el experto financiero, la revisión fija de conceptos con asesoría automatizada.

### Personal Wealth Architect · concepto v5.1 · 17 de octubre de 2026
- **Qué pasó:** llegó el documento de Carolina "Forma de trabajo y contexto de Carolina v1". Quedó completo en `empresa/forma-de-trabajo.md` (v2), con el complemento de la fábrica.
- **Qué detectó la revisión con su lista de verificación:** la sección 2 del concepto seguía con los rasgos y promesas de v3 y el nombre viejo ("Arquitecto del Siguiente Peso") en el diseño, los referentes y el título del prototipo. Faltaban el formato de pilotos ("si…, entonces…"), OKR con plazo y referente, horizontes con capacidad que dejan, la pregunta "¿quién lo hace?" del motor y el estado explícito de lo que es diseño.
- **Lección:** al cambiar de versión un concepto, buscar en todos los archivos el nombre y las piezas anteriores; los cambios no se aplican solo donde se edita.
- **Mejoras a los especialistas:** los cuatro leen el documento completo y pasan su lista de verificación antes de entregar; el estratega suma estructura del documento, estados, formatos de pilotos, OKR y olas, lenguaje de comité y observaciones por partes; el diseñador, estados visibles, marca y nombres, y todos los equipos.

### Personal Wealth Architect · revisión regulatoria v1 · 17 de octubre de 2026
- **Qué funcionó:** recalcular en código todas las cifras del prototipo antes de opinar (todas cuadraron, y eso permitió concentrarse en lo que los textos dicen); buscar la norma más reciente y no solo la conocida (la Circular Externa 14 de 2025 cambió el nivel de riesgo de la asesoría automatizada); revisar pantalla por pantalla con texto propuesto listo para el diseñador.
- **Qué no funcionó:** el prototipo confundía "pagar renta" con "declarar renta" y describía mal la pérdida del beneficio de la pensión voluntaria; ninguna revisión anterior lo detectó porque nadie había leído el artículo completo.
- **Mejoras propuestas a los especialistas:**
  - **Experto financiero:** revisar siempre contra la definición del concepto (plan antes que producto, cuándo entra el asesor), no solo contra la norma; separar en todo cálculo tributario "paga impuesto" de "debe declarar"; buscar circulares de la Superintendencia de los últimos 12 meses antes de calificar un riesgo regulatorio.
  - **Diseñador:** marcar en cada pantalla si es "información de tu plan" o "recomendación profesional"; nunca escribir que la entidad "mueve" dinero que está en otra cuenta; usar textos del catálogo de `regulatorio.md` en vez de redactar condiciones nuevas.

### Personal Wealth Architect · diseño v5 y fábrica v2 · 17 de octubre de 2026
- **Observaciones de Carolina:** la v4 se sentía como una IA que guía en un chat, no como un asesor personal; y la v5 empezaba con el plan sin el diagnóstico antes. Las dos estaban escritas en el skill del diseñador y no se aplicaron.
- **Lo que cambió en la fábrica:** un revisor independiente (`fabrica-revisor`) que corre como agente aparte, criterios vivos (`criterios-de-revision.md`), activos reutilizables (`activos/`), un vigía semanal y métricas de rondas de corrección (`metricas.md`).
- **Primera prueba del revisor:** devolvió la v5 con 7 hallazgos que bloquean, ninguno señalado antes por Carolina (por ejemplo, el recorrido de Juliana abría pantallas de Laura y el plan se saltaba después del diagnóstico). Es la primera evidencia de que la compuerta encuentra lo que la autoría no ve.
