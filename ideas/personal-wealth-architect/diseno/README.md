# Diseño: Personal Wealth Architect · v4

**17 de octubre de 2026 · Especialista: diseñador de la fábrica** · Parte del brief v3.2 (`../brief.md`). Todos los datos son ficticios.

## 1. Lo que este diseño debe probar
- **Necesidad:** que el dinero extra que llega en fechas conocidas no se diluya.
- **Usuarios:** Laura, de renta masiva, y Juliana, de renta media.
- **Concepto:** un arquitecto que avisa antes de que llegue el dinero, asesora con transparencia, ejecuta y cumple reglas, y para la renta media asigna cada peso al vehículo tributario correcto.
- **Hipótesis principal:** proponer el destino **antes** de que llegue el dinero, con números personales, lleva a actuar (H1). Para la renta media, además, ver el ahorro de impuesto en pesos y el faltante exacto lleva a aportar (H7 y H8).

## 2. Mecánicas adaptadas
| Mecánica | Referente | Cómo la adaptamos | Qué cambiamos |
|---|---|---|---|
| Aviso anticipado con monto estimado | Propio (calendario del dinero colombiano) | WhatsApp dos semanas antes de la prima, con el monto calculado desde el salario | No hay referente: es el diferencial; se cuida que el tono sea de ayuda, no de venta |
| Puntaje con pilares y "qué lo mueve" | Nu Smart Invest, WHOOP | Puntaje de 0 a 1.000 con 5 pilares de un asalariado colombiano; arriba, las 2 decisiones que más lo mueven | De portafolio de inversión a "salud del ahorro"; cada pilar termina en una acción |
| Recomendación con por qué, riesgo en pesos y costo | Origin, BBVA, lección del Fondo E de Chile | Una tarjeta: qué, por qué, cuánto podría bajar en un mal año (en pesos), cuánto cuesta | Nada de etiquetas de riesgo ("conservador") como explicación |
| Tarjeta de transparencia | Discusión del Decreto 661 de 2018; Nu promete imparcialidad sin explicarla | Quién asesora, que la asesoría no es independiente, costo anual y alternativas | Se muestra siempre, no en letra pequeña |
| "Tu impuesto paga parte de tu ahorro" y faltante al punto óptimo | Propio; Robinhood muestra el beneficio en pesos | Barra de progreso hacia el punto óptimo, con impuesto antes y después y supuestos visibles | Solo para quien paga renta; cálculo marcado como estimado |
| Cada peso al vehículo correcto | Propio (asesoría que hoy da un contador) | Tres metas, tres vehículos, cada uno con su condición en una frase | La condición de permanencia se ve antes de aceptar |
| Confirmar con biometría | Revolut AIR | Confirmación con huella | — |
| Mandato con seis campos y "Mis reglas" | AP2, Wealthfront Autopilot, Cleo | Disparador, acción, destino, tope, vigencia y aviso, en lenguaje natural; pausar y cancelar en un toque | Disparadores del calendario colombiano (prima, cesantías) |
| Mismo plan para el asesor | Morgan Stanley | Vista del asesor con plan, conversación, mandatos y el motivo del contacto | — |

## 3. Journey: hoy frente a la propuesta
**Laura, renta masiva:**

| Paso | Hoy | Con el arquitecto | |
|---|---|---|---|
| Antes de la prima | Nada | Aviso con el monto estimado y una pregunta | **Innovación:** anticipación |
| Llega la prima | Cae a la cuenta y se diluye | Ya hay un plan: colchón y largo plazo | |
| Decidir | Sola, con 50 o más alternativas o ninguna | Una recomendación con por qué, riesgo en pesos y costo | **Dolor resuelto:** sobrecarga de opciones |
| Actuar | Varios pasos en otra app | Huella en el mismo flujo | |
| Diciembre | Se repite el ciclo | Una regla se cumple sola, con aviso | **Momento sorpresa:** "no tuve que hacer nada" |

**Juliana, renta media:**

| Paso | Hoy | Con el arquitecto | |
|---|---|---|---|
| Noviembre | No sabe cuánto pagará de renta ni cuánto puede ahorrar | Le dicen su faltante exacto y cuánto ahorra si lo completa | **Momento sorpresa:** "mi impuesto paga parte de mi ahorro" |
| Decidir | Aporta "lo que alcance" en diciembre, a ciegas o nada | Cada peso a su vehículo según la meta, con la condición clara | **Innovación:** asignación tributaria por meta |
| El año siguiente | Repite la carrera de diciembre | Un mandato mensual llega al punto óptimo sin estrés | |

