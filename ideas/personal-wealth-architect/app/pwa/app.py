"""Personal Wealth Architect · MVP v1.

La app es el hogar del plan: primero te conozco, después tu plan, y solo al final una
recomendación si el plan la pide. Datos ficticios. Nada en operación.
"""
import hashlib
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

VERSION_APP = "1.1.0"
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
    perf = d.get("perfil") or {}
    vigente = PF.vigente(perf, d.get("perfil_fecha"), hoy)
    _revisar_mandatos(s, af, vigente, hoy)
    ctx = decision.contexto(af, p, hoy, perfil_vigente=vigente, perfil=perf,
                            perdida_tolerada=PF.perdida_tolerada(perf),
                            plazo_meta_anios=p["casa"]["plazo_anios"] if p["casa"] else None,
                            senales_no_comprende=s["senales_no_comprende"])
    hechas = {a for h in s["hechos"] for a in HECHOS_A_ACCIONES.get(h, [])}
    contactos = registro.contactos_comerciales_semana(s["id"], s["fecha_simulada"])
    dec = decision.decidir(ctx, registro.metricas(), contactos, hechas, s["rechazos"])
    consultor_nombre = datos.CONSULTOR_CON_NOMBRE_POR_SEGMENTO.get(af["segmento"], False)
    cons = ({**af["consultor"], "corto": af["consultor"]["nombre"].split(" ")[0]} if consultor_nombre
            else {"nombre": "Un consultor certificado", "iniciales": "C", "corto": "un consultor"})
    momento = f"{af['nombre']} · {fecha_larga(hoy)}"
    return {"s": s, "af": af, "hoy": hoy, "d": d, "plan": p, "ctx": ctx, "dec": dec, "cons": cons,
            "perfil_txt": PF.resumen(perf), "perfil_clase": PF.clasificar(perf), "perfil_vigente": vigente,
            "consultor_con_nombre": consultor_nombre, "modo_ia": redactor.modo(), "momento": momento}


def _revisar_mandatos(s: dict, af: dict, perfil_vigente: bool, hoy: date) -> None:
    """Las pausas automáticas corren de verdad (H10): se revisan en cada pantalla y queda registro."""
    for md in registro.mandatos(s["id"]):
        m = mandatos.desde_dict(md)
        antes = m.estado
        mandatos.revisar_pausas(m, af["estado"], perfil_vigente, hoy)
        if m.estado != antes:
            registro.guardar_mandato(s["id"], m.dict())
            registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="motor",
                               accion="mandato_pausa_automatica", tipo="mandato", resultado=f"{m.estado}: {m.motivo_estado}")
            if m.estado == "cancelado":
                s["hechos"].discard("regla_prima")
                registro.guardar_sesion(s)


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def fecha_larga(f) -> str:
    if isinstance(f, str):
        f = date.fromisoformat(f)
    return f"{DIAS[f.weekday()]} {f.day} de {MESES[f.month - 1]}"


plantillas.env.filters["fecha"] = lambda f: fecha_larga(f).split(" ", 1)[1] if f else ""


def vars_catalogo(e: dict) -> dict:
    p = e["plan"]
    ing = p["ingreso"]
    if ing["valor"] is None:
        supuestos = "lo que nos contaste"
    elif ing["origen"] == "sabemos":
        supuestos = f"tu salario de cotización de hoy ({ing['txt']}) y la prima de medio salario"
    else:
        supuestos = f"el ingreso que nos contaste ({ing['txt']}) y la prima de medio salario"
    rf = PLAN.registro_familiar(e["d"])
    v = {
        "meses": p["colchon"]["meses_txt"],
        "persona": p["dependiente"] or "tu familia",
        "ya_es": rf["ya_es"], "registrar": rf["registrar"],
        "mes": "junio" if e["hoy"].month <= 6 else "diciembre",
        "supuestos": supuestos,
        "edad": p["pension"]["edad_pension"],
        "reglas": "las reglas de hoy, porque conservarías el régimen de transición" if p["pension"]["conserva_reglas_de_hoy"] else "las reglas de la reforma pensional",
        "fecha_reforma": S.REFORMA_PENSIONAL["fecha_texto"],
        "puntaje": f"{p['puntaje']}",
        "accion": p["lo_que_mas_mueve"]["accion"].lower(),
        "fecha_perfil": (e["d"].get("perfil_fecha") and fecha_larga(e["d"]["perfil_fecha"]).split(" ", 1)[1]) or "",
        "consultor": e["cons"]["corto"][0].upper() + e["cons"]["corto"][1:],
    }
    if p["prima"]:
        v.update(prima=p["prima"]["monto_txt"], pct_colchon=p["prima"]["porcentaje_colchon_txt"])
    if p["pension"]["mostrar_mesada"]:
        v.update(pension=p["pension"]["mesada_txt"], brecha=p["pension"]["brecha_txt"])
    if p["declarar"]:
        v.update(ingresos=p["declarar"]["ingresos_txt"], anio_declara=p["declarar"]["anio_declara"],
                 tope=p["declarar"]["tope_txt"])
    return v


