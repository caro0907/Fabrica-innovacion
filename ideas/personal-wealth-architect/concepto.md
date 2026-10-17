# El Arquitecto del Siguiente Peso

**Personal Wealth Architect para ahorro e inversión · Documento de concepto v3 · 17 de octubre de 2026**

Idea de trabajo para el rol actual de Carolina en una AFP colombiana. Se construye solo con fuentes públicas y datos simulados. Las cifras de empresas son las que ellas reportan y no fueron verificadas de forma independiente. Referentes completos y matriz en `referentes.md`.

> **Cambios frente a v2:** se rehízo desde la visión de Carolina (plan vivo, mandatos, dos caras, plan primero) y con 27 referentes. Aparecen tres diferenciales que v2 no tenía: el **ingreso conocido**, el **calendario del dinero colombiano** y los **mandatos sobre ese calendario**. Se corrigió además un supuesto débil: el beneficio tributario **no** es un gancho para el ingreso medio (ver sección 3).

---

## 1. La tesis en una página

**El problema real no es invertir: es decidir qué hacer con el siguiente peso.** Y en Colombia, el siguiente peso de un asalariado llega en fechas conocidas: la prima de junio, la de diciembre, los intereses de cesantías en enero y la consignación de cesantías en febrero. Hoy ese dinero llega, se diluye en la cuenta y nadie le propone un destino en el momento exacto.

**La oportunidad:** una AFP sabe algo que ningún neobanco sabe: el ingreso de cotización y el empleador de su afiliado. Puede anticipar cuánto llega y cuándo, proponer un plan antes de que el dinero se diluya y ejecutarlo con una regla que el afiliado deja una sola vez.

**El concepto:** un arquitecto de ahorro e inversión, digital y humano, que:
1. ve el patrimonio del afiliado y su capacidad real de ahorro;
2. diseña con él un plan por metas, con números;
3. lo asesora de forma completa y transparente cuando hay que decidir;
4. ejecuta en un toque y, si el afiliado quiere, cumple reglas sobre su calendario del dinero;
5. le pasa el mismo plan a un asesor humano cuando la decisión lo pide.

**Principio rector: el plan primero, el producto después.** El arquitecto recomienda lo que le conviene al afiliado aunque no sea un producto de la AFP: armar primero un fondo de emergencia, pagar una deuda cara o no invertir todavía. Por eso el afiliado confía, vuelve y delega.

**La frase que es el producto (usuario ficticio):**
> "Laura, si separas $200.000 al mes y el 30% de cada prima, en 20 años habrás puesto $79 millones y podrías tener entre $108 y $167 millones en pesos de hoy, según cómo inviertas. ¿Quieres que lo haga por ti cada vez que llegue la prima?"

*Cálculo ilustrativo: rentabilidades reales supuestas de 3% a 7% anual, aportes mensuales más dos aportes de $780.000 al año (30% de una prima de $2.600.000). No es una promesa de rentabilidad.*

---

## 2. Qué es y qué no es

### Rasgos
| Rasgo | Qué significa | Referente que lo valida |
|---|---|---|
| **1. Conoce tu flujo de dinero** | Parte del ingreso y de los momentos en que llega dinero extra, no de un cuestionario. | nuFormer de Nubank y PRAGMA de Revolut: la "película" del cliente predice mejor que la foto |
| **2. Parte de tus metas** | Primero la meta (fondo de emergencia, viaje, vivienda, tranquilidad); los productos llegan después y solo si la resuelven. | DBS NAV Planner, Wealthsimple + Conquest |
| **3. Asesora de verdad, y lo dice** | Recomendación profesional completa, con idoneidad, explicación, costo y conflicto de interés visibles. | Origin (asesor con IA regulado por la SEC), BBVA (comisión explícita) |
| **4. Ejecuta y cumple reglas** | Ejecuta en un toque y cumple mandatos que el afiliado deja una vez, con tope, vigencia y revocación. | AP2 de Google (mandatos firmados), Wealthfront Autopilot, Cleo Autopilot |
| **5. Tiene dos caras** | El afiliado y el asesor ven el mismo plan. El humano entra donde más valor aporta. | Morgan Stanley (Debrief y derivación a asesores) |

