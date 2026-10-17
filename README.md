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

## Flujo de trabajo

```
Idea → Brief + referentes → Aprobación → Prototipo → Prueba con 5 usuarios → Aprobación → MVP → Traspaso
        (estratega)          (Carolina)   (diseñador)                         (Carolina)  (desarrollador)
```

Cada etapa termina con una decisión explícita de Carolina: **AVANZAR**, **AJUSTAR** o **DESCARTAR**. Se registra en `empresa/decisiones.md`.

## Reglas de la casa

1. **Cero datos de empleadores.** Nunca se usan datos reales, confidenciales o internos de Protección ni de ninguna otra empresa. Solo datos públicos (con fuente y fecha) o ficticios marcados como tales.
2. **Innovar, no copiar.** De los referentes tomamos el mecanismo que los hace funcionar, nunca su marca, apariencia ni contenido.
3. **Hechos separados de supuestos.** Todo dato lleva fuente; todo lo demás se marca como supuesto.
4. **El MVP más pequeño que pruebe la hipótesis principal.** Lo demás va como pendiente.
5. **Precios verificados.** Toda decisión de tecnología o infraestructura se toma con precios vigentes y verificados, no estimados.
6. **La fábrica aprende.** Al cerrar cada proyecto se registran aprendizajes en `empresa/aprendizajes.md` y se proponen mejoras a los especialistas.

## Estructura

```
empresa/
  decisiones.md        Registro de decisiones de la gerencia
  aprendizajes.md      Lo que la fábrica aprende en cada proyecto
  herramientas.md      Stack, cuentas y costos verificados
  especialistas/       Copia de las instrucciones de cada especialista (respaldo portable)
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
