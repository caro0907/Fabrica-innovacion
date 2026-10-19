# Criterios de revisión: lo que Carolina revisaría

**v1 · 17 de octubre de 2026.** Es la lista viva que usa el revisor de la fábrica (`fabrica-revisor`). Cada vez que Carolina corrige algo que la fábrica no detectó, se agrega aquí un criterio con su origen. El revisor lo aplica desde el siguiente entregable, sin que nadie tenga que editar los especialistas.

**Cómo leerla:** cada criterio tiene un identificador, la pregunta que se hace el revisor, cómo se ve cuando falla y su origen. **Bloquea** = si falla, el entregable no llega a Carolina.

## A. Fidelidad al concepto

| Id | Pregunta | Cómo se ve cuando falla | Bloquea | Origen |
|---|---|---|---|---|
| A1 | ¿El entregable cumple la definición textual del concepto que dio Carolina? | Se puede leer el entregable sin reconocer la definición; falta alguna de sus partes | Sí | PWA, 17 oct: "un wealth architect diseña el plan completo a partir de las metas de vida, no de los productos; la IA lo pone en el bolsillo; el asesor lo completa cuando la decisión lo pide" |
| A2 | ¿El concepto es el centro, o un mecanismo (un gancho, una fecha, un beneficio) se volvió el producto? | El título, el primer mensaje o la primera pantalla hablan del mecanismo y no del concepto | Sí | PWA v1 a v3: "el siguiente peso" se volvió el producto |
| A3 | ¿El plan va antes que el producto? | Una meta termina siempre en un producto propio; el colchón o una acción del plan se resuelven con un producto de la entidad sin necesidad | Sí | PWA v4, 17 oct: el colchón terminaba en un producto propio |
| A4 | ¿Se cumplen todas las promesas del concepto dentro del alcance del MVP? | Una promesa no aparece en ninguna pantalla o sección | Sí | Estándar del diseñador |
| A5 | ¿Se partió del trabajo previo de Carolina? | Ideas que ella ya había resuelto aparecen como nuevas o contradichas | No | PWA v1: el estratega no partió de su material |
| A6 | ¿Las comparaciones con el mercado usan todos los referentes de la investigación previa (Drive y `referentes.md`), por grupo, y no solo los que nombra la instrucción? | Un informe o concepto que solo mira 4 o 5 competidores conocidos; grupos enteros (pensiones de otros países, reguladores, agentes de terceros) sin mencionar | Sí | Carolina, 18 oct 2026 (vigía semanal) |
| A7 | ¿Ningún texto del catálogo contradice la acción a la que lleva la misma pantalla o decisión? | La nota dice "antes de invertir, el colchón va primero" y el mismo recorrido propone invertir $780.000 en la casa | Sí | Revisor, 18 oct 2026 (MVP v1; lo llamó A6, renumerado) |

## B. Experiencia (cómo se siente para el usuario)

