"""Formato de cifras en español de Colombia."""
from .calculos import redondear_millones


def pesos(valor: float) -> str:
    """$1.820.000"""
    return "$" + f"{round(valor):,}".replace(",", ".")


def millones(valor: float) -> str:
    """$45 M · $9,4 M · $3,0 M · $6,65 M (redondeo a la decena de mil, sin sesgo)."""
    v = redondear_millones(valor) / 1_000_000
    centesimas = round(v * 100)
    if centesimas % 10:
        txt = f"{v:.2f}"
    elif v >= 10 and centesimas % 100 == 0:
        txt = f"{v:.0f}"
    else:
        txt = f"{v:.1f}"
    return "$" + txt.replace(".", ",") + " M"


def miles(valor: float) -> str:
    """$100 mil"""
    return f"${int(round(valor / 1_000))} mil"


def porcentaje(valor: float, decimales: int = 0) -> str:
    return f"{valor * 100:.{decimales}f}%".replace(".", ",")


def meses_txt(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",")
