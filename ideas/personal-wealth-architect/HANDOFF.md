# Traspaso a producción: el MVP prueba que un arquitecto de patrimonio puede armar el plan primero y recomendar después, con reglas que se cumplen en el código

**Personal Wealth Architect · MVP v1.0 · 18 de octubre de 2026 · Especialista: desarrollador de la fábrica.** Parte del diseño v5.2 aprobado por Carolina (`diseno/README.md`, sección 12), del concepto v5.1 y de `regulatorio.md` v1. Código en `app/`.

> **Estado:** MVP para pruebas con usuarios. Nada está en operación, ninguna persona ni cifra es real y nada mueve dinero. Las cifras ficticias (comisión, caída en un mal año) están marcadas en pantalla.

## 1. Qué hace
Un afiliado ficticio recorre la asesoría integral como en banca privada, y el motor decide qué mostrarle con reglas auditables:

| Momento | Qué vive el afiliado | Qué hace el motor |
|---|---|---|
| Lunes 1 de junio · primera reunión | Autoriza el uso de su salario; metas y la más importante; números de sus metas; su vida y su dinero; seis preguntas del perfil; "esto entendí de ti" | Guarda el consentimiento y el perfil con su fecha |
| Tu plan, la primera vez | Patrimonio con origen de cada dato, pensión con supuestos, metas con números, salud del plan en 6 pilares y el orden del plan. Primer paso: confirmar a su hija como beneficiaria (no es un producto) | Arma el plan con reglas deterministas; ninguna meta termina en un producto propio sin necesidad |
| Lunes 15 de junio · la app como hogar del plan | Inicio con patrimonio y salud del plan, nota del arquitecto, revisión de junio, propuesta para la prima (paso del plan separado de la recomendación profesional), aprobación sin mover dinero, regla "Prima con rumbo", Mi plan, simulador de la casa, Patrimonio, Pilares, Tu equipo, Perfil, Cómo funciona, Pregúntale | Restrictivos primero → elegibilidad por el plan → priorización → freno, grupo de control y horario legal → una decisión con cinco campos |
| Andrés · modo servicio | Pide sus cesantías porque perdió el empleo: plazo legal, Mecanismo de Protección al Cesante, regla pausada, consultora a una frase, nada de venta | El restrictivo "pérdida de empleo" bloquea todo lo comercial |
| Vistas internas | El consultor ve el mismo plan, el brief de enganche y el de profundización; el motor muestra los cinco campos, la cola, la traza capa por capa, los escenarios con su ciclo de vida, el freno y el registro | Todo queda registrado con versiones de motor, supuestos y catálogo |

## 2. Cómo correrlo
**Local:** ver `app/README.md` (`uvicorn pwa.app:app`, `python -m pytest`: 41 pruebas que pasan).

**Railway (lo conecta Carolina, una vez):**
1. En Railway, *New Project → Deploy from GitHub repo* → `caro0907/Fabrica-innovacion`, rama `main` (después de aprobar el pull request).
2. En el servicio, *Settings → Root Directory*: `ideas/personal-wealth-architect/app`. Railway lee `railway.json` (comando de arranque y chequeo de salud en `/salud`).
3. *Variables*: `PWA_CLAVE_INTERNA` (una clave larga), `PWA_COOKIE_SEGURA=1`, `PWA_DB=/data/pwa.sqlite`. Opcionales: `ANTHROPIC_API_KEY`, `PWA_TOKEN_AGENTES`.
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
1. **Restrictivos primero:** queja abierta, no contacto, pérdida de empleo, coyuntura crítica, evento sensible, deuda cara sin colchón, sin autorización de uso del salario, perfil vencido y señales de no comprender. Si hay uno, nada comercial, sin excepción.
2. **El plan define lo elegible:** una acción solo entra si cierra una brecha del plan, la persona no la rechazó y, si es un producto, su caída en un mal año cabe en la pérdida que tolera su perfil.
3. **La priorización ordena:** impacto incremental (simulado en el MVP, con las cuatro poblaciones) y valor para el plan de la persona. Los "seguros" no reciben aviso proactivo; los "perdidos" y "no molestar" no se contactan.
4. **Compuertas para iniciar un contacto:** freno de servicio, grupo de control (asignación estable por hash, 10%), horario legal de la Ley 2300 de 2023, un contacto por semana y autorización de mensajes.
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
| Mandatos no discrecionales con control "te propongo y tú confirmas" | La persona fija el reparto y el tope; el sistema solo dispara (riesgo R13). Ningún mandato mueve dinero en el MVP |
| SQLite con volumen en Railway | Suficiente para pruebas con 10 personas; el esquema migra a PostgreSQL sin cambiar el motor |
| El consultor con nombre queda configurable por segmento (`CONSULTOR_CON_NOMBRE_POR_SEGMENTO` en `pwa/motor/datos.py`) | Pendiente 2 de Carolina; hoy está activo en ambos segmentos |

