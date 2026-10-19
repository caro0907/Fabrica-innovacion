"""Mandatos: reglas que el afiliado deja andando, con siete campos y revocación en un toque.

Mandatos no discrecionales (regulatorio.md, sección 6 y riesgo R13): el afiliado fija el
porcentaje, el destino, el tope y la vigencia; el sistema solo dispara. Si algo cambia
(por ejemplo, el salario), el sistema propone y el afiliado confirma.
En el MVP ningún mandato mueve dinero: la ejecución es simulada.
"""
from dataclasses import dataclass, asdict, field
from datetime import date

from . import supuestos as S
from .formato import pesos

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]


def fecha_txt(iso: str) -> str:
    f = date.fromisoformat(iso)
    return f"{f.day} de {MESES[f.month - 1]} de {f.year}"

CONTROLES = {
    "informar": "Te aviso; tú decides y actúas",
    "proponer_y_confirmar": "Te propongo y tú confirmas cada vez",
    "ejecutar_dentro_de_limites": "Lo hago solo dentro del tope y te aviso después",
}

# Las pausas que el MVP de verdad revisa en cada pantalla (revisar_pausas). Solo estas se muestran
# al afiliado (H10). Las otras dos del concepto quedan para producción.
PAUSAS_AUTOMATICAS = [
    "Pérdida de empleo o fin de la cotización",
    "Queja abierta",
    "Perfil vencido",
]
PAUSAS_PARA_PRODUCCION = [
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
    tope: float                             # lo que va a inversión en cada prima no pasa de aquí
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


def texto_consentimiento(m: "Mandato", pct_colchon: int) -> str:
    """Texto de la revisión del experto financiero (H7), en primera persona, pendiente de aprobación de jurídico.
    En "te propongo y tú confirmas" no hay nada que revertir: si la persona no confirma, no se mueve nada."""
    return (f"Autorizo a mi administradora de fondos a proponerme, dos semanas antes de cada prima (junio y diciembre) "
            f"y hasta el {fecha_txt(m.vigencia_hasta)}, separar el {pct_colchon}% para mi colchón en mi cuenta de ahorros, "
            f"mientras no llegue a {S.MESES_COLCHON_SANO} meses de mis gastos, y el resto para mi casa, sin pasar de "
            f"{pesos(m.tope)} a inversión por prima. Un día antes de que llegue la prima me recuerdan confirmar. "
            "Cada vez confirmo yo; si no confirmo, no se mueve nada. La cancelo en Mis reglas.")


def prima_con_rumbo(afiliado_id: str, hoy: date, porcentaje_colchon: float,
                    tope: float = S.TOPE_INVERSION_POR_PRIMA) -> Mandato:
    pct = round(porcentaje_colchon * 100)
    fin = hoy.month - 1 + S.VIGENCIA_MANDATO_MESES
    m = Mandato(
        id=f"{afiliado_id}-prima-con-rumbo",
        afiliado_id=afiliado_id,
        nombre="Prima con rumbo",
        disparador="Llegue tu prima (junio y diciembre)",
        accion=(f"proponerte separar el {pct}% para tu colchón, hasta llegar a {S.MESES_COLCHON_SANO} meses, "
                f"y el resto para tu casa"),
        destino="tu colchón, en tu cuenta de ahorros, y tu casa",
        tope=tope,
        vigencia_hasta=date(hoy.year + fin // 12, fin % 12 + 1, hoy.day).isoformat(),
        aviso="Te propongo dos semanas antes y te recuerdo confirmar un día antes, con opción de saltar esa vez",
        control="proponer_y_confirmar",
        creado=hoy.isoformat(),
    )
    m.consentimiento = texto_consentimiento(m, pct)
    return m


def propuesta_de_la_regla(m: Mandato, prima: float, brecha_colchon: float, porcentaje_colchon: float) -> dict:
    """Lo que la regla propone en una prima: el tope limita lo que va a inversión; lo que lo pasa
    se queda en la cuenta de la persona, sin moverse (tope que limita de verdad, hallazgo 3 del revisor)."""
    al_colchon = min(brecha_colchon, prima * porcentaje_colchon)
    a_la_casa = prima - al_colchon
    a_inversion = min(a_la_casa, m.tope)
    return {"al_colchon": al_colchon, "a_inversion": a_inversion, "queda_en_tu_cuenta": a_la_casa - a_inversion}


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
    """Se pausa sola ante los eventos de la sección 6 del concepto regulatorio. Se llama en cada pantalla."""
    if m.estado != "activo":
        return m
    if hoy.isoformat() > m.vigencia_hasta:
        m.estado = "cancelado"
        m.motivo_estado = "Terminó su vigencia"
        m.historial.append({"fecha": hoy.isoformat(), "evento": "vencido"})
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
