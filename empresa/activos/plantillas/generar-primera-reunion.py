import sys, os
OUT = sys.argv[1]
INK = '#12241F'; MUTED = '#4A5C56'; GROUND = '#F6F3EC'; GREEN = '#0E6A4E'; SGREEN = '#E3EFEA'
AMBER = '#7A4A0E'; SAMBER = '#FFF4E2'; GOLD = '#F3C98A'; LINE = '#E7E2D6'
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
</style>
</helmet>
'''
TAIL = '''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":844}}}}'>
{script}
</script>
</body>
</html>
'''
EMPTY = 'class Component extends DCLogic {\nrenderVals() {\nreturn {};\n}\n}'
ROOT = f'<div style="width: 390px; height: 844px; box-sizing: border-box; background: {GROUND}; font-family: \'Plus Jakarta Sans\', sans-serif; color: {INK}; padding: 22px 18px 18px; display: flex; flex-direction: column; gap: 12px">'

def avatar(i, bg, fg, size=36, fs=13):
    return f'<span aria-hidden="true" style="width: {size}px; height: {size}px; border-radius: {size//2}px; background: {bg}; color: {fg}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: {fs}px; flex-shrink: 0">{i}</span>'

def top(back_href, paso, total):
    dots = ''.join(f'<span style="width: {22 if k < paso else 8}px; height: 8px; border-radius: 4px; background: {GREEN if k < paso else LINE}"></span>' for k in range(total))
    b = (f'<a href="{back_href}" aria-label="Volver" style="width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 22px; background: #FFFFFF"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg></a>')
    return (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 10px">{b}'
            f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px"><span style="font-size: 12px; font-weight: 600; color: {MUTED}">Tu primera reunión · {paso} de {total}</span>'
            f'<div role="img" aria-label="Paso {paso} de {total}" style="display: flex; gap: 4px">{dots}</div></div></div>')

def cta(href, text):
    return f'<a href="{href}" style="min-height: 52px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 16px; display: flex; align-items: center; justify-content: center; text-decoration: none">{text}</a>'

def write(name, title, body, script=EMPTY):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(HEAD.format(title=title) + body + '\n' + TAIL.format(script=script))

def chip_script(state_init, groups):
    """groups: list of (key, options, multi)"""
    lines = ['class Component extends DCLogic {', 'constructor(props) {', 'super(props);', f'this.state = {state_init};', '}', 'renderVals() {', 'var self = this, s = this.state;',
             "function st(on) { return 'min-height: 44px; padding: 0 14px; border-radius: 22px; font-family: inherit; font-size: 14px; font-weight: 600; cursor: pointer; border: 2px solid ' + (on ? '#0E6A4E' : '#E7E2D6') + '; background: ' + (on ? '#E3EFEA' : '#FFFFFF') + '; color: #12241F'; }",
             'return {']
    parts = []
    for key, opts, multi in groups:
        arr = '[' + ','.join("'" + o.replace("'", "\\'") + "'" for o in opts) + ']'
        if multi:
            parts.append(f"{key}: {arr}.map(function (o) {{ var on = s.{key}.indexOf(o) >= 0; return {{ label: o, on: on ? 'true' : 'false', style: st(on), pick: function () {{ var n = s.{key}.slice(); var i = n.indexOf(o); if (i >= 0) {{ n.splice(i, 1); }} else {{ n.push(o); }} self.setState({{ {key}: n }}); }} }}; }})")
        else:
            parts.append(f"{key}: {arr}.map(function (o) {{ var on = s.{key} === o; return {{ label: o, on: on ? 'true' : 'false', style: st(on), pick: function () {{ self.setState({{ {key}: o }}); }} }}; }})")
    lines.append(',\n'.join(parts))
    lines += ['};', '}', '}']
    return '\n'.join(lines)

def chips(key):
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 8px">\n<sc-for list="{{{{{key}}}}}" as="c" hint-placeholder-count="4">\n'
            f'<button type="button" aria-pressed="{{{{c.on}}}}" onClick="{{{{c.pick}}}}" style="{{{{c.style}}}}">{{{{c.label}}}}</button>\n</sc-for>\n</div>')

def card(title, inner, sub=''):
    s = f'<span style="font-size: 12.5px; color: {MUTED}; line-height: 1.4">{sub}</span>' if sub else ''
    return f'<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px"><strong style="font-size: 15px">{title}</strong>{s}{inner}</div>'

# D1 Bienvenida
sabemos = [('Tu pensión obligatoria', '$78 M · 14 años cotizados'), ('Tus cesantías', '$9,4 M'), ('Tu salario de cotización', 'unos $5,2 M al mes'), ('Tus primas', 'junio y diciembre')]
sab = '\n'.join(f'<div style="display: flex; justify-content: space-between; gap: 10px; font-size: 13.5px; padding: 6px 0; border-bottom: 1px solid {LINE}"><span>{a}</span><strong>{b}</strong></div>' for a, b in sabemos)
agenda = ['Lo que quieres lograr', 'Tu vida hoy', 'Cómo te sientes con el riesgo', 'Lo que entendí de ti']
ag = '\n'.join(f'<div style="display: flex; gap: 10px; align-items: center; font-size: 14px"><span style="width: 26px; height: 26px; border-radius: 13px; background: {SGREEN}; color: {GREEN}; font-weight: 700; font-size: 13px; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{k+1}</span>{t}</div>' for k, t in enumerate(agenda))
body = f'''{ROOT}
<div style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 12px; font-weight: 600; color: {MUTED}">Datos ficticios</span><span style="display: flex">{avatar('A', GREEN, '#FFFFFF')}<span style="margin-left: -10px; display: flex">{avatar('DR', GOLD, INK)}</span></span></div>
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 30px; font-weight: 600; line-height: 1.12">Laura, armemos tu plan como en una primera reunión con tu asesor</h1>
<span style="font-size: 14px; color: #2E403A; line-height: 1.5">Primero te conozco; los productos vienen después, solo si te sirven. Son cuatro temas y unos 6 minutos.</span>
{card('Lo que ya sabemos, para no preguntártelo', sab, 'Con tu autorización. Si algo no está bien, lo corriges al final.')}
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px"><strong style="font-size: 15px">De qué vamos a hablar</strong>{ag}</div>
<div style="flex-grow: 1"></div>
{cta('D2-Metas.dc.html', 'Empecemos')}
<a href="H-Equipo.dc.html" style="min-height: 44px; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; font-weight: 700; text-decoration: none">{avatar('DR', GOLD, INK, 28, 11)}Prefiero hacerla con Daniela por video</a>
</div>
'''
write('D1-Bienvenida.dc.html', 'Tu primera reunión', body)

# D2 Metas
body = f'''{ROOT}
{top('D1-Bienvenida.dc.html', 1, 4)}
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">¿Qué te gustaría lograr en los próximos años?</h1>
<span style="font-size: 14px; color: #2E403A; line-height: 1.45">Elige las que sean tuyas. Después les ponemos fecha y números.</span>
{card('Tus metas', chips('metas'))}
{card('Tu casa, ¿para cuándo la quieres?', chips('plazo'), 'Es la meta que marcaste como la más importante.')}
<div style="flex-grow: 1"></div>
{cta('D3-Vida.dc.html', 'Siguiente')}
</div>
'''
write('D2-Metas.dc.html', 'Tus metas', body, chip_script(
    "{ metas: ['Tener tranquilidad', 'Comprar mi casa', 'Pensionarme bien'], plazo: 'En 10 años' }",
    [('metas', ['Tener tranquilidad', 'Comprar mi casa', 'Educar a mis hijos', 'Pensionarme bien', 'Salir de deudas', 'Viajar', 'Emprender'], True),
     ('plazo', ['En 3 años', 'En 5 años', 'En 10 años', 'Más de 10'], False)]))

# D3 Vida hoy
body = f'''{ROOT}
{top('D2-Metas.dc.html', 2, 4)}
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">Cuéntame de tu vida hoy</h1>
{card('¿Alguien depende de ti?', chips('depende'), 'De tu hija solo necesitamos su edad, para su educación y para protegerla.')}
{card('¿Dónde vives?', chips('vivienda'))}
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<label for="gastos" style="font-size: 15px; font-weight: 700">¿Cuánto gastas al mes, más o menos?</label>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px; font-weight: 700">{{{{gastosTxt}}}}</span>
<input id="gastos" type="range" min="1000000" max="5000000" step="100000" value="{{{{gastos}}}}" onChange="{{{{onGastos}}}}" style="width: 100%">
<span style="font-size: 12.5px; color: {MUTED}">Con esto calculamos tu colchón: 3 meses son {{{{colchonTxt}}}}.</span>
</div>
{card('¿Tienes deudas?', chips('deudas'))}
<div style="flex-grow: 1"></div>
{cta('D4-Riesgo.dc.html', 'Siguiente')}
</div>
'''
vida_script = chip_script("{ depende: 'Mi hija', vivienda: 'En arriendo', deudas: 'Tarjeta que pago completa', gastos: 2500000 }",
    [('depende', ['Nadie', 'Mi hija', 'Hijos', 'Mis padres'], False),
     ('vivienda', ['En arriendo', 'Con mi familia', 'Propia', 'Con crédito'], False),
     ('deudas', ['No', 'Tarjeta que pago completa', 'Tarjeta o crédito que pago a cuotas'], False)])
vida_script = vida_script.replace("return {", "function fmt(n) { return '$' + (n / 1000000).toFixed(1).replace('.', ',') + ' M'; }\nreturn {\ngastos: s.gastos,\ngastosTxt: fmt(s.gastos),\ncolchonTxt: fmt(s.gastos * 3),\nonGastos: function (e) { self.setState({ gastos: Number(e.target.value) }); },", 1)
write('D3-Vida.dc.html', 'Tu vida hoy', body, vida_script)

# D4 Riesgo (perfil: 6 criterios)
crit = ['Tu horizonte', 'Tus objetivos', 'Tu conocimiento', 'Tu experiencia', 'Cuánto puedes perder', 'Cómo reaccionas a las bajas']
critrows = ''.join(f'<span style="font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 8px; background: {SGREEN if k < 5 else GOLD}; color: {GREEN if k < 5 else INK}">{c}</span>' for k, c in enumerate(crit))
body = f'''{ROOT}
{top('D3-Vida.dc.html', 3, 4)}
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">¿Cómo te sientes con el riesgo?</h1>
<span style="font-size: 14px; color: #2E403A; line-height: 1.45">Seis preguntas, una por cada cosa que un asesor debe conocer antes de recomendarte. Vas en la sexta.</span>
<div style="display: flex; flex-wrap: wrap; gap: 6px">{critrows}</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 16px; display: flex; flex-direction: column; gap: 12px">
<span style="font-size: 12px; font-weight: 700; color: {MUTED}">PREGUNTA 6 DE 6</span>
<strong style="font-size: 16px; line-height: 1.4">Pusiste $780.000 para tu casa. Un mal año bajan a $690.000. ¿Qué harías?</strong>
<div style="display: flex; flex-direction: column; gap: 8px">
<sc-for list="{{{{resp}}}}" as="c" hint-placeholder-count="3">
<button type="button" aria-pressed="{{{{c.on}}}}" onClick="{{{{c.pick}}}}" style="{{{{c.style}}}}">{{{{c.label}}}}</button>
</sc-for>
</div>
</div>
<div style="background: {SAMBER}; border-radius: 16px; padding: 12px 14px; font-size: 13px; line-height: 1.45">No hay respuestas buenas o malas. Con esto sabemos qué te recomendamos y qué no; lo puedes cambiar cuando tu vida cambie.</div>
<div style="flex-grow: 1"></div>
{cta('D5-Entendi.dc.html', 'Siguiente')}
</div>
'''
riesgo_script = chip_script("{ resp: 'Espero: mi meta es a 10 años' }",
    [('resp', ['Lo saco todo para no perder más', 'Espero: mi meta es a 10 años', 'Aprovecho y pongo más'], False)])
riesgo_script = riesgo_script.replace("'min-height: 44px; padding: 0 14px; border-radius: 22px;", "'min-height: 48px; padding: 0 14px; text-align: left; border-radius: 14px;")
write('D4-Riesgo.dc.html', 'Tu perfil', body, riesgo_script)

# D5 Lo que entendí
entendi = [('Lo que quieres', 'Tranquilidad, tu casa en 10 años y pensionarte bien. Lo primero: tu casa.'),
           ('Tu vida hoy', 'Vives en arriendo con tu hija de 8 años. Gastas unos $2,5 M al mes. Tu tarjeta la pagas completa.'),
           ('Tu perfil', 'Moderado: esperas cuando el mercado baja y tu meta es a largo plazo.'),
           ('Lo que aún no sé', 'Si tienes seguros o ahorros en otras entidades. Cuando quieras me cuentas.')]
ent = '\n'.join(f'<div style="display: flex; flex-direction: column; gap: 3px; padding: 10px 0; border-bottom: 1px solid {LINE}"><span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: {MUTED}">{a.upper()}</span><span style="font-size: 14px; line-height: 1.45">{b}</span></div>' for a, b in entendi)
body = f'''{ROOT}
{top('D4-Riesgo.dc.html', 4, 4)}
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">Esto entendí de ti, Laura</h1>
<span style="font-size: 14px; color: #2E403A; line-height: 1.45">Antes de armar tu plan, revisa que esté bien. Lo que corrijas cambia tus números.</span>
<div style="background: #FFFFFF; border-radius: 20px; padding: 4px 16px">{ent}</div>
<a href="D3-Vida.dc.html" style="font-size: 14px; font-weight: 700; text-align: center; min-height: 36px; display: flex; align-items: center; justify-content: center">Corregir algo</a>
<div style="flex-grow: 1"></div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 18px; padding: 14px 16px; font-size: 13.5px; line-height: 1.5">Con esto y lo que ya sabemos de tu pensión y tus cesantías, tu plan está listo: tu patrimonio, tus metas con números y tu primer paso.</div>
{cta('H-Inicio.dc.html', 'Ver mi plan')}
<span style="font-size: 11px; color: {MUTED}; text-align: center">Tus respuestas quedan guardadas como tu perfil del 15 de junio. Puedes verlas y cambiarlas en Tu equipo.</span>
</div>
'''
write('D5-Entendi.dc.html', 'Esto entendí de ti', body)
print('ok')
