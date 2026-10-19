"""Catálogo de lo que se puede decir, como datos versionados, y su control.

Reglas que este módulo hace cumplir en código:
- Ningún texto para el afiliado se escribe fuera del catálogo: se compone con piezas
  por identificador y variables que calcula el motor.
- Cada beneficio arrastra sus condiciones y advertencias obligatorias (campo 'requiere').
- Un beneficio con condición (por ejemplo, 'paga_impuesto') no se usa si la condición no se cumple.
- Las frases prohibidas de la sección 5.4 se rechazan, vengan de donde vengan.
- Los 'puentes' que puede escribir la IA entre piezas no llevan cifras (ni en números ni en letras)
  ni frases prohibidas.
- Coherencia (criterio A7): una pieza que dice "no te recomiendo invertir" no sale en una pantalla que
  lleva a una recomendación de inversión.
"""
import json
import re
import string
from dataclasses import dataclass, field
from pathlib import Path

_RUTA = Path(__file__).with_name("catalogo_v1.json")
CATALOGO = json.loads(_RUTA.read_text(encoding="utf-8"))
VERSION = CATALOGO["version"]
PIEZAS = CATALOGO["piezas"]
_NUNCA = [(n["id"], re.compile(n["patron"], re.IGNORECASE), n["motivo"]) for n in CATALOGO["nunca"]]
_PERMITIDAS = [f.lower() for f in CATALOGO.get("frases_permitidas_que_contienen_patrones", [])]
_DIGITO = re.compile(r"\d")
_NUMERO_EN_LETRAS = re.compile(
    r"\b(dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|treinta|cuarenta|cincuenta|"
    r"cien|ciento|cientos|mil|miles|mill[oó]n|millones|bill[oó]n|por ciento|mitad|doble|triple)\b", re.IGNORECASE)
LARGO_MAXIMO_PUENTE = 140


class TextoNoPermitido(ValueError):
    """El control de cumplimiento rechazó un texto antes de mostrarlo."""


@dataclass
class Composicion:
    piezas: list[str]
    textos: list[str]
    puentes: list[str] = field(default_factory=list)

    @property
    def texto(self) -> str:
        partes = []
        for i, t in enumerate(self.textos):
            if i < len(self.puentes) and self.puentes[i]:
                partes.append(self.puentes[i])
            partes.append(t)
        return " ".join(partes)


def variables_de(pieza_id: str) -> set[str]:
    return {v for _, v, _, _ in string.Formatter().parse(PIEZAS[pieza_id]["texto"]) if v}


def frases_prohibidas(texto: str) -> list[str]:
    limpio = texto.lower()
    for f in _PERMITIDAS:
        limpio = limpio.replace(f, " ")
    return [f"{nid}: {motivo}" for nid, patron, motivo in _NUNCA if patron.search(limpio)]


def render(pieza_id: str, variables: dict | None = None) -> str:
    if pieza_id not in PIEZAS:
        raise TextoNoPermitido(f"La pieza {pieza_id} no está en el catálogo {VERSION}")
    variables = variables or {}
    faltan = variables_de(pieza_id) - set(variables)
    if faltan:
        raise TextoNoPermitido(f"A la pieza {pieza_id} le faltan variables del motor: {sorted(faltan)}")
    return PIEZAS[pieza_id]["texto"].format(**{k: variables[k] for k in variables_de(pieza_id)})


def con_acompanantes(ids: list[str], contexto: dict | None = None) -> list[str]:
    """Agrega las condiciones y advertencias que cada pieza exige, sin repetir.
    'requiere_si' agrega una advertencia solo si se cumple una condición del afiliado
    (por ejemplo, "usamos tu salario porque nos autorizaste" solo si lo autorizó)."""
    contexto = contexto or {}
    salida: list[str] = []
    for pid in ids:
        if pid not in salida:
            salida.append(pid)
    for pid in list(salida):
        reqs = list(PIEZAS[pid].get("requiere", []))
        for cond, extra in PIEZAS[pid].get("requiere_si", {}).items():
            if contexto.get(cond):
                reqs += extra
        for req in reqs:
            if req not in salida:
                salida.append(req)
    return salida


def componer(ids: list[str], variables: dict, contexto: dict, puentes: list[str] | None = None) -> Composicion:
    """Compone y valida. 'contexto' trae las condiciones del afiliado (paga_impuesto, autoriza_uso_salario...)."""
    puentes = puentes or []
    for pid in ids:
        if pid not in PIEZAS:
            raise TextoNoPermitido(f"La pieza {pid} no está en el catálogo {VERSION}")
        cond = PIEZAS[pid].get("condicion")
        if cond and not contexto.get(cond, False):
            raise TextoNoPermitido(f"La pieza {pid} exige '{cond}' y el afiliado no la cumple")
        if PIEZAS[pid].get("contradice_recomendacion") and contexto.get("recomienda_inversion"):
            raise TextoNoPermitido(f"La pieza {pid} contradice la recomendación de inversión de la misma pantalla")
    completas = con_acompanantes(ids, contexto)
    textos = [render(pid, variables) for pid in completas]
    for p in puentes:
        validar_puente(p)
    comp = Composicion(piezas=completas, textos=textos, puentes=list(puentes))
    problemas = frases_prohibidas(comp.texto)
    if problemas:
        raise TextoNoPermitido("; ".join(problemas))
    return comp


def validar_puente(texto: str) -> None:
    if len(texto) > LARGO_MAXIMO_PUENTE:
        raise TextoNoPermitido("El puente es demasiado largo")
    if _DIGITO.search(texto):
        raise TextoNoPermitido("Un puente no puede llevar cifras: las cifras vienen del motor")
    if _NUMERO_EN_LETRAS.search(texto):
        raise TextoNoPermitido("Un puente no puede llevar cifras en letras: las cifras vienen del motor")
    problemas = frases_prohibidas(texto)
    if problemas:
        raise TextoNoPermitido("; ".join(problemas))


def permitida(pieza_id: str, contexto: dict) -> bool:
    """¿La pieza se puede usar con este afiliado y en esta pantalla?"""
    p = PIEZAS[pieza_id]
    if p.get("condicion") and not contexto.get(p["condicion"]):
        return False
    if p.get("contradice_recomendacion") and contexto.get("recomienda_inversion"):
        return False
    return True


def validar_texto_libre(texto: str) -> list[str]:
    """Para revisar textos fijos de la interfaz: devuelve las frases prohibidas que encuentre."""
    return frases_prohibidas(texto)
