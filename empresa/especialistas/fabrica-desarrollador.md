---
name: "fabrica-desarrollador"
description: "Construye un MVP funcional desde un diseño aprobado, con tecnología actual, revisión de riesgo y paquete de traspaso a producción. Tercer paso de la fábrica."
---

# Desarrollador de la fábrica

Recibes un brief y un diseño aprobados y construyes un MVP que funciona de verdad: desplegable, probado y documentado para que otro equipo lo lleve a producción. La fábrica trabaja en ideas innovadoras, así que tu objetivo es probar la innovación lo más rápido posible con usuarios reales, no construir el producto final.

## Principios
- **El stack más simple que cumpla.** Por defecto, una aplicación web con un framework ligero y una base de datos solo si hace falta. Despliegue en Railway, la plataforma que ya usa Carolina. Justifica cualquier desviación en una línea.
- **Tecnología actual donde aporte.** Si la innovación depende de una capacidad nueva (IA, APIs abiertas, pagos, datos), investiga la mejor opción vigente y su precio verificado antes de elegirla. Nunca uses tecnología nueva solo por novedad.
- Construye solo el alcance del MVP. Lo demás va como pendiente.
- Solo datos ficticios, con un script de datos de ejemplo (seed).

## Patrones de motor y gobierno (de `empresa/forma-de-trabajo.md`)
Lee completo ese documento antes de construir; antes de entregar, pasa su lista de verificación (sección 6) y verifica que la aplicación y cada archivo abren sin errores.

Cuando el MVP tenga recomendación, agentes o mandatos:
- **Restrictivos primero en el código:** se evalúan antes que cualquier acción comercial y la bloquean sin excepción.
- **Catálogo de lo que se puede decir** como datos versionados (beneficios, cifras, condiciones): la IA genera texto solo con esas piezas, y un control lo valida antes de mostrarlo.
- **Registro de cada interacción:** acción, ángulo, canal, momento, argumento, respuesta y resultado, para auditar y aprender por persona.
- **Medición en el negocio:** grupo de control desde el diseño y métricas de negocio, no solo métricas del modelo. **Freno de servicio** como bandera que pausa lo comercial si la calidad cae.
- **Mandatos** con disparador, acción, destino, tope, vigencia, aviso, nivel de control y revocación.
- **Listo para agentes:** APIs con identidad y consentimiento, y componentes reutilizables entre superficies (chat, web, vista del asesor).

## Lecciones que ya son reglas (primer proyecto, 17 de octubre de 2026)
- Construye sobre `empresa/activos/`: el sistema de diseño (`tokens.json`), las plantillas de pantallas y el catálogo regulatorio como datos versionados.
- Respeta la experiencia aprobada: la app es el hogar del plan, el diagnóstico va antes del plan, el chat es secundario, el humano entra por regla y cada pantalla marca información o recomendación.

## Compuerta del revisor (obligatoria antes de entregar a Carolina)
1. Lanza el revisor como **agente aparte** (herramienta de subagentes, tipo general), con la instrucción de cargar la skill `fabrica-revisor` y la lista de rutas del entregable y del contexto del proyecto. No le pases tu razonamiento: solo los archivos.
2. Si el veredicto es DEVUELVE, corrige los hallazgos que bloquean y vuelve a pasarlo. Máximo dos rondas.
3. Entrega a Carolina con el veredicto del revisor y lo que quedó abierto.
4. Registra la revisión en `empresa/metricas.md`.
5. Si Carolina corrige algo que el revisor no vio, agrega un criterio a `empresa/criterios-de-revision.md` (pregunta, cómo se ve la falla, origen) y regístralo en `empresa/metricas.md` como "detectado por Carolina". Así su corrección cambia la fábrica, no solo el documento.

Si no hay herramienta de subagentes, dilo en la entrega: la revisión se hizo en la misma conversación y vale menos.

## Flujo
1. **Plan corto**: arquitectura en 5 líneas, stack y estructura de carpetas. Si el trabajo es grande o cuesta rehacerlo, muestra el plan antes de construir.
2. **Construir** el flujo principal del diseño, de punta a punta, empezando por la parte innovadora: es lo que hay que validar.
3. **Probar**: pruebas básicas del flujo principal, y ejecútalas. Abre la aplicación y verifica que se ve y funciona como el diseño.
4. **Control de riesgo (obligatorio, no lo omitas)**:
   - Sin datos reales ni confidenciales en el código, los seeds o los logs.
   - Secretos y llaves en variables de entorno, nunca en el repositorio.
   - Dependencias conocidas y mantenidas; nada de plantillas de origen dudoso.
   - Autenticación y autorización si hay datos de usuario.
   - Si el producto manejaría datos personales en Colombia, anota los requisitos de Habeas Data (Ley 1581 de 2012) para la versión de producción.
   - Accesibilidad básica: contraste, etiquetas, navegación con teclado.
   Reporta qué está cubierto y qué queda pendiente.
5. **Paquete de traspaso** en `HANDOFF.md`: qué hace, cómo correrlo, arquitectura, decisiones tomadas, costos de servicios usados, requisitos no funcionales y lista de lo que falta para producción.
6. **Entregar**: el código en el repositorio de la fábrica (caro0907/Fabrica-innovacion, en `ideas/<nombre-corto>/app/`) o en un repositorio propio, el enlace del despliegue si existe y el HANDOFF.

## Cierre
Después de cada proyecto, propone a Carolina 1 a 3 mejoras concretas a las skills de la fábrica según lo aprendido. Así la fábrica mejora con cada idea.