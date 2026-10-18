"""Pruebas del recorrido completo de Laura, de Andrés y de las compuertas."""
import os
import tempfile

os.environ["PWA_DB"] = os.path.join(tempfile.mkdtemp(), "prueba.sqlite")
os.environ.pop("ANTHROPIC_API_KEY", None)

import pytest
from fastapi.testclient import TestClient

from pwa import catalogo as CAT
from pwa.app import app


@pytest.fixture()
def cliente():
    with TestClient(app) as c:
        yield c


def _laura_hasta_el_plan(c):
    r = c.post("/demo/laura", follow_redirects=True)
    assert "primera reunión" in r.text
    assert c.post("/d/bienvenida", data={}, follow_redirects=False).headers["location"].startswith("/d/bienvenida")
    c.post("/d/bienvenida", data={"autoriza": "si"})
    c.post("/d/metas", data={"metas": ["Tener tranquilidad", "Comprar mi casa", "Pensionarme bien"], "prioridad": "Comprar mi casa"})
    c.post("/d/numeros", data={"plazo_casa": "En 10 años", "cuota_inicial_casa": "45000000", "pension_deseada": "3000000"})
    c.post("/d/vida", data={"depende": "Mi hija", "edad_dependiente": "8", "vivienda": "En arriendo", "deudas": "Tarjeta que pago completa"})
    c.post("/d/dinero", data={"gastos_mensuales": "2500000", "ahorro": "3000000", "donde_ahorro": "En mi cuenta de ahorros", "seguro_vida": "No sé"})
    c.post("/d/riesgo", data={"horizonte": "Más de 5 años", "objetivo": "Que crezca para mi meta", "conocimiento": "Lo básico",
                              "experiencia": "Nunca", "perdida": "Hasta 15 de cada 100 pesos", "reaccion": "Espero"})
    r = c.get("/d/entendi")
    assert "Moderado" in r.text
    return c.post("/d/entendi", follow_redirects=True)


def test_recorrido_completo_de_laura(cliente):
    c = cliente
    r = _laura_hasta_el_plan(c)
    assert "este es tu plan" in r.text
    assert "Ver supuestos" in r.text and "$90,4 M" in r.text
    # El primer paso no es un producto
    assert "Confirma a tu hija como beneficiaria" in r.text
    # No hay app antes de guardar el plan (mismo momento)
    assert c.get("/inicio", follow_redirects=False).headers["location"] == "/plan-inicial"
    r = c.post("/accion/beneficiaria", data={"volver": "/plan-inicial"}, follow_redirects=True)
    assert "quedó como tu beneficiaria" in r.text
    r = c.post("/plan/guardar", follow_redirects=True)
    assert "Lunes 15 de junio" in r.text and "Tu revisión de junio está lista" in r.text
    # Ya no vuelve a la primera reunión
    assert c.get("/d/metas", follow_redirects=False).headers["location"] == "/inicio"
    r = c.get("/revision")
    assert "$1.820.000" in r.text and "no un producto" in r.text and "Lo que no te propongo todavía" in r.text
    r = c.get("/propuesta")
    assert "Recomendación profesional" in r.text and "$94.000" in r.text and "Asesoría no independiente" in r.text
    assert "no es un depósito" in r.text
    # Sin comprensión no se aprueba
    r = c.post("/propuesta/confirmar", data={"huella": "si", "regla": "si"}, follow_redirects=True)
    assert "Marca que entiendes" in r.text
    r = c.post("/propuesta/confirmar", data={"entiendo": "si", "huella": "si", "regla": "si"}, follow_redirects=True)
    assert "Tu prima ya tiene rumbo" in r.text
    r = c.get("/reglas")
    assert "Prima con rumbo" in r.text and "Te propongo y tú confirmas cada vez" in r.text and "cancela mi regla" in r.text
    rid = "laura-prima-con-rumbo"
    assert "Pausado" in c.post(f"/reglas/{rid}/pausar", follow_redirects=True).text
    assert "Cancelado" in c.post(f"/reglas/{rid}/cancelar", follow_redirects=True).text
    for url in ("/plan", "/meta/casa", "/patrimonio", "/pilares", "/equipo", "/perfil", "/como-funciona", "/pregunta?q=¿Y mi pensión?"):
        r = c.get(url)
        assert r.status_code == 200, url
        assert not CAT.frases_prohibidas(r.text.replace("No es una promesa ni una rentabilidad garantizada", "")), url
    assert c.get("/api/simular/casa?mensual=100000").json()["a_tiempo"] is True


def test_segunda_falta_de_comprension_lleva_al_consultor(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/propuesta/confirmar", data={"huella": "si"})
    c.post("/propuesta/confirmar", data={"huella": "si"})
    r = c.get("/propuesta")
    assert "Mejor veámoslo con Daniela" in r.text
    assert "Aprobar con mi huella" not in r.text


def test_un_no_se_respeta(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/propuesta/no")
    r = c.get("/propuesta")
    assert "Aprobar con mi huella" not in r.text


def test_andres_en_modo_servicio_no_recibe_ofertas(cliente):
    c = cliente
    r = c.post("/demo/andres", follow_redirects=True)
    assert "Modo servicio" in r.text and "5 días" in r.text and "Mecanismo de Protección al Cesante" in r.text
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


def test_vistas_internas_con_clave(cliente):
    c = cliente
    os.environ["PWA_CLAVE_INTERNA"] = "clave-prueba"
    try:
        _laura_hasta_el_plan(c)
        assert c.get("/interno/motor", follow_redirects=False).headers["location"].startswith("/interno/entrar")
        c.post("/interno/entrar", data={"clave": "clave-prueba", "siguiente": "/interno/motor"})
        assert "Una sola decisión" in c.get("/interno/motor").text
        assert "Brief de profundización" in c.get("/interno/consultor").text
    finally:
        os.environ.pop("PWA_CLAVE_INTERNA")


def test_freno_desde_la_vista_interna(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/interno/freno", data={"satisfaccion": "0.80", "resolucion_sin_oficina": "0.82", "transferencia_a_humano": "0.12"})
    assert "ACTIVO" in c.get("/interno/motor").text
    c.post("/interno/freno", data={"satisfaccion": "0.87", "resolucion_sin_oficina": "0.82", "transferencia_a_humano": "0.12"})


def test_retirar_el_permiso_del_salario_no_rompe_la_app(cliente):
    c = cliente
    _laura_hasta_el_plan(c)
    c.post("/plan/guardar")
    c.post("/permisos/autoriza_uso_salario", data={"valor": "no"})
    for url in ("/inicio", "/revision", "/pregunta?q=prima", "/plan", "/reglas"):
        assert c.get(url).status_code == 200, url
    assert "Hoy no te proponemos nada" in c.get("/inicio").text
