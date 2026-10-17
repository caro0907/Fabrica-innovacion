# Brief táctico para el diseñador: El Arquitecto del Siguiente Peso

**v3 · 17 de octubre de 2026 · Veredicto del estratega: AVANZAR** · Concepto completo en `concepto.md`, referentes en `referentes.md`.

## Necesidad, usuario y principio
- **Usuario:** asalariado de 30 a 45 años, de ingreso medio, afiliado a la AFP. Tiene algo ahorrado en un neobanco y nunca ha invertido con un plan.
- **Necesidad:** saber qué hacer con el siguiente peso, sobre todo con el dinero extra que llega en fechas conocidas (prima de junio y de diciembre, intereses y consignación de cesantías), antes de que se diluya.
- **Principio rector:** el plan primero, el producto después. Si no hay colchón o hay deuda cara, el arquitecto no recomienda invertir.

## Propuesta de valor
Tu arquitecto de ahorro e inversión sabe cuándo te llega dinero extra, te propone un destino antes de que se te vaya, te asesora con transparencia y lo hace por ti si se lo pides.

> "Laura, si separas $200.000 al mes y el 30% de cada prima, en 20 años habrás puesto $79 millones y podrías tener entre $108 y $167 millones en pesos de hoy. ¿Quieres que lo haga por ti cada vez que llegue la prima?" *(Ilustrativo, con rentabilidades reales supuestas de 3% a 7%.)*

## MVP (H0: prototipo de 4 semanas, datos ficticios)
**Incluye el journey de Laura completo, en WhatsApp simulado y app web móvil:**
1. Aviso dos semanas antes de la prima, con el monto estimado.
2. Foto: balance, colchón en meses, puntaje de 0 a 1.000 con 5 pilares (colchón, rumbo, riesgo a la medida, costo y eficiencia, constancia) y "lo que más mueve tu puntaje".
3. Metas: colchón y largo plazo, con proyección interactiva.
4. Asesoría: perfil conversacional de 6 preguntas, recomendación con "por qué", riesgo en pesos, costo y tarjeta de transparencia.
5. Ejecución simulada con confirmación biométrica.
6. Mandato sobre la prima de diciembre (disparador, acción, destino, tope, vigencia, aviso) y pantalla "Mis reglas".
7. Botón "hablar con un asesor" en todo momento, y una vista del asesor con el mismo plan.

**No incluye:** datos reales, dinero real, integración con sistemas, finanzas abiertas, modelos de IA entrenados (reglas deterministas explícitas), pensión obligatoria como eje, ni otras dimensiones (vivienda, seguros).

## Hipótesis del MVP y umbrales
| Hipótesis | Umbral |
|---|---|
| H1 · Proponer el destino antes de la prima convierte más que después | Intención al menos 30% mayor en la versión "antes" |
| H2 · El afiliado deja un mandato si tiene tope, aviso y revocación | Al menos 3 de 5 lo activan |
| H3 · Ejecuta una recomendación automatizada sin pedir un humano | Al menos 3 de 5 |
| H4 · La transparencia sube la confianza | Confianza igual o mayor con la tarjeta |
| H5 · Le confía a su AFP el ahorro de mediano plazo | Al menos 3 de 5 sin objeción de fondo |

## Mecánicas que el diseño debe aterrizar
1. **Aviso anticipado con monto estimado** — calendario del dinero colombiano (diferencial propio, sin referente directo).
2. **Puntaje con pilares y "qué lo mueve"** — Nu Smart Invest y WHOOP.
3. **Recomendación con por qué, riesgo en pesos, costo y alternativas** — Origin, BBVA y la lección del Fondo E de Chile.
4. **Mandato con seis campos y "Mis reglas"** — AP2, Wealthfront Autopilot y Cleo Autopilot.
5. **Mismo plan para el afiliado y el asesor** — Morgan Stanley.

## Variantes que el diseño debe soportar
- **Asesoría asistida:** si el AMV o la SFC no habilitan la asesoría completa automatizada, el motor prepara y un asesor certificado firma en un clic.
- **Beneficio tributario:** se muestra solo a quien le aplica, con su cifra. Para el ingreso medio suele ser cero.
