"""Afiliados ficticios del MVP.

Solo datos inventados. Ninguna persona, cifra o dato de este archivo es real.

'lo_que_sabemos' es lo que la entidad ya tiene y no le pregunta al afiliado
(se usa solo con su autorización). 'diagnostico_propuesto' son las cifras que
el arquitecto propone en la primera reunión y que la persona ajusta.
"""
from copy import deepcopy

AFILIADOS = {
    "laura": {
        "id": "laura",
        "nombre": "Laura",
        "sexo": "mujer",
        "edad": 36,
        "segmento": "renta_masiva",
        "arquetipo": "pragmatica",
        "ciudad": "Medellín",
        "lo_que_sabemos": {
            "saldo_pension_obligatoria": 78_000_000,
            "anios_cotizados": 14,
            "semanas_cotizadas": 730,
            "salario_cotizacion": 5_200_000,
            "cesantias": 9_400_000,
            "comision_pension_anual": 0.012,   # ficticia
            "primas": ["junio", "diciembre"],
            "beneficiarios_confirmados": False,
            "cotiza_activamente": True,
        },
        "diagnostico_propuesto": {
            "metas": ["Tener tranquilidad", "Comprar mi casa", "Pensionarme bien"],
            "prioridad": "Comprar mi casa",
            "plazo_casa": "En 10 años",
            "cuota_inicial_casa": 45_000_000,
            "pension_deseada": 3_000_000,
            "depende": "Mi hija",
            "edad_dependiente": 8,
            "vivienda": "En arriendo",
            "deudas": "Tarjeta que pago completa",
            "gastos_mensuales": 2_500_000,
            "ahorro": 3_000_000,
            "donde_ahorro": ["En mi cuenta de ahorros"],
            "seguro_vida": "No sé",
            # Sin perfil precargado (H9): las seis preguntas llegan vacías y las contesta ella.
            "perfil": {},
        },
        "estado": {
            "queja_abierta": False,
            "no_contacto": False,
            "perdida_empleo": False,
            "coyuntura_critica": False,
            "evento_sensible": False,
            "autoriza_uso_salario": False,
            "autoriza_mensajes_comerciales": False,   # se pregunta; nunca viene marcado (H8)
            "autoriza_agentes_externos": False,
        },
        "consultor": {"nombre": "Daniela R.", "iniciales": "DR"},
    },
    "andres": {
        "id": "andres",
        "nombre": "Andrés",
        "sexo": "hombre",
        "edad": 41,
        "segmento": "renta_masiva",
        "arquetipo": "pragmatico",
        "ciudad": "Bogotá",
        "lo_que_sabemos": {
            "saldo_pension_obligatoria": 96_000_000,
            "anios_cotizados": 16,
            "semanas_cotizadas": 830,
            "salario_cotizacion": 4_100_000,
            "cesantias": 11_200_000,
            "comision_pension_anual": 0.012,
            "primas": ["junio", "diciembre"],
            "beneficiarios_confirmados": True,
            "cotiza_activamente": False,
        },
        "diagnostico_propuesto": {
            "metas": ["Tener tranquilidad"],
            "prioridad": "Tener tranquilidad",
            "plazo_casa": "",
            "cuota_inicial_casa": 0,
            "pension_deseada": 2_500_000,
            "depende": "Hijos",
            "edad_dependiente": 12,
            "vivienda": "En arriendo",
            "deudas": "No tengo",
            "gastos_mensuales": 3_100_000,
            "ahorro": 1_500_000,
            "donde_ahorro": ["En mi cuenta de ahorros"],
            "seguro_vida": "Sí",
            "perfil": {
                "horizonte": "Más de 5 años",
                "objetivo": "Que no baje",
                "conocimiento": "Lo básico",
                "experiencia": "Nunca",
                "perdida": "Hasta 5 de cada 100 pesos",
                "reaccion": "Lo saco todo",
            },
            "perfil_fecha": "2026-01-10",       # lo contestó él en su primera reunión
        },
        "estado": {
            "queja_abierta": False,
            "no_contacto": False,
            "perdida_empleo": True,          # su empleador dejó de cotizar
            "coyuntura_critica": False,
            "evento_sensible": False,
            "autoriza_uso_salario": True,
            "autoriza_mensajes_comerciales": False,   # se pregunta; nunca viene marcado (H8)
            "autoriza_agentes_externos": False,
        },
        "consultor": {"nombre": "Daniela R.", "iniciales": "DR"},
    },
}

# Configurable mientras Carolina decide el pendiente 2: ¿el consultor con nombre
# aplica a la renta masiva o solo a la renta media?
CONSULTOR_CON_NOMBRE_POR_SEGMENTO = {
    "renta_masiva": True,
    "renta_media": True,
}


def afiliado(afiliado_id: str) -> dict:
    """Copia del afiliado, para que ninguna sesión cambie los datos de base."""
    return deepcopy(AFILIADOS[afiliado_id])
