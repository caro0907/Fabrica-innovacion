"""Pruebas del recorrido completo de Laura, de Andrés y de las compuertas.

MVP v1.1: incluye las pruebas que pidió la revisión del 18 de octubre de 2026
(revisiones/2026-10-18-mvp-v1.md): coherencia de la nota, permiso del salario, mandato
desmarcado y posterior a aprobar, perfil sin respuestas precargadas, mensajes comerciales
preguntados y vistas internas cerradas.
"""
import os
import re
import tempfile

os.environ["PWA_DB"] = os.path.join(tempfile.mkdtemp(), "prueba.sqlite")
os.environ.pop("ANTHROPIC_API_KEY", None)
os.environ.pop("PWA_CLAVE_INTERNA", None)
os.environ["PWA_INTERNO_ABIERTO"] = "1"

import pytest
from fastapi.testclient import TestClient

from pwa import catalogo as CAT
from pwa.app import app

PERFIL_LAURA = {"horizonte": "Más de 5 años", "objetivo": "Que crezca para mi meta", "conocimiento": "Lo básico",
                "experiencia": "Nunca", "perdida": "Hasta 15 de cada 100 pesos", "reaccion": "Espero"}
PERFIL_CONSERVADOR = {**PERFIL_LAURA, "objetivo": "Que no baje", "perdida": "Hasta 5 de cada 100 pesos"}


@pytest.fixture()
def cliente():
    with TestClient(app) as c:
        yield c


def _sin_prohibidas(texto: str) -> list[str]:
    return CAT.frases_prohibidas(texto.replace("No es una promesa ni una rentabilidad garantizada", ""))


def _laura_hasta_el_plan(c, autoriza=True, ingreso="", perfil=PERFIL_LAURA, mensajes=""):
    r = c.post("/demo/laura", follow_redirects=True)
    assert "primera reunión" in r.text
    datos_bienvenida = {"ingreso": ingreso, "mensajes": mensajes}
    if autoriza:
        datos_bienvenida["autoriza"] = "si"
    c.post("/d/bienvenida", data=datos_bienvenida)
    c.post("/d/metas", data={"metas": ["Tener tranquilidad", "Comprar mi casa", "Pensionarme bien"], "prioridad": "Comprar mi casa"})
    c.post("/d/numeros", data={"plazo_casa": "En 10 años", "cuota_inicial_casa": "45000000", "pension_deseada": "3000000"})
    c.post("/d/vida", data={"depende": "Mi hija", "edad_dependiente": "8", "vivienda": "En arriendo", "deudas": "Tarjeta que pago completa"})
    c.post("/d/dinero", data={"gastos_mensuales": "2500000", "ahorro": "3000000", "donde_ahorro": "En mi cuenta de ahorros", "seguro_vida": "No sé"})
    c.post("/d/riesgo", data=perfil)
    return c.post("/d/entendi", follow_redirects=True)


def _aprobar_propuesta(c):
    r = c.post("/propuesta/confirmar", data={"entiendo": "si"}, follow_redirects=True)
    assert "Pon tu dedo en el lector" in r.text
    return c.post("/huella", data={"para": "propuesta"}, follow_redirects=True)


