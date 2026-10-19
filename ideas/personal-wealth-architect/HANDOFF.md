# Traspaso a producción: el MVP prueba que un arquitecto de patrimonio puede armar el plan primero y recomendar después, con reglas que se cumplen en el código

**Personal Wealth Architect · MVP v1.1 · 19 de octubre de 2026 · Especialista: desarrollador de la fábrica.** Parte del diseño v5.2 aprobado por Carolina (`diseno/README.md`, sección 12), del concepto v5.1 y de `regulatorio.md` v1. Código en `app/`. La v1.1 corrige lo que devolvieron el revisor y el experto financiero el 18 de octubre (`revisiones/2026-10-18-mvp-v1.md`); el detalle está en la sección 9.

> **Estado:** MVP para pruebas con usuarios. Nada está en operación, ninguna persona ni cifra es real y nada mueve dinero. Las cifras ficticias (comisión, caída en un mal año) están marcadas en pantalla.

## 1. Qué hace
Un afiliado ficticio recorre la asesoría integral como en banca privada, y el motor decide qué mostrarle con reglas auditables:

| Momento | Qué vive el afiliado | Qué hace el motor |
|---|---|---|
| Lunes 1 de junio · primera reunión | Decide sus permisos, todos opcionales y desmarcados (usar su salario, con finalidad y derechos; o contar su ingreso; recibir propuestas por mensajería); metas y la más importante; números de sus metas; su vida y su dinero; seis preguntas del perfil, sin respuestas por defecto; "esto entendí de ti" | Guarda cada consentimiento con su texto, el perfil con su fecha y el diagnóstico completo |
| Tu plan, la primera vez | Patrimonio con origen de cada dato, pensión con supuestos, metas con números, salud del plan en 6 pilares y el orden del plan. Primer paso: registrar a su hija en su grupo familiar (ya es su beneficiaria por ley; no es un producto) | Arma el plan con reglas deterministas; sin permiso del salario ni ingreso contado, no estima nada que dependa del ingreso |
| Lunes 15 de junio · la app como hogar del plan | Inicio con patrimonio y salud del plan, nota del arquitecto coherente con la propuesta, revisión de junio, propuesta para la prima (paso del plan separado de la recomendación profesional), aprobación con un paso visible de huella simulada, y después, opcional, la regla "Prima con rumbo" con sus condiciones y la autorización a la vista y desmarcada; Mi plan, simulador de la casa con escenario malo, Patrimonio (con la probable obligación de declarar), Pilares, Tu equipo, Perfil, Cómo funciona, Cómo tratamos tus datos, Pregúntale | Restrictivos primero → elegibilidad por el plan → priorización → freno, grupo de control y horario legal → una decisión con cinco campos |
| Andrés · modo servicio | Pide sus cesantías porque perdió el empleo: plazo legal, Mecanismo de Protección al Cesante, regla pausada, consultora a una frase, nada de venta | El restrictivo "pérdida de empleo" bloquea todo lo comercial |
| Vistas internas | El consultor ve el mismo plan, el brief de enganche y el de profundización; el motor muestra los cinco campos, la cola, la traza capa por capa, los escenarios con su ciclo de vida, el freno y el registro | Todo queda registrado con versiones de motor, supuestos y catálogo |

## 2. Cómo correrlo
**Local:** ver `app/README.md` (`PWA_INTERNO_ABIERTO=1 uvicorn pwa.app:app`, `python -m pytest`: 71 pruebas que pasan).

**Railway (lo conecta Carolina, una vez):**
1. En Railway, *New Project → Deploy from GitHub repo* → `caro0907/Fabrica-innovacion`, rama `main` (después de aprobar el pull request).
2. En el servicio, *Settings → Root Directory*: `ideas/personal-wealth-architect/app`. Railway lee `railway.json` (comando de arranque y chequeo de salud en `/salud`).
3. *Variables*: `PWA_CLAVE_INTERNA` (una clave larga; sin ella las vistas internas quedan cerradas), `PWA_COOKIE_SEGURA=1`, `PWA_DB=/data/pwa.sqlite`. Opcionales: `ANTHROPIC_API_KEY`, `PWA_TOKEN_AGENTES`. Nunca `PWA_INTERNO_ABIERTO` en Railway.
4. Agregar un volumen montado en `/data`, para que el registro sobreviva a los redespliegues.
5. *Settings → Networking → Generate Domain*. Cada cambio aprobado en `main` se despliega solo.

