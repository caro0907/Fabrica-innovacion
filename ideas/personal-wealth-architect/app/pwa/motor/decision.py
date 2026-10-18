"""La decisión del motor: una sola acción por afiliado, con cinco campos.

Orden de las capas (concepto, sección 4B, y forma de trabajo, sección 3.4):
1. Restrictivos primero: si hay uno, nada comercial, sin excepción.
2. El plan define qué es elegible: una acción solo entra si mejora una meta o cierra una brecha.
3. La priorización ordena las elegibles por impacto incremental y valor para la persona;
   no define el plan. Las poblaciones 'perdidos' y 'no molestar' no se contactan.
4. Freno de servicio, grupo de control y reglas de contacto deciden si se inicia un contacto.
5. Salida: canal, prioridad, vigencia, tono y recomendación, más quién lo hace.

El impacto incremental es simulado en el MVP (tabla de abajo, por arquetipo). En producción
lo estima un modelo de impacto incremental entrenado contra grupos de control.
"""
import hashlib
from datetime import date, datetime, timedelta

from . import supuestos as S
from .escenarios import ACCIONES, evaluar

VERSION_MOTOR = "motor-mvp-1.0"
# Experimento de la prima: la asignación al grupo de control depende de este nombre.
EXPERIMENTO = "prima-con-rumbo-2026-06"

# Impacto incremental simulado: (acción, arquetipo) -> (población, impacto 0-1)
IMPACTO_SIMULADO = {
    ("colchon_con_prima", "pragmatica"): ("persuadible", 0.71),
    ("casa_con_prima", "pragmatica"): ("persuadible", 0.64),
    ("regla_prima", "pragmatica"): ("persuadible", 0.58),
    ("confirmar_beneficiarios", "pragmatica"): ("persuadible", 0.80),
    ("revisar_pension", "pragmatica"): ("seguro", 0.12),
    ("servicio_cesantias", "pragmatico"): ("persuadible", 0.90),
}

# Valor para la persona según su plan: lo que más mueve su salud del plan va primero.
TONO_POR_ARQUETIPO = {
    "pragmatica": "Cercano y directo: cifras redondas, una acción a la vez",
    "pragmatico": "Empático y sereno: primero resolver, nada de venta",
    "inversora": "Preciso: cifras exactas y condiciones a la vista",
}

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

QUIEN = {
    "agente": "El arquitecto digital",
    "asesor": "Un asesor certificado",
    "agente_o_asesor": "El arquitecto digital; el asesor si la persona duda o lo pide",
}


