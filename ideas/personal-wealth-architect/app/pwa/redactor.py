"""El redactor: la IA conversa, el motor calcula, el control revisa.

Dos modos, con el mismo control:
- 'plantillas' (por defecto, costo cero): compone las piezas del catálogo que el motor elige.
- 'claude' (si existe ANTHROPIC_API_KEY): el modelo solo puede elegir el orden de las piezas
  que el motor ya autorizó y escribir 'puentes' cortos sin cifras entre ellas. El control del
  catálogo valida todo antes de mostrarlo; si algo no pasa, se usa la versión de plantillas.

La IA nunca calcula ni escribe una cifra: las cifras vienen como variables del motor.
"""
import json
import os

from . import catalogo as CAT

MODELO = os.environ.get("PWA_MODELO", "claude-haiku-5-5")


def modo() -> str:
    return "claude" if os.environ.get("ANTHROPIC_API_KEY") else "plantillas"


def nota_del_arquitecto(piezas: list[str], variables: dict, contexto: dict, persona: str) -> dict:
    """Devuelve el texto validado, las piezas usadas y el modo con que se redactó."""
    base = CAT.componer(piezas, variables, contexto)
    if modo() != "claude":
        return {"texto": base.texto, "piezas": base.piezas, "modo": "plantillas", "textos": base.textos}
    try:
        orden, puentes = _pedir_a_claude(base, persona)
        comp = CAT.componer(orden, variables, contexto, puentes)
        if set(comp.piezas) != set(base.piezas):
            raise CAT.TextoNoPermitido("El modelo cambió las piezas autorizadas")
        return {"texto": comp.texto, "piezas": comp.piezas, "modo": "claude", "textos": comp.textos}
    except Exception as e:  # cualquier falla vuelve a la versión de plantillas, que ya pasó el control
        return {"texto": base.texto, "piezas": base.piezas, "modo": "plantillas", "textos": base.textos,
                "aviso": f"Se usó la versión de plantillas: {type(e).__name__}"}


def _pedir_a_claude(base: CAT.Composicion, persona: str) -> tuple[list[str], list[str]]:
    import anthropic

    cliente = anthropic.Anthropic()
    piezas = [{"id": pid, "texto": t} for pid, t in zip(base.piezas, base.textos)]
    instruccion = (
        "Eres el redactor de un arquitecto de patrimonio. Solo puedes ordenar las piezas que te doy "
        "y escribir, si ayuda, un puente muy corto antes de cada pieza para que se lea natural para "
        f"{persona}. Reglas: no cambies ni resumas las piezas; los puentes no llevan cifras, promesas, "
        "urgencia ni la palabra 'garantizado'; máximo 12 palabras por puente. Responde solo JSON: "
        '{"orden": ["ID", ...], "puentes": ["", ...]} con un puente por pieza (vacío si no hace falta).'
    )
    r = cliente.messages.create(
        model=MODELO,
        max_tokens=400,
        temperature=0,
        system=instruccion,
        messages=[{"role": "user", "content": json.dumps(piezas, ensure_ascii=False)}],
    )
    texto = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    datos = json.loads(texto[texto.find("{"): texto.rfind("}") + 1])
    return list(datos["orden"]), [str(p) for p in datos.get("puentes", [])]


# La pregunta (superficie secundaria) -------------------------------------------------------
INTENCIONES = [
    ("colchon", ["colchón", "colchon", "emergencia", "tranquilidad"]),
    ("casa", ["casa", "vivienda", "cuota inicial"]),
    ("pension", ["pensión", "pension", "retiro", "jubil"]),
    ("prima", ["prima"]),
    ("cesantias", ["cesantía", "cesantia"]),
    ("asesor", ["hablar con alguien", "asesor", "consultor", "persona", "daniela"]),
    ("impuesto", ["impuesto", "renta", "declarar"]),
]


def intencion(pregunta: str) -> str:
    p = pregunta.lower()
    for nombre, claves in INTENCIONES:
        if any(c in p for c in claves):
            return nombre
    return "otra"
