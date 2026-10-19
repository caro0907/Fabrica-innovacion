"""El plan del afiliado: patrimonio, metas con números, salud del plan y el orden.

El plan se arma con las metas de la persona, no con los productos de la entidad
(principio "el plan primero, el producto después"). Cada dato lleva su origen:
'sabemos' (lo que la entidad ya tiene, con autorización), 'nos contaste'
(diagnóstico) o 'estimado' (calculado con supuestos visibles).
"""
import math
from datetime import date

from . import calculos as C
from . import supuestos as S
from .formato import millones, pesos, miles, meses_txt

FECHA_REFORMA = S.REFORMA_PENSIONAL["fecha_vigencia"]


def _anios_plazo(texto: str) -> int | None:
    for n in (3, 5, 10):
        if str(n) in texto:
            return n
    if "Más de 10" in texto:
        return 15
    return None


def _semanas_hasta_reforma(hoy: date, cotiza: bool) -> int:
    if not cotiza or hoy >= FECHA_REFORMA:
        return 0
    return (FECHA_REFORMA - hoy).days // 7


def _con_dependientes(d: dict) -> bool:
    return d.get("depende") not in (None, "", "Nadie")


def _persona_dependiente(d: dict) -> str:
    return {"Mi hija": "tu hija", "Hijos": "tus hijos", "Mis padres": "tus padres"}.get(d.get("depende"), "tu familia")


def _deuda_cara(d: dict) -> bool:
    return d.get("deudas") == "Tarjeta o crédito que pago a cuotas"