def test_recorrido_completo_de_laura(cliente):
    c = cliente
    r = _laura_hasta_el_plan(c)
    assert "este es tu plan" in r.text
    assert "Ver supuestos" in r.text and "$90,4 M" in r.text
    # El primer paso no es un producto, y dice la verdad sobre los beneficiarios (H4)
    assert "Registra a tu hija en tu grupo familiar" in r.text
    assert "Tu hija ya es tu beneficiaria por ley en tu pensión obligatoria" in r.text
    assert c.get("/inicio", follow_redirects=False).headers["location"] == "/plan-inicial"
    r = c.post("/accion/beneficiaria", data={"volver": "/plan-inicial"}, follow_redirects=True)
    assert "quedó en tu grupo familiar" in r.text
    r = c.post("/plan/guardar", follow_redirects=True)
    assert "Lunes 15 de junio" in r.text and "Tu revisión de junio está lista" in r.text
    assert c.get("/d/metas", follow_redirects=False).headers["location"] == "/inicio"
    r = c.get("/revision")
    assert "$1.820.000" in r.text and "no un producto" in r.text and "Lo que no te propongo todavía" in r.text
    r = c.get("/propuesta")
    assert "Recomendación profesional" in r.text and "$94.000" in r.text and "Asesoría no independiente" in r.text
    assert "no es un depósito" in r.text
    # H2: el vehículo es un portafolio del fondo de pensiones voluntarias, con su condición de retiro
    assert "Portafolio moderado de tu fondo de pensiones voluntarias" in r.text
    assert "no hay beneficio tributario" in r.text
    # H13: quién hace la recomendación
    assert "herramienta tecnológica" in r.text and "puede revisarla contigo" in r.text
    # H12 y H24: sin promesas de correo ni "al año" repetido
    assert "a tu correo" not in r.text and "al año) al año" not in r.text
    # Hallazgo 3: la regla no está en la propuesta
    assert 'name="regla"' not in r.text
    # Sin comprensión no se aprueba
    r = c.post("/propuesta/confirmar", data={}, follow_redirects=True)
    assert "Marca que entiendes" in r.text
    r = _aprobar_propuesta(c)
    assert "Tu prima ya tiene rumbo" in r.text
    assert "¿Quieres que en diciembre te lo proponga igual?" in r.text
    for url in ("/plan", "/meta/casa", "/patrimonio", "/pilares", "/equipo", "/perfil", "/como-funciona",
                "/pregunta?q=¿Y mi pensión?", "/pregunta?q=¿Tengo que declarar renta?", "/privacidad"):
        r = c.get(url)
        assert r.status_code == 200, url
        assert not _sin_prohibidas(r.text), url
    assert c.get("/api/simular/casa?mensual=100000").json()["a_tiempo"] is True


def test_la_regla_se_ofrece_despues_desmarcada_y_con_sus_condiciones(cliente):
    """Hallazgo 3 del revisor y H7: paso posterior, casilla desmarcada, condiciones antes, tope del diseño."""
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    r = _aprobar_propuesta(c)
    oferta = r.text
    assert "$1.000.000 a inversión por prima" in oferta
    assert "15 de junio de 2027" in oferta and "2027-06-15" not in oferta
    assert "Te propongo dos semanas antes y te recuerdo confirmar un día antes" in oferta
    assert "Autorizo a mi administradora de fondos a proponerme" in oferta
    casilla = re.search(r'<input type="checkbox" name="acepto"[^>]*>', oferta).group(0)
    assert "checked" not in casilla
    # Las condiciones aparecen antes del botón de aceptar
    assert oferta.index("Tope") < oferta.index("Sí, déjalo como regla")
    # Sin marcar la autorización no se crea
    r = c.post("/regla/nueva", data={}, follow_redirects=True)
    assert "marca la autorización" in r.text
    assert "Prima con rumbo" not in c.get("/reglas").text
    r = c.post("/regla/nueva", data={"acepto": "si"}, follow_redirects=True)
    assert "Pon tu dedo en el lector" in r.text
    r = c.post("/huella", data={"para": "regla"}, follow_redirects=True)
    assert "Tu regla quedó activa" in r.text and "Prima con rumbo" in r.text
    assert "Te propongo y tú confirmas cada vez" in r.text and "15 de junio de 2027" in r.text
    rid = "laura-prima-con-rumbo"
    assert "Pausado" in c.post(f"/reglas/{rid}/pausar", follow_redirects=True).text
    assert "Cancelado" in c.post(f"/reglas/{rid}/cancelar", follow_redirects=True).text
    # Solo se muestran las pausas que de verdad corren (H10)
    assert "Dos ejecuciones fallidas" not in c.get("/reglas").text


def test_la_nota_del_inicio_no_contradice_la_recomendacion(cliente):
    """Hallazgo 1 del revisor y H3 (criterio A7): la nota dice la regla real, no "antes de invertir"."""
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/accion/beneficiaria", data={"volver": "/plan-inicial"})
    c.post("/plan/guardar")
    r = c.get("/inicio")
    assert "Antes de invertir" not in r.text
    assert "Tu colchón va primero: el 70% de tu prima" in r.text
    assert "Tu casa avanza con el resto" in r.text


