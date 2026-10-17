# Brief: Personal Wealth Architect · Arquitecto de ahorro e inversión

**Fecha:** 17 de octubre de 2026 (versión 2) · **Estado:** borrador para aprobación de Carolina · **Veredicto del estratega:** AVANZAR, con condiciones

Idea de trabajo para el rol actual de Carolina en una AFP colombiana. Se construye solo con datos públicos y simulados. Fuentes en `referentes.md`.

**Cambios frente a la versión 1:**
1. **Asesoría completa con herramientas tecnológicas** como supuesto de trabajo. El equipo jurídico está dispuesto a explorarlo con el AMV (Autorregulador del Mercado de Valores).
2. **Foco en ahorro e inversión.** La pensión obligatoria y las cesantías pasan a ser contexto, no el centro.
3. **Referentes retadores incorporados:** Revolut, BBVA, DBS, Robinhood, Wealthsimple, Mercado Pago y Nu Colombia.

## Necesidad y usuario
**Usuario:** afiliado de 30 a 45 años, de ingreso medio. Ya es cliente por su pensión obligatoria o sus cesantías, ahorra algo (cuenta de ahorros, Nu, un CDT) y no invierte con un plan.

**Momento:** cuando le queda un dinero para ahorrar (prima, aumento, bonificación, fin de año) o cuando entra al canal por un trámite.

**Lo que intenta lograr:** que su ahorro rinda y le sirva para sus metas, sin tener que convertirse en experto.

**Lo que se lo impide:** demasiadas opciones; el rendimiento visible de los neobancos, que le parece suficiente; no saber qué hacer con el siguiente peso; y la desconfianza de que le vendan lo que le conviene a la entidad.

**Contexto:** solo 2 de cada 10 personas bancarizadas en México invierten, y en Colombia menos del 1% invierte en bolsa. La competencia por el ahorro de este usuario hoy la ganan Nu Colombia (más de 5 millones de clientes) y Mercado Pago, con rendimiento simple y visible.

## Referentes y qué tomamos de cada uno
- **BBVA:** la escalera de servicio (orientar, asesorar, gestionar, humano) y la comisión explícita como transparencia.
- **Revolut:** la gestión automática por portafolios modelo con rebalanceo, una entrada a la inversión independiente del producto principal y la conversación que ejecuta con biometría (AIR).
- **DBS NAV Planner:** empezar por el balance y las brechas, abierto a toda la base, con tenencias externas declaradas.
- **Nu Smart Invest:** el puntaje con pilares y la proyección según el aporte mensual.
- **Origin:** la idoneidad antes de recomendar, el motor determinista que calcula, la IA que explica y los controles sobre cada respuesta.
- **Robinhood:** la simulación probabilística de metas y la eficiencia tributaria como valor visible.
- **WHOOP:** mostrar qué decisiones del usuario mueven su puntaje.

## Concepto elegido: el arquitecto del siguiente peso
**Propuesta de valor:** tu arquitecto de ahorro e inversión te muestra cómo está tu dinero, te recomienda qué hacer con el siguiente peso para tus metas y lo ejecuta contigo en un toque, con la transparencia de quién te asesora y cuánto cuesta.

**Nivel de innovación:** adyacente, con un componente disruptivo en el mercado colombiano: asesoría profesional completa entregada por herramientas tecnológicas, en web y WhatsApp.

**La escalera de servicio (núcleo del concepto):**
1. **Ver:** balance de ahorro e inversión (lo que tiene en la AFP más lo que declara afuera: Nu, CDT, otras), con puntaje de 0 a 1.000 y 5 pilares.
2. **Entender:** brechas frente a sus metas y qué decisiones mueven su puntaje.
3. **Recibir asesoría:** perfil de idoneidad conversacional y recomendación profesional automatizada, explicada y marcada como asesoría.
4. **Ejecutar:** aceptar la recomendación y aportar en un toque, con confirmación y biometría.
5. **Delegar:** gestión automática por metas, con portafolio modelo y rebalanceo.
6. **Hablar con un humano** en cualquier escalón.

Conceptos evaluados:
1. **Diagnóstico con asesoría automática** (incremental): puntaje y recomendación, sin ejecución ni gestión. Es rápido, pero se queda corto frente a Revolut y BBVA.
2. **Arquitecto del siguiente peso** (adyacente, **recomendado**): la escalera completa, con el diagnóstico como gancho y la gestión por metas como destino.
3. **Piloto automático del ahorro** (disruptivo): cada ingreso se reparte solo entre metas (emergencia, metas de mediano plazo, inversión de largo plazo, ahorro tributario) mediante mandatos. Es la siguiente fase, porque necesita datos reales de ingresos.

## Por qué es innovador frente a lo que existe hoy
- **En Colombia:** según las fuentes revisadas, ningún actor combina diagnóstico, asesoría profesional automatizada, ejecución y gestión por metas en un solo flujo conversacional. Las AFP digitalizaron trámites; Nu y Mercado Pago ofrecen rendimiento sin asesoría; trii ofrece acceso sin orientación.
- **Frente a los neobancos:** compite por metas y eficiencia tributaria, no por tasa. *A validar: los beneficios tributarios vigentes de los aportes voluntarios y sus topes.*
- **Frente a Nu Smart Invest:** cubre el ahorro de afuera (declarado), ejecuta y gestiona, y muestra el conflicto de interés y el costo en lugar de solo prometer imparcialidad.

