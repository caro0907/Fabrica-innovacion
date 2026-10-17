# Brief: Personal Wealth Architect · Arquitecto de portafolio

**Fecha:** 17 de octubre de 2026 · **Estado:** borrador para aprobación de Carolina · **Veredicto del estratega:** AJUSTAR (ver control crítico)

Idea de trabajo para el rol actual de Carolina en una AFP colombiana. Se construye solo con datos públicos y simulados. Fuentes en `referentes.md`.

## Necesidad y usuario
**Usuario:** afiliado de 30 a 45 años, de ingreso medio. Tiene pensión obligatoria y cesantías, y quizás algo de ahorro voluntario o un CDT. Nunca ha mirado su patrimonio como un portafolio.

**Momento:** cuando tiene un dinero para ahorrar (prima, aumento, cesantías) o cuando entra al canal por un trámite.

**Lo que intenta lograr:** saber si va bien y qué hacer con el siguiente peso que ahorre.

**Lo que se lo impide:** demasiadas opciones (las AFP ofrecen entre 50 y más de 70 alternativas), información dispersa y desconfianza de que le recomienden solo lo que le conviene a la entidad.

## Referentes y qué tomamos de cada uno
- **Nu Smart Invest:** el puntaje con pilares y la proyección según el aporte mensual.
- **Origin:** la idoneidad antes de recomendar, el motor determinista que calcula, la IA que explica y los controles sobre cada respuesta.
- **Betterment:** las explicaciones en lenguaje simple y la supervisión humana visible.
- **AIR de Revolut:** la conversación que termina en una acción segura.
- **WHOOP:** mostrar qué decisiones del afiliado mueven su puntaje.
- **Fintual:** simplificar la elección.

## Concepto elegido: el arquitecto transparente
**Propuesta de valor:** en dos minutos sabes qué tan sano está tu portafolio, por qué, y cuál es el siguiente paso que más te conviene a ti, con la transparencia de quién te lo recomienda y por qué.

**Nivel de innovación:** adyacente. Toma un patrón probado afuera (diagnóstico con puntaje y asesoría con IA) y lo lleva a un contexto donde nadie lo ofrece: el patrimonio pensional del afiliado colombiano.

Conceptos evaluados:
1. **Diagnóstico con puntaje** (incremental): puntaje de 0 a 1.000 sobre pensión obligatoria, voluntaria, cesantías y otras inversiones declaradas. Es rápido, pero por sí solo es una copia adaptada de Nu.
2. **Arquitecto transparente** (adyacente, **recomendado**): el puntaje más un arquitecto conversacional en web y WhatsApp. Orienta de forma automática y escala a recomendación profesional con idoneidad, controles y una tarjeta de transparencia sobre conflictos de interés.
3. **Coach de hábitos de inversión** (disruptivo): mandatos y seguimiento continuo de conductas. Tiene más valor a largo plazo, pero necesita datos reales y ejecución, así que es para una fase siguiente.

## Por qué es innovador frente a lo que existe hoy
- Nadie en Colombia, según las fuentes revisadas, diagnostica el portafolio del afiliado y le da un siguiente paso explicado.
- Convierte el conflicto de interés en confianza: en lugar de prometer "sin conflicto" sin explicar cómo (Nu), lo muestra abiertamente, en línea con la discusión regulatoria sobre el Decreto 661 de 2018.
- El mismo diagnóstico vive en web y en WhatsApp.

## Hipótesis más riesgosas
1. **Comprensión:** el afiliado entiende su puntaje y el siguiente paso, y lo puede explicar con sus palabras.
2. **Acción:** el diagnóstico lo mueve a actuar (aportar, cambiar de alternativa, no retirar).
3. **Confianza:** mostrar el conflicto de interés aumenta la confianza en vez de reducirla.
4. **Regulación:** una AFP puede dar recomendación profesional automatizada sobre sus propias alternativas, como asesoría no independiente. *Debe validarlo Cumplimiento antes del piloto real.*
5. **Datos:** sin finanzas abiertas, el afiliado acepta declarar sus otras inversiones a mano.

