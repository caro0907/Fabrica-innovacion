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


def _dependiente_hijos(d: dict) -> bool:
    return d.get("depende") in ("Mi hija", "Hijos")


def ingreso_para_el_plan(af: dict, d: dict) -> tuple[float | None, str]:
    """El ingreso con que se estiman pensión, prima y casa, y su origen (criterio C10, hallazgo R9 y H5).

    Con el permiso, el salario de cotización ('sabemos'). Sin el permiso, el ingreso que la persona
    contó ('nos contaste'). Sin ninguno de los dos, nada que dependa del ingreso se estima.
    """
    if af["estado"].get("autoriza_uso_salario"):
        return af["lo_que_sabemos"]["salario_cotizacion"], "sabemos"
    if d.get("ingreso_declarado"):
        return float(d["ingreso_declarado"]), "nos contaste"
    return None, "sin permiso"


def ingresos_del_anio(ingreso: float) -> float:
    """Ingresos brutos del año de una persona asalariada: 12 salarios, 2 primas de medio salario,
    cesantías (un salario) e intereses de cesantías (12%). Estimado propio."""
    return ingreso * (12 + 2 * S.FRACCION_PRIMA + 1 + S.TASA_INTERESES_CESANTIAS)


def obligacion_de_declarar(ingreso: float, hoy: date) -> dict:
    uvt = S.UVT.get(hoy.year) or S.UVT[max(S.UVT)]
    tope = S.TOPE_INGRESOS_DECLARAR_UVT * uvt
    ingresos = ingresos_del_anio(ingreso)
    return {"ingresos": ingresos, "tope": tope, "diferencia": ingresos - tope, "probable": ingresos > tope,
            "anio_declara": hoy.year + 1, "ingresos_txt": millones(ingresos), "tope_txt": pesos(tope)}