### Las promesas al afiliado
1. **Sé cuánto tengo y cuánto puedo ahorrar**, sin llenar formularios.
2. **Sé para qué estoy ahorrando**, con un plan por meta y en números.
3. **Sé qué hacer con mi siguiente peso**, antes de que se me vaya.
4. **Lo hago en un toque, o lo dejo andando solo**, y lo puedo deshacer cuando quiera.
5. **Sé quién me asesora, cuánto cuesta y por qué me lo recomienda.**

### El cambio
| Hasta hoy | Con el Arquitecto del Siguiente Peso |
|---|---|
| La prima llega, se gasta y en marzo nadie sabe en qué. | Dos semanas antes de la prima, el afiliado ya sabe cuánto llega y a qué meta va; si dejó una regla, se cumple sola. |
| La asesoría de inversión es para clientes de alto patrimonio o pasa por un asesor con agenda. | Asesoría profesional completa, disponible todos los días en WhatsApp y la app. |
| El afiliado ve 50 o más alternativas y no sabe cuál le sirve. | El afiliado ve una recomendación, por qué, cuánto cuesta y qué otras opciones hay. |
| "Conservador" suena a "seguro". | El riesgo se explica en pesos: cuánto podría bajar en un mal año. |

---

## 3. Por qué ahora y por qué nosotros

