"""Escenarios y acciones del motor, como datos con ciclo de vida.

Los restrictivos se evalúan primero y bloquean toda acción comercial, sin excepción.
Solo los escenarios en estado 'activo' (y 'piloto' para su subconjunto) se evalúan:
'candidato' y 'en revisión' esperan validación humana; 'retirado' no se usa.
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Callable

ESTADOS = ["candidato", "en revisión", "piloto", "activo", "retirado"]


@dataclass
class Escenario:
    id: str
    nombre: str
    tipo: str                       # restrictivo | oportunidad
    estado: str
    disparador: str
    efecto: str
    condicion: Callable[[dict], bool] = field(repr=False)
    acciones: list[str] = field(default_factory=list)
    norma: str = ""


def _f(ctx: dict) -> dict:
    return ctx["afiliado"]["estado"]


ESCENARIOS: list[Escenario] = [
    # Restrictivos: prioridad absoluta -----------------------------------------------
    Escenario("R-QUEJA", "Queja abierta", "restrictivo", "activo", "Queja o reclamo sin resolver",
              "Ningún contacto comercial hasta cerrar la queja", lambda c: _f(c)["queja_abierta"]),
    Escenario("R-NOCONTACTO", "Solicitud de no contacto", "restrictivo", "activo", "Pidió no ser contactado",
              "Ningún contacto comercial", lambda c: _f(c)["no_contacto"]),
    Escenario("R-EMPLEO", "Pérdida de empleo", "restrictivo", "activo", "El empleador dejó de cotizar o informó terminación",
              "Modo servicio: cesantías, colchón y Mecanismo de Protección al Cesante; nada de venta; pausa reglas",
              lambda c: _f(c)["perdida_empleo"], ["servicio_cesantias"], "Ley 50 de 1990, art. 102; Ley 1636 de 2013"),
    Escenario("R-COYUNTURA", "Coyuntura crítica", "restrictivo", "activo", "Emergencia declarada en su zona",
              "Protocolo de comunicación de emergencia", lambda c: _f(c)["coyuntura_critica"]),
    Escenario("R-SENSIBLE", "Evento de vida sensible", "restrictivo", "activo", "Licencia, calamidad",
              "Solo servicio", lambda c: _f(c)["evento_sensible"]),
    Escenario("R-DEUDA", "Deuda cara sin colchón", "restrictivo", "activo", "Deuda a cuotas y colchón menor a 3 meses",
              "No recomendar inversión; primero deuda y colchón",
              lambda c: c["plan"]["deuda_cara"] and not c["plan"]["colchon"]["completo"], ["pagar_deuda"]),
    # Retirado el 19 de octubre de 2026 (revisión del MVP v1, H17): retirar el permiso del salario no
    # es un restrictivo general. El plan deja de estimar lo que depende del ingreso (plan.py) y las
    # acciones que lo necesitan, como la prima, dejan de ser elegibles.
    Escenario("R-AUTORIZACION", "Sin autorización de uso del salario", "restrictivo", "retirado",
              "No autorizó usar su salario de cotización para su plan",
              "Reemplazado: el plan no estima lo que depende del ingreso", lambda c: not _f(c)["autoriza_uso_salario"],
              norma="Ley 1581 de 2012"),
    Escenario("R-PERFIL", "Perfil vencido o inexistente", "restrictivo", "activo", "El perfil no cubre los seis criterios",
              "Pide actualizar el perfil antes de recomendar", lambda c: not c.get("perfil_vigente", False),
              norma="Decreto 2555, art. 2.40.1.1.5"),
    Escenario("R-VULNERABLE", "Señales de no comprender", "restrictivo", "activo",
              "No marca la casilla de comprensión dos veces o pide ayuda",
              "Ofrece al asesor y no ejecuta en el canal digital", lambda c: c.get("senales_no_comprende", 0) >= 2,
              norma="Ley 1328 de 2009, art. 3"),

    # Oportunidad --------------------------------------------------------------------
    Escenario("O-PRIMA", "Prima con rumbo", "oportunidad", "activo", "Prima en 2 semanas o menos y prima estimable",
              "Plan de la prima por metas y una regla para la siguiente",
              lambda c: 0 <= c["dias_para_prima"] <= 15 and c["plan"]["prima"] is not None, ["colchon_con_prima", "casa_con_prima", "regla_prima"]),
    Escenario("O-BENEFICIARIOS", "Grupo familiar por registrar", "oportunidad", "activo",
              "Dependientes declarados y grupo familiar sin registrar", "Registrar el grupo familiar (no es un producto)",
              lambda c: bool(c["plan"]["dependiente"]) and not c["plan"]["beneficiarios_confirmados"], ["confirmar_beneficiarios"]),
    Escenario("O-PENSION", "Brecha pensional", "oportunidad", "activo", "Pensión estimada por debajo de la meta",
              "Revisión de la pensión en diciembre", lambda c: c["plan"]["pension"]["brecha"] > 0, ["revisar_pension"]),
    Escenario("O-ESCALADOR", "Aumento de salario", "oportunidad", "piloto", "Cambio del salario de cotización",
              "Proponer subir el aporte en la misma proporción", lambda c: c.get("subio_salario", False), ["escalador"]),
    Escenario("O-DICIEMBRE", "Diciembre de oro", "oportunidad", "activo", "Renta media, noviembre, faltante al punto óptimo",
              "Completar el punto óptimo de la pensión voluntaria",
              lambda c: c["afiliado"]["segmento"] == "renta_media" and c["hoy"].month in (11, 12), ["punto_optimo"]),
    Escenario("O-FUGA", "Riesgo de fuga", "oportunidad", "candidato", "Retiros o señales de traslado",
              "Conversación de conservación con el plan a la vista", lambda c: False, ["conservacion"]),
]


@dataclass
class Accion:
    id: str
    nombre: str
    es_producto: bool
    comercial: bool
    quien: str                      # agente | asesor | agente_o_asesor
    nivel: str                      # muestra | recomienda | ejecuta | mandato
    meta: str
    objetivo_negocio: str
    angulo: str
    piezas: list[str]
    portafolio: str = ""


ACCIONES: dict[str, Accion] = {a.id: a for a in [
    Accion("confirmar_beneficiarios", "Registrar el grupo familiar", False, False, "agente", "ejecuta",
           "proteccion", "Relación y confianza", "proteger a su familia", ["P6"]),
    Accion("colchon_con_prima", "Separar parte de la prima para el colchón", False, False, "agente", "muestra",
           "colchon", "Experiencia y conservación", "tranquilidad", ["P9", "P5"]),
    Accion("casa_con_prima", "Invertir parte de la prima para la casa", True, True, "agente", "recomienda",
           "casa", "Depósito neto", "su casa", ["B14", "C3", "C4", "C5", "A9"], "fpv_moderado"),
    Accion("regla_prima", "Regla para la próxima prima", False, True, "agente", "mandato",
           "casa", "Depósito neto", "su casa", ["B6"]),
    Accion("revisar_pension", "Revisar la pensión en diciembre", False, False, "agente_o_asesor", "muestra",
           "pension", "Activos administrados", "su pensión", ["B12"]),
    Accion("servicio_cesantias", "Entregar sus cesantías y proteger su colchón", False, False, "agente", "ejecuta",
           "colchon", "Conservación y NPS", "tranquilidad", ["B9", "B10"]),
    Accion("pagar_deuda", "Pagar primero la deuda cara", False, False, "agente", "muestra",
           "colchon", "Confianza y NPS", "tranquilidad", ["P4"]),
    Accion("escalador", "Subir el aporte con el salario", True, True, "agente", "mandato",
           "pension", "Depósito neto", "su pensión", []),
    Accion("punto_optimo", "Completar el punto óptimo", True, True, "agente_o_asesor", "recomienda",
           "casa", "Depósito neto", "su impuesto", ["B2"]),
    Accion("conservacion", "Conversación de conservación", False, True, "asesor", "muestra",
           "pension", "Conservación", "continuidad del plan", ["P8"]),
]}


def evaluar(ctx: dict) -> dict:
    """Devuelve los escenarios activos para el afiliado, restrictivos primero, con su traza."""
    traza = []
    restrictivos, oportunidades = [], []
    for e in ESCENARIOS:
        if e.estado not in ("activo", "piloto"):
            traza.append({"escenario": e.id, "resultado": f"no se evalúa: estado {e.estado}"})
            continue
        if e.estado == "piloto" and not ctx.get("en_piloto", False):
            traza.append({"escenario": e.id, "resultado": "no se evalúa: el afiliado no está en el piloto"})
            continue
        try:
            aplica = bool(e.condicion(ctx))
        except KeyError:
            aplica = False
        traza.append({"escenario": e.id, "resultado": "aplica" if aplica else "no aplica"})
        if aplica:
            (restrictivos if e.tipo == "restrictivo" else oportunidades).append(e)
    return {"restrictivos": restrictivos, "oportunidades": oportunidades, "traza": traza}