def armar_plan(af: dict, diagnostico: dict, hoy: date, hechos: set[str] | None = None) -> dict:
    hechos = hechos or set()
    sabe = af["lo_que_sabemos"]
    d = diagnostico
    ingreso, origen_ingreso = ingreso_para_el_plan(af, d)
    beneficiarios_ok = sabe["beneficiarios_confirmados"] or "beneficiaria_confirmada" in hechos

    # Pensión, el ancla. Sin ingreso no se estima; sin régimen de transición tampoco se muestra
    # la mesada, porque este método no incluye el componente público de la reforma (H22).
    deseada = d.get("pension_deseada") or 0
    pen = None
    if ingreso is not None:
        pen = C.proyectar_pension(af["sexo"], af["edad"], sabe["saldo_pension_obligatoria"], ingreso,
                                  sabe["semanas_cotizadas"],
                                  _semanas_hasta_reforma(hoy, sabe["cotiza_activamente"]))
    mostrar_mesada = pen is not None and pen.conserva_reglas_de_hoy
    mesada = pen.mesada if mostrar_mesada else None
    brecha_pension = max(0.0, deseada - mesada) if mesada is not None else 0.0

    # Colchón
    ahorro_liquido = d["ahorro"] if "En inversiones" not in d.get("donde_ahorro", []) else 0
    col = C.colchon(d["gastos_mensuales"], ahorro_liquido)

    # Prima y su reparto según el plan (solo con ingreso)
    prima = C.prima_estimada(ingreso) if ingreso is not None else None
    reparto = C.repartir_prima(prima, col["brecha"]) if prima else None

    # Casa
    casa = None
    if "Comprar mi casa" in d.get("metas", []) and d.get("cuota_inicial_casa"):
        plazo = _anios_plazo(d.get("plazo_casa", "")) or 10
        inicial = sabe["cesantias"]
        primas_estimadas = reparto is not None
        es_prioridad = d.get("prioridad") == "Comprar mi casa"
        aporte_primas = reparto["a_la_meta"] * 2 / 12 if primas_estimadas and es_prioridad else 0
        meses_solo_primas = (C.meses_para_meta(d["cuota_inicial_casa"], inicial, aporte_primas, S.RENTABILIDAD_ESCENARIO_BUENO)
                             if primas_estimadas and aporte_primas > 0 else None)
        necesario = C.aporte_para_llegar(d["cuota_inicial_casa"], inicial, plazo * 12, S.RENTABILIDAD_ESCENARIO_BUENO)
        extra = max(0.0, necesario - aporte_primas)
        casa = {
            "cuota": d["cuota_inicial_casa"],
            "plazo_anios": plazo,
            "anio_meta": hoy.year + plazo,
            "llevas": inicial,
            "avance": inicial / d["cuota_inicial_casa"],
            "primas_estimadas": primas_estimadas,
            "es_prioridad": es_prioridad,
            "aporte_primas_mensual": aporte_primas,
            "anio_solo_primas": (hoy.year + math.ceil(meses_solo_primas / 12)) if meses_solo_primas else None,
            "extra_mensual_a_tiempo": math.ceil(extra / 10_000) * 10_000,   # un faltante se redondea hacia arriba
            "a_tiempo_solo_con_primas": primas_estimadas and extra <= 0,
            # Lo que ya tiene un vehículo según su plazo: la parte de la prima que aprobó invertir (C9)
            "invertido": (reparto["a_la_meta"] if reparto and "propuesta_confirmada" in hechos else 0.0),
            "destino_anual": aporte_primas * 12,
        }

    # Salud del plan: seis pilares; el puntaje es el promedio × 10 de los que se pueden estimar
    pilares = _pilares(af, d, mesada, deseada, col, casa, beneficiarios_ok, hechos)
    con_valor = [p for p in pilares if p["valor"] is not None]
    puntaje = round(sum(p["valor"] for p in con_valor) / len(con_valor) * 10)
    mueve = min(con_valor, key=lambda p: p["valor"])

    patrimonio_total = sabe["saldo_pension_obligatoria"] + sabe["cesantias"] + d["ahorro"]
    declarar = obligacion_de_declarar(ingreso, hoy) if ingreso is not None else None

    metas = _metas(d, col, casa, mesada, deseada, brecha_pension, beneficiarios_ok, pen)
    orden = _orden(af, d, col, casa, reparto, prima, beneficiarios_ok, brecha_pension)

    if pen is None:
        pension = {"estimable": False, "mostrar_mesada": False, "mesada": None, "mesada_txt": "", "deseada": deseada,
                   "deseada_txt": millones(deseada), "brecha": 0.0, "brecha_txt": "", "avance": 0.0,
                   "edad_pension": S.EDAD_PENSION[af["sexo"]], "conserva_reglas_de_hoy": None,
                   "motivo_sin_mesada": "Sin tu permiso para usar tu salario de cotización no estimamos tu pensión.",
                   "supuestos_txt": ""}
    else:
        pension = {
            **pen.dict(),
            "estimable": True,
            "mostrar_mesada": mostrar_mesada,
            "mesada": mesada,
            "mesada_txt": millones(mesada) if mostrar_mesada else "",
            "deseada": deseada,
            "deseada_txt": millones(deseada),
            "brecha": brecha_pension,
            "brecha_txt": millones(brecha_pension),
            "avance": min(1.0, mesada / deseada) if (mostrar_mesada and deseada) else 0.0,
            "motivo_sin_mesada": "" if mostrar_mesada else (
                "Con las reglas de la reforma pensional, parte de tu cotización iría al componente público y este "
                "cálculo aún no lo incluye: tu pensión la estima un asesor contigo."),
            "supuestos_txt": supuestos_pension_txt(af, pen, ingreso, origen_ingreso),
        }
    return {
        "fecha": hoy.isoformat(),
        "version_supuestos": S.VERSION,
        "ingreso": {"valor": ingreso, "origen": origen_ingreso, "txt": millones(ingreso) if ingreso else ""},
        "patrimonio": {
            "total": patrimonio_total,
            "total_txt": millones(patrimonio_total),
            "dimensiones": _dimensiones(af, d, beneficiarios_ok, ingreso, origen_ingreso, declarar),
        },
        "pension": pension,
        "declarar": declarar,
        "colchon": {**col, "meta_txt": millones(col["meta"]), "tiene_txt": millones(col["tiene"]),
                    "meses_txt": meses_txt(col["meses_cubiertos"])},
        "prima": prima and {"monto": prima, "monto_txt": pesos(prima), "monto_corto": millones(prima), **reparto,
                            "al_colchon_txt": pesos(reparto["al_colchon"]), "a_la_meta_txt": pesos(reparto["a_la_meta"]),
                            "porcentaje_colchon_txt": f"{round(reparto['porcentaje_colchon'] * 100)}%"},
        "casa": casa and {**casa, "cuota_txt": millones(casa["cuota"]), "llevas_txt": millones(casa["llevas"]),
                          "extra_txt": miles(casa["extra_mensual_a_tiempo"])},
        "pilares_estimados": len(con_valor),
        "metas": metas,
        "pilares": pilares,
        "puntaje": puntaje,
        "lo_que_mas_mueve": mueve,
        "orden": orden,
        "dependiente": _persona_dependiente(d) if _con_dependientes(d) else None,
        "dependiente_hijos": _dependiente_hijos(d),
        "prioridad": d.get("prioridad"),
        "prioridad_txt": {"Pensionarme bien": "tu pensión", "Comprar mi casa": "tu casa", "Tener tranquilidad": "tu tranquilidad",
                          "Educar a mis hijos": "la educación de tus hijos", "Salir de deudas": "salir de tus deudas",
                          "Viajar": "viajar", "Emprender": "emprender"}.get(d.get("prioridad"), "tu plan"),
        "beneficiarios_confirmados": beneficiarios_ok,
        "deuda_cara": _deuda_cara(d),
    }


