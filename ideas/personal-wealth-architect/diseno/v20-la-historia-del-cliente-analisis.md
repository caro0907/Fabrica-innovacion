# La conversación arma el plan: análisis del prototipo v20 "La historia del cliente" y ruta para llevarlo a la app con inteligencia real

**Versión 1 · 20 de octubre de 2026 · Análisis para la v2.0 de la app.** El prototipo lo construyó Carolina con su equipo. Es un HTML interactivo de unas 5.700 líneas, sin datos sensibles. El original vive solo en la carpeta de Drive "Fabrica de diseno y desarrollo" con el nombre `Arquitecto_V20_La_Historia.html`: trae la marca de una entidad y no se sube a este repositorio. Aquí se describe con la marca neutralizada ("la administradora").

## 0. Qué se construye y qué es contexto (instrucción de Carolina)
El prototipo tiene tres columnas: **la historia del cliente** (escena narrada y "la visión que se cumple"), **lo que vive el cliente** (el teléfono) y **lo que pasa detrás** (el cerebro digital, los agentes y los servicios).
- **Se desarrolla:** solo la columna del centro, lo que vive el cliente.
- **Es contexto:** la historia, la visión y lo que pasa detrás. Se usan para entender la intención y la lógica del cerebro, no como pantallas.

**El objetivo de Carolina (20 de octubre):** llevar el prototipo a la app real, con inteligencia real (no guion) y bajo la arquitectura actual de la app: *la IA conversa, el motor calcula, el control revisa*.

## 1. La tesis del v20
**El cliente conversa con su arquitecto por voz, video o texto, y su plan en blanco se llena en pantalla mientras habla.** Es la promesa "en tu bolsillo, sin formularios". El MVP v1.1 llega al plan por formularios (D1 a D5) y no tiene ninguna conversación real.

Seis promesas de la visión: en tu bolsillo · cada afiliado · su arquitecto · de patrimonio · digital y humano · en todos sus canales. El ciclo del arquitecto: escucha → entiende → ordena → diseña → simula → recomienda → acompaña → conecta. La gestión patrimonial tiene una base financiera (flujo de caja, presupuesto, ahorro, liquidez y endeudamiento) y cuatro pilares (inversiones, previsional, tributario y sucesoral).

## 2. Lo que vive el cliente, en orden (caso Camilo, recorrido completo de 108 pasos)
| Capítulo | Qué ve el cliente | Qué tiene el MVP v1.1 |
|---|---|---|
| 1 · El contacto | WhatsApp de la cuenta oficial con el motivo real ("tus aportes bajaron, tienes cesantías disponibles") y la opción de conocer a su arquitecto; "Escribe NO si no quieres recibir más mensajes" | El motor decide el aviso proactivo, pero nunca lo envía |
| 2 · Asesoría inicial | Tres permisos (grabar y transcribir, usar sus datos, escribirle por WhatsApp) → "No empiezo de cero" (lo que ya se sabe: edad, oficio, pensión, semanas, cesantías) → conversación de 6 temas (lo que viene, familia, su plata, compromisos, lo que le preocupa, lo que quiere proteger) por voz o texto; el panel "Lo que voy entendiendo de ti" se llena en vivo; los números se escriben → "Esto es lo que entendí de ti" → "Estoy armando tu plan" → plan en imágenes, resumen en audio de 1 minuto y "Activar mi plan" con huella | Formularios D1 a D5 con permisos |
| 3 · Tu plan | **Mi vida:** saludo, botones Hablar / Escribir, "Ahora · Tu decisión de hoy" con camino A (recomendado) y camino B y "¿Por qué te lo propongo?", "Tu patrimonio vivo" (capital humano frente a capital financiero, balance extendido), sueños en carrusel con foto que se colorea según el avance, riesgos por cubrir y círculo familiar. **Mi plan:** pestañas *Mi mes* (cuánto entra y a dónde va), *Mi ruta* (pasos con avance) y *¿Cumplo todo?* (apagar o mover sueños). **Mandato de ahorro "día de pago":** cuando entra un pago mayor a $4,5 M separa $1,9 M (21% del ingreso), tope de $2,3 M al mes, reparto por sueño, "si un mes te entra menos aporto lo mínimo y te aviso", "prima o bono: siempre te pregunto antes", "lo que nunca hago sin ti" | Inicio, plan, patrimonio, pilares, propuesta de la prima y regla "Prima con rumbo" (tope $1 M) |
| 4 · Pruebas del escenario | El cliente pregunta y la decisión de hoy cambia: pagar la tarjeta al 28% con ahorros, o una alternativa cerrada para la casa (llegar en 2032 frente a 2033) | Un escenario malo en el simulador |
| 5 · Tu yo futuro | Hoy, 5 años, 10 años y retiro; "Si sigo igual" frente a "Con mi plan"; "Ponle a prueba a tu yo futuro": pierdo mi ingreso 6 meses, invalidez, el mercado cae 20%, vivo hasta los 95; "Ver todos mis riesgos" | No existe |
| 6 · Los canales | WhatsApp el día de pago, la asesora (Juliana Mejía) recibe la ficha y deja una nota de voz, notificación de la cita, correo con el resumen y "Cómo cambió su vida" (antes y después) | Todo queda en el registro, nada se envía |