### Cifras que cambiaron frente al prototipo v5.2, y por qué
El prototipo mostraba cifras ilustrativas; el MVP las calcula. Ninguna cambia el recorrido aprobado, pero Carolina debe verlas antes de probar con usuarios.

| Dato de Laura | Prototipo v5.2 | MVP | Por qué |
|---|---|---|---|
| Pensión estimada | $2,3 M | **$1,83 M** (brecha $1,17 M) | El MVP lleva a la cuenta individual solo el 11,5% de la cotización, no el 16%. Con el 16% daría unos $2,2 M. Lo debe validar actuaría (pregunta 6 de `regulatorio.md`) |
| Salud del plan | 520 | **552** el 1 de junio; **635** el 15, tras confirmar a su hija | Las reglas de cada pilar ahora están en código (`plan.py`) y suben cuando ella actúa |
| Lo que más mueve su puntaje | El colchón | **Protección** (su hija no era beneficiaria) | Coincide con el primer paso del plan |
| Para llegar a la casa a tiempo | Unos $100 mil más al mes | **Unos $90 mil** | Calculado con el simulador y redondeado hacia arriba |
| Caída en un mal año, comisión, prima, reparto 70/30, colchón | $94.000; 1,2%; $2,6 M; $1.820.000 y $780.000; 1,2 meses | Iguales | — |

## 5. Costos de servicios (precios verificados el 18 de octubre de 2026)
| Servicio | Precio publicado | Para este MVP |
|---|---|---|
| Railway, plan Hobby | USD 5 al mes, con USD 5 de uso incluido. Uso: USD 10 por GB de memoria al mes, USD 20 por vCPU al mes, USD 0,15 por GB de volumen al mes, USD 0,05 por GB de salida ([Railway](https://docs.railway.com/pricing/plans)) | *Estimado propio:* la app usa poca CPU y unos 60 MB de memoria en reposo (medido en local); debería caber en el uso incluido (unos USD 5 al mes en total). Verificar en la factura del primer mes |
| Claude Haiku 5.5 (opcional) | USD 0,10 por millón de tokens de entrada y USD 0,50 de salida, en prompts de hasta 100.000 tokens ([Anthropic](https://platform.claude.com/docs/en/about-claude/pricing)) | *Estimado propio:* unos 700 tokens de entrada y 150 de salida por nota, es decir unos USD 0,00015 por nota. Con 10 personas de prueba, menos de un centavo de dólar |
| GitHub | Gratis (repositorio privado) | — |

## 6. Control de riesgo: cubierto / pendiente
| Tema | Cubierto | Pendiente para producción |
|---|---|---|
| Datos reales | Solo datos ficticios en código, semillas y registro; ningún nombre interno ni cifra de la entidad | — |
| Secretos | Todo por variables de entorno; `.env` y la base fuera de Git; ninguna llave en el repositorio | Rotación de claves y un gestor de secretos |
| Dependencias | Seis dependencias conocidas y mantenidas, con versión fija | Escaneo automático de vulnerabilidades |
| Autenticación | Vistas internas con clave y cookie solo HTTP; consulta de agentes con token y consentimiento específico; cabeceras de seguridad (CSP, no marcos) | Identidad reforzada real del afiliado (la huella está simulada), roles por equipo y registro de accesos |
| Habeas Data (Ley 1581 de 2012) | Autorización específica y revocable del uso del salario; de la hija, solo la edad; la huella es del celular y la entidad no recibe el dato biométrico; permisos visibles y revocables en "Mis reglas y permisos"; cada consentimiento queda registrado | Política de tratamiento y aviso de privacidad; finalidad por dato; retención y borrado; datos de menores con su régimen especial; **al retirar el permiso del salario, el motor deja de proponer y contactar, pero las pantallas todavía muestran cifras calculadas con él**: deben recalcularse sin ese dato |
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
7. **Recalcular sin el salario** cuando la persona retira el permiso (ver sección 6).
8. **PostgreSQL**, copias de respaldo y monitoreo.