def supuestos_pension_txt(af: dict, pen, ingreso: float, origen: str) -> str:
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
    base = (f"tu salario de cotización de hoy ({millones(ingreso)})" if origen == "sabemos"
            else f"el ingreso que nos contaste ({millones(ingreso)})")
    return (f"Parte de tu saldo de hoy en tu pensión obligatoria ({millones(sabe['saldo_pension_obligatoria'])}) y de "
            f"{base}, que suponemos igual en pesos de hoy hasta tus {pen.edad_pension} años. Cada mes van a tu cuenta "
            f"individual {pct_cuenta}% de ese salario y suponemos una rentabilidad real de {pct_rent}% al año, neta de "
            f"comisiones. {transicion} Convierte el saldo en {S.MESADAS_POR_ANIO} mesadas iguales al año durante "
            f"{S.ANIOS_DE_PENSION} años, con la misma rentabilidad: es una aproximación, porque la forma de pensionarte "
            "(retiro programado o renta vitalicia) la eliges con un asesor. Lo confirmamos con tu historia laboral. "
            "No es una promesa ni una rentabilidad garantizada; algunos años puede ser negativa.")


def _pilares(af, d, mesada, deseada, col, casa, beneficiarios_ok, hechos):
    """Seis pilares de 0 a 100. Reglas del MVP, a calibrar con los mejores consultores.

    Un pilar solo cambia cuando cambia lo que mide (criterio C9): crear una regla no mueve la
    suficiencia ni el riesgo, porque no cambia ningún monto. La regla sí suma a la constancia,
    y la pantalla lo dice.
    """
    sabe = af["lo_que_sabemos"]
    dep = _con_dependientes(d)
    persona = _persona_dependiente(d)

    colchon_v = min(100, round(col["meses_cubiertos"] / S.MESES_COLCHON_SANO * 100))

    # Suficiencia: pensión estimada frente a la deseada y ritmo de la casa con el aporte que el plan le da
    partes = []
    if mesada is not None:
        partes.append(min(100, round(mesada / deseada * 100)) if deseada else 100)
    ritmo = None
    if casa and casa["primas_estimadas"] and casa["es_prioridad"]:
        if casa["a_tiempo_solo_con_primas"]:
            ritmo = 100
        elif casa["anio_solo_primas"]:
            ritmo = min(100, round(casa["plazo_anios"] / (casa["anio_solo_primas"] - (casa["anio_meta"] - casa["plazo_anios"])) * 100))
        else:
            ritmo = 0
        partes.append(ritmo)
    suficiencia = round(sum(partes) / len(partes)) if partes else None
    if suficiencia is None:
        texto_suf = "Sin tu permiso para usar tu salario de cotización no estimamos esto"
    else:
        texto_suf = (f"Vas para {millones(mesada)} de pensión; tu meta, {millones(deseada)}" if mesada is not None
                     else "Tu pensión la estima un asesor contigo")
        if ritmo is not None and ritmo < 100 and casa["anio_solo_primas"]:
            texto_suf += f". Tu casa, al ritmo de tus primas, hacia {casa['anio_solo_primas']}"

    # Protección: grupo familiar registrado, seguro de vida y deuda cara
    proteccion = 0
    proteccion += 50 if (beneficiarios_ok or not dep) else 0
    if dep:
        proteccion += {"Sí": 35, "No sé": 10, "No": 0}.get(d.get("seguro_vida"), 0)
    else:
        proteccion += 35
    proteccion += 15 if not _deuda_cara(d) else 0
    if not dep:
        texto_prot = "Sin dependientes declarados"
    elif beneficiarios_ok:
        texto_prot = f"{persona[0].upper() + persona[1:]} ya está en tu grupo familiar"
    else:
        texto_prot = f"{persona[0].upper() + persona[1:]} aún no está registrada en tu grupo familiar" if d.get("depende") == "Mi hija" \
            else f"{persona[0].upper() + persona[1:]} aún no están registrados en tu grupo familiar"
    if dep and d.get("seguro_vida") != "Sí":
        texto_prot += "; falta revisar tu seguro de vida"

    # Riesgo a la medida: sube en proporción a lo que de verdad tiene un vehículo según su plazo
    riesgo = 100
    if not d.get("perfil"):
        riesgo -= 40
    if "En inversiones" in d.get("donde_ahorro", []) and not col["completo"]:
        riesgo -= 30
    sin_vehiculo = 0.0
    if casa and casa["plazo_anios"] > 3:
        if casa["destino_anual"] > 0:
            sin_vehiculo = max(0.0, 1 - casa["invertido"] / casa["destino_anual"])
        else:
            sin_vehiculo = 1.0
        riesgo -= round(30 * sin_vehiculo)
    texto_riesgo = "Tu pensión va en el fondo para tu edad"
    if casa and sin_vehiculo >= 1:
        texto_riesgo += "; tu casa aún no tiene un ahorro según su plazo"
    elif casa and sin_vehiculo > 0:
        texto_riesgo += ("; aprobaste darle a parte de lo de tu casa un ahorro según su plazo "
                         "(cuenta desde tu aprobación; el dinero se mueve cuando confirmes la transferencia)")

    # Eficiencia: usar las cesantías y los beneficios con propósito. La comisión de la pensión
    # obligatoria sale de la cotización, no del saldo, y no depende de la persona (H18).
    con_meta = bool({"Comprar mi casa", "Educar a mis hijos"} & set(d.get("metas", [])))
    eficiencia = 100 if con_meta else 80
    texto_ef = ("Tus cesantías tienen una meta" if con_meta else "Tus cesantías aún no tienen una meta") + \
        ". La comisión de tu pensión obligatoria sale de tu cotización, no de tu saldo"

    constancia = 50 if sabe["cotiza_activamente"] else 20
    if "regla_prima" in hechos:
        constancia += 25

    return [
        {"id": "colchon", "nombre": "Colchón", "valor": colchon_v,
         "texto": f"Cubres {meses_txt(col['meses_cubiertos'])} meses; lo sano son {S.MESES_COLCHON_SANO}",
         "accion": f"Llevar tu colchón a {S.MESES_COLCHON_SANO} meses"},
        {"id": "suficiencia", "nombre": "Suficiencia", "valor": suficiencia, "texto": texto_suf,
         "accion": "Cerrar la brecha de tu meta más importante"},
        {"id": "proteccion", "nombre": "Protección", "valor": proteccion, "texto": texto_prot,
         "accion": "Registrar tu grupo familiar y revisar tu seguro de vida"},
        {"id": "riesgo", "nombre": "Riesgo a la medida", "valor": riesgo, "texto": texto_riesgo,
         "accion": "Darle a cada meta un ahorro según su plazo"},
        {"id": "eficiencia", "nombre": "Eficiencia", "valor": eficiencia, "texto": texto_ef,
         "accion": "Usar tus cesantías y beneficios con propósito"},
        {"id": "constancia", "nombre": "Constancia", "valor": constancia,
         "texto": ("Aportas sin falta a tu pensión" if sabe["cotiza_activamente"] else "Tu cotización está en pausa")
                  + ("; tus primas tienen una regla, y eso suma a tu constancia" if "regla_prima" in hechos
                     else "; tus primas aún no tienen una regla"),
         "accion": "Darle un destino a tus primas"},
    ]