def piezas_permitidas(e: dict, ids: list[str], recomienda_inversion: bool = False) -> list[str]:
    """Quita las piezas cuya condición el afiliado no cumple (por ejemplo, si retiró el permiso de usar su
    salario) y las que contradicen una recomendación de inversión en la misma pantalla (criterio A7)."""
    ctx = contexto_catalogo(e, recomienda_inversion)
    return [i for i in ids if CAT.permitida(i, ctx)] or ["P1"]


def contexto_catalogo(e: dict, recomienda_inversion: bool = False) -> dict:
    p = e["plan"]
    return {"paga_impuesto": False, "autoriza_uso_salario": e["af"]["estado"]["autoriza_uso_salario"],
            "tiene_ingreso": p["ingreso"]["valor"] is not None, "estima_pension": p["pension"]["mostrar_mesada"],
            "dependiente_hijos": p["dependiente_hijos"], "recomienda_inversion": recomienda_inversion}


def recomienda_inversion(e: dict) -> bool:
    """¿La decisión de hoy lleva a una recomendación de inversión?"""
    return (e["dec"]["modo"] == "asesoria" and "casa_con_prima" in [x["accion"] for x in e["dec"]["cola"]]
            and "propuesta_confirmada" not in e["s"]["hechos"])


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


TEXTO_PERMISO_SALARIO = (
    "Autorizo a mi administradora de fondos, como responsable de mis datos, a usar mi salario de cotización, "
    "mis primas y mis cesantías con una sola finalidad: armar y revisar mi plan. Puedo conocer, actualizar y "
    "rectificar mis datos, y retirar este permiso cuando quiera en Mis reglas y permisos.")
TEXTO_PERMISO_MENSAJES = (
    "Acepto que me envíen propuestas de mi plan por mensajería, máximo una vez por semana, de lunes a viernes "
    "de 7 a. m. a 7 p. m. y los sábados de 8 a. m. a 3 p. m., nunca domingos ni festivos. Lo puedo retirar cuando quiera.")
TEXTO_PERMISO_AGENTES = "Acepto que un asistente digital que yo autorice consulte mi plan, solo para leerlo."
TEXTOS_PERMISOS = {"autoriza_uso_salario": TEXTO_PERMISO_SALARIO, "autoriza_mensajes_comerciales": TEXTO_PERMISO_MENSAJES,
                   "autoriza_agentes_externos": TEXTO_PERMISO_AGENTES}


@app.post("/d/bienvenida")
def d1_post(request: Request, autoriza: str = Form(""), mensajes: str = Form(""), ingreso: str = Form("")):
    """El permiso del salario es opcional (H5): sin él, la persona puede contar su ingreso o seguir sin él."""
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["consentimientos"]["autoriza_uso_salario"] = autoriza == "si"
    s["consentimientos"]["autoriza_mensajes_comerciales"] = mensajes == "si"
    if autoriza != "si" and ingreso.strip().isdigit():
        s["diagnostico"]["ingreso_declarado"] = max(0, min(int(ingreso), 100_000_000)) or None
    else:
        s["diagnostico"].pop("ingreso_declarado", None)
    registro.guardar_sesion(s)
    for permiso, valor in (("autoriza_uso_salario", autoriza == "si"), ("autoriza_mensajes_comerciales", mensajes == "si")):
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion=permiso, tipo="consentimiento", respuesta="otorgó" if valor else "no otorgó",
                           texto_mostrado=TEXTOS_PERMISOS[permiso])
    return _a("/d/metas")


@app.get("/privacidad", response_class=HTMLResponse)
def privacidad(request: Request):
    s = sesion_de(request)
    e = estado(s) if s else {}
    return render(request, "privacidad.html", e, volver=request.headers.get("referer", "/") if s else "/")


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
    if r:
        return r
    e = estado(s)
    # La cifra que se propone es la misma con que arranca el deslizador (H25), en cifras redondas de $0,5 M.
    ingreso = e["plan"]["ingreso"]["valor"]
    propuesta = round(ingreso * 0.6 / 500_000) * 500_000 if ingreso else None
    if propuesta and "pension_ajustada" not in s["hechos"]:
        e["d"]["pension_deseada"] = propuesta
    return render(request, "d2b_numeros.html", e, propuesta_pension=propuesta)


