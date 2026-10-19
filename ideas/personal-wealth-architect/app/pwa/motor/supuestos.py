"""Supuestos del motor, versionados.

Cada cifra que ve el afiliado sale de estos supuestos y de sus datos. Las pantallas
muestran los mismos supuestos que usa el cálculo (criterio C9 de la fábrica).

Estado: propuestos por la fábrica para el MVP con datos ficticios. Los valores de
rentabilidad, comisión y caída en un mal año los debe aprobar cumplimiento
(regulatorio.md, sección 9, pregunta 8) antes de cualquier piloto real.
"""
from datetime import date

VERSION = "supuestos-2026.10-mvp1.1"

# Pensión obligatoria (ahorro individual) -----------------------------------
EDAD_PENSION = {"mujer": 57, "hombre": 62}
# De la cotización de 16%, la parte que va a la cuenta individual del afiliado.
PORCENTAJE_A_CUENTA_INDIVIDUAL = 0.115
RENTABILIDAD_REAL_ANUAL = 0.04          # neta de comisiones, en pesos de hoy
MESADAS_POR_ANIO = 13
ANIOS_DE_PENSION = 30
SEMANAS_TRANSICION = {"mujer": 750, "hombre": 900}   # a la fecha de entrada en vigor de la reforma
# Reforma pensional como dato versionado (recomendación de la vigía del 18 de octubre de 2026):
# si la fecha o las reglas cambian, se cambia aquí y todas las pantallas y textos del catálogo se actualizan.
REFORMA_PENSIONAL = {
    "norma": "Ley 2381 de 2024",
    "fecha_vigencia": date(2027, 4, 1),
    "fecha_texto": "1 de abril de 2027",
    "fuente": "Sentencia C-264 de 2026 (regulatorio.md, sección 1)",
    "estado_al": "2026-10-18",
    "vigilar": "Incidente de impacto fiscal abierto el 14 de octubre de 2026; por sí solo no cambia la fecha (vigia/2026-10-18.md)",
}
FECHA_REFORMA = REFORMA_PENSIONAL["fecha_texto"]

# Colchón ---------------------------------------------------------------------
MESES_COLCHON_SANO = 3

# Prima -----------------------------------------------------------------------
# La prima semestral equivale a medio salario mensual (Código Sustantivo del Trabajo, art. 306).
FRACCION_PRIMA = 0.5
# Mientras el colchón tenga brecha, hasta esta parte de la prima va al colchón.
PARTE_PRIMA_AL_COLCHON = 0.70

# Meta con simulador ------------------------------------------------------------
RENTABILIDAD_ESCENARIO_BUENO = 0.04     # real, neta de comisiones
RENTABILIDAD_ESCENARIO_MALO = 0.0       # sin rentabilidad

# Portafolios (ficticios) -------------------------------------------------------
PORTAFOLIOS = {
    "fic_moderado": {
        "nombre": "Fondo de inversión colectiva moderado",
        "comision_anual": 0.012,          # ficticia, hasta tener tarifa pública
        "caida_mal_anio": 0.12,           # método por aprobar (pregunta 8)
        "horizonte_minimo_anios": 3,
        "perfil_minimo": "moderado",
    },
}

# Perfil ------------------------------------------------------------------------
PERFILES_ORDEN = ["conservador", "moderado", "arriesgado"]
VIGENCIA_PERFIL_DIAS = 365

# Contacto (Ley 2300 de 2023) ----------------------------------------------------
HORARIO_CONTACTO = {
    "lunes_a_viernes": (7, 19),
    "sabado": (8, 15),
}
CONTACTOS_COMERCIALES_POR_SEMANA = 1

# Grupo de control ---------------------------------------------------------------
PORCENTAJE_GRUPO_CONTROL = 0.10

# Freno de servicio: líneas base ficticias del canal ------------------------------
FRENO_LINEAS_BASE = {
    "resolucion_sin_oficina": {"base": 0.82, "sentido": "mayor_es_mejor"},
    "satisfaccion": {"base": 0.87, "sentido": "mayor_es_mejor"},
    "transferencia_a_humano": {"base": 0.12, "sentido": "menor_es_mejor"},
}


def resumen():
    """Lo que la pantalla 'Ver supuestos' muestra, con los mismos valores del cálculo."""
    return {
        "version": VERSION,
        "rentabilidad_real": RENTABILIDAD_REAL_ANUAL,
        "porcentaje_cuenta": PORCENTAJE_A_CUENTA_INDIVIDUAL,
        "mesadas": MESADAS_POR_ANIO,
        "anios_pension": ANIOS_DE_PENSION,
    }
