"""Verificación mecánica de un prototipo en lienzo (.dc.html) antes de pasarlo al revisor.

Lo que revisa (lo que una persona no debería tener que encontrar a mano):
  1. Enlaces: cada href existe; ninguno es "#" ni vacío.
  2. Recorrido por persona y momento (criterio E4): una pantalla de una persona solo enlaza pantallas de esa
     misma persona y del mismo momento (<meta name="momento">), salvo los enlaces marcados con
     data-cambia-momento="si"; ninguna pantalla de usuario enlaza una vista interna.
  3. Pantallas huérfanas: toda pantalla de usuario se alcanza desde una entrada.
  4. Textos prohibidos: marcadores sin llenar ([X], $[Y], [NOMBRE], lorem) y siglas sin nombre completo.
  5. Visual (con --visual): contenido que se sale del alto de la pantalla, elementos tocables de menos
     de 44 px y textos de menos de 11 px.

Uso:
  python3 verificar-prototipo.py <carpeta project> --entradas D1-Bienvenida.dc.html,H-InicioJuliana.dc.html \
      --personas Juliana --internas A1-,M1-,S1- [--visual]

Convención de nombres: la pantalla de una persona secundaria termina en su nombre (H-PlanJuliana.dc.html);
la persona principal no lleva sufijo. Las vistas internas empiezan por los prefijos de --internas.
Sale con código 1 si encuentra algo que bloquea.
"""
import argparse, glob, os, re, sys

SIGLAS = ['AFP', 'AMV', 'FPV', 'SFC', 'CDT', 'UVT', 'AFC', 'RNPMV', 'DIAN', 'IA ', 'GMF', 'FIC', 'URF']
MARCADORES = [r'\[X\]', r'\$\[', r'\[Y\]', r'\[[A-ZÁÉÍÓÚ][A-Za-záéíóúñ ]+\]', r'(?i)lorem', r'\bTODO\b', r'XXX']

ap = argparse.ArgumentParser()
ap.add_argument('carpeta')
ap.add_argument('--entradas', required=True)
ap.add_argument('--personas', default='')
ap.add_argument('--internas', default='')
ap.add_argument('--visual', action='store_true')
a = ap.parse_args()

files = sorted(os.path.basename(x) for x in glob.glob(os.path.join(a.carpeta, '*.dc.html')))
personas = [x for x in a.personas.split(',') if x]
internas = [x for x in a.internas.split(',') if x]
def persona(fn):
    stem = fn.replace('.dc.html', '')
    for pz in personas:
        if stem.endswith(pz):
            return pz
    return '(principal)'
def interna(fn):
    return any(fn.startswith(x) for x in internas)

