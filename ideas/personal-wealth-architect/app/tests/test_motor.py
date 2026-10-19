"""Pruebas del motor: lo que no se puede romper sin que alguien lo note."""
from datetime import date, datetime

import pytest

from pwa import catalogo as CAT
from pwa.motor import calculos as C
from pwa.motor import datos, decision, mandatos, plan
from pwa.motor import supuestos as S

HOY = date(2026, 6, 1)
REVISION = date(2026, 6, 15)
PERFIL_MODERADO = {"horizonte": "Más de 5 años", "objetivo": "Que crezca para mi meta", "conocimiento": "Lo básico",
                   "experiencia": "Nunca", "perdida": "Hasta 15 de cada 100 pesos", "reaccion": "Espero"}


def _plan(afiliado_id="laura", hoy=HOY, cambios=None, hechos=None, autoriza=True):
    af = datos.afiliado(afiliado_id)
    d = af["diagnostico_propuesto"]
    if afiliado_id == "laura":
        d.update(perfil=dict(PERFIL_MODERADO), perfil_fecha="2026-06-01")
    d.update(cambios or {})
    af["estado"]["autoriza_uso_salario"] = autoriza
    return af, plan.armar_plan(af, d, hoy, hechos or set())


def _ctx(af, p, hoy=REVISION, **extra):
    d = af["diagnostico_propuesto"]
    extra.setdefault("perfil", d.get("perfil") or {})
    extra.setdefault("plazo_meta_anios", p["casa"]["plazo_anios"] if p["casa"] else None)
    extra.setdefault("ahora", datetime(hoy.year, hoy.month, hoy.day, 9, 12))
    return decision.contexto(af, p, hoy, **extra)


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
    assert S.PORTAFOLIOS["fpv_moderado"]["caida_mal_anio"] <= tolerada


# El plan primero -----------------------------------------------------------------------
def test_el_plan_empieza_por_lo_que_no_es_producto():
    _, p = _plan()
    assert p["orden"][0]["id"] == "beneficiaria"
    assert all(not paso["es_producto"] for paso in p["orden"])


def test_deuda_cara_va_antes_de_invertir():
    af, p = _plan(cambios={"deudas": "Tarjeta o crédito que pago a cuotas"})
    ids = [x["id"] for x in p["orden"]]
    assert ids.index("deuda") < ids.index("prima")
    ctx = _ctx(af, p)
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
    dec = decision.decidir(_ctx(af, p))
    assert dec["modo"] == "servicio"
    assert dec["restrictivos"][0]["id"] == "R-EMPLEO"
    assert dec["principal"]["accion"] == "servicio_cesantias"
    assert not dec["puede_iniciar_contacto"]
    assert all(not x["es_producto"] for x in dec["cola"])


def test_queja_abierta_bloquea_aunque_haya_prima():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    af["estado"]["queja_abierta"] = True
    dec = decision.decidir(_ctx(af, p))
    assert dec["modo"] == "servicio"
    assert dec["principal"] is None or not dec["cola"][0]["es_producto"]


def test_laura_el_15_de_junio_recibe_la_prima_con_rumbo_en_cinco_campos():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(_ctx(af, p))
    assert dec["modo"] == "asesoria"
    assert dec["principal"]["escenario"] == "O-PRIMA"
    assert set(dec["cinco_campos"]) == {"canal", "prioridad", "vigencia", "tono", "recomendacion"}
    assert dec["cinco_campos"]["vigencia"] == "2026-06-30"
    assert "no es un producto" in dec["cinco_campos"]["recomendacion"]


def test_el_no_se_respeta():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(_ctx(af, p), rechazos={"casa_con_prima"})
    assert "casa_con_prima" not in [x["accion"] for x in dec["cola"]]


def test_fuera_de_horario_no_se_inicia_contacto():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    domingo = datetime(2026, 6, 14, 10, 0)
    dec = decision.decidir(_ctx(af, p, date(2026, 6, 14), ahora=domingo))
    assert not dec["puede_iniciar_contacto"]
    assert decision.en_horario_de_contacto(datetime(2026, 6, 16, 9, 12))
    assert not decision.en_horario_de_contacto(datetime(2026, 6, 13, 16, 0))   # sábado después de las 3 p. m.


def test_festivo_no_se_inicia_contacto_y_espera_al_siguiente_dia_habil():
    """H16: el 15 de junio de 2026 es festivo (Sagrado Corazón)."""
    assert decision.es_festivo(date(2026, 6, 15))
    assert not decision.en_horario_de_contacto(datetime(2026, 6, 15, 9, 12))
    assert decision.siguiente_momento_de_contacto(datetime(2026, 6, 15, 9, 12)) == datetime(2026, 6, 16, 7, 0)
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    af["estado"]["autoriza_mensajes_comerciales"] = True
    dec = decision.decidir(_ctx(af, p))
    assert not dec["puede_iniciar_contacto"]
    assert dec["siguiente_contacto"] == "2026-06-16T07:00:00"
    dec = decision.decidir(_ctx(af, p, ahora=datetime(2026, 6, 16, 9, 0)))
    assert dec["puede_iniciar_contacto"]
    dec = decision.decidir(_ctx(af, p, ahora=datetime(2026, 6, 16, 9, 0)), contactos_esta_semana=1)
    assert not dec["puede_iniciar_contacto"]


