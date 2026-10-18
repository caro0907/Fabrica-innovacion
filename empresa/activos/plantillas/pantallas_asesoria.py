"""Componentes de pantallas de asesoría para lienzos de diseño (.dc.html).
Activo de la fábrica: empresa/activos/plantillas/pantallas_asesoria.py
Uso: from pantallas_asesoria import *; set_out('<carpeta>/project'); luego write(...)
"""
import os

OUT = '.'
def set_out(path):
    global OUT
    OUT = path

INK = '#12241F'; MUTED = '#4A5C56'; BODY = '#2E403A'; GROUND = '#F6F3EC'; GREEN = '#0E6A4E'; SGREEN = '#E3EFEA'
AMBER = '#7A4A0E'; SAMBER = '#FFF4E2'; GOLD = '#F3C98A'; LINE = '#E7E2D6'; WARN = '#B9721C'; GREY = '#ECE8DE'

HEAD = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&amp;family=Newsreader:opsz,wght@6..72,500;6..72,600&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#0E6A4E}}a:hover{{color:#09503A}}
input[type=range]{{accent-color:#0E6A4E}}
summary{{list-style-position:inside}}
</style>
</helmet>
'''
TAIL = '''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":{h}}}}}'>
{script}
</script>
</body>
</html>
'''
EMPTY = 'class Component extends DCLogic {\nrenderVals() {\nreturn {};\n}\n}'

def write(name, title, body, script=EMPTY, h=844):
    html = HEAD.format(title=title) + body + '\n' + TAIL.format(script=script, h=h)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)

def root(pad=True, h=844):
    if pad:
        return f'<div style="width: 390px; height: {h}px; box-sizing: border-box; background: {GROUND}; font-family: \'Plus Jakarta Sans\', sans-serif; color: {INK}; padding: 20px 18px 18px; display: flex; flex-direction: column; gap: 11px">'
    return f'<div style="width: 390px; height: {h}px; box-sizing: border-box; background: {GROUND}; font-family: \'Plus Jakarta Sans\', sans-serif; color: {INK}; display: flex; flex-direction: column">'

def inner(gap=12, pad='20px 16px 10px'):
    return f'<div style="flex-grow: 1; padding: {pad}; display: flex; flex-direction: column; gap: {gap}px; overflow: hidden">'

# ---------- etiquetas ----------
def tag(text, fg, bg):
    return f'<span style="font-size: 11.5px; font-weight: 700; color: {fg}; background: {bg}; padding: 3px 8px; border-radius: 8px; flex-shrink: 0">{text}</span>'
TAG_INFO = tag('Información de tu plan', GREEN, SGREEN)
TAG_REC = tag('Recomendación profesional', AMBER, SAMBER)
ORIGEN = {'s': ('Sabemos', GREEN, SGREEN), 'c': ('Nos contaste', AMBER, SAMBER), 'e': ('Estimado', '#3A3F7A', '#E8E9F6'), 'p': ('Por completar', '#3F3F3F', GREY)}
def origen(k):
    t, fg, bg = ORIGEN[k]
    return tag(t, fg, bg)

def avatar(i, bg=INK, fg='#FFFFFF', size=36, fs=13):
    return f'<span aria-hidden="true" style="width: {size}px; height: {size}px; border-radius: {size//2}px; background: {bg}; color: {fg}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: {fs}px; flex-shrink: 0; border: 2px solid {GROUND}">{i}</span>'

def eyebrow(t, color=MUTED):
    return f'<span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.06em; color: {color}">{t.upper()}</span>'

def p(t, size=14, color=BODY, extra=''):
    return f'<span style="font-size: {size}px; line-height: 1.45; color: {color}{extra}">{t}</span>'

def small(t, center=False):
    c = '; text-align: center' if center else ''
    return f'<span style="font-size: 12px; color: {MUTED}; line-height: 1.4{c}">{t}</span>'

def h1(t, serif=True, size=28):
    fam = "'Newsreader', serif; font-weight: 600" if serif else "'Bricolage Grotesque', sans-serif; font-weight: 700"
    return f'<h1 style="margin: 0; font-family: {fam}; font-size: {size}px; line-height: 1.15">{t}</h1>'

def card(inner_html, bg='#FFFFFF', gap=8, pad='14px 16px', r=20):
    return f'<div style="background: {bg}; border-radius: {r}px; padding: {pad}; display: flex; flex-direction: column; gap: {gap}px">{inner_html}</div>'

def bar(pct, color=GREEN, track=GREY, hgt=6):
    return f'<span style="display: block; height: {hgt}px; border-radius: {hgt//2}px; background: {track}"><span style="display: block; height: {hgt}px; border-radius: {hgt//2}px; width: {pct}%; background: {color}"></span></span>'

def row(a, b):
    return f'<div style="display: flex; justify-content: space-between; gap: 10px; font-size: 13.5px; padding: 5px 0; border-bottom: 1px solid {LINE}"><span>{a}</span><strong style="text-align: right">{b}</strong></div>'

def cta(href, text, h=52):
    return f'<a href="{href}" style="min-height: {h}px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 16px; display: flex; align-items: center; justify-content: center; text-decoration: none; text-align: center; padding: 0 12px">{text}</a>'

def link(href, text, center=True):
    j = 'center' if center else 'flex-start'
    return f'<a href="{href}" style="min-height: 44px; display: flex; align-items: center; justify-content: {j}; gap: 8px; font-size: 14px; font-weight: 700; text-decoration: none">{text}</a>'

def details(summary, body):
    return (f'<details style="font-size: 12.5px; line-height: 1.5; color: {BODY}"><summary style="min-height: 44px; display: flex; align-items: center; font-weight: 700; font-size: 13.5px; color: {GREEN}; cursor: pointer">{summary}</summary>{body}</details>')

def back(href, right=''):
    return (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 10px">'
            f'<a href="{href}" aria-label="Volver" style="width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 22px; background: #FFFFFF"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg></a>'
            f'{right}</div>')

# ---------- navegación por persona ----------
ICONS = {
 'inicio': '<path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path>',
 'plan': '<path d="M4 19V5"></path><path d="M4 19h16"></path><path d="M8 15l4-4 3 3 5-6"></path>',
 'patrimonio': '<rect x="3" y="6" width="18" height="13" rx="2"></rect><path d="M3 10h18"></path><path d="M16 15h2"></path>',
 'equipo': '<circle cx="9" cy="8" r="3"></circle><path d="M3 20c0-3 3-5 6-5s6 2 6 5"></path><circle cx="17" cy="9" r="2.5"></circle><path d="M16 15c3 0 5 2 5 4"></path>',
}
def f(base, persona):
    """Nombre de archivo de una pantalla para una persona. Persona principal: sufijo vacío."""
    return f'{base}{persona}.dc.html'

def tabbar(active, persona=''):
    tabs = [('inicio', 'Inicio', f('H-Inicio', persona)), ('plan', 'Mi plan', f('H-Plan', persona)),
            ('patrimonio', 'Patrimonio', f('H-Patrimonio', persona)), ('equipo', 'Tu equipo', f('H-Equipo', persona))]
    out = [f'<nav aria-label="Secciones" style="background: #FFFFFF; border-top: 1px solid {LINE}; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); padding: 6px 6px 20px; flex-shrink: 0">']
    for k, label, href in tabs:
        col = GREEN if k == active else MUTED
        out.append(f'<a href="{href}"{" aria-current=\"page\"" if k == active else ""} style="min-height: 48px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; text-decoration: none; color: {col}; font-size: 11.5px; font-weight: {700 if k == active else 600}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>{label}</a>')
    out.append('</nav>')
    return '\n'.join(out)

def ask_bar(persona=''):
    return (f'<a href="{f("H-Chat", persona)}" style="margin: 0 16px 8px; min-height: 46px; border-radius: 23px; background: #FFFFFF; border: 1px solid {LINE}; display: flex; align-items: center; gap: 10px; padding: 0 16px; text-decoration: none; color: {MUTED}; font-size: 14px; flex-shrink: 0">'
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H8l-4 4z"></path></svg>Pregúntale algo a tu arquitecto</a>')

# ---------- primera reunión ----------
def top(back_href, paso, total, label='Tu primera reunión'):
    dots = ''.join(f'<span style="width: {22 if k < paso else 8}px; height: 8px; border-radius: 4px; background: {GREEN if k < paso else LINE}"></span>' for k in range(total))
    return (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 10px">'
            f'<a href="{back_href}" aria-label="Volver" style="width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 22px; background: #FFFFFF"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg></a>'
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px"><span style="font-size: 12px; font-weight: 600; color: {MUTED}">{label} · tema {paso} de {total}</span>'
            f'<div role="img" aria-label="Tema {paso} de {total}" style="display: flex; gap: 4px">{dots}</div></div></div>')

def chips(key, col=False):
    d = 'flex-direction: column; ' if col else 'flex-wrap: wrap; '
    return (f'<div style="display: flex; {d}gap: 8px">\n<sc-for list="{{{{{key}}}}}" as="c" hint-placeholder-count="3">\n'
            f'<button type="button" aria-pressed="{{{{c.on}}}}" onClick="{{{{c.pick}}}}" style="{{{{c.style}}}}">{{{{c.label}}}}</button>\n</sc-for>\n</div>')

def slider(key, label, mn, mx, step, note=''):
    n = f'<span style="font-size: 12.5px; color: {MUTED}; line-height: 1.4">{note}</span>' if note else ''
    return (f'<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 6px">'
            f'<label for="{key}" style="font-size: 15px; font-weight: 700">{label}</label>'
            f'<span style="font-family: \'Bricolage Grotesque\', sans-serif; font-size: 24px; font-weight: 700">{{{{{key}Txt}}}}</span>'
            f'<input id="{key}" type="range" min="{mn}" max="{mx}" step="{step}" value="{{{{{key}}}}}" onChange="{{{{on_{key}}}}}" style="width: 100%; min-height: 44px; margin: 0">{n}</div>')

CHIP_STYLE = ("function st(on, wide) { return 'min-height: 44px; padding: 0 14px; ' + (wide ? 'text-align: left; border-radius: 14px; ' : 'border-radius: 22px; ') + "
              "'font-family: inherit; font-size: 14px; font-weight: 600; cursor: pointer; border: 2px solid ' + (on ? '#0E6A4E' : '#E7E2D6') + '; background: ' + (on ? '#E3EFEA' : '#FFFFFF') + '; color: #12241F'; }\n"
              "function fmt(n) { return '$' + (n / 1000000).toFixed(1).replace('.', ',') + ' M'; }")

def script(state, chip_groups=(), sliders=(), extra='', methods=''):
    """chip_groups: (key, opciones, multi, ancho). sliders: claves numéricas en millones."""
    parts = []
    for key, opts, multi, wide in chip_groups:
        arr = '[' + ','.join("'" + o.replace("'", "\\'") + "'" for o in opts) + ']'
        w = 'true' if wide else 'false'
        if multi:
            parts.append(f"{key}: {arr}.map(function (o) {{ var on = s.{key}.indexOf(o) >= 0; return {{ label: o, on: on ? 'true' : 'false', style: st(on, {w}), pick: function () {{ var n = s.{key}.slice(); var i = n.indexOf(o); if (i >= 0) {{ n.splice(i, 1); }} else {{ n.push(o); }} self.setState({{ {key}: n }}); }} }}; }})")
        else:
            parts.append(f"{key}: {arr}.map(function (o) {{ var on = s.{key} === o; return {{ label: o, on: on ? 'true' : 'false', style: st(on, {w}), pick: function () {{ var o2 = {{}}; o2['{key}'] = o; self.setState(o2); }} }}; }})")
    for key in sliders:
        parts.append(f"{key}: s.{key}, {key}Txt: fmt(s.{key}), on_{key}: function (e) {{ var o2 = {{}}; o2['{key}'] = Number(e.target.value); self.setState(o2); }}")
    if extra:
        parts.append(extra)
    return ('class Component extends DCLogic {\nconstructor(props) {\nsuper(props);\nthis.state = ' + state + ';\n}\n' + methods +
            'renderVals() {\nvar self = this, s = this.state;\n' + CHIP_STYLE + '\nreturn {\n' + ',\n'.join(parts) + '\n};\n}\n}')