def test_sin_permiso_del_salario_ninguna_pantalla_muestra_cifras_derivadas(cliente):
    """Hallazgo 2 del revisor, H5, H6 y H17 (criterio C10)."""
    c = cliente
    r = c.post("/demo/laura", follow_redirects=True)
    assert 'name="autoriza"' in r.text and "required" not in re.search(r'<input type="checkbox" name="autoriza"[^>]*>', r.text).group(0)
    assert "finalidad" in r.text and "/privacidad" in r.text
    r = _laura_hasta_el_plan(c, autoriza=False)
    assert "este es tu plan" in r.text
    derivadas = ("$5,2 M", "$2.600.000", "$1.820.000", "$780.000", "$1,83 M", "$2,6 M", "$624 mil", "nos autorizaste", "$73,42 M")
    c.post("/plan/guardar")
    for url in ("/inicio", "/plan", "/patrimonio", "/pilares", "/meta/casa", "/revision", "/pregunta?q=prima",
                "/pregunta?q=¿Y mi pensión?", "/pregunta?q=impuesto", "/reglas"):
        r = c.get(url)
        assert r.status_code == 200, url
        for cifra in derivadas:
            assert cifra not in r.text, (url, cifra)
    r = c.get("/inicio")
    assert "Sin tu permiso para usar tu salario de cotización no estimamos esto" in r.text
    assert "Hoy no te proponemos nada" not in r.text     # no es un restrictivo general
    assert "Con 5 de 6 pilares" in r.text
    assert c.get("/propuesta", follow_redirects=False).headers["location"] == "/revision"


