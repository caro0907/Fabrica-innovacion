"""Personal Wealth Architect · MVP v1.

La app es el hogar del plan: primero te conozco, después tu plan, y solo al final una
recomendación si el plan la pide. Datos ficticios. Nada en operación.
"""
import os
import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Form, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import catalogo as CAT
from . import redactor, registro
from .motor import calculos as C
from .motor import datos, decision, mandatos, perfil as PF, plan as PLAN
from .motor import supuestos as S
from .motor.escenarios import ACCIONES, ESCENARIOS
from .motor.formato import millones, miles, pesos, porcentaje

VERSION_APP = "1.0.0"
RAIZ = Path(__file__).resolve().parent
FECHA_REUNION = date(2026, 6, 1)
FECHA_REVISION = date(2026, 6, 15)
COOKIE = "pwa_sesion"
COOKIE_INTERNA = "pwa_interno"

@asynccontextmanager
async def _ciclo(_app):
    registro.iniciar()
    yield


app = FastAPI(title="Personal Wealth Architect · MVP", version=VERSION_APP, docs_url=None, redoc_url=None, lifespan=_ciclo)
app.mount("/static", StaticFiles(directory=RAIZ / "static"), name="static")
plantillas = Jinja2Templates(directory=RAIZ / "templates")
plantillas.env.globals.update(millones=millones, pesos=pesos, miles=miles, porcentaje=porcentaje,
                              VERSION_APP=VERSION_APP, PREGUNTAS_PERFIL=PF.PREGUNTAS,
                              tipo_pieza=lambda pid: CAT.PIEZAS[pid]["tipo"])


@app.middleware("http")
async def _cabeceras_seguras(request: Request, call_next):
    r = await call_next(request)
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["Referrer-Policy"] = "same-origin"
    r.headers["X-Frame-Options"] = "DENY"
    r.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'")
    return r


# Estado de la sesión de demostración ---------------------------------------------------------
HECHOS_A_ACCIONES = {
    "beneficiaria_confirmada": ["confirmar_beneficiarios"],
    "propuesta_confirmada": ["colchon_con_prima", "casa_con_prima"],
    "regla_prima": ["regla_prima"],
}


def sesion_de(request: Request) -> dict | None:
    sid = request.cookies.get(COOKIE)
    return registro.leer_sesion(sid) if sid else None


def estado(s: dict) -> dict:
    af = datos.afiliado(s["afiliado_id"])
    af["estado"].update({k: v for k, v in s["consentimientos"].items() if k in af["estado"]})
    hoy = date.fromisoformat(s["fecha_simulada"])
    d = s["diagnostico"]
    p = PLAN.armar_plan(af, d, hoy, s["hechos"])
    perf = d.get("perfil", {})
    ctx = decision.contexto(af, p, hoy, perfil_vigente=PF.completo(perf),
                            perdida_tolerada=PF.perdida_tolerada(perf),
                            senales_no_comprende=s["senales_no_comprende"])
    hechas = {a for h in s["hechos"] for a in HECHOS_A_ACCIONES.get(h, [])}
    dec = decision.decidir(ctx, registro.metricas(), s["contactos_semana"], hechas, s["rechazos"])
    consultor_nombre = datos.CONSULTOR_CON_NOMBRE_POR_SEGMENTO.get(af["segmento"], False)
    cons = ({**af["consultor"], "corto": af["consultor"]["nombre"].split(" ")[0]} if consultor_nombre
            else {"nombre": "Un consultor certificado", "iniciales": "C", "corto": "un consultor"})
    momento = f"{af['nombre']} · {fecha_larga(hoy)}"
    return {"s": s, "af": af, "hoy": hoy, "d": d, "plan": p, "ctx": ctx, "dec": dec, "cons": cons,
            "perfil_txt": PF.resumen(perf), "perfil_clase": PF.clasificar(perf),
            "consultor_con_nombre": consultor_nombre, "modo_ia": redactor.modo(), "momento": momento}


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def fecha_larga(f) -> str:
    if isinstance(f, str):
        f = date.fromisoformat(f)
    return f"{DIAS[f.weekday()]} {f.day} de {MESES[f.month - 1]}"


plantillas.env.filters["fecha"] = lambda f: fecha_larga(f).split(" ", 1)[1] if f else ""