| Id | Pregunta | Cómo se ve cuando falla | Bloquea | Origen |
|---|---|---|---|---|
| B1 | ¿Se siente como un asesor personal y no como una conversación con una IA? | El chat es la experiencia principal; el plan solo existe dentro de una conversación | Sí | PWA v4, 17 oct: "parece más una interacción con una IA que guía en un chat" |
| B2 | ¿El recorrido empieza por conocer a la persona (diagnóstico) antes de mostrarle un plan o una recomendación? | Aparece un plan, un puntaje o una recomendación sin que antes se hayan hecho las preguntas | Sí | PWA v5, 17 oct: "¿por qué no iniciamos con las preguntas o el diagnóstico?" |
| B3 | ¿El inicio muestra el patrimonio y el plan de la persona? | El inicio es un menú, un saldo de un producto o una conversación | Sí | Benchmark de experiencia, 17 oct |
| B4 | ¿Hay una persona con nombre que ve el mismo plan y entra por regla cuando la decisión lo pide? | El humano es solo un botón genérico "hablar con alguien" | Sí | PWA v4, 17 oct |
| B5 | ¿Se distingue lo que es información de lo que es recomendación profesional? | Puntajes, planes o avisos se leen como recomendaciones | Sí | Regulatorio v1 (Circular Externa 14 de 2025) |
| B6 | ¿Cada propuesta dice su porqué, su riesgo en pesos, su costo y lo que no se propone? | Recomendación sin porqué, riesgo en etiquetas ("conservador") o sin costo | Sí | Concepto PWA y benchmark (revisión periódica) |
| B7 | ¿Se hizo un benchmark de experiencia con los mejores (incluidos Nubank y Revolut) antes de diseñar pantallas? | Pantallas sin `benchmark-experiencia.md` o sin tabla de mecánicas adaptadas | Sí | PWA v5, 17 oct: Carolina pidió analizar Nubank, Revolut y fintech |
| B8 | ¿Quién controla cada cosa delegada y cómo se deshace está a la vista? | Mandatos sin tope, vigencia, nivel de control o forma de cancelar | Sí | Concepto PWA |
| B9 | ¿Un usuario nuevo entiende en 5 segundos qué hacer en cada pantalla? | Pantallas con más de una acción principal o textos largos arriba | No | Estándar del diseñador |
| B10 | ¿Cada dato que usa el plan viene de lo que ya se sabe o de una pregunta del diagnóstico, con su origen visible? | El plan muestra montos (ahorro, cuota de la casa, meta de pensión) que nunca se preguntaron | Sí | Revisor, 17 oct 2026 (prototipo v5) |
| B11 | ¿La primera vez, después del diagnóstico, la persona ve su plan completo antes de cualquier propuesta? | Del diagnóstico pasa a una "revisión" o una propuesta como si fuera usuaria antigua | Sí | Revisor, 17 oct 2026 (prototipo v5) |
| B12 | ¿Toda aceptación de un mandato o consentimiento empieza desmarcada y muestra sus condiciones (tope, vigencia, aviso, cómo cancelar) antes de aceptar? | La casilla de la regla viene marcada en la propuesta y el tope y la vigencia solo se ven en Mis reglas | Sí | Revisor, 18 oct 2026 (MVP v1) |

## C. Rigor regulatorio y de cifras

| Id | Pregunta | Cómo se ve cuando falla | Bloquea | Origen |
|---|---|---|---|---|
| C1 | ¿Cada cifra tiene fuente y fecha, o está marcada como estimado con supuestos visibles? | Cifras sin supuestos; estimados que parecen promesas | Sí | Forma de trabajo, sección 1 |
| C2 | ¿Nada está redondeado hacia el lado que favorece la decisión? | $6,7 M cuando el cálculo da $6,65 M | No | Regulatorio v1 |
| C3 | ¿Se separa "paga impuesto" de "debe declarar"? | "No declaras renta" porque no paga | Sí | Regulatorio v1 |
| C4 | ¿Las condiciones de los beneficios están completas y correctas antes del beneficio? | "Lo devuelves en tu declaración"; permanencia sin decir qué pasa al retirar | Sí | Regulatorio v1 |
| C5 | ¿Los textos usan el catálogo de lo que se puede decir (`empresa/activos/catalogo-regulatorio-base.md`)? | Condiciones redactadas de nuevo, frases prohibidas ("garantizado", "sin conflicto de interés", "como nuestro mejor consultor") | Sí | Regulatorio v1 |
| C6 | ¿La entidad nunca "mueve" dinero que está en otra cuenta sin confirmación o autorización? | "Movemos tu dinero el 30 de junio" | Sí | Regulatorio v1 |
| C7 | ¿Las proyecciones son netas de comisiones y muestran un escenario malo? | Rangos solo optimistas | No | Regulatorio v1 |
| C8 | ¿La caída en pesos de un mal año de cada recomendación cabe en la pérdida que la persona dijo tolerar en su perfil? | El perfil dice "hasta 10%" y la recomendación "caída de 12%" | Sí | Revisor, 17 oct 2026 (prototipo v5.1) |
| C9 | ¿Cada estimado sale, recalculado en código, de los supuestos que la misma pantalla muestra, con el mismo método para todas las personas? | Pensión de $5,6 M con un saldo que, con esos supuestos, da unos $3,0 M | Sí | Revisor, 17 oct 2026 (prototipo v5.1) |
| C10 | ¿Retirar un permiso cambia de verdad lo que se muestra? Ninguna pantalla muestra cifras derivadas del dato sin permiso, y el texto lo dice | El motor deja de proponer, pero Mi plan, el inicio y el puntaje siguen con cifras del salario "que usamos porque nos autorizaste" | Sí | Revisor, 18 oct 2026 (MVP v1) |

