# Métricas de la fábrica: ¿está aprendiendo?

**v1 · 17 de octubre de 2026.** La pregunta que mide si la fábrica sirve: **¿cuántas veces tiene que corregir Carolina un entregable que ya pasó por la fábrica?** Si la fábrica aprende, ese número baja de un proyecto al siguiente, y cada vez más hallazgos los detecta el revisor y no ella.

## Indicadores
| Indicador | Cómo se calcula | Meta |
|---|---|---|
| **Rondas de Carolina por entregable** | Veces que Carolina devolvió observaciones de fondo antes de aprobar | Bajar en cada proyecto; 1 o menos en el tercer proyecto |
| **Detectado por la fábrica vs. por Carolina** | Hallazgos que bloquean encontrados por el revisor o un especialista frente a los que encontró Carolina | Que la fábrica encuentre más de 3 de cada 4 |
| **Criterios nuevos por proyecto** | Criterios agregados a `criterios-de-revision.md` | Alto al principio, decreciente después |
| **Reutilización de activos** | Pantallas o textos que salieron de `empresa/activos/` en lugar de hacerse de cero | Subir en cada proyecto |

## Línea base: Personal Wealth Architect (reconstruida de `aprendizajes.md` y de la sesión del 17 de octubre)
| Entregable | Rondas de Carolina | Lo que detectó Carolina | Lo que detectó la fábrica |
|---|---|---|---|
| Concepto (v1 a v5.1) | 3 | Un mecanismo se volvió el producto; faltaba su trabajo previo y la tesis; faltaban formatos de su método | La revisión con su lista de verificación detectó nombres viejos y formatos faltantes en v5.1 |
| Revisión regulatoria v1 | 0 | — | 3 textos inexactos (retiro de la pensión voluntaria, "no declaras renta", retención por nómina), 27 ajustes y la Circular Externa 14 de 2025 |
| Diseño (v1 a v5) | 4 | v2: volver al concepto integral; v4: se siente como chat, no como asesor; v5: falta el diagnóstico antes del plan (y el recordatorio de la definición) | v4: desvíos de fidelidad (plan de Juliana, colchón, asesor por regla) al revisar contra la definición que ella recordó |
| **Total** | **7 rondas** | **Los desvíos de fondo los detectó ella** | Los errores de detalle y normativos los detectó la fábrica |

## Revisiones del revisor independiente
| Fecha | Entregable | Veredicto | Hallazgos que bloquean | Nota |
|---|---|---|---|---|
| 17 oct 2026 | Prototipo v5 del Personal Wealth Architect (primera reunión y app del arquitecto) | DEVUELVE | 7 (16 que no bloquean) | Primera prueba del revisor. Encontró problemas que Carolina no había señalado: el plan se salta después del diagnóstico y el mecanismo de la prima vuelve al centro; datos del plan que el diagnóstico no pidió; información y recomendación mezcladas en la revisión; la pensión sin supuestos; el beneficio de Juliana sin su condición; el recorrido de Juliana abre pantallas de Laura; el mandato de Juliana sin vigencia ni aviso. Propuso 2 criterios nuevos (E4 y B10) |
| 17 oct 2026 | Prototipo v5.1 (segunda ronda) | DEVUELVE | 2 (15 que no bloquean) | De los 7 anteriores, 5 resueltos y 2 con residuo menor. Nuevos: la pensión de Juliana ($5,6 M) no salía de sus propios supuestos (recalculada: unos $3,0 M), y Laura saltaba entre la primera reunión y la app. Propuso C8 (perfil y producto coherentes) y ampliar E4 a "el mismo momento". Corregido en v5.2 junto con 12 de los 15 que no bloquean; según la skill, no hay tercera ronda: va a Carolina con lo abierto a la vista |
| 17 oct 2026 | Prototipo v5.2 · verificación mecánica | 0 que bloquean | — | La herramienta, ampliada para revisar momentos, encontró un salto que el revisor no vio ("Ver tus 8 dimensiones" en el plan del 1 de junio abría el patrimonio del 15 de junio). Lo mecánico lo hace la herramienta; el juicio, el revisor |
| 18 oct 2026 | Vigía semanal `vigia/2026-10-18.md` | PASA | 0 (5 que no bloquean, aplicados) | Primera revisión de un informe del vigía |
| 18 oct 2026 | Experto financiero v3 y sección 2.3 del vigía (referentes ampliados) | DEVUELVE | 1 (5 que no bloquean) | La revisión ampliada dejaba fuera, sin decirlo, 2 de los 6 grupos de referentes |
| 18 oct 2026 | Experto financiero v3 y sección 2.3 (segunda ronda) | PASA | 0 (3 que no bloquean, aplicados) | — |
| 19 oct 2026 | Radar de fintech de ahorro e inversión v1 y experto financiero v5 | DEVUELVE | 2 (5 que no bloquean) | Revolut sin fuente ni fecha; ronda de Ualá sin fecha. Faltaba el orden de prioridad |
| 19 oct 2026 | Radar de fintech v1.1 (segunda ronda) | PASA | 0 (2 que no bloquean, aplicados) | — |

## Detectado por Carolina después de pasar por el revisor
| Fecha | Entregable | Observación | Criterio agregado |
|---|---|---|---|
| 18 oct 2026 | Prototipo v5.2 | Ninguna: "el prototipo quedó perfecto". Aprobado sin rondas de corrección | — |
| 18 oct 2026 | Vigía semanal | La evaluación debía usar todos los referentes de su investigación previa en Drive, no solo los nombrados en la instrucción | A6 |

## Lectura después del primer proyecto (17 de octubre de 2026)
- **Detectado por la fábrica vs. por Carolina en el diseño:** desde que existe el revisor, 9 hallazgos que bloquean los encontró la fábrica y 0 Carolina (hasta su próxima revisión). Antes del revisor, los 4 desvíos de fondo los había encontrado ella.
- **Cifras:** la segunda ronda encontró una cifra que el diseñador inventó en la corrección (la pensión de Juliana). Por eso los generadores calculan las cifras derivadas y el revisor las recalcula en código.
- **Primer resultado medible (18 de octubre de 2026):** el diseño necesitó 4 rondas de Carolina antes del revisor y 0 después. Es un solo caso; la meta se confirma si se repite en el desarrollo y en el próximo proyecto.
