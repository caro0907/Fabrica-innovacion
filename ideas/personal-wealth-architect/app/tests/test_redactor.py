"""El modo con Claude no puede saltarse el catálogo: si el modelo desobedece, se usa la versión de plantillas."""
import pytest

from pwa import redactor

VARS = {"meses": "1,2", "mes": "junio", "prima": "$2.600.000", "supuestos": "tu salario de hoy"}
CTX = {"autoriza_uso_salario": True}


@pytest.fixture()
def con_llave(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "prueba")


def _modelo(monkeypatch, orden, puentes):
    monkeypatch.setattr(redactor, "_pedir_a_claude", lambda base, persona: (orden(base), puentes))


def test_sin_llave_usa_plantillas(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    r = redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")
    assert r["modo"] == "plantillas" and "A5" in r["piezas"]


def test_modelo_obediente(con_llave, monkeypatch):
    _modelo(monkeypatch, lambda b: list(reversed(b.piezas)), ["", "Y algo importante:", "", ""])
    r = redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")
    assert r["modo"] == "claude" and "Y algo importante:" in r["texto"]


def test_puente_con_cifra_se_rechaza(con_llave, monkeypatch):
    _modelo(monkeypatch, lambda b: b.piezas, ["Con 5 millones más llegas", "", "", ""])
    r = redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")
    assert r["modo"] == "plantillas" and "5 millones" not in r["texto"]


def test_puente_prohibido_se_rechaza(con_llave, monkeypatch):
    _modelo(monkeypatch, lambda b: b.piezas, ["Es una inversión sin riesgo", "", "", ""])
    assert redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")["modo"] == "plantillas"


def test_modelo_que_quita_una_advertencia_se_rechaza(con_llave, monkeypatch):
    _modelo(monkeypatch, lambda b: [p for p in b.piezas if p != "A5"], [])
    r = redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")
    assert "A5" in r["piezas"]


def test_modelo_que_agrega_una_pieza_se_rechaza(con_llave, monkeypatch):
    _modelo(monkeypatch, lambda b: b.piezas + ["P4"], [])
    assert redactor.nota_del_arquitecto(["B6", "P3"], VARS, CTX, "Laura")["modo"] == "plantillas"