## 3. Arquitectura
```
Afiliado (app, hogar del plan)          Consultor (mismo plan + brief)          Agente externo (solo lectura)
          │                                         │                                      │
          ▼                                         ▼                                      ▼
   Rutas web (FastAPI + plantillas)  ────────  Vistas internas con clave  ────────  GET /api/v1/plan (token + consentimiento)
          │
          ▼
   Motor determinista: plan · perfil · cálculos · escenarios (restrictivos primero) · decisión con cinco campos · mandatos
          │                         │
          ▼                         ▼
   Catálogo de lo que se puede decir (JSON versionado) + control  ◄──  Redactor: plantillas o Claude (solo ordena piezas y escribe puentes sin cifras)
          │
          ▼
   Registro (SQLite): sesiones, interacciones, mandatos, métricas del freno
```
**El flujo de la decisión**, en este orden y en código (`pwa/motor/decision.py`):
1. **Restrictivos primero:** queja abierta, no contacto, pérdida de empleo, coyuntura crítica, evento sensible, deuda cara sin colchón, perfil vencido o inexistente (completo y de menos de 365 días) y señales de no comprender. Si hay uno, nada comercial, sin excepción. Retirar el permiso del salario ya no es un restrictivo general: el plan deja de estimar lo que depende del ingreso y la prima deja de ser elegible.
2. **El plan define lo elegible:** una acción solo entra si cierra una brecha del plan, la persona no la rechazó y, si es un producto, es idóneo: la clase de perfil alcanza el mínimo del portafolio, el horizonte no es "menos de 2 años", el plazo de la meta supera el horizonte mínimo y la caída de un mal año cabe en la pérdida que tolera.
3. **La priorización ordena:** impacto incremental (simulado en el MVP, con las cuatro poblaciones) y valor para el plan de la persona. Los "seguros" no reciben aviso proactivo; los "perdidos" y "no molestar" no se contactan.
4. **Compuertas para iniciar un contacto:** freno de servicio, grupo de control (asignación estable por hash, 10%), horario legal de la Ley 2300 de 2023 con los festivos de 2026 (el 15 de junio es festivo: el aviso esperaría al martes 16 a las 7 a. m.), un contacto por semana contado en el registro y autorización de mensajes, que viene en "no" hasta que la persona la da. El canal dice dónde se muestra; el aviso proactivo va en un campo aparte y en el MVP nunca se envía.
5. **Salida:** canal, prioridad, vigencia, tono y recomendación, más "¿quién lo hace?" (el arquitecto digital o un asesor certificado, según la tabla de `regulatorio.md`, sección 1B).

## 4. Decisiones tomadas
| Decisión | Por qué |
|---|---|
| Python con FastAPI y páginas que genera el servidor, sin framework de interfaz | El stack más simple que cumple; funciona sin JavaScript (el script solo actualiza cifras en vivo); un solo despliegue |
| La salida del motor tiene cinco campos: canal, prioridad, vigencia, tono y recomendación | Es el mismo contrato de interfaz que usa un motor de recomendación por afiliado en producción: el MVP se puede conectar después, no es un prototipo aparte |
| El plan define lo elegible y la priorización solo ordena | Fidelidad a la definición: el plan parte de las metas, no de los productos |
| Catálogo como datos versionados (`pwa/catalogo/catalogo_v1.json`, de `regulatorio.md` sección 5) y control en código | Cada beneficio arrastra sus condiciones y advertencias; un beneficio con condición no sale si la persona no la cumple; las frases prohibidas se rechazan |
| La IA solo ordena piezas y escribe puentes cortos sin cifras; si desobedece, se usa la plantilla | "La IA conversa, el motor calcula, el control revisa". Probado con un modelo simulado que desobedece (`tests/test_redactor.py`) |
| Claude Haiku 5.5 para la redacción, apagado por defecto | El trabajo del modelo es pequeño (ordenar y unir piezas); es el más barato vigente |
| Pensión: 11,5% del salario a la cuenta individual, 4% real neta, 13 mesadas durante 30 años, mismo método para todos | Criterio C9: cada estimado se recalcula en código con los supuestos que la pantalla muestra |
| Mandatos no discrecionales con control "te propongo y tú confirmas" | La persona fija el reparto y el tope; el sistema solo dispara (riesgo R13). Se ofrecen después de aprobar, como en el diseño, con la autorización desmarcada y a la vista; tope de $1.000.000 a inversión por prima (lo que pase de ahí se queda en su cuenta); vigencia de un año; las pausas automáticas corren en cada pantalla. Ningún mandato mueve dinero en el MVP |
| La recomendación es un portafolio del fondo de pensiones voluntarias de la administradora, no un fondo de inversión colectiva | Lectura del experto financiero: una administradora de fondos de pensiones y cesantías no administra fondos de inversión colectiva. A validar con jurídico (`regulatorio.md`, sección 9, pregunta 12) |
| Sin permiso del salario, el plan usa el ingreso que la persona contó o no estima nada que dependa del ingreso | Criterio C10: retirar un permiso cambia de verdad lo que se muestra. El puntaje se calcula con los pilares que sí se pueden estimar y lo dice |
| SQLite con volumen en Railway | Suficiente para pruebas con 10 personas; el esquema migra a PostgreSQL sin cambiar el motor |
| El consultor con nombre queda configurable por segmento (`CONSULTOR_CON_NOMBRE_POR_SEGMENTO` en `pwa/motor/datos.py`) | Pendiente 2 de Carolina; hoy está activo en ambos segmentos |

