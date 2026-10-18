"""Pruebas del motor: lo que no se puede romper sin que alguien lo note."""
from datetime import date, datetime

import pytest

from pwa import catalogo as CAT
from pwa.motor import calculos as C
from pwa.motor import datos, decision, mandatos, plan
from pwa.motor import supuestos as S

HOY = date(2026, 6, 1)
REVISION = date(2026, 6, 15)


def _plan(afiliado_id="laura", hoy=HOY, cambios=None, hechos=None):
    af = datos.afiliado(afiliado_id)
    d = af["diagnostico_propuesto"]
    d.update(cambios or {})
    af["estado"]["autoriza_uso_salario"] = True
    return af, plan.armar_plan(af, d, hoy, hechos or set())


# Cálculos ------------------------------------------------------------------------------
def test_pension_mismo_metodo_y_supuestos_visibles():
    """C9: la mesada se recalcula con los supuestos que muestra la pantalla."""
    af, p = _plan()
    sabe = af["lo_que_sabemos"]
    anios = S.EDAD_PENSION["mujer"] - af["edad"]
    saldo = C.valor_futuro(sabe["saldo_pension_obligatoria"], sabe["salario_cotizacion"] * S.PORCENTAJE_A_CUENTA_INDIVIDUAL,
                           anios * 12, S.RENTABILIDAD_REAL_ANUAL)
    esperada = saldo / (S.MESADAS_POR_ANIO * C.factor_anualidad(S.ANIOS_DE_PENSION, S.RENTABILIDAD_REAL_ANUAL))
    assert p["pension"]["mesada"] == pytest.approx(esperada)
    for valor in ("11,5%", "4%", "13 mesadas", "30", "57"):
        assert valor in p["pension"]["supuestos_txt"]


def test_laura_conserva_reglas_de_hoy_por_semanas():
    _, p = _plan()
    assert p["pension"]["semanas_hoy"] == 730
    assert p["pension"]["conserva_reglas_de_hoy"] is True


def test_colchon_y_prima_de_laura():
    _, p = _plan()
    assert p["colchon"]["meta"] == 7_500_000
    assert p["colchon"]["meses_txt"] == "1,2"
    assert p["prima"]["monto"] == 2_600_000
    assert p["prima"]["al_colchon"] == pytest.approx(1_820_000)
    assert p["prima"]["a_la_meta"] == pytest.approx(780_000)


def test_prima_sin_brecha_de_colchon_va_toda_a_la_meta():
    _, p = _plan(cambios={"ahorro": 10_000_000})
    assert p["prima"]["al_colchon"] == 0
    assert p["prima"]["a_la_meta"] == p["prima"]["monto"]


def test_simulador_de_meta_escenario_sin_rentabilidad_es_mas_lento():
    rapido = C.meses_para_meta(45_000_000, 9_400_000, 212_000, 0.04)
    lento = C.meses_para_meta(45_000_000, 9_400_000, 212_000, 0.0)
    assert rapido <= 120 < lento


def test_riesgo_nunca_se_redondea_hacia_abajo():
    assert C.redondear_riesgo(93_600) == 94_000
    assert C.redondear_riesgo(93_001) == 94_000


def test_caida_cabe_en_la_perdida_tolerada():
    """C8: la caída de un mal año del portafolio recomendado cabe en lo que la persona tolera."""
    af, _ = _plan()
    from pwa.motor import perfil as PF
    tolerada = PF.perdida_tolerada(af["diagnostico_propuesto"]["perfil"])
    assert S.PORTAFOLIOS["fic_moderado"]["caida_mal_anio"] <= tolerada


# El plan primero -----------------------------------------------------------------------
def test_el_plan_empieza_por_lo_que_no_es_producto():
    _, p = _plan()
    assert p["orden"][0]["id"] == "beneficiaria"
    assert all(not paso["es_producto"] for paso in p["orden"])


def test_deuda_cara_va_antes_de_invertir():
    af, p = _plan(cambios={"deudas": "Tarjeta o crédito que pago a cuotas"})
    ids = [x["id"] for x in p["orden"]]
    assert ids.index("deuda") < ids.index("prima")
    ctx = decision.contexto(af, p, REVISION)
    dec = decision.decidir(ctx)
    assert dec["modo"] == "servicio"
    assert all(not x["es_producto"] for x in dec["cola"])


def test_cada_dato_del_plan_tiene_origen():
    _, p = _plan()
    assert len(p["patrimonio"]["dimensiones"]) == 8
    assert all(d["origen"] for d in p["patrimonio"]["dimensiones"])


# Decisión ---------------------------------------------------------------------------------
def test_restrictivo_bloquea_todo_lo_comercial():
    af, p = _plan("andres")
    dec = decision.decidir(decision.contexto(af, p, REVISION))
    assert dec["modo"] == "servicio"
    assert dec["restrictivos"][0]["id"] == "R-EMPLEO"
    assert dec["principal"]["accion"] == "servicio_cesantias"
    assert not dec["puede_iniciar_contacto"]
    assert all(not x["es_producto"] for x in dec["cola"])