def _metas(d, col, casa, mesada, deseada, brecha_pension, beneficiarios_ok, pen):
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
        if not casa["primas_estimadas"]:
            texto += " Sin tu permiso para usar tu salario no estimamos cuánto le aportan tus primas."
        elif not casa["es_prioridad"]:
            texto += " Hoy tus primas van a tu meta más importante, no a tu casa."
        elif not casa["a_tiempo_solo_con_primas"] and casa["anio_solo_primas"]:
            texto += f" Solo con tus primas llegas hacia {casa['anio_solo_primas']}; a tiempo, con unos {miles(casa['extra_mensual_a_tiempo'])} más al mes"
        metas.append({
            "id": "casa", "nombre": f"Tu casa en {casa['plazo_anios']} años" + (" · tu meta más importante" if prioridad else ""),
            "estado": ("En camino" if casa["a_tiempo_solo_con_primas"] else "Por estimar" if not casa["primas_estimadas"]
                       else "Con brecha" if casa["es_prioridad"] else "En espera"),
            "texto": texto, "avance": casa["avance"],
            "nota": "Tus cesantías se pueden usar para tu vivienda; si las usas, dejan de ser tu respaldo si pierdes el empleo. Por eso tu colchón va aparte.",
            "catalogo": ["P7", "B8"],
        })
    if "Pensionarme bien" in d.get("metas", []):
        if mesada is None:
            estado, texto, avance = "Por estimar", (pen and "Tu pensión la estima un asesor contigo, con las reglas de la reforma"
                                                    or "Sin tu permiso para usar tu salario de cotización no la estimamos"), 0.0
        else:
            estado = "En camino" if brecha_pension <= 0 else "Con brecha"
            texto = f"Te faltan unos {millones(brecha_pension)} al mes (estimado)" if brecha_pension > 0 else "Vas en camino (estimado)"
            avance = min(1.0, mesada / deseada) if deseada else 1.0
        metas.append({"id": "pension", "nombre": f"Tu pensión con {millones(deseada)} al mes", "estado": estado,
                      "texto": texto, "avance": avance, "nota": "", "catalogo": ["B12", "A4"]})
    if _con_dependientes(d):
        persona = _persona_dependiente(d)
        metas.append({
            "id": "proteccion", "nombre": f"Proteger a {persona}",
            "estado": "En camino" if beneficiarios_ok else "Por empezar",
            "texto": ("Registrada en tu grupo familiar" if beneficiarios_ok else "Registrarla en tu grupo familiar")
                     + (" · falta revisar tu seguro de vida" if d.get("seguro_vida") != "Sí" else ""),
            "avance": 0.5 if beneficiarios_ok else 0.0, "nota": "", "catalogo": ["P6"],
        })
    return metas