def vars_catalogo(e: dict) -> dict:
    p, af = e["plan"], e["af"]
    return {
        "meses": p["colchon"]["meses_txt"],
        "persona": p["dependiente"] or "tu familia",
        "mes": "junio" if e["hoy"].month <= 6 else "diciembre",
        "prima": p["prima"]["monto_txt"],
        "supuestos": f"tu salario de cotización de hoy ({millones(af['lo_que_sabemos']['salario_cotizacion'])}) y la prima de medio salario",
        "pension": p["pension"]["mesada_txt"],
        "edad": p["pension"]["edad_pension"],
        "brecha": p["pension"]["brecha_txt"],
        "reglas": "las reglas de hoy, porque conservarías el régimen de transición" if p["pension"]["conserva_reglas_de_hoy"] else "las reglas de la reforma pensional",
        "puntaje": f"{p['puntaje']}",
        "accion": p["lo_que_mas_mueve"]["accion"].lower(),
    }


def piezas_permitidas(e: dict, ids: list[str]) -> list[str]:
    """Quita las piezas cuya condición el afiliado no cumple (por ejemplo, si retiró el permiso de usar su salario)."""
    ctx = contexto_catalogo(e)
    return [i for i in ids if not CAT.PIEZAS[i].get("condicion") or ctx.get(CAT.PIEZAS[i]["condicion"])] or ["P1"]


def contexto_catalogo(e: dict) -> dict:
    return {"paga_impuesto": False, "autoriza_uso_salario": e["af"]["estado"]["autoriza_uso_salario"]}


def render(request: Request, plantilla: str, e: dict | None = None, **extra):
    datos_vista = {"request": request, **(e or {}), **extra}
    return plantillas.TemplateResponse(request, plantilla, datos_vista)


def _a(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=303)


def requiere_sesion(request: Request, momento: str | None = None):
    """Cada pantalla vive en su momento: la primera reunión el 1 de junio y la app desde el 15."""
    s = sesion_de(request)
    if not s:
        return None, _a("/")
    if s["afiliado_id"] == "andres" and momento != "servicio":
        return None, _a("/servicio")
    if momento == "reunion" and "plan_guardado" in s["hechos"]:
        return None, _a("/inicio")
    if momento == "app" and "plan_guardado" not in s["hechos"]:
        return None, _a("/plan-inicial" if "diagnostico_listo" in s["hechos"] else "/d/bienvenida")
    return s, None


# Portada y demostraciones ---------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def portada(request: Request):
    return render(request, "portada.html", modo_ia=redactor.modo())


@app.post("/demo/{afiliado_id}")
def iniciar_demo(afiliado_id: str):
    if afiliado_id not in ("laura", "andres"):
        raise HTTPException(404)
    af = datos.afiliado(afiliado_id)
    if afiliado_id == "laura":
        sid = registro.crear_sesion("laura", FECHA_REUNION.isoformat(), af["diagnostico_propuesto"])
        destino = "/d/bienvenida"
    else:
        sid = registro.crear_sesion("andres", FECHA_REVISION.isoformat(), af["diagnostico_propuesto"],
                                    {"autoriza_uso_salario": True})
        s = registro.leer_sesion(sid)
        s["hechos"] |= {"plan_guardado", "diagnostico_listo"}
        registro.guardar_sesion(s)
        registro.guardar_mandato(sid, mandatos.pausar(
            mandatos.prima_con_rumbo("andres", date(2026, 1, 10), 0.7, 2_050_000), mandatos.PAUSAS_AUTOMATICAS[0],
            FECHA_REVISION).dict())
        destino = "/servicio"
    r = _a(destino)
    r.set_cookie(COOKIE, sid, httponly=True, samesite="lax", secure=os.environ.get("PWA_COOKIE_SEGURA") == "1")
    return r


# Primera reunión (1 de junio) ----------------------------------------------------------------
@app.get("/d/bienvenida", response_class=HTMLResponse)
def d1(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    e = estado(s)
    return render(request, "d1_bienvenida.html", e)


@app.post("/d/bienvenida")
def d1_post(request: Request, autoriza: str = Form("")):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    if autoriza != "si":
        return _a("/d/bienvenida?falta=autorizacion")
    s["consentimientos"]["autoriza_uso_salario"] = True
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="autorizar_uso_salario", tipo="consentimiento", respuesta="autorizó",
                       texto_mostrado="Autorizo usar mi salario de cotización, mis primas y mis cesantías para armar mi plan.")
    return _a("/d/metas")


