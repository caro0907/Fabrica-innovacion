"""Recorre la app en un navegador real (390 x 844), toma capturas y revisa lo básico de accesibilidad:
elementos tocables de menos de 44 px, desborde horizontal y textos sin etiqueta.

Uso: python3 scripts/revisar_pantallas.py http://localhost:8765 <carpeta-de-capturas>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765"
SALIDA = Path(sys.argv[2] if len(sys.argv) > 2 else "capturas")
SALIDA.mkdir(parents=True, exist_ok=True)

REVISION_JS = """
() => {
  const problemas = [];
  const vw = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > vw + 1) problemas.push('desborde horizontal: ' + document.documentElement.scrollWidth);
  document.querySelectorAll('a, button, input[type=checkbox], input[type=radio] + span, input[type=range], input[type=number], input:not([type]), summary').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (el.closest('.marco-demo')) return;
    const alto = el.matches('input[type=checkbox]') ? el.closest('label').getBoundingClientRect().height : r.height;
    if (alto < 43.5) problemas.push('toque de ' + Math.round(alto) + ' px: ' + (el.innerText || el.getAttribute('aria-label') || el.outerHTML).slice(0, 50).replace(/\\s+/g, ' '));
  });
  document.querySelectorAll('input:not([type=hidden]), select').forEach(el => {
    const tieneEtiqueta = el.labels && el.labels.length || el.getAttribute('aria-label');
    if (!tieneEtiqueta) problemas.push('campo sin etiqueta: ' + el.name);
  });
  return problemas;
}
"""

pasos = []


def captura(page, nombre):
    page.wait_for_load_state("networkidle")
    page.screenshot(path=str(SALIDA / f"{len(pasos) + 1:02d}-{nombre}.png"), full_page=True)
    pasos.append((nombre, page.url, page.evaluate(REVISION_JS)))


with sync_playwright() as p:
    nav = p.chromium.launch()
    page = nav.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    page.goto(BASE + "/")
    captura(page, "portada")
    page.click("text=Empezar como Laura")
    captura(page, "d1-bienvenida")
    page.check("input[name=autoriza]")
    page.click("text=Empecemos")
    captura(page, "d2-metas")
    page.click("button:has-text('Siguiente')")
    captura(page, "d2b-numeros")
    page.click("button:has-text('Siguiente')")
    captura(page, "d3-vida")
    page.click("button:has-text('Siguiente')")
    captura(page, "d3b-dinero")
    page.click("button:has-text('Siguiente')")
    captura(page, "d4-riesgo")
    for nombre, valor in [("horizonte", "Más de 5 años"), ("objetivo", "Que crezca para mi meta"), ("conocimiento", "Lo básico"),
                          ("experiencia", "Nunca"), ("perdida", "Hasta 15 de cada 100 pesos"), ("reaccion", "Espero")]:
        page.check(f"input[name={nombre}][value='{valor}']")
    page.click("button:has-text('Siguiente')")
    captura(page, "d5-entendi")
    page.click("text=Ver mi plan")
    captura(page, "plan-inicial")
    page.click("button:has-text('Registrar a tu hija')")
    page.click("text=Guardar mi plan")
    captura(page, "inicio")
    page.click("text=Ver mi revisión")
    captura(page, "revision")
    page.click("text=Ver mi propuesta")
    captura(page, "propuesta")
    page.check("input[name=entiendo]")
    page.click("text=Seguir: confirmar con mi huella")
    captura(page, "huella")
    page.click("text=Confirmar con mi huella (simulado)")
    captura(page, "propuesta-lista")
    page.check("input[name=acepto]")
    page.click("text=Sí, déjalo como regla")
    page.click("text=Confirmar con mi huella (simulado)")
    captura(page, "reglas")
    for url, nombre in [("/plan", "plan"), ("/meta/casa", "meta-casa"), ("/patrimonio", "patrimonio"), ("/pilares", "pilares"),
                        ("/equipo", "equipo"), ("/perfil", "perfil"), ("/como-funciona", "como-funciona"),
                        ("/pregunta?q=¿Cuándo llego a mi casa?", "pregunta"), ("/privacidad", "privacidad")]:
        page.goto(BASE + url)
        captura(page, nombre)
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(BASE + "/interno/consultor")
    captura(page, "interno-consultor")
    page.goto(BASE + "/interno/motor")
    captura(page, "interno-motor")
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(BASE + "/")
    page.click("text=Entrar como Andrés")
    captura(page, "servicio-andres")
    # Laura sin el permiso del salario (criterio C10)
    page.goto(BASE + "/")
    page.click("text=Empezar como Laura")
    page.click("text=Empecemos")
    for _ in range(4):
        page.click("button:has-text('Siguiente')")
    for nombre, valor in [("horizonte", "Más de 5 años"), ("objetivo", "Que crezca para mi meta"), ("conocimiento", "Lo básico"),
                          ("experiencia", "Nunca"), ("perdida", "Hasta 15 de cada 100 pesos"), ("reaccion", "Espero")]:
        page.check(f"input[name={nombre}][value='{valor}']")
    page.click("button:has-text('Siguiente')")
    page.click("text=Ver mi plan")
    captura(page, "plan-inicial-sin-permiso")
    page.click("text=Guardar mi plan")
    captura(page, "inicio-sin-permiso")
    nav.close()

total = 0
for nombre, url, problemas in pasos:
    reales = [x for x in problemas if not (nombre.startswith("interno") and x.startswith("toque"))]
    total += len(reales)
    print(f"{nombre:18} {'OK' if not reales else ''}")
    for x in reales:
        print("   -", x)
print(f"\n{len(pasos)} pantallas, {total} problemas")
