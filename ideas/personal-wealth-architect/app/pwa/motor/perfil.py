"""Perfil del afiliado: seis preguntas, una por criterio del Decreto 2555, art. 2.40.1.1.5
(horizonte, objetivos, conocimiento, experiencia, capacidad de asumir pérdidas y tolerancia)."""

PREGUNTAS = [
    ("horizonte", "1 · Tu horizonte", "¿Para cuándo necesitas el dinero de tu meta?",
     ["Menos de 2 años", "De 2 a 5 años", "Más de 5 años"]),
    ("objetivo", "2 · Tus objetivos", "¿Qué buscas, sobre todo?",
     ["Que no baje", "Que crezca un poco", "Que crezca para mi meta"]),
    ("conocimiento", "3 · Tu conocimiento", "¿Qué tanto sabes de inversiones?", ["Nada", "Lo básico", "Bastante"]),
    ("experiencia", "4 · Tu experiencia", "¿Has invertido, además de tu pensión y tus cesantías?",
     ["Nunca", "Alguna vez", "Con frecuencia"]),
    ("perdida", "5 · Cuánto puedes perder", "En un mal año, ¿cuánto podría bajar sin afectar tu vida?",
     ["Nada", "Hasta 5 de cada 100 pesos", "Hasta 15 de cada 100 pesos", "Más"]),
    ("reaccion", "6 · Cómo reaccionas a las bajas",
     "Si pusieras $1.000.000 y en un mal año bajara a $880.000, ¿qué harías?", ["Lo saco todo", "Espero", "Pongo más"]),
]

PERDIDA = {"Nada": 0.0, "Hasta 5 de cada 100 pesos": 0.05, "Hasta 15 de cada 100 pesos": 0.15, "Más": 0.25}


def completo(perfil: dict) -> bool:
    return bool(perfil) and all(perfil.get(k) in opciones for k, _, _, opciones in PREGUNTAS)


def perdida_tolerada(perfil: dict) -> float:
    return PERDIDA.get(perfil.get("perdida", "Nada"), 0.0)


def clasificar(perfil: dict) -> str:
    if not completo(perfil):
        return "sin perfil"
    if (perdida_tolerada(perfil) < 0.05 or perfil["objetivo"] == "Que no baje"
            or perfil["horizonte"] == "Menos de 2 años" or perfil["reaccion"] == "Lo saco todo"):
        return "conservador"
    if perfil["perdida"] == "Más" and perfil["reaccion"] == "Pongo más" and perfil["conocimiento"] == "Bastante":
        return "arriesgado"
    return "moderado"


OBJETIVO_TXT = {"Que no baje": "que no baje", "Que crezca un poco": "que crezca un poco",
                "Que crezca para mi meta": "que crezca para tu meta"}
REACCION_TXT = {"Lo saco todo": "lo sacas todo", "Espero": "esperas", "Pongo más": "pones más"}


def resumen(perfil: dict) -> str:
    clase = clasificar(perfil)
    if clase == "sin perfil":
        return "Aún no tienes perfil"
    return (f"{clase.capitalize()}: tu meta es a {perfil['horizonte'].lower()}, quieres "
            f"{OBJETIVO_TXT[perfil['objetivo']]}, en un mal año aceptas bajas de {perfil['perdida'].lower()} "
            f"y {REACCION_TXT[perfil['reaccion']]} cuando el mercado baja.")