def registro_familiar(d: dict) -> dict:
    """Variables de la pieza P6 (H4): en la pensión obligatoria los hijos ya son beneficiarios por ley."""
    persona = _persona_dependiente(d)
    if d.get("depende") == "Mi hija":
        return {"ya_es": "Tu hija ya es tu beneficiaria", "registrar": "Registrarla", "persona": persona,
                "titulo": "Registra a tu hija en tu grupo familiar", "boton": "Registrar a tu hija", "pieza": "P6"}
    if d.get("depende") == "Hijos":
        return {"ya_es": "Tus hijos ya son tus beneficiarios", "registrar": "Registrarlos", "persona": persona,
                "titulo": "Registra a tus hijos en tu grupo familiar", "boton": "Registrar a tus hijos", "pieza": "P6"}
    return {"ya_es": "", "registrar": "", "persona": persona, "titulo": f"Registra a {persona} en tu grupo familiar",
            "boton": f"Registrar a {persona}", "pieza": "P6b"}


def _orden(af, d, col, casa, reparto, prima, beneficiarios_ok, brecha_pension):
    """El orden del plan: primero lo que no es producto, al final el producto si el plan lo pide."""
    pasos = []
    if _con_dependientes(d) and not beneficiarios_ok:
        rf = registro_familiar(d)
        from .. import catalogo as CAT
        texto = CAT.render(rf["pieza"], rf) + " Toma 2 minutos y no es un producto."
        pasos.append({"id": "beneficiaria", "cuando": "Hoy", "es_producto": False,
                      "titulo": rf["titulo"], "boton": rf["boton"], "texto": texto, "catalogo": [rf["pieza"]]})
    if _deuda_cara(d):
        pasos.append({"id": "deuda", "cuando": "Antes de invertir", "es_producto": False,
                      "titulo": "Paga primero tu deuda cara",
                      "texto": "Te cuesta más de lo que ganarías invirtiendo. No te recomiendo invertir todavía.",
                      "catalogo": ["P4"]})
    if prima and "junio" in af["lo_que_sabemos"]["primas"]:
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