## Hipótesis más riesgosas
1. **Mover el ahorro:** el usuario está dispuesto a mover ahorro desde un neobanco con rendimiento visible hacia un plan de inversión de su AFP, si ve metas, proyección y beneficio tributario.
2. **La AFP como marca de inversión:** el usuario confía en su AFP para ahorro e inversión, no solo para la pensión.
3. **Asesoría sin humano:** el usuario acepta y ejecuta una recomendación profesional automatizada sin hablar con nadie.
4. **Transparencia:** mostrar costo y conflicto de interés aumenta la conversión en vez de reducirla.
5. **Regulación (supuesto de trabajo):** la asesoría completa con herramientas tecnológicas es viable con el AMV y la SFC. Si no lo es, el diseño debe degradarse sin romperse: el escalón 3 pasa a un asesor certificado.

## MVP (prototipo con datos simulados)
**Incluye:**
- **App web móvil:** onboarding conversacional; balance con tenencias de la AFP y externas declaradas; puntaje con 5 pilares (diversificación, rentabilidad, liquidez, protección y eficiencia tributaria); metas con proyección "si aportas $X al mes"; perfil de idoneidad; recomendación profesional explicada; tarjeta de transparencia (quién asesora, tipo de asesoría, costo, alternativas); ejecución simulada en un toque; activación simulada de la gestión automática por metas.
- **WhatsApp:** conversación simulada que entrega el diagnóstico, responde preguntas, da la recomendación y lleva a ejecutar o a la app.
- **Motor de reglas explícito y determinista** para puntaje, proyecciones y recomendación. La IA solo explica y conversa.

**No incluye:** datos reales, dinero real o pagos, mandatos automáticos sobre ingresos, conexión a finanzas abiertas, pensión obligatoria como eje (solo aparece como contexto), otras dimensiones del patrimonio (vivienda, deudas, seguros), integración con sistemas de ninguna entidad ni modelos de IA entrenados.

## Métrica de éxito
**Prueba con 5 usuarios:**
- Al menos 4 de 5 explican con sus palabras su puntaje y su siguiente paso.
- Al menos 3 de 5 eligen ejecutar la recomendación en el prototipo.
- Al menos 3 de 5 prefieren este plan antes que dejar el dinero en su cuenta de ahorro actual, y explican por qué.
- Confianza promedio de 4 o más sobre 5 después de ver la tarjeta de transparencia.

**En un piloto real, más adelante:** porcentaje que ejecuta en 30 días frente a un grupo de control, monto nuevo administrado por usuario y porcentaje que activa la gestión automática.

## Guía para el diseñador (mecánicas a aterrizar)
1. **Escalera de servicio visible:** el usuario siempre sabe en qué escalón está y puede subir o bajar (BBVA).
2. **Balance primero:** la primera pantalla de valor es su foto completa, incluido lo de afuera (DBS).
3. **Puntaje con pilares y "qué lo mueve":** cada pilar termina en una acción posible (Nu y WHOOP).
4. **Recomendación con "por qué", proyección y costo,** en una sola tarjeta (Origin, Robinhood y BBVA).
5. **Ejecutar en un toque y delegar por metas,** con confirmación clara y biometría (Revolut).

## Control crítico
**5 razones por las que fallaría:**
1. **El rendimiento visible gana:** el usuario compara la tasa de su cuenta de ahorro con un portafolio de largo plazo y se queda donde está. Mitigación: la conversación es por metas y beneficio tributario, no por tasa.
2. **La marca no da permiso:** el usuario ve a la AFP como "la de la pensión" y no le confía su inversión. Puede necesitar una entrada con identidad propia, como Revolut Invest.
3. **El supuesto regulatorio falla o tarda:** si el AMV o la SFC exigen un profesional en la recomendación, el escalón 3 se vuelve asistido. El diseño debe soportarlo desde el inicio.
4. **Conflicto de interés real:** recomendar solo alternativas propias contradice la transparencia si la tarjeta no muestra alternativas y costos honestamente.
5. **Exceso de alcance:** seis escalones en el primer prototipo pueden diluir la prueba. El diseñador debe priorizar el recorrido ver → asesoría → ejecutar.

**¿Innovación real o copia?** Cada pieza existe en algún referente. La innovación está en juntarlas en un flujo conversacional para un usuario de ingreso medio en Colombia, con asesoría completa automatizada y transparencia de costos. Eso no aparece en el mercado local según las fuentes revisadas.

**¿Alguien lo hace en nuestro mercado?** Nu y Mercado Pago capturan el ahorro; BBVA lo hace en México sin metas ni IA; ninguna AFP lo muestra públicamente. No es concluyente.

**¿Funciona en Colombia?** Hay demanda digital (trii con 500.000 usuarios en Colombia, Nu con más de 5 millones de clientes), pero la desconfianza en LatAm es alta. La transparencia y el humano a una frase son condiciones, no adornos.

**¿Es lo más rápido para probar la hipótesis?** Sí, si el prototipo prioriza el recorrido ver → asesoría → ejecutar y deja la gestión automática como una pantalla de activación.

**Veredicto: AVANZAR**, con tres condiciones:
1. El escalón de asesoría se diseña con una variante asistida (asesor certificado), por si la exploración con el AMV no prospera.
2. El primer prototipo prioriza el recorrido ver → asesoría → ejecutar.
3. La tarjeta de transparencia muestra costos y alternativas de verdad.