## 4. Pantallas (texto real en el prototipo)
**Laura:** L1 WhatsApp con el aviso · L2 Tu foto (puntaje y colchón) · L3 Plan para tu prima · L4 Recomendación, transparencia y huella · L5 Mis reglas.

**Juliana:** J1 WhatsApp diciembre de oro · J2 Tu impuesto paga parte de tu ahorro · J3 Cada peso a su vehículo · J4 Confirmar y regla mensual.

**Asesor:** A1 Mismo plan, con contexto.

## 5. Plan de prueba con 5 usuarios por segmento
**Participantes:**
- **Renta masiva:** 5 asalariados de 30 a 45 años con salario entre $3,5 y $6 millones, que reciben prima y tienen ahorro en una cuenta o un neobanco.
- **Renta media:** 5 asalariados con salario entre $8 y $9 millones, que declaran renta.

Nadie que trabaje en el sector financiero.

**Tareas:**

| # | Laura (masiva) | Juliana (media) |
|---|---|---|
| 1 | "Te llegó este mensaje. ¿Qué harías?" (L1) | "Te llegó este mensaje. ¿Qué entiendes?" (J1) |
| 2 | "Explica con tus palabras cómo estás y qué mueve tu puntaje." (L2) | "¿Cuánto ahorrarías de impuesto y qué tendrías que hacer?" (J2) |
| 3 | "Decide qué hacer con tu prima." (L3 y L4) | "Reparte tu aporte entre tus metas. ¿Qué condición tiene cada opción?" (J3) |
| 4 | "Deja que diciembre pase solo." (L5) | "Deja listo el año siguiente." (J4) |

**Qué observar y medir:**
- Tiempo hasta entender el mensaje inicial (meta: menos de 10 segundos).
- Si explican el puntaje o el ahorro de impuesto con sus palabras.
- Si ejecutan o activan la regla.
- Confianza de 1 a 5, antes y después de ver la tarjeta de transparencia.
- Si mencionan la condición de permanencia sin que se les pregunte.
- En qué momento piden hablar con alguien y por qué.

**Criterio de que la innovación funciona** (no solo que la interfaz se entiende):
- Al menos 3 de 5 dicen que actuarían **porque el aviso llegó antes**.
- Al menos 3 de 5 activan la regla.
- En renta media, al menos 3 de 5 suben su aporte hacia el punto óptimo **y** explican la condición del vehículo que eligieron.
- La confianza no baja con la tarjeta de transparencia.

**Prueba A/B dentro del mismo estudio:**
- L1 con aviso "antes" frente a mensaje "ya te llegó la prima".
- J1 con faltante personalizado frente a mensaje genérico de beneficio tributario.

## 6. Autocrítica aplicada
- **¿Se entiende en 5 segundos?** El primer mensaje de cada journey dice monto, fecha y pregunta en dos líneas.
- **¿Se nota la innovación?** El aviso anticipado y el faltante tributario abren cada journey, en lugar de quedar escondidos dentro de una pantalla.
- **¿Qué se eliminó?**
  - El onboarding largo: el perfil de idoneidad se resume en 6 preguntas que ya se dan por respondidas en el prototipo, con un enlace para verlas.
  - Una pantalla de metas separada: las metas viven dentro del plan.

## 7. Prototipo
- **Lienzo de diseño editable** en Claude: "Personal Wealth Architect · Prototipo" (antes "Arquitecto del Siguiente Peso"), con 10 pantallas.
- **Copia de las fuentes** en `prototipo/`.
- **Pantallas interactivas:**
  - L3: deslizador de la prima y montos mensuales, con proyección.
  - L4: confirmación con huella.
  - L5: pausar la regla.
  - J3: casilla "tengo crédito de vivienda" y casilla de comprensión de la condición.
  - J4: confirmación y regla mensual.
- **Costos de las alternativas:** quedan como marcadores `[X]%` hasta tener tarifas públicas.
- **Beneficios de la pensión voluntaria más allá de la renta:** menos retención mensual (J2) y abono a la hipoteca (J1 y J3), según `empresa/beneficios-tributarios.md`.

## 8. Versión 2 del prototipo (17 de octubre de 2026)
Ajustes a partir de las observaciones de Carolina (ver `../concepto.md`, v4):
- **Laura recorre la asesoría integral completa:** aviso → diagnóstico conversacional (L2) → mi patrimonio en 8 dimensiones (L3) → mi plan de vida con la pensión como ancla (L4) → siguiente paso: la prima (L5) → recomendación (L6) → mis reglas (L7).
- **Nueva vista para negocio, "el motor por dentro" (M1):** conocimiento, plan, escenarios (con los restrictivos), acciones elegibles, priorización, activación y medición.
- **Juliana y la vista del consultor** se mantienen como el escenario tributario de renta media.
- **Nuevas hipótesis:** H9 (paridad de calidad con consultor senior) y H10 (integral frente a transaccional), en el concepto.

