# Brief táctico para el diseñador: El Arquitecto del Siguiente Peso

**v3.1 · 17 de octubre de 2026 · Veredicto del estratega: AVANZAR** · Concepto completo en `concepto.md`, referentes en `referentes.md`.

## Necesidad, usuario y principio
- **Usuarios:** asalariados de 30 a 45 años afiliados a la AFP, en dos segmentos:
  - **Renta masiva** (hasta unos $6 millones al mes): no paga renta; tiene algo ahorrado en un neobanco y nunca ha invertido con un plan.
  - **Renta media** ($8 a $9 millones al mes): paga entre $2,7 y $4,4 millones de renta al año y no sabe cuánto podría ahorrar con la pensión voluntaria.
- **Necesidad:** saber qué hacer con el siguiente peso, sobre todo con el dinero extra que llega en fechas conocidas (prima de junio y diciembre, intereses y consignación de cesantías), antes de que se diluya.
- **Principio rector:** el plan primero, el producto después. Si no hay colchón o hay deuda cara, el arquitecto no recomienda invertir.

## Propuesta de valor
Tu arquitecto de ahorro e inversión sabe cuándo te llega dinero extra, te propone un destino antes de que se te vaya, te asesora con transparencia y lo hace por ti si se lo pides. Si pagas renta, además te muestra cuánto te ahorra tu impuesto y cuál es tu punto óptimo de aporte.

> **Renta media:** "Juliana, ganas $8,5 millones y este año pagarías unos $3,6 millones de renta. Si aportas $1.000.000 al mes a tu pensión voluntaria, pagas unos $1,7 millones menos: de cada 100 pesos que ahorras, 14 los pone tu impuesto."
>
> **Renta masiva:** "Laura, si separas $200.000 al mes y el 30% de cada prima, en 20 años habrás puesto $79 millones y podrías tener entre $108 y $167 millones en pesos de hoy."

*Ilustrativos y simplificados; cálculo tributario a validar con un experto.*

## MVP (H0: prototipo de 4 semanas, datos ficticios)
**Incluye dos journeys, en WhatsApp simulado y app web móvil:**
- **Laura (renta masiva), prima de junio:** aviso anticipado con el monto, foto con puntaje y colchón, metas con proyección, asesoría con perfil de 6 preguntas, ejecución simulada con biometría y mandato para la prima de diciembre.
- **Juliana (renta media), diciembre de oro:** impuesto estimado del año, aporte acumulado, faltante para su punto óptimo, explicación de la permanencia de 10 años conectada a una meta, ejecución antes del 31 de diciembre y mandato mensual para el año siguiente.

**Comunes a ambos:** puntaje de 0 a 1.000 con 5 pilares (colchón, rumbo, riesgo a la medida, costo y eficiencia, constancia), tarjeta de transparencia, "Mis reglas", botón "hablar con un asesor" y vista del asesor con el mismo plan.

**Calculadora tributaria simplificada y explícita:** salario, aportes del año y supuestos visibles. Nunca se muestra a quien no paga renta.

**No incluye:** datos reales, dinero real, integración con sistemas, finanzas abiertas, modelos de IA entrenados (reglas deterministas), pensión obligatoria como eje, ni otras dimensiones (vivienda, seguros).

## Hipótesis del MVP y umbrales
| Hipótesis | Umbral |
|---|---|
| H1 · Proponer el destino antes de la prima convierte más que después | Intención al menos 30% mayor en la versión "antes" |
| H2 · El afiliado deja un mandato si tiene tope, aviso y revocación | Al menos 3 de 5 lo activan |
| H3 · Ejecuta una recomendación automatizada sin pedir un humano | Al menos 3 de 5 |
| H4 · La transparencia sube la confianza | Confianza igual o mayor con la tarjeta |
| H7 · El ahorro de impuesto en pesos y el punto óptimo mueven a aportar más (renta media) | Al menos 3 de 5 suben su aporte simulado y explican la permanencia |
| H8 · El faltante personalizado de diciembre convierte más que un mensaje genérico | Intención al menos 30% mayor |

## Mecánicas que el diseño debe aterrizar
1. **Aviso anticipado con monto estimado** — calendario del dinero colombiano (diferencial propio).
2. **"Tu impuesto paga parte de tu ahorro" y el punto óptimo** — diferencial propio para la renta media; la lógica de mostrar el beneficio en pesos se inspira en Robinhood.
3. **Puntaje con pilares y "qué lo mueve"** — Nu Smart Invest y WHOOP.
4. **Recomendación con por qué, riesgo en pesos, costo y alternativas** — Origin, BBVA y la lección del Fondo E de Chile.
5. **Mandato con seis campos y "Mis reglas"** — AP2, Wealthfront Autopilot y Cleo Autopilot.

## Variantes que el diseño debe soportar
- **Asesoría asistida:** si el AMV o la SFC no habilitan la asesoría completa automatizada, el motor prepara y un asesor certificado firma en un clic.
- **Caso tributario complejo:** si el afiliado tiene dependientes, otras deducciones o ingresos no laborales, el cálculo se marca como estimado y se ofrece un asesor.