def armar_plan(af: dict, diagnostico: dict, hoy: date, hechos: set[str] | None = None) -> dict:
    hechos = hechos or set()
    sabe = af["lo_que_sabemos"]
    d = diagnostico
    salario = sabe["salario_cotizacion"]
    beneficiarios_ok = sabe["beneficiarios_confirmados"] or "beneficiaria_confirmada" in hechos

    # Pensión, el ancla
    pen = C.proyectar_pension(af["sexo"], af["edad"], sabe["saldo_pension_obligatoria"], salario,
                              sabe["semanas_cotizadas"],
                              _semanas_hasta_reforma(hoy, sabe["cotiza_activamente"]))
    deseada = d.get("pension_deseada") or 0
    brecha_pension = max(0.0, deseada - pen.mesada)

    # Colchón
    ahorro_liquido = d["ahorro"] if "En inversiones" not in d.get("donde_ahorro", []) else 0
    col = C.colchon(d["gastos_mensuales"], ahorro_liquido)

    # Prima y su reparto según el plan
    prima = C.prima_estimada(salario)
    reparto = C.repartir_prima(prima, col["brecha"])

    # Casa
    casa = None
    if "Comprar mi casa" in d.get("metas", []) and d.get("cuota_inicial_casa"):
        plazo = _anios_plazo(d.get("plazo_casa", "")) or 10
        inicial = sabe["cesantias"]
        aporte_primas = reparto["a_la_meta"] * 2 / 12 if d.get("prioridad") == "Comprar mi casa" else 0
        meses_solo_primas = C.meses_para_meta(d["cuota_inicial_casa"], inicial, aporte_primas, S.RENTABILIDAD_ESCENARIO_BUENO)
        necesario = C.aporte_para_llegar(d["cuota_inicial_casa"], inicial, plazo * 12, S.RENTABILIDAD_ESCENARIO_BUENO)
        extra = max(0.0, necesario - aporte_primas)
        casa = {
            "cuota": d["cuota_inicial_casa"],
            "plazo_anios": plazo,
            "anio_meta": hoy.year + plazo,
            "llevas": inicial,
            "avance": inicial / d["cuota_inicial_casa"],
            "aporte_primas_mensual": aporte_primas,
            "anio_solo_primas": (hoy.year + math.ceil(meses_solo_primas / 12)) if meses_solo_primas else None,
            "extra_mensual_a_tiempo": math.ceil(extra / 10_000) * 10_000,   # un faltante se redondea hacia arriba
            "a_tiempo_solo_con_primas": extra <= 0,
        }

    # Salud del plan: seis pilares, el puntaje es su promedio × 10
    pilares = _pilares(af, d, pen.mesada, deseada, col, casa, beneficiarios_ok, hechos)
    puntaje = round(sum(p["valor"] for p in pilares) / len(pilares) * 10)
    mueve = min(pilares, key=lambda p: p["valor"])

    patrimonio_total = sabe["saldo_pension_obligatoria"] + sabe["cesantias"] + d["ahorro"]

    metas = _metas(d, col, casa, pen.mesada, deseada, brecha_pension, beneficiarios_ok)
    orden = _orden(af, d, col, casa, reparto, prima, beneficiarios_ok, brecha_pension)

    return {
        "fecha": hoy.isoformat(),
        "version_supuestos": S.VERSION,
        "patrimonio": {
            "total": patrimonio_total,
            "total_txt": millones(patrimonio_total),
            "dimensiones": _dimensiones(af, d, beneficiarios_ok),
        },
        "pension": {
            **pen.dict(),
            "mesada_txt": millones(pen.mesada),
            "deseada": deseada,
            "deseada_txt": millones(deseada),
            "brecha": brecha_pension,
            "brecha_txt": millones(brecha_pension),
            "avance": min(1.0, pen.mesada / deseada) if deseada else 1.0,
            "supuestos_txt": supuestos_pension_txt(af, pen),
        },
        "colchon": {**col, "meta_txt": millones(col["meta"]), "tiene_txt": millones(col["tiene"]),
                    "meses_txt": meses_txt(col["meses_cubiertos"])},
        "prima": {"monto": prima, "monto_txt": pesos(prima), "monto_corto": millones(prima), **reparto,
                  "al_colchon_txt": pesos(reparto["al_colchon"]), "a_la_meta_txt": pesos(reparto["a_la_meta"])},
        "casa": casa and {**casa, "cuota_txt": millones(casa["cuota"]), "llevas_txt": millones(casa["llevas"]),
                          "extra_txt": miles(casa["extra_mensual_a_tiempo"])},
        "metas": metas,
        "pilares": pilares,
        "puntaje": puntaje,
        "lo_que_mas_mueve": mueve,
        "orden": orden,
        "dependiente": _persona_dependiente(d) if _con_dependientes(d) else None,
        "beneficiarios_confirmados": beneficiarios_ok,
        "deuda_cara": _deuda_cara(d),
    }


def supuestos_pension_txt(af: dict, pen) -> str:
    sabe = af["lo_que_sabemos"]
    if pen.conserva_reglas_de_hoy and pen.semanas_hoy < pen.semanas_transicion:
        transicion = (f"Tienes unas {pen.semanas_hoy} semanas cotizadas: si sigues cotizando, llegas a "
                      f"{pen.semanas_transicion} antes del {S.FECHA_REFORMA} y conservarías las reglas de hoy "
                      "(régimen de transición de la reforma pensional).")
    elif pen.conserva_reglas_de_hoy:
        transicion = (f"Con tus {pen.semanas_hoy} semanas superas las {pen.semanas_transicion}: conservarías las "
                      f"reglas de hoy (régimen de transición de la reforma pensional, que rige desde el {S.FECHA_REFORMA}).")
    else:
        transicion = (f"Con las reglas de la reforma pensional, que rige desde el {S.FECHA_REFORMA}, parte de tu "
                      "cotización iría al componente público; este cálculo aún no lo incluye y lo revisa un asesor.")
    pct_cuenta = f"{S.PORCENTAJE_A_CUENTA_INDIVIDUAL * 100:g}".replace(".", ",")
    pct_rent = f"{S.RENTABILIDAD_REAL_ANUAL * 100:g}".replace(".", ",")
    return (f"Estimado con tu salario de cotización de hoy ({millones(sabe['salario_cotizacion'])}), cotizando hasta los "
            f"{pen.edad_pension}. Cada mes van a tu cuenta individual {pct_cuenta}% de tu salario y suponemos una "
            f"rentabilidad real de {pct_rent}% al año, "
            f"neta de comisiones. {transicion} Supone {S.MESADAS_POR_ANIO} mesadas al año durante {S.ANIOS_DE_PENSION} "
            "años. Lo confirmamos con tu historia laboral. No es una promesa ni una rentabilidad garantizada; algunos "
            "años puede ser negativa.")


