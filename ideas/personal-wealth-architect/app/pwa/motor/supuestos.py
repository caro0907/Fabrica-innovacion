"""Supuestos del motor, versionados.

Cada cifra que ve el afiliado sale de estos supuestos y de sus datos. Las pantallas
muestran los mismos supuestos que usa el cálculo (criterio C9 de la fábrica).

Estado: propuestos por la fábrica para el MVP con datos ficticios. Los valores de
rentabilidad, comisión y caída en un mal año los debe aprobar cumplimiento
(regulatorio.md, sección 9, pregunta 8) antes de cualquier piloto real.
"""
from datetime import date

VERSION = "supuestos-2026.10-mvp1.2"

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
RENTABILIDAD_ESCENARIO_MALO = 0.0       # sin rentabilidad, después de un mal año (ver CAIDA_ESCENARIO_MALO)

# Portafolios (ficticios) -------------------------------------------------------
# Opción A del experto financiero (revisión del 18 de octubre de 2026, H2): una administradora de
# fondos de pensiones y cesantías no administra fondos de inversión colectiva, así que la
# recomendación es un portafolio de su propio fondo de pensiones voluntarias. Lectura a validar
# con jurídico (regulatorio.md, sección 9, pregunta 12).
PORTAFOLIOS = {
    "fpv_moderado": {
        "nombre": "Portafolio moderado de tu fondo de pensiones voluntarias",
        "nombre_corto": "portafolio moderado de pensiones voluntarias",
        "comision_anual": 0.012,          # ficticia, hasta tener tarifa pública
        "caida_mal_anio": 0.12,           # método por aprobar (pregunta 8)
        "horizonte_minimo_anios": 3,
        "perfil_minimo": "moderado",
    },
}

# Mandato "Prima con rumbo" (diseño v5.2, pantalla Mis reglas) -------------------
TOPE_INVERSION_POR_PRIMA = 1_000_000     # lo que va a inversión en cada prima no pasa de aquí
VIGENCIA_MANDATO_MESES = 12

# Obligación de declarar renta (empresa/beneficios-tributarios.md, v2) ----------------
UVT = {2026: 52_374}                      # DIAN, año gravable 2026
TOPE_INGRESOS_DECLARAR_UVT = 1_400
TASA_INTERESES_CESANTIAS = 0.12

# Festivos de Colombia (Ley 51 de 1983). Sin contacto comercial en festivos (Ley 2300 de 2023).
# Fuente: calendario oficial de festivos 2026, consultado el 19 de octubre de 2026.
FESTIVOS = {
    date(2026, 1, 1), date(2026, 1, 12), date(2026, 3, 23), date(2026, 4, 2), date(2026, 4, 3),
    date(2026, 5, 1), date(2026, 5, 18), date(2026, 6, 8), date(2026, 6, 15), date(2026, 6, 29),
    date(2026, 7, 20), date(2026, 8, 7), date(2026, 8, 17), date(2026, 10, 12), date(2026, 11, 2),
    date(2026, 11, 16), date(2026, 12, 8), date(2026, 12, 25),
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