def test_el_canal_no_dice_que_se_envio_un_aviso():
    """Revisor, no bloqueante: el canal es donde se muestra; el aviso proactivo va aparte."""
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    af["estado"]["autoriza_mensajes_comerciales"] = True
    dec = decision.decidir(_ctx(af, p, ahora=datetime(2026, 6, 16, 9, 0)))
    assert "mensajería" not in dec["cinco_campos"]["canal"]


def test_freno_de_servicio_pausa_lo_comercial():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(_ctx(af, p), metricas_servicio={"satisfaccion": 0.80})
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
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.validar_puente("Con cinco millones llegas")       # H15: cifras en letras
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.validar_puente("Ahorra el doble")
    CAT.validar_puente("Esto es lo primero de tu plan:")


def test_patrones_prohibidos_ampliados():
    """H15."""
    assert CAT.frases_prohibidas("Es mejor que un asesor")
    assert CAT.frases_prohibidas("No te toca declarar")
    assert CAT.frases_prohibidas("Inversión sin pérdidas")


def test_una_pieza_que_dice_no_invertir_no_sale_con_una_recomendacion():
    """Criterio A7 (hallazgo 1 del revisor): coherencia entre la nota y la acción."""
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.componer(["P4"], {"tipo": "tarjeta"}, {"recomienda_inversion": True})
    CAT.componer(["P4"], {"tipo": "tarjeta"}, {})
    assert "Antes de invertir" not in CAT.PIEZAS["P3"]["texto"]


def test_pieza_sin_variables_del_motor_no_sale():
    with pytest.raises(CAT.TextoNoPermitido):
        CAT.render("P3", {})


def test_todas_las_piezas_del_catalogo_pasan_el_control():
    for pid in CAT.PIEZAS:
        texto = CAT.PIEZAS[pid]["texto"]
        assert not CAT.frases_prohibidas(texto), pid


# Mandatos -------------------------------------------------------------------------------------
def test_mandato_tiene_siete_campos_y_consentimiento():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7)
    for campo in ("disparador", "accion", "destino", "tope", "vigencia_hasta", "aviso", "control"):
        assert getattr(m, campo)
    assert m.control == "proponer_y_confirmar"
    assert m.tope == 1_000_000 and "$1.000.000 a inversión por prima" in m.consentimiento
    assert "15 de junio de 2027" in m.consentimiento and "2027-06-15" not in m.consentimiento
    assert "si no confirmo, no se mueve nada" in m.consentimiento
    assert "revierte" not in m.consentimiento          # sin sentido en "te propongo y tú confirmas" (H7)
    assert "Autorizo" in m.consentimiento and " tu " not in m.consentimiento   # una sola persona gramatical


def test_el_tope_de_la_regla_limita_de_verdad():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7)
    r = mandatos.propuesta_de_la_regla(m, prima=6_000_000, brecha_colchon=0, porcentaje_colchon=0.7)
    assert r["a_inversion"] == 1_000_000 and r["queda_en_tu_cuenta"] == 5_000_000


def test_el_mandato_termina_en_su_vigencia():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7)
    mandatos.revisar_pausas(m, {}, True, date(2027, 6, 16))
    assert m.estado == "cancelado" and m.motivo_estado == "Terminó su vigencia"


def test_mandato_se_pausa_si_el_perfil_vence():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7)
    mandatos.revisar_pausas(m, {}, False, REVISION)
    assert m.estado == "pausado" and m.motivo_estado == "Perfil vencido"


def test_mandato_se_pausa_solo_si_pierde_el_empleo():
    m = mandatos.prima_con_rumbo("laura", REVISION, 0.7)
    mandatos.revisar_pausas(m, {"perdida_empleo": True}, True, REVISION)
    assert m.estado == "pausado"
    mandatos.cancelar(m, REVISION)
    assert m.estado == "cancelado"


def test_producto_que_no_cabe_en_el_perfil_no_es_elegible():
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(_ctx(af, p, perfil={**PERFIL_MODERADO, "perdida": "Hasta 5 de cada 100 pesos"}))
    assert "casa_con_prima" not in [x["accion"] for x in dec["cola"]]
    dec = decision.decidir(_ctx(af, p))
    assert "casa_con_prima" in [x["accion"] for x in dec["cola"]]


@pytest.mark.parametrize("cambio, motivo", [
    ({"objetivo": "Que no baje"}, "conservador"),
    ({"horizonte": "Menos de 2 años"}, "menos de 2 años"),
    ({"perdida": "Nada"}, "caída"),
])
def test_idoneidad_completa(cambio, motivo):
    """H1: perfil mínimo, horizonte y caída. Un conservador no recibe el portafolio moderado."""
    from pwa.motor import perfil as PF
    idoneo, motivos = PF.idoneidad("fpv_moderado", {**PERFIL_MODERADO, **cambio}, 10)
    assert not idoneo and any(motivo in m for m in motivos)
    af, p = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    dec = decision.decidir(_ctx(af, p, perfil={**PERFIL_MODERADO, **cambio}))
    assert "casa_con_prima" not in [x["accion"] for x in dec["cola"]]