def _pilares(af, d, mesada, deseada, col, casa, beneficiarios_ok, hechos):
    sabe = af["lo_que_sabemos"]
    dep = _con_dependientes(d)

    colchon_v = min(100, round(col["meses_cubiertos"] / S.MESES_COLCHON_SANO * 100))

    suf_pension = min(100, round(mesada / deseada * 100)) if deseada else 100
    if casa:
        if casa["a_tiempo_solo_con_primas"] or "regla_prima" in hechos:
            ritmo = 100
        elif casa["anio_solo_primas"]:
            ritmo = round(casa["plazo_anios"] / (casa["anio_solo_primas"] - (casa["anio_meta"] - casa["plazo_anios"])) * 100)
        else:
            ritmo = 0
        suficiencia = round((suf_pension + min(100, ritmo)) / 2)
    else:
        suficiencia = suf_pension

    proteccion = 0
    proteccion += 50 if (beneficiarios_ok or not dep) else 0
    if dep:
        proteccion += {"Sí": 35, "No sé": 10, "No": 0}.get(d.get("seguro_vida"), 0)
    else:
        proteccion += 35
    proteccion += 15 if not _deuda_cara(d) else 0

    riesgo = 100
    if not d.get("perfil"):
        riesgo -= 40
    if "En inversiones" in d.get("donde_ahorro", []) and not col["completo"]:
        riesgo -= 30
    if casa and casa["plazo_anios"] > 3 and "regla_prima" not in hechos:
        riesgo -= 30

    eficiencia = 100
    if sabe.get("comision_pension_anual", 0) > 0.01:
        eficiencia -= 20
    if not ({"Comprar mi casa", "Educar a mis hijos"} & set(d.get("metas", []))):
        eficiencia -= 20

    constancia = 50 if sabe["cotiza_activamente"] else 20
    if "regla_prima" in hechos:
        constancia += 25

    persona = _persona_dependiente(d)
    return [
        {"id": "colchon", "nombre": "Colchón", "valor": colchon_v,
         "texto": f"Cubres {meses_txt(col['meses_cubiertos'])} meses; lo sano son {S.MESES_COLCHON_SANO}",
         "accion": f"Llevar tu colchón a {S.MESES_COLCHON_SANO} meses"},
        {"id": "suficiencia", "nombre": "Suficiencia", "valor": suficiencia,
         "texto": f"Vas para {millones(mesada)} de pensión; tu meta, {millones(deseada)}" + (
             f". Tu casa, a este ritmo, hacia {casa['anio_solo_primas']}" if casa and casa["anio_solo_primas"] and not casa["a_tiempo_solo_con_primas"] else ""),
         "accion": "Cerrar la brecha de tu meta más importante"},
        {"id": "proteccion", "nombre": "Protección", "valor": proteccion,
         "texto": (f"{persona[0].upper() + persona[1:]} ya es tu beneficiaria confirmada" if beneficiarios_ok and dep
                   else (f"{persona[0].upper() + persona[1:]} aún no es tu beneficiaria confirmada" if dep else "Sin dependientes declarados"))
         + ("; falta revisar tu seguro de vida" if dep and d.get("seguro_vida") != "Sí" else ""),
         "accion": "Confirmar beneficiarios y revisar tu seguro de vida"},
        {"id": "riesgo", "nombre": "Riesgo a la medida", "valor": riesgo,
         "texto": "Tu pensión va en el fondo para tu edad" + ("; tu casa aún no tiene un ahorro según su plazo" if casa and riesgo < 100 else ""),
         "accion": "Darle a cada meta un ahorro según su plazo"},
        {"id": "eficiencia", "nombre": "Eficiencia", "valor": eficiencia,
         "texto": f"Comisión de {str(round(sabe.get('comision_pension_anual', 0) * 100, 1)).replace('.', ',')}% al año (ficticia)"
                  + ("; cesantías con meta" if eficiencia >= 80 else ""),
         "accion": "Usar tus cesantías y beneficios con propósito"},
        {"id": "constancia", "nombre": "Constancia", "valor": constancia,
         "texto": ("Aportas sin falta a tu pensión" if sabe["cotiza_activamente"] else "Tu cotización está en pausa")
                  + ("; tus primas tienen una regla" if "regla_prima" in hechos else "; tus primas aún no tienen meta"),
         "accion": "Darle un destino a tus primas"},
    ]