@app.post("/d/numeros")
def d2b_post(request: Request, plazo_casa: str = Form("En 10 años"), cuota_inicial_casa: int = Form(45_000_000),
             pension_deseada: int = Form(3_000_000)):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    s["diagnostico"].update(plazo_casa=plazo_casa, cuota_inicial_casa=max(0, min(cuota_inicial_casa, 300_000_000)),
                            pension_deseada=max(1_000_000, min(pension_deseada, 20_000_000)))
    s["hechos"].add("pension_ajustada")
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


def _leer_perfil(f) -> dict | None:
    """Solo respuestas de la persona: si falta una, no hay perfil (H9). Nunca se completa por defecto."""
    perf = {}
    for k, _, _, opciones in PF.PREGUNTAS:
        v = f.get(k)
        if v not in opciones:
            return None
        perf[k] = v
    return perf


@app.post("/d/riesgo")
async def d4_post(request: Request):
    s, r = requiere_sesion(request, "reunion")
    if r:
        return r
    perf = _leer_perfil(await request.form())
    if perf is None:
        return _a("/d/riesgo?falta=perfil")
    s["diagnostico"]["perfil"] = perf
    s["diagnostico"]["perfil_fecha"] = s["fecha_simulada"]
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="perfil", tipo="perfil", argumento=perf, perfil_usado=PF.resumen(perf))
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
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="diagnostico_confirmado", tipo="diagnostico", argumento=s["diagnostico"],
                       perfil_usado=PF.resumen(s["diagnostico"].get("perfil") or {}), respuesta="confirmó lo que entendimos")
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
                       argumento=[PLAN.registro_familiar(s["diagnostico"])["pieza"]], tipo="paso del plan",
                       respuesta="registró", resultado="grupo familiar registrado (simulado)", quien="El arquitecto digital")
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
        # Coherencia (hallazgo 1 del revisor, H3): si la decisión lleva a invertir para la casa, la nota dice la
        # regla real (P9: colchón primero con el 70%, la casa con el resto), nunca "antes de invertir".
        reco = recomienda_inversion(e)
        piezas = ["B6", "P9"] if reco and e["plan"]["casa"] and e["plan"]["prima"]["al_colchon"] > 0 else ["B6", "P3"]
        nota = redactor.nota_del_arquitecto(piezas_permitidas(e, piezas, reco), vars_catalogo(e),
                                            contexto_catalogo(e, reco), e["af"]["nombre"])
    sin_ingreso = None
    if e["plan"]["ingreso"]["valor"] is None:
        sin_ingreso = CAT.componer(["P10"], {}, {})
    return render(request, "inicio.html", e, nota=nota, vuelves=vuelves, pestana="inicio", sin_ingreso=sin_ingreso)


