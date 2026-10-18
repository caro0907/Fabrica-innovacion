"""Cálculos deterministas del arquitecto.

Funciones puras: los mismos datos siempre dan el mismo resultado. Ninguna cifra
que ve el afiliado se calcula fuera de este módulo (catálogo, regla 5.4.1).
Todos los montos están en pesos de hoy.
"""
import math
from dataclasses import dataclass, asdict

from . import supuestos as S


def tasa_mensual(tasa_anual: float) -> float:
    return (1 + tasa_anual) ** (1 / 12) - 1


def valor_futuro(inicial: float, aporte_mensual: float, meses: int, tasa_anual: float) -> float:
    r = tasa_mensual(tasa_anual)
    if r == 0:
        return inicial + aporte_mensual * meses
    return inicial * (1 + r) ** meses + aporte_mensual * (((1 + r) ** meses - 1) / r)


def factor_anualidad(anios: int, tasa_anual: float) -> float:
    if tasa_anual == 0:
        return float(anios)
    return (1 - (1 + tasa_anual) ** -anios) / tasa_anual


# Pensión -----------------------------------------------------------------------
@dataclass
class ProyeccionPension:
    mesada: float
    saldo_al_pensionarse: float
    edad_pension: int
    anios_para_pensionarse: int
    aporte_mensual_a_cuenta: float
    semanas_hoy: int
    semanas_transicion: int
    conserva_reglas_de_hoy: bool
    semanas_que_faltan_para_transicion: int

    def dict(self):
        return asdict(self)


def proyectar_pension(sexo: str, edad: int, saldo: float, salario: float, semanas: int,
                      semanas_cotizables_antes_reforma: int = 0,
                      tasa: float = S.RENTABILIDAD_REAL_ANUAL) -> ProyeccionPension:
    """Pensión estimada en el ahorro individual, con el mismo método para todas las personas.

    Acumula el saldo y la parte de la cotización que va a la cuenta individual con la
    rentabilidad real supuesta, neta de comisiones, hasta la edad de pensión. Convierte el
    saldo en 13 mesadas al año durante 30 años con la misma tasa.
    """
    edad_pension = S.EDAD_PENSION[sexo]
    anios = max(0, edad_pension - edad)
    aporte = salario * S.PORCENTAJE_A_CUENTA_INDIVIDUAL
    saldo_final = valor_futuro(saldo, aporte, anios * 12, tasa)
    mesada = saldo_final / (S.MESADAS_POR_ANIO * factor_anualidad(S.ANIOS_DE_PENSION, tasa))
    umbral = S.SEMANAS_TRANSICION[sexo]
    proyectadas = semanas + semanas_cotizables_antes_reforma
    return ProyeccionPension(
        mesada=mesada,
        saldo_al_pensionarse=saldo_final,
        edad_pension=edad_pension,
        anios_para_pensionarse=anios,
        aporte_mensual_a_cuenta=aporte,
        semanas_hoy=semanas,
        semanas_transicion=umbral,
        conserva_reglas_de_hoy=proyectadas >= umbral,
        semanas_que_faltan_para_transicion=max(0, umbral - semanas),
    )


# Colchón -------------------------------------------------------------------------
def colchon(gastos_mensuales: float, ahorro_disponible: float) -> dict:
    meta = gastos_mensuales * S.MESES_COLCHON_SANO
    meses = ahorro_disponible / gastos_mensuales if gastos_mensuales else 0
    return {
        "meta": meta,
        "tiene": ahorro_disponible,
        "meses_cubiertos": meses,
        "brecha": max(0.0, meta - ahorro_disponible),
        "completo": ahorro_disponible >= meta,
    }


# Prima -------------------------------------------------------------------------------
def prima_estimada(salario: float) -> float:
    return salario * S.FRACCION_PRIMA


def repartir_prima(prima: float, brecha_colchon: float) -> dict:
    """Regla del plan: mientras el colchón tenga brecha, hasta 70% de la prima va al colchón
    y el resto a la meta más importante. Si no hay brecha, todo va a la meta."""
    al_colchon = min(brecha_colchon, prima * S.PARTE_PRIMA_AL_COLCHON)
    return {"al_colchon": al_colchon, "a_la_meta": prima - al_colchon,
            "porcentaje_colchon": al_colchon / prima if prima else 0}


# Metas con simulador ------------------------------------------------------------------
def meses_para_meta(meta: float, inicial: float, aporte_mensual: float, tasa_anual: float,
                    tope_meses: int = 50 * 12) -> int | None:
    """Meses hasta llegar a la meta. None si no llega dentro del tope."""
    if inicial >= meta:
        return 0
    if aporte_mensual <= 0 and tasa_anual <= 0:
        return None
    r = tasa_mensual(tasa_anual)
    saldo = inicial
    for mes in range(1, tope_meses + 1):
        saldo = saldo * (1 + r) + aporte_mensual
        if saldo >= meta:
            return mes
    return None


def aporte_para_llegar(meta: float, inicial: float, meses: int, tasa_anual: float) -> float:
    """Aporte mensual que lleva de 'inicial' a 'meta' en 'meses'."""
    r = tasa_mensual(tasa_anual)
    falta = meta - inicial * (1 + r) ** meses
    if falta <= 0:
        return 0.0
    if r == 0:
        return falta / meses
    return falta * r / ((1 + r) ** meses - 1)


# Riesgo en pesos -------------------------------------------------------------------------
def caida_mal_anio(monto: float, portafolio: str) -> float:
    return monto * S.PORTAFOLIOS[portafolio]["caida_mal_anio"]


def costo_anual(monto: float, portafolio: str) -> float:
    return monto * S.PORTAFOLIOS[portafolio]["comision_anual"]


# Redondeo para mensajes (catálogo 5.5) ------------------------------------------------------
def redondear_millones(valor: float) -> float:
    """A la decena de mil, sin sesgo: se redondea al más cercano."""
    return round(valor / 10_000) * 10_000


def redondear_riesgo(valor: float) -> float:
    """Un riesgo nunca se redondea hacia abajo: al millar superior."""
    return math.ceil(valor / 1_000) * 1_000