def test_plazo_corto_de_la_meta_no_es_idoneo():
    from pwa.motor import perfil as PF
    assert not PF.idoneidad("fpv_moderado", PERFIL_MODERADO, 3)[0]
    assert PF.idoneidad("fpv_moderado", PERFIL_MODERADO, 10)[0]


# Puntaje (hallazgo 4 del revisor, criterio C9) ------------------------------------------------
def test_crear_la_regla_no_mueve_suficiencia_ni_riesgo():
    _, sin = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada", "propuesta_confirmada"})
    _, con = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada", "propuesta_confirmada", "regla_prima"})
    a = {x["id"]: x["valor"] for x in sin["pilares"]}
    b = {x["id"]: x["valor"] for x in con["pilares"]}
    assert a["suficiencia"] == b["suficiencia"] and a["riesgo"] == b["riesgo"]
    assert b["constancia"] > a["constancia"]
    assert "suma a tu constancia" in [x for x in con["pilares"] if x["id"] == "constancia"][0]["texto"]
    assert con["puntaje"] - sin["puntaje"] == round(25 / 6 * 10)      # solo la constancia, y se dice


def test_riesgo_sube_en_proporcion_a_lo_que_tiene_vehiculo():
    _, antes = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada"})
    _, despues = _plan(hoy=REVISION, hechos={"beneficiaria_confirmada", "propuesta_confirmada"})
    r0 = [x for x in antes["pilares"] if x["id"] == "riesgo"][0]["valor"]
    r1 = [x for x in despues["pilares"] if x["id"] == "riesgo"][0]["valor"]
    assert r0 == 70 and r1 == 85       # la mitad de lo del año que va a la casa ya tiene vehículo


# Permiso del salario (hallazgo 2 del revisor, C10) ---------------------------------------------
def test_sin_permiso_el_plan_no_usa_el_salario():
    _, p = _plan(autoriza=False)
    assert p["ingreso"]["valor"] is None
    assert p["prima"] is None and not p["pension"]["estimable"] and p["pension"]["mesada"] is None
    assert [x for x in p["pilares"] if x["id"] == "suficiencia"][0]["valor"] is None
    assert p["pilares_estimados"] == 5
    assert all(o["id"] != "prima" for o in p["orden"])
    textos = " ".join(x["texto"] for x in p["patrimonio"]["dimensiones"])
    assert "5,2" not in textos
    af, p = _plan(autoriza=False, hoy=REVISION)
    dec = decision.decidir(_ctx(af, p))
    assert dec["modo"] == "asesoria"                    # no es un restrictivo general (H17)
    assert all(e["id"] != "O-PRIMA" for e in dec["oportunidades"])


def test_con_ingreso_contado_el_plan_lo_usa():
    _, p = _plan(autoriza=False, cambios={"ingreso_declarado": 4_000_000})
    assert p["ingreso"]["origen"] == "nos contaste" and p["prima"]["monto"] == 2_000_000
    assert "el ingreso que nos contaste" in p["pension"]["supuestos_txt"]


# Otros hallazgos del experto financiero ----------------------------------------------------------
def test_probable_obligacion_de_declarar_de_laura():
    """H20: con prima, cesantías e intereses, Laura pasa el tope de 1.400 UVT por unos $100.400."""
    _, p = _plan()
    assert p["declarar"]["probable"] and p["declarar"]["diferencia"] == pytest.approx(100_400)


def test_sin_regimen_de_transicion_no_se_muestra_mesada():
    """H22."""
    _, p = _plan(cambios={})
    assert p["pension"]["mostrar_mesada"]
    af = datos.afiliado("laura")
    af["lo_que_sabemos"]["semanas_cotizadas"] = 300
    af["estado"]["autoriza_uso_salario"] = True
    d = {**af["diagnostico_propuesto"], "perfil": PERFIL_MODERADO}
    p = plan.armar_plan(af, d, HOY)
    assert not p["pension"]["mostrar_mesada"] and p["pension"]["mesada"] is None


def test_supuestos_de_la_pension_dicen_saldo_salario_constante_y_forma_de_pensionarse():
    """H23."""
    _, p = _plan()
    t = p["pension"]["supuestos_txt"]
    assert "$78 M" in t and "igual en pesos de hoy" in t and "retiro programado o renta vitalicia" in t


def test_la_comision_de_la_obligatoria_no_penaliza_el_plan():
    """H18."""
    _, p = _plan()
    ef = [x for x in p["pilares"] if x["id"] == "eficiencia"][0]
    assert ef["valor"] == 100 and "sale de tu cotización" in ef["texto"]


def test_beneficiarios_por_ley():
    """H4."""
    _, p = _plan()
    assert "ya es tu beneficiaria por ley" in p["orden"][0]["texto"]