### Cifras que cambiaron frente al prototipo v5.2, y por qué
El prototipo mostraba cifras ilustrativas; el MVP las calcula. Ninguna cambia el recorrido aprobado, pero Carolina debe verlas antes de probar con usuarios.

| Dato de Laura | Prototipo v5.2 | MVP | Por qué |
|---|---|---|---|
| Pensión estimada | $2,3 M | **$1,83 M** (brecha $1,17 M) | El MVP lleva a la cuenta individual solo el 11,5% de la cotización, no el 16%. Con el 16% daría unos $2,2 M. Lo debe validar actuaría (pregunta 6 de `regulatorio.md`) |
| Salud del plan | 520 | **585** el 1 de junio; **668** tras registrar a su hija; **693** tras aprobar la propuesta; **735** si deja la regla | Las reglas de cada pilar están en código (`plan.py`). En la v1.1 la regla ya no mueve la suficiencia ni el riesgo: el riesgo sube en proporción a lo que de verdad tiene un vehículo, y la constancia premia la regla y lo dice. La comisión de la pensión obligatoria ya no penaliza (sale de la cotización, no del saldo) |
| Lo que más mueve su puntaje | El colchón | **Protección** (su hija no era beneficiaria) | Coincide con el primer paso del plan |
| Para llegar a la casa a tiempo | Unos $100 mil más al mes | **Unos $90 mil** | Calculado con el simulador y redondeado hacia arriba |
| Caída en un mal año, comisión, prima, reparto 70/30, colchón | $94.000; 1,2%; $2,6 M; $1.820.000 y $780.000; 1,2 meses | Iguales | — |

