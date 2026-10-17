# Brief táctico para el diseñador: Personal Wealth Architect

**v5.1 · 17 de octubre de 2026 · Veredicto del estratega: AVANZAR** · Concepto completo en `concepto.md` v5.1, referentes en `referentes.md`, beneficios tributarios en `../../empresa/beneficios-tributarios.md` y método en `../../empresa/forma-de-trabajo.md`.

> **Cambios frente a v4:** puntaje de 6 pilares como primera versión visible; arquitectura en cuatro capas; nivel de control en cada mandato; pantalla de modo servicio para los escenarios restrictivos; reglas de la conversación; estados visibles; hipótesis H11; pilotos en formato "si…, entonces…".

## La tesis y el principio
- **Tesis:** llevar con tecnología la mejor asesoría integral, la que hoy solo reciben los grandes patrimonios, a las rentas medias y masivas.
- **Principio rector:** el plan primero, el producto después. El motor elige solo entre acciones que mejoran una meta del afiliado; el objetivo de negocio prioriza entre ellas.
- **Fórmula:** Relevancia = Entender × Guiar × Resolver × Confiar.

## Arquitectura que el prototipo debe mostrar
| Capa | En el prototipo |
|---|---|
| Lo que vive el afiliado: el Personal Wealth Architect | Sus cinco promesas, en orden: sé dónde estoy, sé a dónde voy, sé qué hacer hoy, lo hago en un toque o lo delego, nunca estoy solo |
| Quién conversa y actúa: el agente | Chat que resuelve primero, recomienda una sola cosa con su porqué, ejecuta y cumple mandatos |
| Dónde lo encuentra: superficies | Chat para conversar y actuar; la app como "hogar del plan" (puntaje, plan, mis reglas); el consultor con el mismo plan |
| Qué lo hace inteligente: el motor | Vista interna "el motor por dentro" con estados (todo es diseño) |

## Usuarios (segmento × arquetipo × momento)
- **Laura, pragmática de renta masiva** ($5,2 millones al mes, 36 años): quiere tranquilidad y una casa. Su momento es la prima de junio.
- **Juliana, inversora de renta media** ($8,5 millones al mes, 41 años): quiere optimizar. Su momento es el cierre del año, con su gancho tributario.
- **Andrés, en pérdida de empleo** (escenario restrictivo): muestra qué hace el arquitecto cuando no debe vender.

## MVP (prototipo v3, datos ficticios)
**Recorrido de Laura (integral, de principio a fin):** aviso de la prima → diagnóstico conversacional → mi patrimonio en 8 dimensiones (la foto) → **mi puntaje de 6 pilares** (colchón, suficiencia, protección, riesgo a la medida, eficiencia, constancia) con la acción que más lo mueve → mi plan de vida con la pensión como ancla → siguiente paso (plan de la prima) → recomendación con transparencia y huella → mis reglas, con nivel de control.

**Recorrido de Juliana:** diciembre de oro, "tu impuesto paga parte de tu ahorro", cada peso a su vehículo, y confirmación con regla mensual que ejecuta dentro del tope y avisa después.

**Modo servicio (Andrés):** pide sus cesantías por desempleo; el agente resuelve, le muestra cuánto le duran, pausa las recomendaciones y la regla de la prima, y deja al consultor a una frase.

**Vistas internas:** el consultor con el mismo plan, y "el motor por dentro" (conocimiento, plan, escenarios con los restrictivos primero, acciones elegibles, priorización con las cuatro poblaciones, activación, medición), con el estado "diseño, nada en operación".

**No incluye:** datos reales, dinero real, integración con sistemas, finanzas abiertas, modelos entrenados (reglas y puntajes simulados y explicados), ingreso para el retiro y productos para la familia (necesidades que piden otro tipo de respuesta; ver concepto, sección 4C).

## Hipótesis del MVP y umbrales
| Hipótesis | Umbral |
|---|---|
| H10 · Ver el patrimonio, el puntaje y el plan aumenta la intención de actuar frente a recibir solo la recomendación | Al menos 20% más |
| H9 · Paridad de calidad: un consultor senior aprobaría el plan y la recomendación | Al menos 80% sin cambios de fondo |
| H11 · Recomendar después de resolver lo que pidió no baja la satisfacción | Satisfacción igual o mayor; 30% abre la recomendación |
| H1 · Proponer antes de la prima convierte más que después | Al menos 30% más |
| H2 · El afiliado deja un mandato si ve tope, aviso, nivel de control y cómo deshacerlo | Al menos 3 de 5 |
| H7 · El ahorro de impuesto en pesos y el punto óptimo mueven a aportar (renta media) | Al menos 3 de 5 |

## Mecánicas que el diseño debe aterrizar
1. **Diagnóstico conversacional antes que formularios** — método del mejor consultor; Wealthsimple con Conquest.
2. **Puntaje por pilares que termina en una acción** — Nu Smart Invest y WHOOP, con la pensión adentro.
3. **Plan de vida con brechas y la pensión como ancla** — el diferencial de una administradora de pensiones.
4. **Siguiente paso explicado, con riesgo en pesos, costo y transparencia** — Origin, BBVA, Nu Smart Invest.
5. **Delegación con control visible** — AP2, Wealthfront Autopilot, Cleo; tres niveles: informar, proponer y confirmar, ejecutar dentro de límites.
6. **Motor visible para negocio**, con restrictivos primero y estados — trabajo previo de Carolina.

## Reglas que el diseño no rompe
Lo que pidió va primero · una recomendación por conversación, con su porqué · un "no" se respeta · el humano a una frase · nada se mueve sin aviso · nombres de productos completos, sin siglas · datos marcados como ficticios y cálculos como estimados.