bloquea, avisos = [], []
links = {}
momento = {}
saltos = {}
visible = {}
for fn in files:
    s = open(os.path.join(a.carpeta, fn), encoding='utf-8').read()
    body = s.split('</helmet>')[-1].split('<script type="text/x-dc"')[0]
    links[fn] = re.findall(r'href="([^"]*)"', body)
    m = re.search(r'<meta name="momento" content="([^"]*)"', s)
    momento[fn] = m.group(1) if m else ''
    saltos[fn] = set(re.findall(r'<a href="([^"]*)" data-cambia-momento="si"', body))
    txt = re.sub(r'<svg.*?</svg>', ' ', body, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    script = s.split('data-dc-script')[-1] if 'data-dc-script' in s else ''
    visible[fn] = txt + ' ' + ' '.join(re.findall(r"'([^']{12,})'", script))

for fn, hs in links.items():
    for h in hs:
        if h in ('', '#'):
            bloquea.append(f'{fn}: enlace muerto ("{h}")')
        elif h.startswith('http'):
            continue
        elif h not in files:
            bloquea.append(f'{fn}: enlace a una pantalla que no existe ({h})')
        else:
            if not interna(fn) and interna(h):
                bloquea.append(f'{fn}: una pantalla de usuario abre una vista interna ({h})')
            if not interna(fn) and not interna(h) and persona(fn) != persona(h):
                bloquea.append(f'{fn} ({persona(fn)}): enlaza una pantalla de otra persona ({h}, {persona(h)})')
            elif not interna(fn) and not interna(h) and momento[fn] and momento[h] and momento[fn] != momento[h] and h not in saltos[fn]:
                bloquea.append(f'{fn} ({momento[fn]}): salta a otro momento sin marcarlo ({h}, {momento[h]})')

entradas = a.entradas.split(',')
vistos, cola = set(), list(entradas)
while cola:
    x = cola.pop()
    if x in vistos or x not in links:
        continue
    vistos.add(x)
    cola += [h for h in links[x] if h in links]
for fn in files:
    if not interna(fn) and not momento[fn]:
        avisos.append(f'{fn}: no declara su momento (<meta name="momento">)')
    if not interna(fn) and fn not in vistos:
        avisos.append(f'{fn}: no se llega desde ninguna entrada ({", ".join(entradas)})')

for fn, t in visible.items():
    for m in MARCADORES:
        if re.search(m, t):
            bloquea.append(f'{fn}: marcador sin llenar ({m.strip(chr(92))})')
    for sg in SIGLAS:
        if re.search(r'(?<![A-Za-zÁÉÍÓÚáéíóúñ])' + re.escape(sg.strip()) + r'(?![A-Za-zÁÉÍÓÚáéíóúñ])', t):
            avisos.append(f'{fn}: sigla sin nombre completo ({sg.strip()})')

if a.visual:
    from playwright.sync_api import sync_playwright
    stub = '''<script>
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('sc-if').forEach(function (e) { if ((e.getAttribute('hint-placeholder-val') || '').indexOf('false') >= 0) e.remove(); });
  document.querySelectorAll('sc-for, sc-if, x-dc').forEach(function (e) { e.style.display = 'contents'; });
  document.querySelectorAll('helmet').forEach(function (e) { e.style.display = 'none'; });
});
</script>'''
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 900})
        pg.route('**/*', lambda rt: rt.abort() if 'fonts.' in rt.request.url else rt.continue_())
        for fn in files:
            if interna(fn):
                continue
            html = open(os.path.join(a.carpeta, fn), encoding='utf-8').read().replace('<script src="./support.js"></script>', stub)
            pg.set_content(html, wait_until='domcontentloaded')
            r = pg.evaluate('''() => {
              const root = document.querySelector('x-dc > div');
              if (!root) return null;
              const out = {alto: root.clientHeight, contenido: root.scrollHeight, chicos: [], letra: []};
              const walk = (el) => { for (const c of el.children) { if (getComputedStyle(c).overflow === 'hidden' && c !== root) { if (c.scrollHeight > c.clientHeight + 2) out.contenido = Math.max(out.contenido, root.clientHeight + (c.scrollHeight - c.clientHeight)); } walk(c); } };
              walk(root);
              document.querySelectorAll('a, button, summary, input').forEach(e => {
                const bb = e.getBoundingClientRect();
                if (bb.height > 0 && bb.height < 43.5 && !e.closest('nav') && !e.closest('label') && (e.getAttribute('style') || '').indexOf('{{') < 0) out.chicos.push((e.innerText || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 40) + ' (' + Math.round(bb.height) + ' px)');
              });
              document.querySelectorAll('span, strong, label, a, button, p').forEach(e => {
                const fs = parseFloat(getComputedStyle(e).fontSize);
                if (fs > 0 && fs < 11 && e.innerText && e.innerText.trim()) out.letra.push(e.innerText.trim().slice(0, 30) + ' (' + fs + ' px)');
              });
              return out;
            }''')
            if not r:
                continue
            if r['contenido'] > r['alto'] + 2:
                bloquea.append(f'{fn}: el contenido ({r["contenido"]} px) no cabe en la pantalla ({r["alto"]} px)')
            for c in r['chicos']:
                avisos.append(f'{fn}: elemento tocable de menos de 44 px: {c}')
            for c in r['letra'][:3]:
                avisos.append(f'{fn}: texto de menos de 11 px: {c}')
        b.close()

print(f'Pantallas: {len(files)} · alcanzables desde las entradas: {len(vistos)}')
print(f'\nBLOQUEAN ({len(bloquea)})')
for x in bloquea: print(' -', x)
print(f'\nAVISOS ({len(avisos)})')
for x in avisos: print(' -', x)
sys.exit(1 if bloquea else 0)
