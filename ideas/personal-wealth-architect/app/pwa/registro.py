"""Persistencia del MVP: sesiones de demostración, registro de interacciones, mandatos y
métricas de servicio. SQLite, porque el MVP no necesita más (ver HANDOFF.md).

El registro de interacciones guarda lo que exige la fábrica y la norma (Decreto 2555,
art. 2.40.4.1.2): acción, escenario, ángulo, canal, momento, argumento (piezas del
catálogo), texto mostrado, versiones de catálogo, motor y supuestos, perfil usado,
respuesta, resultado y grupo (control o tratamiento). Nunca guarda datos reales.
"""
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

RUTA = Path(os.environ.get("PWA_DB", Path(__file__).resolve().parent.parent / "data" / "pwa.sqlite"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS sesiones (
  id TEXT PRIMARY KEY, afiliado_id TEXT NOT NULL, fecha_simulada TEXT NOT NULL,
  diagnostico TEXT NOT NULL, hechos TEXT NOT NULL DEFAULT '[]', rechazos TEXT NOT NULL DEFAULT '[]',
  consentimientos TEXT NOT NULL DEFAULT '{}', senales_no_comprende INTEGER NOT NULL DEFAULT 0,
  contactos_semana INTEGER NOT NULL DEFAULT 0, creada TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS interacciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT, sesion_id TEXT, afiliado_id TEXT NOT NULL, momento_real TEXT NOT NULL,
  fecha_simulada TEXT, canal TEXT, accion TEXT, escenario TEXT, angulo TEXT, argumento TEXT,
  texto_mostrado TEXT, tipo TEXT, version_catalogo TEXT, version_motor TEXT, version_supuestos TEXT,
  perfil_usado TEXT, respuesta TEXT, resultado TEXT, grupo TEXT, quien TEXT
);
CREATE TABLE IF NOT EXISTS mandatos (
  id TEXT NOT NULL, sesion_id TEXT NOT NULL, datos TEXT NOT NULL, PRIMARY KEY (id, sesion_id)
);
CREATE TABLE IF NOT EXISTS metricas_servicio (
  nombre TEXT PRIMARY KEY, valor REAL NOT NULL, actualizada TEXT NOT NULL
);
"""


@contextmanager
def conexion():
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(RUTA)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def iniciar() -> None:
    with conexion() as con:
        con.executescript(ESQUEMA)


def _ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# Sesiones ---------------------------------------------------------------------------
def crear_sesion(afiliado_id: str, fecha_simulada: str, diagnostico: dict, consentimientos: dict | None = None) -> str:
    sid = uuid.uuid4().hex
    with conexion() as con:
        con.execute("INSERT INTO sesiones (id, afiliado_id, fecha_simulada, diagnostico, consentimientos, creada) VALUES (?,?,?,?,?,?)",
                    (sid, afiliado_id, fecha_simulada, json.dumps(diagnostico, ensure_ascii=False),
                     json.dumps(consentimientos or {}), _ahora()))
    return sid


def leer_sesion(sid: str) -> dict | None:
    with conexion() as con:
        fila = con.execute("SELECT * FROM sesiones WHERE id = ?", (sid,)).fetchone()
    if not fila:
        return None
    s = dict(fila)
    for k in ("diagnostico", "hechos", "rechazos", "consentimientos"):
        s[k] = json.loads(s[k])
    s["hechos"] = set(s["hechos"])
    s["rechazos"] = set(s["rechazos"])
    return s


def guardar_sesion(s: dict) -> None:
    with conexion() as con:
        con.execute("""UPDATE sesiones SET fecha_simulada=?, diagnostico=?, hechos=?, rechazos=?, consentimientos=?,
                       senales_no_comprende=?, contactos_semana=? WHERE id=?""",
                    (s["fecha_simulada"], json.dumps(s["diagnostico"], ensure_ascii=False), json.dumps(sorted(s["hechos"])),
                     json.dumps(sorted(s["rechazos"])), json.dumps(s["consentimientos"]),
                     s["senales_no_comprende"], s["contactos_semana"], s["id"]))


# Interacciones -------------------------------------------------------------------------
def registrar(afiliado_id: str, **campos) -> int:
    columnas = ["sesion_id", "fecha_simulada", "canal", "accion", "escenario", "angulo", "argumento", "texto_mostrado",
                "tipo", "version_catalogo", "version_motor", "version_supuestos", "perfil_usado", "respuesta",
                "resultado", "grupo", "quien"]
    valores = []
    for c in columnas:
        v = campos.get(c)
        valores.append(json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
    with conexion() as con:
        cur = con.execute(
            f"INSERT INTO interacciones (afiliado_id, momento_real, {', '.join(columnas)}) VALUES (?, ?, {', '.join('?' * len(columnas))})",
            [afiliado_id, _ahora(), *valores])
        return cur.lastrowid


def interacciones(sesion_id: str | None = None, limite: int = 50) -> list[dict]:
    with conexion() as con:
        if sesion_id:
            filas = con.execute("SELECT * FROM interacciones WHERE sesion_id = ? ORDER BY id DESC LIMIT ?", (sesion_id, limite))
        else:
            filas = con.execute("SELECT * FROM interacciones ORDER BY id DESC LIMIT ?", (limite,))
        return [dict(f) for f in filas.fetchall()]


# Mandatos --------------------------------------------------------------------------------
def guardar_mandato(sesion_id: str, mandato: dict) -> None:
    with conexion() as con:
        con.execute("INSERT OR REPLACE INTO mandatos (id, sesion_id, datos) VALUES (?,?,?)",
                    (mandato["id"], sesion_id, json.dumps(mandato, ensure_ascii=False)))


def mandatos(sesion_id: str) -> list[dict]:
    with conexion() as con:
        filas = con.execute("SELECT datos FROM mandatos WHERE sesion_id = ?", (sesion_id,)).fetchall()
    return [json.loads(f["datos"]) for f in filas]


# Métricas de servicio (freno) ----------------------------------------------------------------
def metricas() -> dict:
    with conexion() as con:
        return {f["nombre"]: f["valor"] for f in con.execute("SELECT nombre, valor FROM metricas_servicio").fetchall()}


def fijar_metrica(nombre: str, valor: float) -> None:
    with conexion() as con:
        con.execute("INSERT OR REPLACE INTO metricas_servicio (nombre, valor, actualizada) VALUES (?,?,?)",
                    (nombre, valor, _ahora()))