## 5. Costos de servicios (precios verificados de nuevo el 19 de octubre de 2026 en las páginas oficiales)
| Servicio | Precio publicado | Para este MVP |
|---|---|---|
| Railway, plan Hobby | USD 5 al mes, con USD 5 de uso incluido; la suscripción se paga aunque no se use. Uso: USD 10 por GB de memoria al mes, USD 20 por vCPU al mes, USD 0,15 por GB de volumen al mes, USD 0,05 por GB de salida ([Railway, Pricing Plans](https://docs.railway.com/pricing/plans), consultada el 19 de octubre de 2026) | *Estimado propio:* la app usa poca CPU y unos 60 MB de memoria en reposo (medido en local); debería caber en el uso incluido (unos USD 5 al mes en total). Verificar en la factura del primer mes |
| Claude Haiku 5.5 (opcional) | USD 0,10 por millón de tokens de entrada y USD 0,50 de salida en prompts de hasta 100.000 tokens; por encima, USD 0,50 y USD 2,50 ([Anthropic, Pricing](https://platform.claude.com/docs/en/about-claude/pricing), consultada el 19 de octubre de 2026) | *Estimado propio:* unos 700 tokens de entrada y 150 de salida por nota, es decir unos USD 0,00015 por nota. Con 10 personas de prueba, menos de un centavo de dólar |
| GitHub | Gratis (repositorio privado) | — |

## 6. Control de riesgo: cubierto / pendiente
| Tema | Cubierto | Pendiente para producción |
|---|---|---|
| Datos reales | Solo datos ficticios en código, semillas y registro; ningún nombre interno ni cifra de la entidad | — |
| Secretos | Todo por variables de entorno; `.env` y la base fuera de Git; ninguna llave en el repositorio | Rotación de claves y un gestor de secretos |
| Dependencias | Seis dependencias conocidas y mantenidas, con versión fija | Escaneo automático de vulnerabilidades |
| Autenticación | Vistas internas cerradas por defecto, con clave y una cookie que guarda una ficha derivada, no la clave; el freno solo se cambia con acceso interno; consulta de agentes con token y consentimiento específico; cabeceras de seguridad (CSP, no marcos) | Identidad reforzada real del afiliado (la huella está simulada, ahora como paso visible), roles por equipo y registro de accesos |
| Habeas Data (Ley 1581 de 2012) | Autorización opcional, desmarcada, con responsable, finalidad y derechos, y enlace a "Cómo tratamos tus datos" (borrador); de la hija, solo la edad; la huella es del celular y la entidad no recibe el dato biométrico; permisos visibles, con su texto y su efecto, y revocables en "Mis reglas y permisos"; cada consentimiento queda registrado con el texto mostrado; **sin el permiso, ninguna pantalla muestra cifras derivadas del salario** (probado) | Política de tratamiento aprobada por jurídico; retención y borrado; datos de menores con su régimen especial |
| Contacto (Ley 2300 de 2023) | Horario, un contacto por semana y autorización de mensajes como compuertas del motor | Plantillas aprobadas del canal de mensajería; validar con jurídico si el horario aplica a todo contacto comercial |
| Accesibilidad | Contraste del sistema de diseño, etiquetas en todos los campos, navegación con teclado y foco visible, toques de 44 px o más (verificado en navegador con `scripts/revisar_pantallas.py`: 25 pantallas, 0 problemas) | Prueba con lector de pantalla |

## 7. Requisitos no funcionales
- **Auditabilidad:** cada interacción guarda acción, escenario, ángulo, canal, fecha, piezas del catálogo, texto mostrado, versión del motor, de los supuestos y del catálogo, perfil usado, respuesta, resultado y grupo.
- **Determinismo:** los mismos datos dan la misma decisión; la IA está apagada por defecto y, encendida, no puede cambiar cifras ni piezas.
- **Disponibilidad del MVP:** una instancia; aceptable para pruebas.
- **Desempeño:** cada pantalla se calcula en milisegundos.
- **Responsive:** diseñada a 390 px; en escritorio se ve como un teléfono centrado.

## 8. Lo que falta para producción
1. **Datos reales con consentimiento:** conectar el plan a los datos de la entidad y a los simuladores oficiales de pensión obligatoria y voluntaria, en lugar del método simplificado.
2. **Impacto incremental real:** reemplazar `IMPACTO_SIMULADO` por un modelo entrenado contra grupos de control, y medir el efecto en depósito neto, conservación, recaudo y satisfacción.
3. **Aprobaciones:** cumplimiento aprueba el catálogo y los supuestos (rentabilidad, caída en un mal año, comisiones); jurídico, el texto de consentimiento de los mandatos; las 6 preguntas de prioridad alta de `regulatorio.md`, sección 9.
4. **Ejecución:** transferencias reales con confirmación en el momento, débito o descuento de nómina autorizado; las credenciales nunca pasan por el agente.
5. **Juliana (renta media)** y su cálculo tributario; vistas de los equipos comercial, remoto y de servicio; "Mis documentos" (pendiente 4 del diseñador).
6. **Canal de mensajería** para el aviso anticipado, con plantillas aprobadas.
7. **PostgreSQL**, copias de respaldo y monitoreo.
8. **Pausas automáticas que faltan:** cambio de la ley que afecte el beneficio y dos ejecuciones fallidas seguidas (no se muestran al afiliado hasta que corran).
9. **Envío real del aviso** por mensajería y de la recomendación y los consentimientos por correo y en "Mis documentos"; hoy solo quedan en el registro.

## 9. Cambios de la v1.1 (19 de octubre de 2026) frente a la revisión del 18 de octubre
**Los 4 hallazgos que bloqueaban (revisor) y los 10 de prioridad alta (experto financiero) están corregidos, cada uno con su prueba.**

| Hallazgo | Qué cambió | Prueba |
|---|---|---|
| Revisor 1 y H3 · contradicción del colchón | P3 nueva ("la mayor parte de lo que te llegue va primero a tu colchón") y P9 en el inicio cuando la decisión lleva a invertir para la casa. Control nuevo: una pieza marcada "contradice la recomendación" (P4) no sale en una pantalla con recomendación de inversión | `test_la_nota_del_inicio_no_contradice_la_recomendacion`, `test_una_pieza_que_dice_no_invertir_no_sale_con_una_recomendacion` |
| Revisor 2, H5, H6 y H17 · permiso del salario | Bienvenida sin casilla obligatoria, con responsable, finalidad, derechos y política; si no autoriza, puede contar su ingreso ("nos contaste"). Sin ninguno, el plan no estima pensión, prima ni ritmo de la casa, y lo dice. No es un restrictivo general | `test_sin_permiso_del_salario_ninguna_pantalla_muestra_cifras_derivadas` (10 pantallas, 9 cifras), `test_retirar_el_permiso_despues_cambia_lo_que_se_muestra` |
| Revisor 3 y H7 · mandato | Paso posterior a aprobar, con condiciones y autorización visibles antes, casilla desmarcada, tope de $1.000.000 que limita de verdad, vigencia y aviso en lenguaje natural, texto del experto en primera persona, huella como paso visible | `test_la_regla_se_ofrece_despues_desmarcada_y_con_sus_condiciones`, `test_el_tope_de_la_regla_limita_de_verdad` |
| Revisor 4 · puntaje | Crear la regla no mueve suficiencia ni riesgo; el riesgo sube en proporción a lo invertido; la constancia premia la regla y lo dice | `test_crear_la_regla_no_mueve_suficiencia_ni_riesgo`, `test_riesgo_sube_en_proporcion_a_lo_que_tiene_vehiculo` |
| H1 · idoneidad | Perfil mínimo, horizonte, plazo de la meta y caída; un conservador no recibe el portafolio | `test_idoneidad_completa`, `test_perfil_conservador_no_recibe_el_portafolio` |
| H2 · vehículo | Opción A: portafolio moderado del fondo de pensiones voluntarias, con condición de retiro (C5) | `test_recorrido_completo_de_laura` |
| H4 · beneficiarios | "Tu hija ya es tu beneficiaria por ley… registrarla en tu grupo familiar agiliza el trámite"; P6 cambia también en `regulatorio.md` | `test_beneficiarios_por_ley` |
| H8, H9 y H10 | Mensajes comerciales en "no" y preguntados; perfil sin respuestas por defecto y botón que se activa con las seis; vigencia del perfil por fecha, pausas que corren en cada pantalla y solo las que funcionan a la vista | `test_mensajes_comerciales_se_preguntan_y_vienen_en_no`, `test_el_perfil_no_llega_contestado`, `test_mandato_se_pausa_si_el_perfil_vence` |
| Prioridad media | H11 registro del diagnóstico y del texto de cada permiso · H12 sin promesas de correo · H13 quién hace la recomendación (A9) · H14 "frases del catálogo, pendientes de aprobación" · H15 patrones prohibidos ampliados y cifras en letras en los puentes · H16 festivos de 2026 y conteo semanal de contactos · H18 sin penalizar la comisión de la obligatoria · H19 escenario malo con la caída de un mal año · H20 probable obligación de declarar (Laura, $100.400 por encima del tope) · H21 constancia de terminación y condición del Mecanismo de Protección al Cesante · H22 sin régimen de transición no hay mesada · H23 supuestos completos de la pensión | Una prueba por hallazgo en `tests/` |
| Prioridad baja y no bloqueantes | H24 sin "al año" repetido · H25 la pensión propuesta y el deslizador arrancan en la misma cifra ($3,0 M) · H26 tono sin "cifras redondas" · H27 y revisor: vistas internas cerradas sin clave y cookie sin la clave · porqué del brief según la acción · canal sin aviso no enviado · fechas en español · huella visible · precios con cita y fecha de consulta | Pruebas de flujo y revisión en navegador (29 pantallas, 0 problemas) |

**Lo que sigue abierto:** vistas de los equipos comercial, remoto y de servicio y "Mis documentos" (pendiente 4, diseñador); textos fijos de plantillas que no salen del catálogo (las pruebas los revisan contra las frases prohibidas, pero no son piezas versionadas); la pregunta 12 a jurídico sobre el vehículo.