def _metas(d, col, casa, mesada, deseada, brecha_pension, beneficiarios_ok):
    metas = []
    if "Tener tranquilidad" in d.get("metas", []) or not col["completo"]:
        metas.append({
            "id": "colchon", "nombre": f"Tranquilidad: colchón de {S.MESES_COLCHON_SANO} meses",
            "estado": "Completo" if col["completo"] else "Lo primero",
            "texto": f"{millones(col['meta'])}, {S.MESES_COLCHON_SANO} meses de tus gastos · tienes {millones(col['tiene'])}",
            "avance": min(1.0, col["tiene"] / col["meta"]) if col["meta"] else 1.0,
            "nota": "Puede quedarse en tu cuenta de ahorros: lo importante es que esté separado y disponible.",
            "catalogo": ["P3", "P5"],
        })
    if casa:
        prioridad = d.get("prioridad") == "Comprar mi casa"
        texto = f"Cuota inicial de {millones(casa['cuota'])} · llevas {millones(casa['llevas'])} en tus cesantías."
        if not casa["a_tiempo_solo_con_primas"] and casa["anio_solo_primas"]:
            texto += f" Solo con tus primas llegas hacia {casa['anio_solo_primas']}; a tiempo, con unos {miles(casa['extra_mensual_a_tiempo'])} más al mes"
        metas.append({
            "id": "casa", "nombre": f"Tu casa en {casa['plazo_anios']} años" + (" · tu meta más importante" if prioridad else ""),
            "estado": "En camino" if casa["a_tiempo_solo_con_primas"] else "Con brecha",
            "texto": texto, "avance": casa["avance"],
            "nota": "Tus cesantías se pueden usar para tu vivienda; si las usas, dejan de ser tu respaldo si pierdes el empleo. Por eso tu colchón va aparte.",
            "catalogo": ["P7", "B8"],
        })
    if "Pensionarme bien" in d.get("metas", []):
        metas.append({
            "id": "pension", "nombre": f"Tu pensión con {millones(deseada)} al mes",
            "estado": "En camino" if brecha_pension <= 0 else "Con brecha",
            "texto": f"Te faltan unos {millones(brecha_pension)} al mes (estimado)" if brecha_pension > 0 else "Vas en camino (estimado)",
            "avance": min(1.0, mesada / deseada) if deseada else 1.0, "nota": "", "catalogo": ["B12", "A4"],
        })
    if _con_dependientes(d):
        persona = _persona_dependiente(d)
        metas.append({
            "id": "proteccion", "nombre": f"Proteger a {persona}",
            "estado": "En camino" if beneficiarios_ok else "Por empezar",
            "texto": ("Beneficiaria confirmada" if beneficiarios_ok else "Confirmarla como beneficiaria")
                     + (" · falta revisar tu seguro de vida" if d.get("seguro_vida") != "Sí" else ""),
            "avance": 0.5 if beneficiarios_ok else 0.0, "nota": "", "catalogo": ["P6"],
        })
    return metas