## 9. Versión 3 del prototipo (17 de octubre de 2026)
Alineada con el concepto v5.1 y el brief v5.1:
- **Nueva pantalla L3b · Mi puntaje:** 520 de 1.000 sobre 6 pilares (colchón, suficiencia, protección, riesgo a la medida, eficiencia, constancia), cada uno con su nota, y la acción que más lo mueve. Se llega desde "Mi patrimonio" (la foto).
- **Nueva pantalla S1 · Modo servicio:** Andrés pierde su empleo y pide sus cesantías; el agente resuelve, no vende, pausa la regla de la prima y deja al consultor a una frase. Incluye lo que hizo el motor (vista interna).
- **Nivel de control en los mandatos:** "Te propongo y tú confirmas" (Laura, Mis reglas) y "lo hago solo dentro del tope y te aviso después" (Juliana, regla mensual).
- **Estados visibles:** "el motor por dentro" dice que todo es diseño y nada está en operación.
- **Nombre:** el lienzo pasa a "Personal Wealth Architect · Prototipo".
- **Pendiente:** revisión de los textos sensibles por el experto financiero antes de probar con usuarios.

## 10. Versión 4 del prototipo (17 de octubre de 2026, noche): fiel a la definición del concepto
Revisión de las 15 pantallas contra la definición de Carolina: *"un wealth architect diseña el plan completo del patrimonio a partir de las metas de vida, y no a partir de los productos que vende; la IA lo pone en el bolsillo de cada afiliado, y el asesor lo completa cuando la decisión lo pide"*. La copia de v3 queda en `versiones-anteriores/prototipo-v3/`.

**Desvíos que se corrigieron:**

| Desvío en v3 | Qué cambia en v4 | Parte de la definición |
|---|---|---|
| El recorrido de Juliana empezaba por el impuesto y la pensión voluntaria | El aviso parte de sus metas (casa en la costa a los 55, pensión) y hay una pantalla nueva, **J2 · Tu plan antes del impuesto**, con colchón, casa, pensión como ancla y protección. El beneficio tributario aparece como la forma de cerrar la brecha | Plan a partir de las metas |
| El colchón de Laura terminaba en un producto de la entidad | El colchón es un **paso del plan, separado en su cuenta, marcado "no es un producto"**; la alternativa de liquidez queda como opción con sus diferencias. Solo los $780.000 de largo plazo son recomendación profesional | No a partir de los productos que vende |
| El plan de vida solo tenía metas que terminan en productos | Nueva acción sin producto: **confirmar a la hija como beneficiaria** | Plan completo del patrimonio |
| El asesor era solo "Hablar con alguien" | Entra **por regla cuando la decisión lo pide**: el aporte que solo sirve para pensión lo propone un asesor certificado (J4, vista del consultor y motor) | El asesor lo completa cuando la decisión lo pide |
| No se distinguía información de recomendación | Cada pantalla de la app lleva la marca **"Información de tu plan"** o **"Recomendación profesional"** | La IA en el bolsillo, con reglas claras |
| No había un lugar que explicara el servicio | Pantalla nueva **L8 · Cómo funciona tu arquitecto** (reglamento de uso): plan primero, información o recomendación, quién asesora, cuándo entra el asesor, tus permisos | Las tres partes |

**Ajustes regulatorios aplicados** (de `../regulatorio.md`, sección 4): los 7 de prioridad alta y los de prioridad media y baja que tocan pantallas existentes, entre ellos: "con el método de nuestros consultores", autorización del uso del salario de cotización, remitente identificado, "no pagas impuesto" en vez de "no declaras", reglas de la reforma pensional en la proyección, proyección neta de comisiones, condición correcta de retiro de la pensión voluntaria (7%), faltante exacto de $6,65 M, regla mensual por nómina con autorización ante la empresa, plazo de 5 días para las cesantías y el Mecanismo de Protección al Cesante en modo servicio. El motor suma el control de cumplimiento, el horario de contacto y la pregunta "¿quién lo hace?".

**Recorridos v4:** Laura L1 a L8 (aviso → diagnóstico → patrimonio → puntaje → plan de vida → siguiente paso → recomendación → mis reglas → cómo funciona). Juliana J1 a J5 (aviso → su plan → impuesto → cada peso a su meta → confirmar y regla). Vista del consultor, motor por dentro y modo servicio.

**Pendiente:** revisión visual en el lienzo de L4 (cuatro metas), L6 (recomendación con el colchón como paso del plan) y S1 (un mensaje más), que crecieron en contenido.