### El calendario del dinero colombiano (verificado)
| Momento | Fecha | Qué llega | Fuente |
|---|---|---|---|
| Intereses de cesantías | Hasta el 31 de enero | Pago directo al trabajador | [Valora Analitik, 9-dic-2025](https://www.valoraanalitik.com/hasta-cuando-hay-plazo-para-consignar-las-cesantias-en-colombia/) |
| Consignación de cesantías | Hasta el 14 de febrero | Al fondo de cesantías | Misma fuente |
| Prima de mitad de año | Hasta el 30 de junio | Unos 15 días de salario | [Blu Radio](https://www.bluradio.com/economia/finanzas-personales/hasta-cuando-hay-plazo-pagar-prima-junio-colombia-2023) |
| Prima de fin de año | Diciembre (la ley fija el 20 de diciembre; *a verificar con la norma*) | Unos 15 días de salario | Misma fuente |
| Cierre del año gravable | 31 de diciembre | Último día para aportes con efecto tributario del año | Estatuto Tributario, art. 126-1 |

**El hallazgo:** en las fuentes revisadas, ningún actor del mercado colombiano usa este calendario para proponer un destino al dinero antes de que llegue. Nu y Mercado Pago compiten por el saldo una vez está en la cuenta; las AFP digitalizaron los trámites. *Supuesto: no se encontró evidencia pública de que alguien lo haga; no es concluyente.*

### Lo que la AFP sabe y nadie más sabe
- **Ingreso de cotización y empleador**, mes a mes: permite estimar la capacidad de ahorro y el valor de la prima sin preguntar.
- **La historia laboral completa**, desde el primer empleo.
- **Los momentos de vida** que se leen en esa historia: cambio de empleo, aumento, licencia, retiro de cesantías.

*En el MVP todo esto se simula. En producción depende de las reglas de uso de datos de la entidad y del consentimiento del afiliado (Ley 1581 de 2012).*

### Una corrección importante: el beneficio tributario no es el gancho del ingreso medio
Los aportes voluntarios a pensiones y a cuentas AFC son renta exenta hasta el 30% del ingreso y 3.800 UVT, con permanencia de 10 años salvo compra de vivienda o pensión. Pero entran en el límite general de la cédula general: **40% del ingreso neto y máximo 1.340 UVT ($70,2 millones en 2026)**, compartido con otras rentas exentas. [Gerencie](https://www.gerencie.com/guia-renta/conceptos/renta-exenta-en-aportes-a-fondos-voluntarios-de-pension) · [INCP: UVT 2026 = $52.374](https://incp.org.co/agendatributariaincp/noticias/2025/12/dian-fijo-en-52-374-en-valor-de-la-uvt-para-el-ano-gravable-2026/)

La tarifa de renta para personas empieza a cobrar por encima de 1.090 UVT de renta líquida gravable ($57,1 millones en 2026). *Cálculo simplificado, a validar con un experto tributario:* un asalariado de ingreso medio, después de aportes obligatorios y de la renta exenta del 25%, muchas veces queda por debajo de ese umbral. **Para él, el ahorro tributario es cero.** El beneficio solo pesa desde ingresos medio-altos.

**Consecuencia para el diseño:** el arquitecto muestra el beneficio tributario solo a quien de verdad lo tiene, y con su cifra. Al resto se le habla de metas, disciplina automática y rendimiento explicado. Prometer un beneficio que no existe destruiría la confianza.

### La alerta competitiva
- **Nubank** tiene más de 5 millones de clientes en Colombia y US$3.300 millones en depósitos colombianos (junio de 2026). Está probando nuFormer en sus tarjetas colombianas y lanzó Nu Smart Invest en Brasil el 15 de octubre de 2026. Es el competidor más probable para un diagnóstico de inversión en Colombia en los próximos 12 meses.
- **Mercado Pago** creció 77% en activos administrados en un año, hasta casi US$20.000 millones en LatAm, con rendimiento visible como gancho.
- **BBVA** ya tiene el asesor virtual en México y anunció un asistente de IA conversacional en España.

### La oportunidad
Ninguno combina las cinco piezas. El neobanco tiene la app y el saldo, pero no conoce el ingreso ni el calendario; el banco tiene la asesoría, pero cara y por agenda; los robo-advisors tienen la automatización, pero no la relación ni el contexto colombiano. **La AFP tiene el ingreso, el calendario y la confianza de largo plazo; le falta la experiencia.** Eso es lo que construye este concepto.

### Una lección de Chile: "conservador" no es "sin riesgo"
Entre enero y septiembre de 2026, el Fondo E (el más conservador del sistema chileno) cayó en promedio 10,39% real, y las siete AFP perdieron casi lo mismo. [El Clarín de Chile, 16-oct-2026](https://www.elclarin.cl/2026/10/16/efecto-manada-afp-perdidas-fondo-e-2026/). **Implicación:** el arquitecto no puede usar etiquetas de riesgo como explicación. Debe mostrar el riesgo en pesos ("en un mal año esto podría bajar $X") y diversificar con el horizonte de la meta.

---

## 4. Cómo funciona

### Las capacidades del arquitecto
| Capacidad | Qué incluye | Qué sabemos hoy (en el MVP, simulado) | Cómo lo vamos a conocer en producción |
|---|---|---|---|
| **Flujo de dinero** | Ingreso, prima, cesantías, intereses, capacidad de ahorro | Ingreso de cotización y empleador | Datos propios de la AFP, con consentimiento |
| **Patrimonio de ahorro e inversión** | Ahorro voluntario, fondos, CDT, cuentas en otras entidades | Productos en la AFP | Lo que el afiliado declara en la conversación; extractos que comparte; finanzas abiertas cuando estén disponibles (Decreto 0368 de 2026) |
| **Metas** | Fondo de emergencia, metas de mediano plazo, largo plazo | Nada | Conversación: "¿para qué estás ahorrando?" |
| **Perfil e idoneidad** | Riesgo, horizonte, conocimiento, situación | Nada | Perfil conversacional de 5 a 7 preguntas, actualizado con cada evento |
| **Deudas** | Deudas caras que conviene pagar antes de invertir | Nada | Declarado por el afiliado; finanzas abiertas a futuro |
| **Situación tributaria** | Si el beneficio tributario aplica y cuánto vale | Nada | Declarado; certificado de ingresos que el afiliado comparte |

### Los niveles de capacidad
| Nivel | Qué hace | Ejemplo |
|---|---|---|
| **1. Muestra** | Balance, puntaje y metas | "Tu ahorro cubre 1,2 meses de gastos; la meta sana son 3." |
| **2. Recomienda** | Asesoría profesional con idoneidad, explicación, costo y alternativas | "Te recomiendo X, por esto, cuesta Y al año, y estas son tus otras opciones." |
| **3. Ejecuta** | Aporte en un toque, con confirmación y biometría | "Confirma con tu huella y lo aporto ahora." |
| **4. Cumple mandatos** | Reglas sobre el calendario del dinero, con tope, vigencia, aviso y revocación | "Cada prima, aporta el 30% a tu meta de largo plazo, con tope de $1.000.000." |
| **5. Escala al humano** | Un asesor con el mismo plan y la conversación a la vista | "Quiero hablar con alguien." |

### Los mandatos: delegar es seguro porque deshacer es fácil
Cada mandato tiene seis campos: **disparador** (llega la prima), **acción** (aportar el 30%), **destino** (meta de largo plazo), **tope** ($1.000.000), **vigencia** (12 meses) y **aviso** (24 horas antes, con opción de saltar esa vez). El afiliado los ve, pausa y cancela en "Mis reglas".

Se inspira en tres referentes:
- **AP2 de Google**, que distingue un mandato de intención (las reglas que el usuario fija de antemano) de la transacción final, firmados de forma verificable.
- **Wealthfront Autopilot**, que mueve el excedente sobre un umbral y deja cancelar dentro de 24 horas.
- **Cleo Autopilot**, que ejecuta solo decisiones dentro de un plan ya aprobado.

### El puntaje: un número que termina en una acción
Puntaje de 0 a 1.000, construido sobre 5 pilares adaptados al ahorro e inversión de un asalariado colombiano. Cada pilar termina en una acción posible, al estilo WHOOP: "esto es lo que más mueve tu puntaje".

| Pilar | Pregunta que responde |
|---|---|
| **Colchón** | ¿Tengo un fondo de emergencia de al menos 3 meses? |
| **Rumbo** | ¿Mi ahorro tiene metas y voy al ritmo? |
| **Riesgo a la medida** | ¿Lo que tengo coincide con el horizonte de cada meta? (explicado en pesos) |
| **Costo y eficiencia** | ¿Cuánto pago en comisiones y aprovecho los beneficios que sí me aplican? |
| **Constancia** | ¿Aprovecho mis momentos de dinero extra o se me diluyen? |

### El motor: la IA conversa, el motor calcula, el control revisa
Siguiendo el modelo de Origin:
- Un **motor determinista** hace proyecciones, puntaje y elegibilidad, con reglas explícitas y auditables.
- La **IA generativa** conversa, explica y captura metas y datos declarados.
- Un **control de cumplimiento** revisa cada recomendación antes de mostrarla: idoneidad, conflicto declarado, costo visible, lenguaje no engañoso.

---

## 5. Cómo lo vive un afiliado (journey ilustrativo)

**Laura, 36 años, contadora en Medellín, salario de $5.200.000. Tiene $3.000.000 en una cuenta de Nu y nunca ha invertido. (Usuaria ficticia.)**

| # | Momento | Qué pasa | Nivel |
|---|---|---|---|
| 1 | **Mediados de junio, dos semanas antes de la prima** | Le llega un WhatsApp: *"Laura, a finales de junio te llega la prima, unos $2.600.000. ¿Quieres que te ayude a que no se te vaya sin darte cuenta? Me toma 2 minutos."* | Muestra |
| 2 | **Ve su foto** | *"Con lo que me contaste, tu colchón cubre 1,2 meses de gastos; lo sano son 3. Tu puntaje es 520. Lo que más lo mueve: armar el colchón y darle un rumbo a la prima."* | Muestra |
| 3 | **Define una meta** | *"Quiero tener tranquilidad y en 10 años algo para invertir en mi casa."* El arquitecto arma dos metas: colchón (corto plazo, liquidez alta) y patrimonio (largo plazo). | Muestra |
| 4 | **Recibe asesoría** | Responde 6 preguntas de perfil. *"Te recomiendo poner $1.800.000 de la prima en tu colchón, en una alternativa de liquidez diaria, y $780.000 en tu meta de largo plazo, en un portafolio moderado. En un mal año, este último podría bajar unos $90.000. Cuesta X al año. Te lo recomiendo porque…"* Tarjeta de transparencia: quién asesora, que la asesoría no es independiente, costo y alternativas. | Recomienda |
| 5 | **Ejecuta y deja una regla** | Confirma con su huella el día que llega la prima. Luego: *"¿Quieres que en diciembre lo haga igual, con aviso un día antes?"* Laura deja el mandato con tope de $1.000.000. | Ejecuta · Cumple mandatos |
| 6 | **Pide un humano** | En diciembre escribe: *"¿y si mejor pago la tarjeta?"* El arquitecto le muestra el costo de la deuda frente a lo que ganaría invirtiendo y le ofrece un asesor, que la atiende con el mismo plan a la vista. | Escala al humano |

---

## 6. Las piezas y lo que falta (lectura honesta)

| Pieza | Existe hoy en el mercado o es público | Habría que construir | Depende de terceros o de regulación |
|---|---|---|---|
| Diagnóstico con puntaje | Patrón probado (Nu, DBS) | Pilares adaptados al asalariado colombiano | No |
| Asesoría completa automatizada | Patrón probado afuera (Origin); el Decreto 661 de 2018 permite herramientas tecnológicas | Motor, idoneidad, control de cumplimiento | **Sí:** viabilidad con el AMV y la SFC |
| Calendario del dinero | Fechas legales públicas | Motor de eventos sobre ingreso y empleador | Uso de datos internos con consentimiento |
| Mandatos | Patrón probado (AP2, Wealthfront, Cleo) | Modelo de mandato, "Mis reglas", ejecución | Integración con medios de pago |
| Patrimonio externo | Finanzas abiertas obligatorias desde abril de 2026 | Captura por conversación y documentos | **Sí:** cronograma de estándares de la SFC |
| Dos caras | Patrón probado (Morgan Stanley) | Vista del asesor con el mismo plan | No |

---

## 7. Hipótesis, pruebas y umbrales

| # | Hipótesis | Cómo se prueba | Umbral que la confirma |
|---|---|---|---|
| H1 | **El momento importa:** proponer un destino antes de la prima convierte más que hacerlo después. | Prototipo con dos versiones del mensaje (antes y después de la prima) con 10 usuarios | Intención de ejecutar al menos 30% mayor en la versión "antes" |
| H2 | **Delegar:** el afiliado acepta dejar un mandato sobre la prima si tiene tope, aviso y revocación. | Prueba de usuario | Al menos 3 de 5 activan el mandato en el prototipo |
| H3 | **Asesoría sin humano:** el afiliado ejecuta una recomendación automatizada sin hablar con nadie. | Prueba de usuario | Al menos 3 de 5 ejecutan; ninguno pide humano por desconfianza |
| H4 | **Transparencia:** mostrar costo y conflicto de interés aumenta la confianza. | A/B en el prototipo, con y sin tarjeta | Confianza igual o mayor con la tarjeta (escala de 1 a 5) |
| H5 | **Permiso de marca:** el afiliado le confía su ahorro de mediano plazo a su AFP, no solo su pensión. | Entrevistas antes del prototipo | Al menos 3 de 5 lo consideran sin objeción de fondo |
| H6 | **Plan primero:** recomendar el colchón antes que la inversión aumenta la confianza, aunque reduzca la venta inmediata. | Prueba de usuario | Al menos 4 de 5 lo valoran explícitamente |

---

## 8. Ruta y puertas de decisión

| Horizonte | Qué incluye | Puerta para avanzar |
|---|---|---|
| **H0 · Prototipo (semanas 1 a 4)** | Web y WhatsApp simulados: journey de Laura completo con datos ficticios | H1, H2, H3 y H5 cumplen umbral con 5 a 10 usuarios |
| **H1 · Piloto de orientación (meses 2 a 4)** | Calendario del dinero y diagnóstico con datos reales de un grupo pequeño, sin ejecución | Intención de ahorro frente a grupo de control; cero incidentes de datos |
| **H2 · Piloto de asesoría y ejecución (meses 4 a 8)** | Asesoría completa automatizada y ejecución, sujeta a la validación con el AMV y la SFC | Aporte nuevo por usuario frente a grupo de control; quejas por asesoría en cero |
| **H3 · Mandatos y escala (meses 8 a 18)** | Mandatos sobre la prima y las cesantías, vista del asesor, patrimonio externo vía finanzas abiertas | Mandatos activos y tasa de revocación menor al 15%; activos administrados por usuario |

### Pilotos y OKR
| Piloto | Hipótesis | OKR |
|---|---|---|
| P1 · Prima con destino | H1 y H2 | 15% de los contactados ejecuta antes de la prima; 5% deja mandato |
| P2 · Asesoría en el chat | H3 y H4 | 20% de quienes reciben asesoría ejecuta en 7 días |
| P3 · Colchón primero | H6 | NPS de la recomendación de 60 o más |

*Los OKR son metas iniciales para discutir, no benchmarks verificados.*

---

## 9. Control crítico

| # | Por qué fallaría | Mitigación |
|---|---|---|
| 1 | **Nubank llega primero** con Smart Invest a Colombia, con app y saldo ya ganados. | Competir donde Nu no puede: ingreso conocido, calendario del dinero y mandatos antes de que el dinero llegue a la cuenta. |
| 2 | **El AMV o la SFC no habilitan la asesoría completa automatizada**, o tardan. | Diseñar la variante asistida desde el inicio: el motor prepara y un asesor certificado firma en un clic. |
| 3 | **El uso del ingreso de cotización** para recomendar no está permitido o incomoda al afiliado. | Consentimiento explícito y revocable, propósito claro, y la opción de declarar en vez de inferir. |
| 4 | **La recomendación se vuelve venta disfrazada** y la transparencia pierde credibilidad. | El principio rector con reglas: si hay deuda cara o no hay colchón, el arquitecto no recomienda invertir. Medir y publicar internamente ese porcentaje. |
| 5 | **Exceso de alcance**: cinco niveles diluyen la prueba. | El H0 prueba solo el journey de Laura; cada nivel tiene su puerta. |

**¿Innovación real o copia?** Las piezas existen por separado. La innovación es la combinación: ingreso conocido + calendario del dinero colombiano + mandatos antes de que el dinero llegue + asesoría completa y transparente. En la investigación no apareció nadie que la tenga, ni en Colombia ni afuera.

**¿Alguien puede hacerlo en 12 meses?** Nu puede hacer diagnóstico y rendimiento, pero no conoce el ingreso ni la prima. Un banco con nómina sí podría: es el riesgo a vigilar.

**¿Funciona en Colombia?** La prima y las cesantías son instituciones colombianas: el concepto nace del contexto local, no se importa. La desconfianza digital es alta, y por eso la transparencia y el humano a una frase son condiciones del diseño.

**¿Es lo más rápido para probar la hipótesis?** Sí. Un prototipo del journey de Laura prueba las hipótesis de mayor riesgo en semanas, sin datos reales.

**Veredicto: AVANZAR.**

---

## 10. Glosario
- **AMV:** Autorregulador del Mercado de Valores de Colombia.
- **AP2:** Agent Payments Protocol de Google, estándar para que agentes de IA hagan pagos con mandatos firmados.
- **Idoneidad:** evaluación del perfil del cliente antes de recomendarle un producto.
- **Mandato:** regla que el afiliado delega al arquitecto, con disparador, acción, tope, vigencia, aviso y revocación.
- **Modelo fundacional financiero:** modelo de IA entrenado con secuencias de eventos de clientes (PRAGMA, nuFormer).
- **Plan vivo:** plan que se actualiza con cada evento de la vida y del dinero del afiliado.
- **UVT:** Unidad de Valor Tributario; $52.374 en 2026.