## MVP
**Incluye:**
- App web móvil: perfil de idoneidad conversacional (5 a 7 preguntas), portafolio simulado (pensión obligatoria, voluntaria, cesantías e inversiones declaradas), puntaje de 0 a 1.000 con 5 pilares, 3 recomendaciones explicadas y priorizadas, proyección "si aportas $X al mes", tarjeta de transparencia y botón "hablar con un asesor".
- WhatsApp: conversación simulada que entrega el mismo diagnóstico y responde preguntas sobre él.
- Dos carriles visibles: **orientación** automática y **recomendación profesional**, que pasa por idoneidad y queda marcada como tal.

**No incluye:** datos reales, pagos o ejecución de aportes, mandatos, conexión a finanzas abiertas, otras dimensiones del patrimonio (vivienda, deudas, educación), modelos de IA entrenados (las reglas del puntaje son deterministas y explícitas) ni integración con sistemas de ninguna entidad.

## Métrica de éxito del piloto (prueba con 5 usuarios)
- Al menos 4 de 5 explican su puntaje y su siguiente paso con sus propias palabras.
- Al menos 3 de 5 dicen que harían la acción recomendada.
- Confianza promedio de 4 o más sobre 5 después de ver la tarjeta de transparencia.

En un piloto real, más adelante: porcentaje que ejecuta la recomendación en 30 días frente a un grupo de control.

## Guía para el diseñador (mecánicas a aterrizar)
1. **Puntaje con 5 pilares**, adaptados al contexto pensional: diversificación, rentabilidad, liquidez, protección y eficiencia tributaria.
2. **"Por qué" en cada recomendación**, en una frase simple y con su efecto sobre el puntaje.
3. **Proyección interactiva:** "si aportas $X al mes, tu puntaje y tu resultado cambian así".
4. **Tarjeta de transparencia:** quién recomienda, si la asesoría es independiente o no, y qué alternativas existen.
5. **Qué mueve tu puntaje:** las 3 decisiones del afiliado con más efecto, al estilo WHOOP.

## Control crítico
**5 razones por las que fallaría:**
1. Cumplimiento podría exigir que la recomendación formal la haga un profesional certificado, lo que frenaría la automatización del segundo carril.
2. En la pensión obligatoria el afiliado tiene pocas palancas. Si el puntaje no ofrece acciones reales, se vuelve un número decorativo.
3. Sin finanzas abiertas, el portafolio depende de lo que el afiliado declare, y puede quedar incompleto.
4. Recomendar alternativas propias puede contradecir la promesa de transparencia si la tarjeta no es honesta de verdad.
5. Nubank opera en Colombia y podría traer Smart Invest; otras AFP también pueden lanzar algo similar.

**¿Innovación real o copia?** El puntaje es de Nu. La diferencia está en tres cosas: aplicarlo al patrimonio pensional, separar orientación de recomendación profesional, y hacer visible el conflicto de interés. Si se quita la transparencia, queda una copia.

**¿Alguien lo hace en nuestro mercado?** En las fuentes públicas revisadas no aparece. No es concluyente.

**¿Funciona en Colombia?** La desconfianza digital en LatAm es alta (Fintual en México), y menos del 1% invierte en bolsa. A favor: WhatsApp ya es un canal aceptado para asesoría en el sector.

**¿Es lo más rápido para probar la hipótesis?** Sí. Un prototipo con datos simulados y reglas explícitas prueba comprensión, acción y confianza en días.

**Veredicto: AJUSTAR.** Los cambios:
1. El prototipo prueba primero el carril de **orientación**. La **recomendación profesional** se diseña como un paso visible, pero su automatización queda sujeta a validación de Cumplimiento.
2. El puntaje debe girar alrededor de las palancas que el afiliado sí controla, para que cada pilar termine en una acción posible.

Con estos dos ajustes, la idea queda lista para pasar al diseñador.