@app.get("/revision", response_class=HTMLResponse)
def revision(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    reco = recomienda_inversion(e)
    nota = redactor.nota_del_arquitecto(piezas_permitidas(e, ["B6", "P5"], reco), vars_catalogo(e),
                                        contexto_catalogo(e, reco), e["af"]["nombre"])
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"],
                       canal="app (la persona abrió su revisión)", accion="revision_periodica", escenario="O-PRIMA",
                       angulo="tranquilidad", argumento=nota["piezas"], texto_mostrado=nota["texto"], tipo="informacion",
                       version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                       perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
    return render(request, "revision.html", e, nota=nota)


PORTAFOLIO_CASA = ACCIONES["casa_con_prima"].portafolio


def _propuesta(e: dict) -> dict:
    p = e["plan"]
    monto = p["prima"]["a_la_meta"]
    port = S.PORTAFOLIOS[PORTAFOLIO_CASA]
    caida = C.redondear_riesgo(C.caida_mal_anio(monto, PORTAFOLIO_CASA))
    costo = C.costo_anual(monto, PORTAFOLIO_CASA)
    v = {**vars_catalogo(e), "caida": pesos(caida),
         "metodo": f"una caída de {porcentaje(port['caida_mal_anio'])} en un mal año (método por aprobar)",
         "comision": f"{porcentaje(port['comision_anual'], 1)} al año, unos {pesos(costo)} sobre {pesos(monto)} (tarifa ficticia)",
         "alternativas": "dejarlo en tu cuenta de ahorros, un certificado de depósito a término o fondos de otras entidades"}
    comp = CAT.componer(ACCIONES["casa_con_prima"].piezas, v, contexto_catalogo(e, True))
    textos = dict(zip(comp.piezas, comp.textos))
    elegible = "casa_con_prima" in [x["accion"] for x in e["dec"]["cola"]]
    plazo = p["casa"]["plazo_anios"] if p["casa"] else None
    idoneo, motivos = PF.idoneidad(PORTAFOLIO_CASA, e["d"].get("perfil") or {}, plazo)
    return {"monto": monto, "portafolio": port, "caida": caida, "costo": costo, "textos": textos,
            "piezas": comp.piezas, "elegible": elegible and idoneo, "idoneo": idoneo, "motivos_no_idoneo": motivos}


@app.get("/propuesta", response_class=HTMLResponse)
def propuesta(request: Request, falta: str = ""):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    if not e["plan"]["prima"] or not e["plan"]["casa"]:
        return _a("/revision")
    pr = _propuesta(e)
    if "propuesta_confirmada" not in s["hechos"]:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="casa_con_prima", escenario="O-PRIMA", angulo="su casa", argumento=pr["piezas"],
                           texto_mostrado=" ".join(pr["textos"].values()), tipo="recomendacion profesional",
                           version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                           perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
    return render(request, "propuesta.html", e, pr=pr, falta=falta)


@app.post("/propuesta/confirmar")
def propuesta_confirmar(request: Request, entiendo: str = Form("")):
    """Paso 1: la comprensión. Paso 2, visible: la huella (simulada) en /huella."""
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    if entiendo != "si":
        s["senales_no_comprende"] += 1
        registro.guardar_sesion(s)
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="casa_con_prima", tipo="recomendacion profesional", respuesta="no marcó la comprensión",
                           resultado=f"señal de no comprender #{s['senales_no_comprende']}")
        return _a("/propuesta?falta=entiendo")
    s["hechos"].add("huella_pendiente:propuesta")
    registro.guardar_sesion(s)
    return _a("/huella?para=propuesta")


QUE_SE_APRUEBA = {"propuesta": "Aprobar tu propuesta para la prima", "regla": "Dejar tu regla Prima con rumbo"}


@app.get("/huella", response_class=HTMLResponse)
def huella(request: Request, para: str = "propuesta"):
    """Paso visible de la confirmación con la huella del celular (simulada en el MVP)."""
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    if para not in QUE_SE_APRUEBA or f"huella_pendiente:{para}" not in s["hechos"]:
        return _a("/propuesta" if para == "propuesta" else "/propuesta/lista")
    return render(request, "huella.html", estado(s), para=para, que=QUE_SE_APRUEBA[para])


@app.post("/huella")
def huella_post(request: Request, para: str = Form("propuesta")):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    if para not in QUE_SE_APRUEBA or f"huella_pendiente:{para}" not in s["hechos"]:
        return _a("/inicio")
    e = estado(s)
    s["hechos"].discard(f"huella_pendiente:{para}")
    if para == "propuesta":
        pr = _propuesta(e)
        if not pr["elegible"]:
            registro.guardar_sesion(s)
            return _a("/propuesta")
        s["hechos"].add("propuesta_confirmada")
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="casa_con_prima", escenario="O-PRIMA", angulo="su casa", argumento=pr["piezas"],
                           texto_mostrado=" ".join(pr["textos"].values()),
                           tipo="recomendacion profesional", respuesta="aprobó con su huella (simulada)",
                           resultado="aprobado; sin movimiento de dinero: se pedirá confirmar cada transferencia el 30 de junio",
                           version_catalogo=CAT.VERSION, version_motor=decision.VERSION_MOTOR, version_supuestos=S.VERSION,
                           perfil_usado=e["perfil_txt"], grupo=e["dec"]["grupo"], quien=e["dec"]["quien_lo_hace"])
        registro.guardar_sesion(s)
        return _a("/propuesta/lista")
    m = mandatos.prima_con_rumbo(s["afiliado_id"], e["hoy"], e["plan"]["prima"]["porcentaje_colchon"])
    registro.guardar_mandato(s["id"], m.dict())
    s["hechos"].add("regla_prima")
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="regla_prima", escenario="O-PRIMA", tipo="mandato", texto_mostrado=m.consentimiento,
                       respuesta="marcó la autorización, que vio antes de aceptar, y confirmó con su huella (simulada)",
                       resultado="regla activa: te propongo y tú confirmas")
    return _a("/reglas?nueva=1")