def test_retirar_el_permiso_despues_cambia_lo_que_se_muestra(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    assert "$1,83 M" in c.get("/plan").text
    c.post("/permisos/autoriza_uso_salario", data={"valor": "no"})
    r = c.get("/plan")
    assert "$1,83 M" not in r.text and "nos autorizaste" not in r.text
    assert "Sin tu permiso para usar tu salario de cotización no estimamos" in r.text


def test_con_el_ingreso_que_cuenta_el_plan_se_estima_con_ese_dato(cliente):
    c = cliente
    r = _laura_hasta_el_plan(c, autoriza=False, ingreso="4000000")
    assert "este es tu plan" in r.text
    c.post("/plan/guardar")
    r = c.get("/plan")
    assert "el ingreso que nos contaste ($4,0 M)" in r.text
    assert "nos autorizaste" not in r.text


def test_perfil_conservador_no_recibe_el_portafolio(cliente):
    """H1: idoneidad completa."""
    c = cliente
    _laura_hasta_el_plan(c, perfil=PERFIL_CONSERVADOR)
    c.post("/plan/guardar")
    r = c.get("/propuesta")
    assert "Seguir: confirmar con mi huella" not in r.text
    assert "Con tu perfil de hoy no te recomendamos aquí" in r.text
    assert "coincide con tu perfil" not in r.text


def test_el_perfil_no_llega_contestado(cliente):
    """H9: las seis preguntas llegan vacías y nunca se completan por defecto."""
    c = cliente
    c.post("/demo/laura")
    c.post("/d/bienvenida", data={"autoriza": "si"})
    r = c.get("/d/riesgo")
    assert " checked" not in r.text
    r = c.post("/d/riesgo", data={"horizonte": "Más de 5 años"}, follow_redirects=True)
    assert "Contesta las seis preguntas" in r.text


def test_mensajes_comerciales_se_preguntan_y_vienen_en_no(cliente):
    """H8."""
    c = cliente
    r = c.post("/demo/laura", follow_redirects=True)
    casilla = re.search(r'<input type="checkbox" name="mensajes"[^>]*>', r.text).group(0)
    assert "checked" not in casilla
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    motor = c.get("/interno/motor").text
    assert "Sin autorización de mensajes comerciales" in motor
    # El 15 de junio de 2026 es festivo: el aviso esperaría al martes 16 (H16)
    assert "festivo" in motor and "martes 16" in motor


def test_segunda_falta_de_comprension_lleva_al_consultor(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/propuesta/confirmar", data={})
    c.post("/propuesta/confirmar", data={})
    r = c.get("/propuesta")
    assert "Mejor veámoslo con Daniela" in r.text
    assert "Seguir: confirmar con mi huella" not in r.text


def test_un_no_se_respeta(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/propuesta/no")
    r = c.get("/propuesta")
    assert "Seguir: confirmar con mi huella" not in r.text


def test_la_huella_no_se_salta(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    r = c.post("/huella", data={"para": "propuesta"}, follow_redirects=False)
    assert r.headers["location"] == "/inicio"
    assert c.get("/propuesta/lista", follow_redirects=False).headers["location"] == "/propuesta"


def test_andres_en_modo_servicio_no_recibe_ofertas(cliente):
    c = cliente
    r = c.post("/demo/andres", follow_redirects=True)
    assert "Modo servicio" in r.text and "5 días" in r.text and "Mecanismo de Protección al Cesante" in r.text
    assert "constancia de terminación" in r.text and "al menos un año en los últimos tres" in r.text   # H21
    assert "Pausé tu regla" in r.text
    assert c.get("/inicio", follow_redirects=False).headers["location"] == "/servicio"
    r = c.get("/interno/motor")
    assert "Servicio (restrictivo activo)" in r.text and "Pérdida de empleo" in r.text
    r = c.post("/servicio/solicitar", follow_redirects=True)
    assert "Recibimos tu solicitud" in r.text


def test_api_de_agentes_exige_token_y_consentimiento(cliente):
    c = cliente
    os.environ["PWA_TOKEN_AGENTES"] = "prueba-token"
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    sid = c.cookies.get("pwa_sesion")
    assert c.get("/api/v1/plan", headers={"x-sesion": sid}).status_code == 401
    h = {"authorization": "Bearer prueba-token", "x-sesion": sid}
    assert c.get("/api/v1/plan", headers=h).status_code == 403
    c.post("/permisos/autoriza_agentes_externos", data={"valor": "si"})
    r = c.get("/api/v1/plan", headers=h)
    assert r.status_code == 200 and "No es una recomendación profesional" in r.json()["aviso"]


def test_vistas_internas_cerradas_sin_clave(cliente, monkeypatch):
    """Revisor, no bloqueante: sin PWA_CLAVE_INTERNA las vistas internas están cerradas por defecto."""
    c = cliente
    monkeypatch.delenv("PWA_INTERNO_ABIERTO")
    _laura_hasta_el_plan(c)
    assert c.get("/interno/motor", follow_redirects=False).headers["location"].startswith("/interno/entrar")
    assert c.post("/interno/freno", data={"satisfaccion": "0.5"}, follow_redirects=False).headers["location"].startswith("/interno/entrar")


def test_vistas_internas_con_clave(cliente, monkeypatch):
    c = cliente
    monkeypatch.setenv("PWA_CLAVE_INTERNA", "clave-prueba")
    monkeypatch.delenv("PWA_INTERNO_ABIERTO")
    _laura_hasta_el_plan(c)
    assert c.get("/interno/motor", follow_redirects=False).headers["location"].startswith("/interno/entrar")
    r = c.post("/interno/entrar", data={"clave": "clave-prueba", "siguiente": "/interno/motor"}, follow_redirects=False)
    assert "clave-prueba" not in r.headers.get("set-cookie", "")       # la cookie no guarda la clave en claro
    assert "Una sola decisión" in c.get("/interno/motor").text
    assert "Brief de profundización" in c.get("/interno/consultor").text


def test_freno_desde_la_vista_interna(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/interno/freno", data={"satisfaccion": "0.80", "resolucion_sin_oficina": "0.82", "transferencia_a_humano": "0.12"})
    assert "ACTIVO" in c.get("/interno/motor").text
    c.post("/interno/freno", data={"satisfaccion": "0.87", "resolucion_sin_oficina": "0.82", "transferencia_a_humano": "0.12"})


def test_el_brief_del_consultor_sale_de_la_accion(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/accion/beneficiaria", data={"volver": "/plan-inicial"})
    c.post("/plan/guardar")
    r = c.get("/interno/consultor")
    assert "Porqué: su colchón cubre 1,2 meses de 3 y su prima de $2.600.000 llega el 30 de junio" in r.text