def _orden(af, d, col, casa, reparto, prima, beneficiarios_ok, brecha_pension):
    """El orden del plan: primero lo que no es producto, al final el producto si el plan lo pide."""
    pasos = []
    if _con_dependientes(d) and not beneficiarios_ok:
        persona = _persona_dependiente(d)
        pasos.append({"id": "beneficiaria", "cuando": "Hoy", "es_producto": False,
                      "titulo": f"Confirma a {persona} como beneficiaria",
                      "texto": "Es lo que la protege si algo te pasa. Toma 2 minutos y no es un producto.",
                      "catalogo": ["P6"]})
    if _deuda_cara(d):
        pasos.append({"id": "deuda", "cuando": "Antes de invertir", "es_producto": False,
                      "titulo": "Paga primero tu deuda cara",
                      "texto": "Te cuesta más de lo que ganarías invirtiendo. No te recomiendo invertir todavía.",
                      "catalogo": ["P4"]})
    if "junio" in af["lo_que_sabemos"]["primas"]:
        destino = []
        if reparto["al_colchon"] > 0:
            destino.append("tu colchón primero")
        if casa and d.get("prioridad") == "Comprar mi casa" and not _deuda_cara(d):
            destino.append("avanzar tu casa")
        pasos.append({"id": "prima", "cuando": "30 de junio", "es_producto": False,
                      "titulo": f"Tu prima, unos {millones(prima)}",
                      "texto": (" y ".join(destino).capitalize() + ". " if destino else "")
                               + "Dos semanas antes te preparo tu revisión con una propuesta, y tú decides.",
                      "catalogo": ["B6"]})
    if brecha_pension > 0:
        pasos.append({"id": "pension", "cuando": "Diciembre", "es_producto": False,
                      "titulo": "Revisamos tu pensión",
                      "texto": "Con tu colchón más completo, vemos cómo cerrar tu brecha.",
                      "catalogo": ["B12"]})
    return pasos


def _dimensiones(af, d, beneficiarios_ok):
    sabe = af["lo_que_sabemos"]
    dims = [
        ("Pensión y retiro", f"Pensión obligatoria {millones(sabe['saldo_pension_obligatoria'])} · {sabe['anios_cotizados']} años cotizados", "sabemos"),
        ("Ahorro e inversión", f"{millones(d['ahorro'])} · " + ", ".join(d.get("donde_ahorro", [])).lower(), "nos contaste"),
        ("Vivienda", d.get("vivienda", "") + f" · cesantías {millones(sabe['cesantias'])}"
         + (f" · meta: tu casa {d.get('plazo_casa', '').lower()}" if "Comprar mi casa" in d.get("metas", []) else ""), "sabemos y nos contaste"),
        ("Flujo de dinero y deudas", f"Salario de cotización {millones(sabe['salario_cotizacion'])} · gastos {millones(d['gastos_mensuales'])} · {d.get('deudas', '').lower()}", "sabemos y nos contaste"),
        ("Educación", "Meta elegida" if "Educar a mis hijos" in d.get("metas", []) else "Por conocer: la sumamos si quieres", "nos contaste" if "Educar a mis hijos" in d.get("metas", []) else "por completar"),
        ("Protección de la familia", ("Beneficiaria confirmada" if beneficiarios_ok else "Beneficiarios por confirmar") + f" · seguro de vida: {d.get('seguro_vida', 'no sé').lower()}", "sabemos y nos contaste"),
        ("Impuestos", "Por completar: lo vemos con tu certificado de ingresos", "por completar"),
        ("Legado", "Por conocer", "por completar"),
    ]
    return [{"nombre": a, "texto": b, "origen": c} for a, b, c in dims]