@app.post("/regla/nueva")
def regla_nueva(request: Request, acepto: str = Form("")):
    """La regla se ofrece después de aprobar (diseño v5.2), con condiciones y autorización visibles y la casilla
    desmarcada (criterio B12). Sin la casilla no se crea."""
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    if "propuesta_confirmada" not in s["hechos"] or "regla_prima" in s["hechos"]:
        return _a("/propuesta/lista")
    if acepto != "si":
        return _a("/propuesta/lista?falta=acepto")
    s["hechos"].add("huella_pendiente:regla")
    registro.guardar_sesion(s)
    return _a("/huella?para=regla")


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
def propuesta_lista(request: Request, falta: str = ""):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    if "propuesta_confirmada" not in s["hechos"]:
        return _a("/propuesta")
    m = mandatos.prima_con_rumbo(s["afiliado_id"], e["hoy"], e["plan"]["prima"]["porcentaje_colchon"])
    ofrecer = "regla_prima" not in s["hechos"] and not any(x["estado"] != "cancelado" for x in registro.mandatos(s["id"]))
    if ofrecer and not falta:
        registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                           accion="regla_prima", escenario="O-PRIMA", tipo="mandato", texto_mostrado=m.consentimiento,
                           respuesta="se le mostró la autorización antes de aceptar")
    return render(request, "propuesta_lista.html", e, regla=m, ofrecer=ofrecer, falta=falta,
                  CONTROLES=mandatos.CONTROLES, fecha_txt=mandatos.fecha_txt)


@app.get("/plan", response_class=HTMLResponse)
def mi_plan(request: Request):
    s, r = requiere_sesion(request, "app")
    if r:
        return r
    e = estado(s)
    ingreso = e["plan"]["ingreso"]["valor"]
    sin = "Sin estimar"
    calendario = [("30 jun", "Prima de mitad de año", e["plan"]["prima"]["monto_corto"] if ingreso else sin),
                  ("20 dic", "Prima de fin de año (primeros 20 días de diciembre)", e["plan"]["prima"]["monto_corto"] if ingreso else sin),
                  ("31 ene", "Intereses de tus cesantías (12% de lo del año)", miles(ingreso * S.TASA_INTERESES_CESANTIAS) if ingreso else sin),
                  ("14 feb", "Tu empresa consigna tus cesantías del año", millones(ingreso) if ingreso else sin)]
    p10 = CAT.componer(["P10"], {}, {}) if not ingreso else None
    return render(request, "plan.html", e, calendario=calendario, pestana="plan", p10=p10)


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
    """Dos escenarios con los supuestos versionados (H19): el bueno con la rentabilidad real supuesta y el malo
    sin rentabilidad, más la caída en pesos de un mal año sobre lo que habrías puesto en un año."""
    casa = e["plan"]["casa"]
    mensual = max(0, min(int(mensual), 2_000_000))
    aporte = casa["aporte_primas_mensual"] + mensual
    bueno = C.meses_para_meta(casa["cuota"], casa["llevas"], aporte, S.RENTABILIDAD_ESCENARIO_BUENO)
    malo = C.meses_para_meta(casa["cuota"], casa["llevas"], aporte, S.RENTABILIDAD_ESCENARIO_MALO)
    inicio = e["hoy"].year + (e["hoy"].month - 1) / 12
    caida = C.redondear_riesgo(C.caida_mal_anio(aporte * 12, PORTAFOLIO_CASA)) if aporte else 0

    def anio(m):
        return int(inicio + m / 12) if m is not None else None
    return {"mensual": mensual, "mensual_txt": miles(mensual) if mensual else "$0", "aporte_total": aporte,
            "anio_bueno": anio(bueno), "anio_malo": anio(malo), "a_tiempo": bueno is not None and bueno <= casa["plazo_anios"] * 12,
            "puesto_10": pesos(aporte * casa["plazo_anios"] * 12),
            "rent_buena_txt": porcentaje(S.RENTABILIDAD_ESCENARIO_BUENO), "caida_txt": pesos(caida),
            "caida_pct_txt": porcentaje(S.PORTAFOLIOS[PORTAFOLIO_CASA]["caida_mal_anio"])}


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
    return render(request, "reglas.html", estado(s), lista=registro.mandatos(s["id"]), nueva=request.query_params.get("nueva"),
                  CONTROLES=mandatos.CONTROLES, PAUSAS=mandatos.PAUSAS_AUTOMATICAS, fecha_txt=mandatos.fecha_txt,
                  TEXTOS_PERMISOS=TEXTOS_PERMISOS, pestana="equipo")


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
                       accion=permiso, tipo="consentimiento", respuesta="otorgó" if valor == "si" else "retiró",
                       texto_mostrado=TEXTOS_PERMISOS[permiso])
    return _a("/reglas#permisos")


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
    perf = _leer_perfil(await request.form())
    if perf is None:
        return _a("/perfil/cambiar?falta=perfil")
    s["diagnostico"]["perfil"] = perf
    s["diagnostico"]["perfil_fecha"] = s["fecha_simulada"]
    registro.guardar_sesion(s)
    registro.registrar(s["afiliado_id"], sesion_id=s["id"], fecha_simulada=s["fecha_simulada"], canal="app",
                       accion="actualizar_perfil", tipo="perfil", argumento=perf, perfil_usado=PF.resumen(perf))
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
        "casa": (["B8"], "/meta/casa" if e["plan"]["casa"] else "/plan", "Ver tu casa con el simulador" if e["plan"]["casa"] else "Ver tu plan"),
        "pension": (["B12"], "/plan", "Ver tu pensión y sus supuestos"),
        "prima": (["B6"] if e["plan"]["prima"] else ["P10"], "/revision", "Ver tu revisión de junio"),
        "cesantias": (["B8"], "/patrimonio", "Ver tu patrimonio"),
        "asesor": (["P8"], "/equipo", f"Hablar con {e['cons']['nombre']}"),
        "impuesto": ([], "/equipo", f"Verlo con {e['cons']['nombre']}"),
        "otra": (["P1"], "/plan", "Ver tu plan"),
    }
    piezas, enlace, enlace_txt = mapa[it]
    if it == "impuesto":
        decl = e["plan"]["declarar"]
        piezas = ["B15"] if decl and decl["probable"] else ["A2"]
        nota = redactor.nota_del_arquitecto(piezas_permitidas(e, piezas), v, ctx, e["af"]["nombre"])
        return {"intencion": it, "texto": nota["texto"], "piezas": nota["piezas"], "enlace": enlace,
                "enlace_txt": enlace_txt, "textos": nota["textos"]}
    if it == "pension" and not e["plan"]["pension"]["mostrar_mesada"]:
        piezas = ["P10"] if not e["plan"]["pension"]["estimable"] else ["A4"]
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
def _ficha_interna(clave: str) -> str:
    """La cookie guarda una ficha derivada de la clave, nunca la clave en claro."""
    return hashlib.sha256(f"pwa-interno:{clave}".encode()).hexdigest()


