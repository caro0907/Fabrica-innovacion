"""Mandatos: reglas que el afiliado deja andando, con siete campos y revocación en un toque.

Mandatos no discrecionales (regulatorio.md, sección 6 y riesgo R13): el afiliado fija el
porcentaje, el destino, el tope y la vigencia; el sistema solo dispara. Si algo cambia
(por ejemplo, el salario), el sistema propone y el afiliado confirma.
En el MVP ningún mandato mueve dinero: la ejecución es simulada.
"""
from dataclasses import dataclass, asdict, field
from datetime import date

from .formato import pesos

CONTROLES = {
    "informar": "Te aviso; tú decides y actúas",
    "proponer_y_confirmar": "Te propongo y tú confirmas cada vez",
    "ejecutar_dentro_de_limites": "Lo hago solo dentro del tope y te aviso después",
}

PAUSAS_AUTOMATICAS = [
    "Pérdida de empleo o fin de la cotización",
    "Queja abierta sobre la regla",
    "Perfil vencido",
    "Cambio de la ley que afecte el beneficio",
    "Dos ejecuciones fallidas seguidas",
]


@dataclass
class Mandato:
    id: str
    afiliado_id: str
    nombre: str
    disparador: str
    accion: str
    destino: str
    tope: float
    vigencia_hasta: str
    aviso: str
    control: str
    estado: str = "activo"                  # activo | pausado | cancelado
    motivo_estado: str = ""
    creado: str = ""
    consentimiento: str = ""
    historial: list = field(default_factory=list)

    def dict(self):
        return asdict(self)


def texto_consentimiento(nombre_entidad: str, m: "Mandato", origen: str) -> str:
    """Texto propuesto en regulatorio.md, sección 6, pendiente de aprobación de jurídico."""
    return (f"Autorizo a {nombre_entidad} a {m.accion} a {m.destino} cada vez que {m.disparador.lower()}, "
            f"desde {origen}, con un tope de {pesos(m.tope)} cada vez y hasta el {m.vigencia_hasta}. "
            f"Me avisará {m.aviso.lower()}. Puedo pausar o cancelar esta regla en cualquier momento escribiendo "
            "'cancela mi regla' o desde Mis reglas. Si la regla ejecuta algo distinto a lo que autorizo, la entidad lo revierte.")


def prima_con_rumbo(afiliado_id: str, hoy: date, porcentaje_colchon: float, tope: float) -> Mandato:
    m = Mandato(
        id=f"{afiliado_id}-prima-con-rumbo",
        afiliado_id=afiliado_id,
        nombre="Prima con rumbo",
        disparador="Llegue tu prima (junio y diciembre)",
        accion=(f"proponerte separar el {round(porcentaje_colchon * 100)}% para tu colchón y el "
                f"{100 - round(porcentaje_colchon * 100)}% para tu casa"),
        destino="tu colchón, en tu cuenta de ahorros, y tu meta de casa",
        tope=tope,
        vigencia_hasta=date(hoy.year + 1, hoy.month, hoy.day).isoformat(),
        aviso="Dos semanas antes de cada prima, con la opción de saltarla esa vez",
        control="proponer_y_confirmar",
        creado=hoy.isoformat(),
    )
    m.consentimiento = texto_consentimiento("tu administradora", m, "la cuenta donde recibes tu prima")
    return m


def pausar(m: Mandato, motivo: str, hoy: date) -> Mandato:
    if m.estado == "cancelado":
        return m
    m.estado = "pausado"
    m.motivo_estado = motivo
    m.historial.append({"fecha": hoy.isoformat(), "evento": "pausado", "motivo": motivo})
    return m


def reanudar(m: Mandato, hoy: date) -> Mandato:
    if m.estado == "pausado":
        m.estado = "activo"
        m.motivo_estado = ""
        m.historial.append({"fecha": hoy.isoformat(), "evento": "reanudado"})
    return m


def cancelar(m: Mandato, hoy: date) -> Mandato:
    m.estado = "cancelado"
    m.historial.append({"fecha": hoy.isoformat(), "evento": "cancelado"})
    return m


def revisar_pausas(m: Mandato, estado_afiliado: dict, perfil_vigente: bool, hoy: date) -> Mandato:
    """Se pausa sola ante los eventos de la sección 6 del concepto regulatorio."""
    if m.estado != "activo":
        return m
    if estado_afiliado.get("perdida_empleo"):
        return pausar(m, PAUSAS_AUTOMATICAS[0], hoy)
    if estado_afiliado.get("queja_abierta"):
        return pausar(m, PAUSAS_AUTOMATICAS[1], hoy)
    if not perfil_vigente:
        return pausar(m, PAUSAS_AUTOMATICAS[2], hoy)
    return m


def desde_dict(d: dict) -> Mandato:
    return Mandato(**d)