**Laboratorios:** motor de sueños (estudios propios o de un hijo, vivienda y uno genérico, con tipo de institución, costo, caminos A/B/C y simulación por semestre), beneficio tributario (aporte a pensión voluntaria o a cuenta para el fomento de la construcción y lo que baja de la renta) y directorio de universidades e inmobiliarias.

**Personas del v20:** Camilo (37, psicólogo independiente, ingreso variable de $6 M a $9 M, hija de 5 años, debe $4,2 M en tarjeta al 28%), Laura (29, ingeniera empleada, $5,5 M, vive sola), Jorge (54, gerente, $14 M, prepensión, esposa Marta), Luis (líder técnico, $20 M, empresa familiar del papá) y un escenario abierto ("Tú", por voz). Historias: "La casa de Laura", "A Luis le cambia la vida" (se casa y nace su hijo) y "Jorge llega al retiro" (renta vitalicia o retiro programado).

## 3. Cómo está hecho el prototipo (lo que hay que volver real)
- **La conversación es un guion.** No hay modelo de lenguaje. El escenario abierto entiende por palabras clave.
- **La voz usa las funciones del navegador:** reconocimiento de voz (`webkitSpeechRecognition`) y síntesis (`speechSynthesis`); la cámara usa `getUserMedia` para el video.
- **Las cifras están en el código del prototipo.** Ninguna sale de un motor auditable.

## 4. Lo que hay que resolver antes de construir (hallazgos del análisis)
1. **Inteligencia real.** Hacen falta un modelo que conduzca la conversación con el método de la asesoría integral y extraiga datos estructurados (familia, ingresos, gastos, deudas, sueños, preocupaciones), y una decisión sobre la voz. Precios verificados antes de decidir (regla 5).
2. **Permisos marcados por defecto.** En el v20, "Autorizo grabar y transcribir" y la lectura de documentos vienen marcados. Deben venir desmarcados (criterios H8, H9 y C10).
3. **El mandato "día de pago" debita una cuenta de ahorros de otro banco.** Choca con el aprendizaje "nunca escribir que la entidad mueve dinero que está en otra cuenta". Lo revisa el experto financiero.
4. **Las cifras del yo futuro, de la decisión de hoy y de los sueños salen del motor** (criterio C9). Ejemplos: $770,7 M a 10 años, pensión de $3,5 M al mes.
5. **Elenco.** En el MVP, Laura tiene una hija y Juliana es una clienta de renta media. En el v20, Laura vive sola y Juliana Mejía es la asesora.
6. **Marca neutralizada en la app**, como en el MVP.
7. **Directorio de universidades e inmobiliarias:** la neutralidad del arquitecto y si son aliados comerciales.
8. **Grabación de voz y video:** consentimiento, retención y si la voz se trata como dato sensible.

## 5. Ruta propuesta (pendiente de aprobación de Carolina)
Sobre la app actual, reutilizando el motor, el catálogo, el registro, los consentimientos y las vistas internas:
- **Ola 1 · v2.0, la conversación arma el plan:** asesoría inicial conversacional real por texto y voz (permisos desmarcados, "No empiezo de cero", seis temas, panel en vivo, "Esto es lo que entendí de ti"); "Mi vida" con la decisión de hoy en dos caminos y "¿Por qué te lo propongo?"; Hablar / Escribir con el arquitecto sobre su plan en cualquier momento. Caso principal: Camilo.
- **Ola 2 · v2.1:** Mi plan (mes, ruta, ¿cumplo todo?), laboratorios de sueños y tributario, mandato del día de pago, yo futuro y sus pruebas.
- **Ola 3 · v2.2:** canales (WhatsApp, correo, notificaciones), ficha y nota de voz de la asesora, video, documentos y círculo familiar.

**Arquitectura de la inteligencia (propuesta):** la IA conduce la conversación y extrae datos con una salida estructurada que se valida en código. El motor recalcula el plan y la decisión con cada dato nuevo. El control revisa todo texto que llega al cliente contra el catálogo y las frases prohibidas. La IA nunca escribe cifras propias ni recomienda productos fuera de la decisión del motor.

**Flujo de la fábrica:** el diseño ya existe, así que no se rediseña. El diseñador lo convierte en la especificación de la v2.0 (pantallas, el dato de cada una, qué calcula el motor y qué dice la IA); luego revisan el experto financiero (hallazgos 2, 3, 7 y 8) y el revisor, aprueba Carolina y construye el desarrollador, con revisor otra vez antes de desplegar.

## 6. Decisiones abiertas para Carolina
1. ¿La Ola 1 es el alcance de la primera versión?
2. ¿Se adopta el elenco del v20 (Camilo como caso principal, Juliana como asesora)?
3. ¿La voz arranca con las funciones del navegador (sin costo) y se evalúa un servicio de voz en tiempo real, con precios verificados, para la Ola 2?
4. ¿Qué modelo conversa? Se decide con precios verificados el día de la decisión.