def test_queja_abierta_bloquea_aunque_haya_prima():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    af["estado"]["queja_abierta"] = True
    dec = decision.decidir(decision.contexto(af, p, REVISION))
    assert dec["modo"] == "servicio"
    assert dec["principal"] is None or not dec["cola"][0]["es_producto"]


def test_laura_el_15_de_junio_recibe_la_prima_con_rumbo_en_cinco_campos():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(decision.contexto(af, p, REVISION))
    assert dec["modo"] == "asesoria"
    assert dec["principal"]["escenario"] == "O-PRIMA"
    assert set(dec["cinco_campos"]) == {"canal", "prioridad", "vigencia", "tono", "recomendacion"}
    assert dec["cinco_campos"]["vigencia"] == "2026-06-30"
    assert "no es un producto" in dec["cinco_campos"]["recomendacion"]


def test_el_no_se_respeta():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(decision.contexto(af, p, REVISION), rechazos={"casa_con_prima"})
    assert "casa_con_prima" not in [x["accion"] for x in dec["cola"]]


def test_fuera_de_horario_no_se_inicia_contacto():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    domingo = datetime(2026, 6, 14, 10, 0)
    dec = decision.decidir(decision.contexto(af, p, date(2026, 6, 14), ahora=domingo))
    assert not dec["puede_iniciar_contacto"]
    assert decision.en_horario_de_contacto(datetime(2026, 6, 15, 9, 12))
    assert not decision.en_horario_de_contacto(datetime(2026, 6, 13, 16, 0))   # sábado después de las 3 p. m.


def test_freno_de_servicio_pausa_lo_comercial():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(decision.contexto(af, p, REVISION), metricas_servicio={"satisfaccion": 0.80})
    assert dec["freno"]["activo"]
    assert not dec["puede_iniciar_contacto"]


def test_grupo_de_control_es_estable():
    a = decision.en_grupo_control("laura", "exp")
    assert all(decision.en_grupo_control("laura", "exp") == a for _ in range(5))
    total = sum(decision.en_grupo_control(f"afiliado-{i}", "exp") for i in range(5000))
    assert 0.07 < total / 5000 < 0.13


def test_laura_no_esta_en_el_grupo_de_control_del_experimento():
    assert not decision.en_grupo_control("laura", decision.EXPERIMENTO)


# Catálogo -----------------------------------------------------------------------------------
def test_beneficio_arrastra_sus_condiciones():
    comp = CAT.componer(["B4"], {}, {})
    assert "C1" in comp.piezas


def test_beneficio_tributario_no_se_muestra_a_quien_no_paga_impuesto():
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.componer(["B1"], {"ahorro_por_100": "14"}, {"paga_impuesto": False})


def test_frases_prohibidas():
    assert CAT.frases_prohibidas("Es una inversión sin riesgo")
    assert CAT.frases_prohibidas("Somos imparciales")
    assert CAT.frases_prohibidas("Solo hoy")
    assert not CAT.frases_prohibidas("No es una promesa ni una rentabilidad garantizada. Algunos años puede ser negativa.")


def test_puente_no_puede_llevar_cifras():
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.validar_puente("Con 5 millones llegas")
    CAT.validar_puente("Esto es lo primero de tu plan:")


def test_pieza_sin_variables_del_motor_no_sale():
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.render("P3", {})


def test_todas_las_piezas_del_catalogo_pasan_el_control():
    for pid in CAT.PIEZAS:
        texto = CAT.PIEZAS[pid]["texto"]
        assert not CAT.frases_prohibidas(texto), pid


# Mandatos -------------------------------------------------------------------------------------
def test_mandato_tiene_siete_campos_y_consentimiento():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7, 2_600_000)
    for campo in ("disparador", "accion", "destino", "tope", "vigencia_hasta", "aviso", "control"):
        assert getattr(m, campo)
    assert m.control == "proponer_y_confirmar"
    assert "cancela mi regla" in m.consentimiento
    assert "$2.600.000" in m.consentimiento


def test_mandato_se_pausa_solo_si_pierde_el_empleo():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7, 2_600_000)
    mandatos.revisar_pausas(m, {"perdida_empleo": True}, True, REVISION)
    assert m.estado == "pausado"
    mandatos.cancelar(m, REVISION)
    assert m.estado == "cancelado"


def test_producto_que_no_cabe_en_el_perfil_no_es_elegible():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(decision.contexto(af, p, REVISION, perdida_tolerada=0.05))
    assert "casa_con_prima" not in [x["accion"] for x in dec["cola"]]
    dec = decision.decidir(decision.contexto(af, p, REVISION, perdida_tolerada=0.15))
    assert "casa_con_prima" in [x["accion"] for x in dec["cola"]]
