# Fábrica de Innovación

Manual de operación de la empresa. Este repositorio es la memoria de la fábrica: aquí vive cada idea, su investigación, su diseño, su código y las decisiones tomadas.

## Propósito

Convertir ideas innovadoras en soluciones reales en semanas, no en meses. Estudiamos lo que hacen los mejores del mundo, entendemos por qué funciona, lo adaptamos a necesidades reales y lo llevamos de forma táctica a un diseño y a un producto.

## Cómo está organizada

| Rol | Quién | Responsabilidad |
|---|---|---|
| Gerencia de innovación | Carolina | Encuentra oportunidades, decide qué avanza, aprueba cada paso |
| Estratega de innovación | Especialista IA (`fabrica-estratega`) | Investiga referentes globales, encuentra la oportunidad, escribe el brief |
| Diseñador de innovación | Especialista IA (`fabrica-disenador`) | Traduce el brief en journey, prototipo navegable y plan de prueba |
| Desarrollador | Especialista IA (`fabrica-desarrollador`) | Construye el MVP, lo prueba, revisa riesgos y deja el traspaso |
| Experto financiero, regulatorio y tributario | Especialista IA (`fabrica-experto-financiero`) | Encuentra beneficios, diferenciales y restricciones (AMV, SFC, Estatuto Tributario) y revisa el trabajo de los demás |
| Revisor independiente | Especialista IA (`fabrica-revisor`), corre como agente aparte | Revisa cada entregable con los ojos de Carolina (`empresa/criterios-de-revision.md`) y decide si pasa o vuelve, antes de que ella lo vea |
| Vigía semanal | Tarea programada, lunes 6:56 a. m. | Busca cambios regulatorios y de la competencia y deja un informe en `vigia/` |

## Flujo de trabajo

```
Idea → Concepto y brief → Revisor → Carolina → Benchmark de experiencia y prototipo → Experto → Revisor → Carolina
        (estratega + experto)                    (diseñador, desde empresa/activos/)

     → Prueba con 5 usuarios → Carolina → MVP → Revisor → Carolina → Traspaso
                                          (desarrollador)
```

**La compuerta del revisor:** ningún entregable llega a Carolina sin pasar por el revisor, que corre como agente aparte y no vio cómo se hizo el trabajo. Si devuelve, el especialista corrige (máximo dos rondas).

**La fábrica aprende sola:** cuando Carolina corrige algo que el revisor no vio, se agrega un criterio a `empresa/criterios-de-revision.md` y queda en `empresa/metricas.md`. Desde el siguiente entregable, el revisor lo exige.

Cada etapa termina con una decisión explícita de Carolina: **AVANZAR**, **AJUSTAR** o **DESCARTAR**. Se registra en `empresa/decisiones.md`.

## Reglas de la casa

1. **Cero datos de empleadores.** Nunca se usan datos reales, confidenciales o internos de Protección ni de ninguna otra empresa. Solo datos públicos (con fuente y fecha) o ficticios marcados como tales.
2. **Innovar, no copiar.** De los referentes tomamos el mecanismo que los hace funcionar, nunca su marca, apariencia ni contenido.
3. **Hechos separados de supuestos.** Todo dato lleva fuente; todo lo demás se marca como supuesto.
4. **El MVP más pequeño que pruebe la hipótesis principal.** Lo demás va como pendiente.
5. **Precios verificados.** Toda decisión de tecnología o infraestructura se toma con precios vigentes y verificados, no estimados.
6. **La fábrica aprende.** Cada corrección de Carolina se vuelve un criterio del revisor; al cerrar cada proyecto se registran aprendizajes en `empresa/aprendizajes.md`, se actualizan los especialistas y se mide en `empresa/metricas.md` si las rondas de corrección bajan.
7. **El método de Carolina manda.** Todo especialista lee `empresa/forma-de-trabajo.md` antes de empezar.
8. **Primero los activos.** Antes de crear algo, se parte de `empresa/activos/` (sistema de diseño, plantillas de pantallas, catálogo regulatorio base).

## Estructura

```
empresa/
  decisiones.md        Registro de decisiones de la gerencia
  aprendizajes.md      Lo que la fábrica aprende en cada proyecto
  forma-de-trabajo.md  Cómo piensa, escribe y decide Carolina (lo leen todos los especialistas)
  herramientas.md      Stack, cuentas y costos verificados
  criterios-de-revision.md  Lo que revisaría Carolina (lista viva del revisor)
  metricas.md          Rondas de corrección y lo que detecta la fábrica frente a Carolina
  activos/             Sistema de diseño, plantillas de pantallas y catálogo regulatorio base
  especialistas/       Copia de las instrucciones de cada especialista (respaldo portable)
vigia/                 Informes semanales del vigía regulatorio y competitivo
ideas/
  _plantilla/          Copiar esta carpeta para cada idea nueva
  <nombre-corto>/
    brief.md
    referentes.md
    diseno/
    app/
    HANDOFF.md
```

## Cómo iniciar una idea nueva

1. Copia `ideas/_plantilla/` como `ideas/<nombre-corto>/`.
2. Pídele a Claude: *"Usa fabrica-estratega con esta idea: ..."*.
3. Revisa el brief y los referentes, y registra tu decisión.
4. Continúa con `fabrica-disenador` y luego con `fabrica-desarrollador`.

## Dónde vive cada cosa

- **Especialistas:** skills en la cuenta personal de Claude de Carolina (respaldo en `empresa/especialistas/`).
- **Memoria de trabajo:** este repositorio privado en GitHub personal.
- **Documentos de negocio para compartir con personas:** Google Drive personal, carpeta [Fabrica de diseno y desarrollo](https://drive.google.com/drive/folders/1OkCAbsVsBPeJYCKYoa95wWobkbGfo93l).
- **Prototipos y MVPs desplegados:** Railway.