def _dimensiones(af, d, beneficiarios_ok, ingreso, origen_ingreso, declarar):
    sabe = af["lo_que_sabemos"]
    if ingreso is None:
        flujo = f"Ingreso: sin tu permiso no usamos tu salario de cotización · gastos {millones(d['gastos_mensuales'])} · {d.get('deudas', '').lower()}"
        origen_flujo = "nos contaste"
    else:
        etiqueta = "Salario de cotización" if origen_ingreso == "sabemos" else "Ingreso que nos contaste"
        flujo = f"{etiqueta} {millones(ingreso)} · gastos {millones(d['gastos_mensuales'])} · {d.get('deudas', '').lower()}"
        origen_flujo = "sabemos y nos contaste" if origen_ingreso == "sabemos" else "nos contaste"
    if declarar and declarar["probable"]:
        impuestos = (f"Con tus ingresos estimados del año, unos {declarar['ingresos_txt']}, probablemente debas declarar "
                     f"renta en {declarar['anio_declara']} (el tope es de {declarar['tope_txt']}). Declarar no es lo mismo "
                     "que pagar impuesto: lo confirmamos con tu certificado de ingresos")
        origen_imp = "estimado"
    elif declarar:
        impuestos = "Por completar: lo vemos con tu certificado de ingresos"
        origen_imp = "por completar"
    else:
        impuestos = "Por completar: sin tu ingreso no lo estimamos"
        origen_imp = "por completar"
    dims = [
        ("Pensión y retiro", f"Pensión obligatoria {millones(sabe['saldo_pension_obligatoria'])} · {sabe['anios_cotizados']} años cotizados", "sabemos"),
        ("Ahorro e inversión", f"{millones(d['ahorro'])} · " + ", ".join(d.get("donde_ahorro", [])).lower(), "nos contaste"),
        ("Vivienda", d.get("vivienda", "") + f" · cesantías {millones(sabe['cesantias'])}"
         + (f" · meta: tu casa {d.get('plazo_casa', '').lower()}" if "Comprar mi casa" in d.get("metas", []) else ""), "sabemos y nos contaste"),
        ("Flujo de dinero y deudas", flujo, origen_flujo),
        ("Educación", "Meta elegida" if "Educar a mis hijos" in d.get("metas", []) else "Por conocer: la sumamos si quieres", "nos contaste" if "Educar a mis hijos" in d.get("metas", []) else "por completar"),
        ("Protección de la familia", ("Grupo familiar registrado" if beneficiarios_ok else "Grupo familiar por registrar") + f" · seguro de vida: {d.get('seguro_vida', 'no sé').lower()}", "sabemos y nos contaste"),
        ("Impuestos", impuestos, origen_imp),
        ("Legado", "Por conocer", "por completar"),
    ]
    return [{"nombre": a, "texto": b, "origen": c} for a, b, c in dims]