def en_grupo_control(afiliado_id: str, experimento: str) -> bool:
    """Asignación estable y auditable: el mismo afiliado siempre cae en el mismo grupo."""
    h = hashlib.sha256(f"{experimento}:{afiliado_id}".encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF < S.PORCENTAJE_GRUPO_CONTROL


def en_horario_de_contacto(momento: datetime, festivo: bool = False) -> bool:
    """Ley 2300 de 2023: lunes a viernes de 7 a. m. a 7 p. m., sábados de 8 a. m. a 3 p. m., sin domingos ni festivos."""
    if festivo or momento.weekday() == 6:
        return False
    desde, hasta = S.HORARIO_CONTACTO["sabado" if momento.weekday() == 5 else "lunes_a_viernes"]
    return desde <= momento.hour < hasta


def freno_activo(metricas: dict) -> tuple[bool, list[str]]:
    """Lo comercial solo crece si el servicio no retrocede frente a su línea base."""
    motivos = []
    for nombre, cfg in S.FRENO_LINEAS_BASE.items():
        actual = metricas.get(nombre, cfg["base"])
        peor = actual < cfg["base"] if cfg["sentido"] == "mayor_es_mejor" else actual > cfg["base"]
        if peor:
            motivos.append(f"{nombre.replace('_', ' ')}: {actual:.0%} frente a una línea base de {cfg['base']:.0%}")
    return bool(motivos), motivos


def proxima_prima(hoy: date) -> date:
    junio = date(hoy.year, 6, 30)
    diciembre = date(hoy.year, 12, 20)
    if hoy <= junio:
        return junio
    if hoy <= diciembre:
        return diciembre
    return date(hoy.year + 1, 6, 30)


def contexto(afiliado: dict, plan: dict, hoy: date, ahora: datetime | None = None, **extra) -> dict:
    prima = proxima_prima(hoy)
    return {
        "afiliado": afiliado,
        "plan": plan,
        "hoy": hoy,
        "ahora": ahora or datetime(hoy.year, hoy.month, hoy.day, 9, 12),
        "dias_para_prima": (prima - hoy).days,
        "fecha_prima": prima,
        "perfil_vigente": extra.pop("perfil_vigente", True),
        **extra,
    }


def decidir(ctx: dict, metricas_servicio: dict | None = None, contactos_esta_semana: int = 0,
            acciones_hechas: set[str] | None = None, rechazos: set[str] | None = None) -> dict:
    af = ctx["afiliado"]
    plan = ctx["plan"]
    hechas = acciones_hechas or set()
    rechazos = rechazos or set()
    traza = []

    ev = evaluar(ctx)
    traza.append({"capa": "Escenarios", "detalle": ev["traza"]})

    # 1. Restrictivos primero
    restrictivos = ev["restrictivos"]
    modo = "servicio" if restrictivos else "asesoria"
    if restrictivos:
        traza.append({"capa": "Restrictivos", "detalle": [f"{e.nombre}: {e.efecto}" for e in restrictivos]})

    # 2. Elegibilidad por el plan
    metas_con_brecha = {m["id"] for m in plan["metas"] if m["estado"] not in ("Completo", "En camino")}
    candidatas = []
    fuentes = restrictivos if restrictivos else ev["oportunidades"]
    for e in fuentes:
        for aid in e.acciones:
            a = ACCIONES[aid]
            motivo = None
            if aid in hechas:
                motivo = "ya la hizo"
            elif aid in rechazos:
                motivo = "la persona dijo que no: se respeta"
            elif restrictivos and a.comercial:
                motivo = "bloqueada por un restrictivo"
            elif not restrictivos and a.meta not in metas_con_brecha:
                motivo = f"no cierra una brecha del plan ({a.meta})"
            elif a.portafolio and S.PORTAFOLIOS[a.portafolio]["caida_mal_anio"] > ctx.get("perdida_tolerada", 0):
                motivo = "la caída de un mal año supera lo que tolera su perfil: la ve con su consultor"
            candidatas.append((e, a, motivo))
    elegibles = [(e, a) for e, a, m in candidatas if m is None]
    traza.append({"capa": "Elegibilidad por el plan",
                  "detalle": [f"{a.nombre}: {'elegible' if m is None else 'no elegible, ' + m}" for _, a, m in candidatas]})

    # 3. Priorización entre elegibles
    valor_meta = {p["id"]: 100 - p["valor"] for p in plan["pilares"]}
    pilar_de_meta = {"colchon": "colchon", "casa": "suficiencia", "pension": "suficiencia", "proteccion": "proteccion"}
    puntuadas = []
    for e, a in elegibles:
        poblacion, impacto = IMPACTO_SIMULADO.get((a.id, af["arquetipo"]), ("persuadible", 0.5))
        valor = valor_meta.get(pilar_de_meta.get(a.meta, ""), 50) / 100
        puntaje = round(0.5 * impacto + 0.5 * valor, 3)
        puntuadas.append({"escenario": e, "accion": a, "poblacion": poblacion, "impacto": impacto,
                          "valor_persona": round(valor, 2), "puntaje": puntaje})
    puntuadas.sort(key=lambda x: x["puntaje"], reverse=True)
    traza.append({"capa": "Priorización", "detalle": [
        f"{p['accion'].nombre}: población {p['poblacion']}, impacto simulado {p['impacto']:.2f}, "
        f"valor para su plan {p['valor_persona']:.2f}, puntaje {p['puntaje']:.2f}" for p in puntuadas]})

    contactables = [p for p in puntuadas if p["poblacion"] in ("persuadible", "seguro")]

    # 4. Freno, grupo de control y reglas de contacto (solo para iniciar contactos comerciales)
    freno, motivos_freno = freno_activo(metricas_servicio or {})
    control = en_grupo_control(af["id"], EXPERIMENTO)
    horario = en_horario_de_contacto(ctx["ahora"])
    frecuencia_ok = contactos_esta_semana < S.CONTACTOS_COMERCIALES_POR_SEMANA
    autoriza = af["estado"]["autoriza_mensajes_comerciales"]

    principal = contactables[0] if contactables else None
    puede_contactar = False
    bloqueos = []
    if principal and modo == "asesoria":
        # Toda propuesta que inicia la entidad pasa por las cinco compuertas.
        if freno and any(p["accion"].comercial for p in contactables):
            bloqueos.append("Freno de servicio activo: " + "; ".join(motivos_freno))
        if control:
            bloqueos.append("Grupo de control: no recibe la propuesta proactiva (sí ve su plan)")
        if not horario:
            bloqueos.append("Fuera del horario legal de contacto: espera la siguiente ventana")
        if not frecuencia_ok:
            bloqueos.append("Ya hubo un contacto comercial esta semana")
        if not autoriza:
            bloqueos.append("Sin autorización de mensajes comerciales")
        if principal["poblacion"] == "seguro":
            bloqueos.append("Población 'seguro': actuaría sin contacto; se muestra en su app, sin aviso proactivo")
        puede_contactar = not bloqueos
    elif principal:
        bloqueos.append("Modo servicio: responde a lo que la persona pide, no inicia contactos")
    traza.append({"capa": "Activación", "detalle": [
        f"Grupo: {'control' if control else 'tratamiento'}",
        f"Horario legal: {'sí' if horario else 'no'} ({DIAS[ctx['ahora'].weekday()]} {ctx['ahora']:%H:%M})",
        f"Contactos comerciales esta semana: {contactos_esta_semana} de {S.CONTACTOS_COMERCIALES_POR_SEMANA}",
        f"Freno de servicio: {'activo' if freno else 'inactivo'}",
    ] + bloqueos})

    # 5. Salida con cinco campos
    if principal:
        a = principal["accion"]
        canal = "App (inicio del plan)" + (" y aviso por mensajería" if puede_contactar else "")
        if modo == "servicio":
            canal = "Donde la persona escribió (responde, no inicia)"
        vigencia = ctx["fecha_prima"] if principal["escenario"].id == "O-PRIMA" else ctx["hoy"] + timedelta(days=30)
        recomendacion = _recomendacion(principal, plan, modo)
        cinco = {
            "canal": canal,
            "prioridad": 1,
            "vigencia": vigencia.isoformat(),
            "tono": TONO_POR_ARQUETIPO.get(af["arquetipo"], "Cercano"),
            "recomendacion": recomendacion,
        }
        quien = QUIEN[a.quien]
    else:
        cinco = {"canal": "Ninguno", "prioridad": None, "vigencia": None,
                 "tono": TONO_POR_ARQUETIPO.get(af["arquetipo"], "Cercano"),
                 "recomendacion": "Nada que proponer hoy: el plan va en camino"}
        quien = QUIEN["agente"]

    return {
        "version_motor": VERSION_MOTOR,
        "modo": modo,
        "restrictivos": [{"id": e.id, "nombre": e.nombre, "efecto": e.efecto, "norma": e.norma} for e in restrictivos],
        "oportunidades": [{"id": e.id, "nombre": e.nombre, "estado": e.estado} for e in ev["oportunidades"]],
        "cola": [{"accion": p["accion"].id, "nombre": p["accion"].nombre, "es_producto": p["accion"].es_producto,
                  "poblacion": p["poblacion"], "puntaje": p["puntaje"], "angulo": p["accion"].angulo,
                  "quien": QUIEN[p["accion"].quien], "piezas": p["accion"].piezas} for p in puntuadas],
        "principal": principal and {"accion": principal["accion"].id, "escenario": principal["escenario"].id,
                                    "angulo": principal["accion"].angulo},
        "cinco_campos": cinco,
        "quien_lo_hace": quien,
        "puede_iniciar_contacto": puede_contactar,
        "grupo": "control" if control else "tratamiento",
        "freno": {"activo": freno, "motivos": motivos_freno},
        "traza": traza,
    }


def _recomendacion(p: dict, plan: dict, modo: str) -> str:
    a = p["accion"]
    if a.id == "colchon_con_prima" or a.id == "casa_con_prima":
        return (f"Prima con rumbo: {plan['prima']['al_colchon_txt']} a su colchón (paso del plan, no es un producto) "
                f"y {plan['prima']['a_la_meta_txt']} a su casa con una recomendación profesional.")
    if a.id == "servicio_cesantias":
        return "Entregar sus cesantías en el plazo legal, contarle del Mecanismo de Protección al Cesante y pausar sus reglas."
    if a.id == "confirmar_beneficiarios":
        return f"Confirmar a {plan['dependiente']} como beneficiaria."
    return a.nombre


def brief_enganche(decision: dict, plan: dict, afiliado: dict) -> list[str]:
    """3 a 5 líneas para el canal digital, de la misma fuente que el brief del consultor."""
    if decision["modo"] == "servicio":
        return [f"{afiliado['nombre']} está en modo servicio: {decision['restrictivos'][0]['nombre'].lower()}.",
                "Resolver lo que pidió, sin ofertas.",
                "El consultor queda a una frase."]
    lineas = [f"{afiliado['nombre']}: {decision['cinco_campos']['recomendacion']}",
              f"Porqué: {plan['lo_que_mas_mueve']['texto'].lower()}; su meta más importante es su casa.",
              f"Tono: {decision['cinco_campos']['tono'].lower()}."]
    if plan["casa"] and not plan["casa"]["a_tiempo_solo_con_primas"]:
        lineas.append(f"Con solo sus primas llega a su casa hacia {plan['casa']['anio_solo_primas']}, no en {plan['casa']['plazo_anios']} años.")
    return lineas[:5]