def acceso_interno(request: Request) -> bool:
    """Cerradas por defecto: sin PWA_CLAVE_INTERNA solo se abren si PWA_INTERNO_ABIERTO=1 (uso local)."""
    clave = os.environ.get("PWA_CLAVE_INTERNA")
    if not clave:
        return os.environ.get("PWA_INTERNO_ABIERTO") == "1"
    return secrets.compare_digest(request.cookies.get(COOKIE_INTERNA, ""), _ficha_interna(clave))


@app.get("/interno/entrar", response_class=HTMLResponse)
def interno_entrar(request: Request, siguiente: str = "/interno/motor"):
    return render(request, "interno_entrar.html", siguiente=siguiente)


@app.post("/interno/entrar")
def interno_entrar_post(clave: str = Form(""), siguiente: str = Form("/interno/motor")):
    esperada = os.environ.get("PWA_CLAVE_INTERNA", "")
    if not esperada or not secrets.compare_digest(clave, esperada):
        return _a("/interno/entrar?error=1")
    r = _a(siguiente if siguiente.startswith("/interno/") else "/interno/motor")
    r.set_cookie(COOKIE_INTERNA, _ficha_interna(clave), httponly=True, samesite="strict",
                 secure=os.environ.get("PWA_COOKIE_SEGURA") == "1")
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
    pr = _propuesta(e) if (e["dec"]["modo"] == "asesoria" and e["plan"]["prima"] and e["plan"]["casa"]) else None
    return render(request, "interno_consultor.html", e, enganche=enganche, pr=pr if (pr and e["plan"]["prima"]) else None,
                  historia=registro.interacciones(e["s"]["id"], 30), lista=registro.mandatos(e["s"]["id"]),
                  sin_clave=not os.environ.get("PWA_CLAVE_INTERNA"), fecha_txt=mandatos.fecha_txt)


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