## D. Forma de Carolina

| Id | Pregunta | Cómo se ve cuando falla | Bloquea | Origen |
|---|---|---|---|---|
| D1 | ¿La tesis está en el título y la conclusión va primero? | Títulos descriptivos ("Propuesta de canales") | No | Forma de trabajo, sección 2 |
| D2 | ¿Nombres completos, sin siglas, en lenguaje que un comité entiende? | AFP, AMV, FPV, SFC en textos para usuarios o comité | No | Forma de trabajo, sección 5 |
| D3 | ¿Los estados son explícitos (existe, en construcción, visión) y lo que se construye este año no aparece como existente? | Vistas internas sin estado | Sí | Forma de trabajo, sección 5 |
| D4 | ¿Están todos los equipos que viven el modelo (comercial, remoto, servicio, consultor)? | Vistas internas solo para un equipo | No | Forma de trabajo, sección 5 |
| D5 | ¿Ninguna frase critica lo construido antes ni suena a recorte? | Comparaciones negativas con lo que existe | No | Forma de trabajo, sección 5 |
| D6 | ¿No aparece el nombre de la solución de otra empresa como propia? | Marcas de referentes en pantallas | Sí | Forma de trabajo, sección 5 |

## E. Calidad del entregable

| Id | Pregunta | Cómo se ve cuando falla | Bloquea | Origen |
|---|---|---|---|---|
| E1 | ¿Cada pantalla cabe en su alto, con botones de al menos 44 px y contraste suficiente? | Contenido que se corta; textos grises claros | No | PWA, pantalla "Mi puntaje" |
| E2 | ¿Versión nueva en el nombre y dentro del documento, la anterior archivada, nada perdido? | Archivos sobrescritos sin versión | No | Forma de trabajo, sección 1 |
| E3 | ¿El CONTEXTO está actualizado? | Pendientes que ya se hicieron, decisiones sin registrar | No | Forma de trabajo, sección 1 |
| E4 | ¿Cada enlace lleva a una pantalla de la misma persona, la misma versión y el mismo momento, sin botones muertos ni salidas a versiones anteriores o a vistas internas? Se comprueba con `empresa/activos/plantillas/verificar-prototipo.py` (cada pantalla declara su momento) y, a mano, que cada salto de momento marcado tenga sentido | El inicio de Juliana abre el plan y la consultora de Laura; la bienvenida del 1 de junio abre la app del 15 de junio | Sí | Revisor, 17 oct 2026 (prototipos v5 y v5.1) |

## Historial de criterios agregados
- 19 de octubre de 2026: A7, B12 y C10, propuestos por el revisor en la primera revisión del MVP v1 (el que llamó A6 se numeró A7 porque A6 ya existía).
- 18 de octubre de 2026: A6, por una observación de Carolina sobre el vigía semanal (detectado por Carolina).
- 17 de octubre de 2026: C8 y C9, y E4 ampliado a "el mismo momento", propuestos por el revisor en la segunda ronda (prototipo v5.1).
- 17 de octubre de 2026: B10, B11 y E4, propuestos por el revisor en su primera revisión (prototipo v5).
- 17 de octubre de 2026: creación con A1 a E3, a partir de `forma-de-trabajo.md`, `aprendizajes.md` y las observaciones de Carolina sobre el Personal Wealth Architect.