@app.get("/d/metas", response_class=HTMLResponse)
def d2(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d2_metas.html", estado(s), METAS=METAS)


METAS = ["Tener tranquilidad", "Comprar mi casa", "Educar a mis hijos", "Pensionarme bien", "Salir de deudas", "Viajar", "Emprender"]


@app.post("/d/metas")
async def d2_post(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    f = await request.form()
    metas = [m for m in f.getlist("metas") if m in METAS] or ["Tener tranquilidad"]
    prioridad = f.get("prioridad") if f.get("prioridad") in metas else metas[0]
    s["diagnostico"].update(metas=metas, prioridad=prioridad)
    registro.guardar_sesion(s)
    return _a("/d/numeros")


@app.get("/d/numeros", response_class=HTMLResponse)
def d2b(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d2b_numeros.html", estado(s))


@app.post("/d/numeros")
def d2b_post(request: Request, plazo_casa: str = Form("En 10 años"), cuota_inicial_casa: int = Form(45_000_000),
             pension_deseada: int = Form(3_000_000)):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["diagnostico"].update(plazo_casa=plazo_casa, cuota_inicial_casa=max(0, min(cuota_inicial_casa, 300_000_000)),
                            pension_deseada=max(1_000_000, min(pension_deseada, 20_000_000)))
    registro.guardar_sesion(s)
    return _a("/d/vida")


@app.get("/d/vida", response_class=HTMLResponse)
def d3(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d3_vida.html", estado(s))


@app.post("/d/vida")
def d3_post(request: Request, depende: str = Form("Nadie"), edad_dependiente: int = Form(0),
            vivienda: str = Form("En arriendo"), deudas: str = Form("No tengo")):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["diagnostico"].update(depende=depende, edad_dependiente=max(0, min(edad_dependiente, 25)),
                            vivienda=vivienda, deudas=deudas)
    registro.guardar_sesion(s)
    return _a("/d/dinero")


@app.get("/d/dinero", response_class=HTMLResponse)
def d3b(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d3b_dinero.html", estado(s))


@app.post("/d/dinero")
async def d3b_post(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    f = await request.form()
    gastos = max(500_000, min(int(f.get("gastos_mensuales", 2_500_000)), 30_000_000))
    ahorro = max(0, min(int(f.get("ahorro", 0)), 500_000_000))
    s["diagnostico"].update(gastos_mensuales=gastos, ahorro=ahorro,
                            donde_ahorro=f.getlist("donde_ahorro") or ["En mi cuenta de ahorros"],
                            seguro_vida=f.get("seguro_vida", "No sé"))
    registro.guardar_sesion(s)
    return _a("/d/riesgo")


@app.get("/d/riesgo", response_class=HTMLResponse)
def d4(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d4_riesgo.html", estado(s), accion_form="/d/riesgo", volver="/d/dinero", paso=3)


def _leer_perfil(f) -> dict:
    perf = {}
    for k, _, _, opciones in PF.PREGUNTAS:
        v = f.get(k)
        perf[k] = v if v in opciones else opciones[0]
    return perf


@app.post("/d/riesgo")
async def d4_post(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["diagnostico"]["perfil"] = _leer_perfil(await request.form())
    s["diagnostico"]["perfil_fecha"] = s["fecha_simulada"]
    registro.guardar_sesion(s)
    return _a("/d/entendi")


@app.get("/d/entendi", response_class=HTMLResponse)
def d5(request: Request):
    s, r = requiere_sesion(request, "reunion")
    return r or render(request, "d5_entendi.html", estado(s))


@app.post("/d/entendi")
def d5_post(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["hechos"].add("diagnostico_listo")
    registro.guardar_sesion(s)
    return _a("/plan-inicial")


@app.get("/agenda", response_class=HTMLResponse)
def agenda(request: Request, desde: str = "bienvenida", slot: str = ""):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    e = estado(s)
    if slot:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="agendar_consultor", tipo="servicio", respuesta=slot, quien=e["cons"]["nombre"])
    volver = "/plan-inicial" if desde == "plan" else "/d/bienvenida"
    return render(request, "agenda.html", e, volver=volver, slot=slot, desde=desde)


# Tu plan, la primera vez -------------------------------------------------------------------------
@app.get("/plan-inicial", response_class=HTMLResponse)
def plan_inicial(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    if "diagnostico_listo" not in s["hechos"]:
        return _a("/d/bienvenida")
    e = estado(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="mostrar_plan", tipo="informacion", argumento=["P2", "P3", "P6", "B11", "A3"],
                       version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR,
                       version_supuestos=S.VERSION, perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"])
    return render(request, "plan_inicial.html", e)


@app.post("/accion/beneficiaria")
def confirmar_beneficiaria(request: Request, volver: str = Form("/plan-inicial")):
    s = sesion_de(request)
    if not s:
        return _a("/")
    s["hechos"].add("beneficiaria_confirmada")
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="confirmar_beneficiarios", escenario="O-BENEFICIARIOS", angulo="proteger a su familia",
                       argumento=["P6"], tipo="paso del plan", respuesta="confirmó", resultado="beneficiaria confirmada",
                       quien="El arquitecto digital")
    return _a(volver if volver in ("/plan-inicial", "/plan") else "/plan-inicial")


@app.post("/plan/guardar")
def guardar_plan(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["hechos"].add("plan_guardado")
    s["fecha_simulada"] = FECHA_REVISION.isoformat()
    registro.guardar_sesion(s)
    return _a("/inicio?vuelves=1")


# La app del plan (desde el 15 de junio) --------------------------------------------------------------
@app.get("/inicio", response_class=HTMLResponse)
def inicio(request: Request, vuelves: int = 0):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    nota = None
    if "propuesta_confirmada" not in s["hechos"] and e["dec"]["principal"] and e["dec"]["principal"]["escenario"] == "O-PRIMA":
        nota = redactor.nota_del_arquitecto(piezas_permitidas(e, ["B6", "P3"]), vars_catalogo(e), contexto_catalogo(e), e["af"]["nombre"])
    return render(request, "inicio.html", e, nota=nota, vuelves=vuelves, pestana="inicio")


@app.get("/revision", response_class=HTMLResponse)
def revision(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    nota = redactor.nota_del_arquitecto(piezas_permitidas(e, ["B6", "P5"]), vars_catalogo(e), contexto_catalogo(e), e["af"]["nombre"])
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"],
                       canal=e["dec"]["cinco_campos"]["canal"], accion="revision_periodica", escenario="O-PRIMA",
                       angulo="tranquilidad", argumento=nota["piezas"], texto_mostrado=nota["texto"], tipo="informacion",
                       version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                       perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
    return render(request, "revision.html", e, nota=nota)


def _propuesta(e: dict) -> dict:
    p = e["plan"]
    monto = p["prima"]["a_la_meta"]
    port = S.PORTAFOLIOS["fic_moderado"]
    caida = C.redondear_riesgo(C.caida_mal_anio(monto, "fic_moderado"))
    costo = C.costo_anual(monto, "fic_moderado")
    v = {"caida": pesos(caida), "metodo": f"una caída de {porcentaje(port['caida_mal_anio'])} en un mal año (método por aprobar)",
         "comision": f"{porcentaje(port['comision_anual'], 1)} ({pesos(costo)} al año sobre {pesos(monto)}, ficticia)",
         "alternativas": "dejarlo en tu cuenta de ahorros, un CDT o fondos de otras entidades"}
    comp = CAT.componer(["B14", "C3", "C4"], v, contexto_catalogo(e))
    textos = dict(zip(comp.piezas, comp.textos))
    elegible = "casa_con_prima" in [x["accion"] for x in e["dec"]["cola"]]
    return {"monto": monto, "portafolio": port, "caida": caida, "costo": costo, "textos": textos,
            "piezas": comp.piezas, "elegible": elegible, "cabe_en_perfil": port["caida_mal_anio"] <= PF.perdida_tolerada(e["d"].get("perfil", {}))}


@app.get("/propuesta", response_class=HTMLResponse)
def propuesta(request: Request, falta: str = ""):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    pr = _propuesta(e)
    if "propuesta_confirmada" not in s["hechos"]:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="casa_con_prima", escenario="O-PRIMA", angulo="su casa", argumento=pr["piezas"],
                           texto_mostrado=" ".join(pr["textos"].values()), tipo="recomendacion profesional",
                           version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                           perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
    return render(request, "propuesta.html", e, pr=pr, falta=falta)


@app.post("/propuesta/confirmar")
def propuesta_confirmar(request: Request, entiendo: str = Form(""), regla: str = Form(""), huella: str = Form("")):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    if entiendo != "si":
        s["senales_no_comprende"] += 1
        registro.guardar_sesion(s)
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="casa_con_prima", tipo="recomendacion profesional", respuesta="no marcó la comprensión",
                           resultado=f"señal de no comprender #{s['senales_no_comprende']}")
        return _a("/propuesta?falta=entiendo")
    if huella != "si":
        return _a("/propuesta?falta=huella")
    s["hechos"].add("propuesta_confirmada")
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="casa_con_prima", escenario="O-PRIMA", angulo="su casa", argumento=["B14", "C3", "C4", "A8"],
                       tipo="recomendacion profesional", respuesta="aceptó con confirmación biométrica (simulada)",
                       resultado="aprobado; sin movimiento de dinero: se pedirá cada transferencia el 30 de junio",
                       version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                       perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
    if regla == "si":
        m = mandatos.prima_con_rumbo(s["afiliado_id"], e["hoy"], e["plan"]["prima"]["porcentaje_colchon"], e["plan"]["prima"]["monto"])
        registro.guardar_mandato(s["id"], m.dict())
        s["hechos"].add("regla_prima")
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="regla_prima", escenario="O-PRIMA", tipo="mandato", texto_mostrado=m.consentimiento,
                           respuesta="aceptó el consentimiento", resultado="regla activa, proponer y confirmar")
    registro.guardar_sesion(s)
    return _a("/propuesta/lista")


@app.post("/propuesta/no")
def propuesta_no(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    s["rechazos"].add("casa_con_prima")
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="casa_con_prima", escenario="O-PRIMA", tipo="recomendacion profesional",
                       respuesta="no, gracias", resultado="se respeta; vuelve al motor como señal")
    return _a("/inicio")


@app.get("/propuesta/lista", response_class=HTMLResponse)
def propuesta_lista(request: Request):
    s, r = requiere_sesion(request, "app")
    return r or render(request, "propuesta_lista.html", estado(s))


@app.get("/plan", response_class=HTMLResponse)
def mi_plan(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    sabe = e["af"]["lo_que_sabemos"]
    calendario = [("30 jun", "Prima de mitad de año", e["plan"]["prima"]["monto_corto"]),
                  ("20 dic", "Prima de fin de año (primeros 20 días de diciembre)", e["plan"]["prima"]["monto_corto"]),
                  ("31 ene", "Intereses de tus cesantías (12% de lo del año)", miles(sabe["salario_cotizacion"] * 0.12)),
                  ("14 feb", "Tu empresa consigna tus cesantías del año", millones(sabe["salario_cotizacion"]))]
    return render(request, "plan.html", e, calendario=calendario, pestana="plan")


@app.get("/meta/casa", response_class=HTMLResponse)
def meta_casa(request: Request, mensual: int = 100_000):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    if not e["plan"]["casa"]:
        return _a("/plan")
    return render(request, "meta.html", e, sim=simular_casa(e, mensual), pestana="plan")


def simular_casa(e: dict, mensual: int) -> dict:
    casa = e["plan"]["casa"]
    mensual = max(0, min(int(mensual), 2_000_000))
    aporte = casa["aporte_primas_mensual"] + mensual
    bueno = C.meses_para_meta(casa["cuota"], casa["llevas"], aporte, S.RENTABILIDAD_ESCENARIO_BUENO)
    malo = C.meses_para_meta(casa["cuota"], casa["llevas"], aporte, S.RENTABILIDAD_ESCENARIO_MALO)
    inicio = e["hoy"].year + (e["hoy"].month - 1) / 12

    def anio(m):
        return int(inicio + m / 12) if m is not None else None
    return {"mensual": mensual, "mensual_txt": miles(mensual) if mensual else "$0", "aporte_total": aporte,
            "anio_bueno": anio(bueno), "anio_malo": anio(malo), "a_tiempo": bueno is not None and bueno <= casa["plazo_anios"] * 12,
            "puesto_10": pesos(aporte * casa["plazo_anios"] * 12)}


@app.get("/api/simular/casa")
def api_simular(request: Request, mensual: int = 0):
    s, r = requiere_sesion(request, "app")
    if r:
        raise HTTPException(401)
    e = estado(s)
    if not e["plan"]["casa"]:
        raise HTTPException(404)
    return simular_casa(e, mensual)


@app.get("/patrimonio", response_class=HTMLResponse)
def patrimonio(request: Request):
    s, r = requiere_sesion(request, "app")
    return r or render(request, "patrimonio.html", estado(s), pestana="patrimonio")


@app.get("/pilares", response_class=HTMLResponse)
def pilares(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    b11 = CAT.componer(["B11"], vars_catalogo(e), contexto_catalogo(e))
    return render(request, "pilares.html", e, b11=b11, pestana="patrimonio")


@app.get("/reglas", response_class=HTMLResponse)
def reglas(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    return render(request, "reglas.html", estado(s), lista=registro.mandatos(s["id"]),
                  CONTROLES=mandatos.CONTROLES, PAUSAS=mandatos.PAUSAS_AUTOMATICAS, pestana="equipo")


@app.post("/reglas/{mandato_id}/{accion}")
def regla_accion(request: Request, mandato_id: str, accion: str):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    for md in registro.mandatos(s["id"]):
        if md["id"] == mandato_id:
            m = mandatos.desde_dict(md)
            hoy = date.fromisoformat(s["fecha_simulada"])
            if accion == "pausar":
                mandatos.pausar(m, "La pausaste tú", hoy)
            elif accion == "reanudar":
                mandatos.reanudar(m, hoy)
            elif accion == "cancelar":
                mandatos.cancelar(m, hoy)
                s["hechos"].discard("regla_prima")
                registro.guardar_sesion(s)
            else:
                raise HTTPException(400)
            registro.guardar_mandato(s["id"], m.dict())
            registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                               accion=f"mandato_{accion}", tipo="mandato", respuesta=accion, resultado=m.estado)
    return _a("/reglas")


@app.post("/permisos/{permiso}")
def permisos(request: Request, permiso: str, valor: str = Form("no")):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    if permiso not in ("autoriza_agentes_externos", "autoriza_mensajes_comerciales", "autoriza_uso_salario"):
        raise HTTPException(400)
    s["consentimientos"][permiso] = valor == "si"
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion=permiso, tipo="consentimiento", respuesta="otorgó" if valor == "si" else "retiró")
    return _a("/reglas")


@app.get("/equipo", response_class=HTMLResponse)
def equipo(request: Request, slot: str = ""):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    if slot:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="agendar_consultor", tipo="servicio", respuesta=slot, quien=e["cons"]["nombre"])
    return render(request, "equipo.html", e, slot=slot, pestana="equipo")


@app.get("/perfil", response_class=HTMLResponse)
def ver_perfil(request: Request):
    s, r = requiere_sesion(request, "app")
    return r or render(request, "perfil.html", estado(s), pestana="equipo")


@app.get("/perfil/cambiar", response_class=HTMLResponse)
def cambiar_perfil(request: Request):
    s, r = requiere_sesion(request, "app")
    return r or render(request, "d4_riesgo.html", estado(s), accion_form="/perfil/cambiar", volver="/perfil", paso=None)


@app.post("/perfil/cambiar")
async def cambiar_perfil_post(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    s["diagnostico"]["perfil"] = _leer_perfil(await request.form())
    s["diagnostico"]["perfil_fecha"] = s["fecha_simulada"]
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="actualizar_perfil", tipo="perfil", perfil_usado=PF.resumen(s["diagnostico"]["perfil"]))
    return _a("/perfil")


@app.get("/como-funciona", response_class=HTMLResponse)
def como_funciona(request: Request):
    s, r = requiere_sesion(request, "app")
    return r or render(request, "como_funciona.html", estado(s), pestana="equipo")


@app.get("/pregunta", response_class=HTMLResponse)
def pregunta(request: Request, q: str = ""):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    respuesta = responder(e, q) if q else None
    if q:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app · pregunta",
                           accion=f"responder_{respuesta['intencion']}", tipo="informacion", argumento=respuesta["piezas"],
                           texto_mostrado=respuesta["texto"], respuesta=q[:200], version_catalogo=CAT.VERSION)
    return render(request, "pregunta.html", e, q=q, respuesta=respuesta)


def responder(e: dict, q: str) -> dict:
    """La pregunta responde con piezas del catálogo y lleva al plan. Lo que pidió va primero."""
    it = redactor.intencion(q)
    v, ctx = vars_catalogo(e), contexto_catalogo(e)
    mapa = {
        "colchon": (["P3", "P5"], "/plan", "Ver tu plan"),
        "casa": (["B8"], "/meta/casa", "Ver tu casa con el simulador"),
        "pension": (["B12"], "/plan", "Ver tu pensión y sus supuestos"),
        "prima": (["B6"], "/revision", "Ver tu revisión de junio"),
        "cesantias": (["B8"], "/patrimonio", "Ver tu patrimonio"),
        "asesor": (["P8"], "/equipo", f"Hablar con {e['cons']['nombre']}"),
        "impuesto": ([], "/equipo", f"Verlo con {e['cons']['nombre']}"),
        "otra": (["P1"], "/plan", "Ver tu plan"),
    }
    piezas, enlace, enlace_txt = mapa[it]
    if it == "impuesto":
        texto = ("Con tu salario, el cálculo del impuesto lo ve un asesor con tu certificado de ingresos: "
                 "pagar impuesto y tener que declarar son dos cosas distintas, y la obligación de declarar la confirma un asesor contigo.")
        return {"intencion": it, "texto": texto, "piezas": ["A2"], "enlace": enlace, "enlace_txt": enlace_txt}
    if it == "pension" and e["plan"]["pension"]["brecha"] <= 0:
        piezas = ["B12"]
    nota = redactor.nota_del_arquitecto(piezas_permitidas(e, piezas), v, ctx, e["af"]["nombre"])
    return {"intencion": it, "texto": nota["texto"], "piezas": nota["piezas"], "enlace": enlace, "enlace_txt": enlace_txt,
            "textos": nota["textos"]}


# Modo servicio: Andrés -----------------------------------------------------------------------------
@app.get("/servicio", response_class=HTMLResponse)
def servicio(request: Request, solicitado: int = 0, escalado: int = 0):
    s = sesion_de(request)
    if not s or s["afiliado_id"] != "andres":
        return _a("/")
    e = estado(s)
    v = {**vars_catalogo(e)}
    comp = CAT.componer(["B9", "B10"], v, contexto_catalogo(e))
    meses = e["af"]["lo_que_sabemos"]["cesantias"] / e["d"]["gastos_mensuales"]
    return render(request, "servicio.html", e, textos=dict(zip(comp.piezas, comp.textos)), meses=meses,
                  solicitado=solicitado, escalado=escalado, reglas_lista=registro.mandatos(s["id"]))


@app.post("/servicio/consultor")
def servicio_consultor(request: Request):
    s = sesion_de(request)
    if not s or s["afiliado_id"] != "andres":
        return _a("/")
    registro.registrar("andres", sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app · pregunta",
                       accion="escalar_a_consultor", escenario="R-EMPLEO", tipo="servicio", respuesta="pidió hablar con alguien",
                       resultado="traspaso con el contexto completo", quien="Consultor")
    q = "?escalado=1" + ("&solicitado=1" if request.query_params.get("solicitado") else "")
    return _a("/servicio" + q)


@app.post("/servicio/solicitar")
def servicio_solicitar(request: Request):
    s = sesion_de(request)
    if not s or s["afiliado_id"] != "andres":
        return _a("/")
    registro.registrar("andres", sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app · pregunta",
                       accion="servicio_cesantias", escenario="R-EMPLEO", angulo="tranquilidad", argumento=["B9", "B10", "A6"],
                       tipo="servicio", respuesta="solicitó el retiro total de sus cesantías",
                       resultado="solicitud recibida (simulada); sin ofertas", quien="El arquitecto digital")
    return _a("/servicio?solicitado=1")


# Vistas internas ------------------------------------------------------------------------------------
def acceso_interno(request: Request) -> bool:
    clave = os.environ.get("PWA_CLAVE_INTERNA")
    if not clave:
        return True
    return secrets.compare_digest(request.cookies.get(COOKIE_INTERNA, ""), clave)


@app.get("/interno/entrar", response_class=HTMLResponse)
def interno_entrar(request: Request, siguiente: str = "/interno/motor"):
    return render(request, "interno_entrar.html", siguiente=siguiente)


@app.post("/interno/entrar")
def interno_entrar_post(clave: str = Form(""), siguiente: str = Form("/interno/motor")):
    esperada = os.environ.get("PWA_CLAVE_INTERNA", "")
    if not esperada or not secrets.compare_digest(clave, esperada):
        return _a("/interno/entrar?error=1")
    r = _a(siguiente if siguiente.startswith("/interno/") else "/interno/motor")
    r.set_cookie(COOKIE_INTERNA, clave, httponly=True, samesite="strict", secure=os.environ.get("PWA_COOKIE_SEGURA") == "1")
    return r


def _interno(request: Request, destino: str):
    if not acceso_interno(request):
        return None, _a(f"/interno/entrar?siguiente={destino}")
    s = sesion_de(request)
    if not s:
        return None, _a("/")
    return estado(s), None


@app.get("/interno/consultor", response_class=HTMLResponse)
def interno_consultor(request: Request):
    e, r = _interno(request, "/interno/consultor")
    if r:
        return r
    enganche = decision.brief_enganche(e["dec"], e["plan"], e["af"])
    pr = _propuesta(e) if e["dec"]["modo"] == "asesoria" else None
    return render(request, "interno_consultor.html", e, enganche=enganche, pr=pr,
                  historia=registro.interacciones(e["s"]["id"], 30), lista=registro.mandatos(e["s"]["id"]),
                  sin_clave=not os.environ.get("PWA_CLAVE_INTERNA"))


@app.get("/interno/motor", response_class=HTMLResponse)
def interno_motor(request: Request):
    e, r = _interno(request, "/interno/motor")
    if r:
        return r
    return render(request, "interno_motor.html", e, ESCENARIOS=ESCENARIOS, ACCIONES=ACCIONES, CAT=CAT, S=S,
                  metricas=registro.metricas(), historia=registro.interacciones(e["s"]["id"], 40),
                  sin_clave=not os.environ.get("PWA_CLAVE_INTERNA"), VERSION_MOTOR=decision.VERSION_MOTOR)


@app.post("/interno/freno")
def interno_freno(request: Request, satisfaccion: float = Form(0.87), resolucion_sin_oficina: float = Form(0.82),
                  transferencia_a_humano: float = Form(0.12)):
    if not acceso_interno(request):
        return _a("/interno/entrar")
    registro.fijar_metrica("satisfaccion", max(0, min(satisfaccion, 1)))
    registro.fijar_metrica("resolucion_sin_oficina", max(0, min(resolucion_sin_oficina, 1)))
    registro.fijar_metrica("transferencia_a_humano", max(0, min(transferencia_a_humano, 1)))
    return _a("/interno/motor#freno")


# Consulta de solo lectura para agentes externos ---------------------------------------------------------
@app.get("/api/v1/plan")
def api_plan(request: Request, authorization: str = Header(""), x_sesion: str = Header("")):
    """Un agente externo autorizado consulta el plan, nunca lo cambia.
    Exige token del agente y el consentimiento específico del afiliado."""
    token = os.environ.get("PWA_TOKEN_AGENTES")
    if not token or not secrets.compare_digest(authorization, f"Bearer {token}"):
        raise HTTPException(401, "Agente no identificado")
    s = registro.leer_sesion(x_sesion) if x_sesion else None
    if not s:
        raise HTTPException(404, "Afiliado no encontrado")
    if not s["consentimientos"].get("autoriza_agentes_externos"):
        raise HTTPException(403, "El afiliado no autorizó la consulta de agentes externos")
    e = estado(s)
    p = e["plan"]
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="api",
                       accion="consulta_agente_externo", tipo="consulta de solo lectura", resultado="entregado")
    return JSONResponse({
        "aviso": "Información del plan. No es una recomendación profesional. Datos ficticios.",
        "version": {"motor": decision.VERSION_MOTOR, "supuestos": S.VERSION, "catalogo": CAT.VERSION},
        "puntaje": p["puntaje"],
        "pilares": [{k: x[k] for k in ("nombre", "valor", "texto")} for x in p["pilares"]],
        "metas": [{k: m[k] for k in ("nombre", "estado", "texto")} for m in p["metas"]],
        "orden_del_plan": [{k: o[k] for k in ("cuando", "titulo", "es_producto")} for o in p["orden"]],
        "pension": {"estimada": p["pension"]["mesada_txt"], "supuestos": p["pension"]["supuestos_txt"]},
    })


@app.get("/salud")
def salud():
    return {"estado": "ok", "version": VERSION_APP, "modo_ia": redactor.modo()}
