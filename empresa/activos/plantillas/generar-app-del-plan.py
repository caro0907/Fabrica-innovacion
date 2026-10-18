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
EMPTY_SCRIPT = '''class Component extends DCLogic {
renderVals() {
return {};
}
}'''

ROOT = f'<div style="width: 390px; height: 844px; box-sizing: border-box; background: {GROUND}; font-family: \'Plus Jakarta Sans\', sans-serif; color: {INK}; display: flex; flex-direction: column">'

ICONS = {
 'inicio': '<path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path>',
 'plan': '<path d="M4 19V5"></path><path d="M4 19h16"></path><path d="M8 15l4-4 3 3 5-6"></path>',
 'patrimonio': '<rect x="3" y="6" width="18" height="13" rx="2"></rect><path d="M3 10h18"></path><path d="M16 15h2"></path>',
 'equipo': '<circle cx="9" cy="8" r="3"></circle><path d="M3 20c0-3 3-5 6-5s6 2 6 5"></path><circle cx="17" cy="9" r="2.5"></circle><path d="M16 15c3 0 5 2 5 4"></path>',
}
def tabbar(active, inicio='H-Inicio.dc.html'):
    tabs = [('inicio', 'Inicio', inicio), ('plan', 'Mi plan', 'H-Plan.dc.html'),
            ('patrimonio', 'Patrimonio', 'H-Patrimonio.dc.html'), ('equipo', 'Tu equipo', 'H-Equipo.dc.html')]
    out = [f'<nav aria-label="Secciones" style="background: #FFFFFF; border-top: 1px solid {LINE}; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); padding: 8px 6px 22px">']
    for k, label, href in tabs:
        col = GREEN if k == active else MUTED
        weight = '700' if k == active else '600'
        out.append(f'<a href="{href}" style="min-height: 48px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; text-decoration: none; color: {col}; font-size: 11px; font-weight: {weight}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>{label}</a>')
    out.append('</nav>')
    return '\n'.join(out)

def back(href, label):
    return (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 10px">'
            f'<a href="{href}" aria-label="Volver" style="width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 22px; background: #FFFFFF"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg></a>'
            f'{label}</div>')

TAG_INFO = f'<span style="font-size: 11px; font-weight: 700; color: {GREEN}; background: {SGREEN}; padding: 3px 8px; border-radius: 8px">Información de tu plan</span>'
TAG_REC = f'<span style="font-size: 11px; font-weight: 700; color: {AMBER}; background: {SAMBER}; padding: 3px 8px; border-radius: 8px">Recomendación profesional</span>'

def avatar(initials, bg=INK, fg='#FFFFFF', size=36, fs=13):
    return f'<span aria-hidden="true" style="width: {size}px; height: {size}px; border-radius: {size//2}px; background: {bg}; color: {fg}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: {fs}px; flex-shrink: 0; border: 2px solid {GROUND}">{initials}</span>'

def ask_bar():
    return (f'<a href="Main.dc.html" style="margin: 0 16px 10px; min-height: 46px; border-radius: 23px; background: #FFFFFF; border: 1px solid {LINE}; display: flex; align-items: center; gap: 10px; padding: 0 16px; text-decoration: none; color: {MUTED}; font-size: 14px">'
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H8l-4 4z"></path></svg>Pregúntale algo a tu arquitecto</a>')

def write(name, title, body, script=EMPTY_SCRIPT):
    html = HEAD.format(title=title) + body + '\n' + TAIL.format(script=script)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)

# ---------- H-Inicio (Laura) ----------
def inicio(name, persona, fecha, total, desglose, puntaje, nota_titulo, nota_texto, nota_cta, nota_href, consultor_ini, consultor, metas_list, meta_href, tab_inicio):
    tiles = []
    for nombre, pct, estado, color, chipbg, chipfg in metas_list:
        tiles.append(f'''<a href="{meta_href}" style="flex: 0 0 150px; min-height: 128px; box-sizing: border-box; background: #FFFFFF; border-radius: 18px; padding: 14px; display: flex; flex-direction: column; gap: 8px; text-decoration: none; color: {INK}">
<span style="font-size: 14px; font-weight: 700; line-height: 1.25">{nombre}</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 24px; font-weight: 700">{pct}%</span>
<span style="height: 6px; border-radius: 3px; background: #ECE8DE"><span style="display: block; height: 6px; border-radius: 3px; width: {pct}%; background: {color}"></span></span>
<span style="align-self: flex-start; font-size: 11px; font-weight: 700; color: {chipfg}; background: {chipbg}; padding: 3px 8px; border-radius: 8px">{estado}</span>
</a>''')
    body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 12px; display: flex; flex-direction: column; gap: 14px; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: center">
<div style="display: flex; flex-direction: column; gap: 2px">
<span style="font-size: 13px; color: {MUTED}">{fecha}</span>
<h1 style="margin: 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px; line-height: 1.1">Hola, {persona}</h1>
</div>
<a href="H-Equipo.dc.html" aria-label="Tu equipo: tu arquitecto y {consultor}" style="display: flex; text-decoration: none">{avatar('A', GREEN)}<span style="margin-left: -10px; display: flex">{avatar(consultor_ini, GOLD, INK)}</span></a>
</div>
<a href="H-Patrimonio.dc.html" style="background: {INK}; color: #FFFFFF; border-radius: 22px; padding: 18px; display: flex; justify-content: space-between; align-items: center; gap: 12px; text-decoration: none">
<div style="display: flex; flex-direction: column; gap: 4px; min-width: 0">
<span style="font-size: 13px; color: #B8CCC4">Tu patrimonio hoy</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 32px; font-weight: 700; line-height: 1.05">{total}</span>
<span style="font-size: 12px; color: #B8CCC4; line-height: 1.4">{desglose}</span>
</div>
<div style="width: 76px; height: 76px; border-radius: 38px; border: 5px solid {GOLD}; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0">
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 20px; font-weight: 700; line-height: 1">{puntaje}</span>
<span style="font-size: 10px; color: #B8CCC4">salud del plan</span>
</div>
</a>
<div style="background: #FFFFFF; border-radius: 22px; padding: 16px 18px; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px">
<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.06em; color: {AMBER}">NOTA DE TU ARQUITECTO</span>
{TAG_INFO}
</div>
<span style="font-family: 'Newsreader', serif; font-size: 22px; font-weight: 600; line-height: 1.2">{nota_titulo}</span>
<span style="font-size: 14px; line-height: 1.5; color: #2E403A">{nota_texto}</span>
<a href="{nota_href}" style="min-height: 46px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; text-decoration: none">{nota_cta}</a>
<span style="font-size: 12px; color: {MUTED}; line-height: 1.4">Si prefieres verlo con alguien, {consultor} conoce tu plan.</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: baseline">
<h2 style="margin: 0; font-size: 16px">Tus metas</h2>
<a href="H-Plan.dc.html" style="font-size: 13px; font-weight: 700">Ver mi plan</a>
</div>
<div style="display: flex; gap: 10px; overflow-x: auto; margin-right: -16px; padding-right: 16px">
{chr(10).join(tiles)}
</div>
</div>
{ask_bar()}
{tabbar('inicio', tab_inicio)}
</div>
'''
    write(name, f'Inicio de {persona}', body)

inicio('H-Inicio.dc.html', 'Laura', 'Lunes 15 de junio · datos ficticios', '$90,4 M',
       'Pensión $78 M · Cesantías $9,4 M · Ahorro $3,0 M', '520',
       'Tu prima llega en 15 días',
       'Preparé tu revisión de junio. Con la prima puedes cerrar la brecha más urgente de tu plan, tu colchón, y avanzar tu casa. Te toma 2 minutos.',
       'Ver mi revisión de junio', 'H-Revision.dc.html', 'DR', 'Daniela, tu consultora,',
       [('Colchón de 3 meses', 40, 'Requiere atención', '#B9721C', SAMBER, AMBER),
        ('Tu casa en 10 años', 21, 'En camino', GREEN, SGREEN, GREEN),
        ('Tu pensión a los 57', 77, 'Con brecha', '#B9721C', SAMBER, AMBER),
        ('Proteger a tu hija', 0, 'Por empezar', '#9AA8A3', '#ECE8DE', '#3F3F3F')],
       'H-Meta.dc.html', 'H-Inicio.dc.html')

inicio('H-InicioJuliana.dc.html', 'Juliana', 'Lunes 23 de noviembre · datos ficticios', '$257 M',
       'Pensión $185 M · Pensión voluntaria $24 M · Ahorro $34 M · Cesantías $14 M', '640',
       'Cierre de año: tu casa y tu impuesto',
       'Tu casa en la costa va en 27%. Preparé tu revisión de cierre de año: completar el aporte de este año para tu casa te acerca a tu meta y, como pagas renta, baja tu impuesto unos $950.000.',
       'Ver mi revisión de cierre de año', 'J1b-Plan.dc.html', 'CV', 'Camilo, tu consultor,',
       [('Colchón de 4 meses', 100, 'Completo', GREEN, SGREEN, GREEN),
        ('Casa en la costa a los 55', 27, 'En camino', GREEN, SGREEN, GREEN),
        ('Tu pensión a los 57', 80, 'Con brecha', '#B9721C', SAMBER, AMBER)],
       'J1b-Plan.dc.html', 'H-InicioJuliana.dc.html')

# ---------- H-Revision ----------
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 18px 14px; display: flex; flex-direction: column; gap: 12px">
{back('H-Inicio.dc.html', TAG_INFO)}
<div style="background: #FFFFFF; border-radius: 22px; padding: 18px 18px 16px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; flex-direction: column; gap: 2px">
<span style="font-size: 12px; color: {MUTED}">Preparada para Laura · 15 de junio</span>
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">Tu revisión de junio</h1>
</div>
<div style="display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.06em; color: {MUTED}">CÓMO VAS</span>
<span style="font-size: 14px; line-height: 1.45">Tu pensión va en 77% de la meta que tienes para vivir tranquila.</span>
<span style="font-size: 14px; line-height: 1.45">Tu colchón cubre 1,2 meses de gastos; lo sano son 3.</span>
<span style="font-size: 14px; line-height: 1.45">Tu hija aún no está confirmada como tu beneficiaria.</span>
</div>
<div style="height: 1px; background: {LINE}"></div>
<div style="display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.06em; color: {MUTED}">QUÉ CAMBIÓ</span>
<span style="font-size: 14px; line-height: 1.45">El 30 de junio llega tu prima, unos $2.600.000. Es tu mejor momento del semestre para avanzar.</span>
</div>
<div style="height: 1px; background: {LINE}"></div>
<div style="display: flex; flex-direction: column; gap: 8px">
<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.06em; color: {MUTED}">LO QUE TE PROPONGO</span>
<span style="font-size: 14px; line-height: 1.45"><strong>1.</strong> Separa $1.820.000 en tu cuenta para tu colchón. Es un paso de tu plan, no un producto.</span>
<span style="font-size: 14px; line-height: 1.45"><strong>2.</strong> Pon $780.000 a tu casa, en un portafolio moderado.</span>
<span style="font-size: 14px; line-height: 1.45"><strong>3.</strong> Confirma a tu hija como beneficiaria. Toma 2 minutos.</span>
</div>
<div style="background: {SAMBER}; border-radius: 14px; padding: 10px 12px; font-size: 13px; line-height: 1.45"><strong>Lo que no te propongo todavía:</strong> invertir para tu pensión. Primero tu colchón; en diciembre lo revisamos.</div>
</div>
<div style="flex-grow: 1"></div>
<a href="H-Decision.dc.html" style="min-height: 52px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 16px; display: flex; align-items: center; justify-content: center; text-decoration: none">Revisar mi propuesta</a>
<a href="H-Equipo.dc.html" style="min-height: 44px; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; font-weight: 700; text-decoration: none">{avatar('DR', GOLD, INK, 28, 11)}Verla con Daniela, tu consultora</a>
<span style="font-size: 11px; color: {MUTED}; text-align: center; line-height: 1.4">Preparada por tu arquitecto digital con tus datos y lo que nos contaste. Cifras estimadas; no son promesas.</span>
</div>
</div>
'''
write('H-Revision.dc.html', 'Tu revisión de junio', body)

# ---------- H-Plan ----------
metas = [('Colchón de 3 meses', 'Requiere atención', 'Tienes $3,0 M de $7,5 M', 40, '#B9721C', SAMBER, AMBER),
         ('Tu casa en 10 años', 'En camino', 'Cuota inicial de $45 M · llevas $9,4 M', 21, GREEN, SGREEN, GREEN),
         ('Proteger a tu hija', 'Por empezar', 'Confírmala como beneficiaria · sin producto', 0, '#9AA8A3', '#ECE8DE', '#3F3F3F'),
         ('Educación de tu hija', 'Por definir', 'La universidad empieza en 10 años', 0, '#9AA8A3', '#ECE8DE', '#3F3F3F')]
rows = []
for n, e, t, p, c, cb, cf in metas:
    href = 'H-Meta.dc.html' if 'casa' in n else 'H-Revision.dc.html'
    rows.append(f'''<a href="{href}" style="display: flex; flex-direction: column; gap: 6px; padding: 11px 0; border-bottom: 1px solid {LINE}; text-decoration: none; color: {INK}">
<span style="display: flex; justify-content: space-between; gap: 8px; align-items: center"><strong style="font-size: 14px">{n}</strong><span style="font-size: 11px; font-weight: 700; color: {cf}; background: {cb}; padding: 3px 8px; border-radius: 8px; flex-shrink: 0">{e}</span></span>
<span style="font-size: 12.5px; color: #2E403A">{t}</span>
<span style="height: 6px; border-radius: 3px; background: #ECE8DE"><span style="display: block; height: 6px; border-radius: 3px; width: {p}%; background: {c}"></span></span>
</a>''')
cal = [('30 jun', 'Prima de mitad de año', '$2,6 M'), ('20 dic', 'Prima de fin de año', '$2,6 M'), ('31 ene', 'Intereses de tus cesantías', '$624 mil'), ('14 feb', 'Tu empresa consigna tus cesantías', '$5,2 M')]
calrows = '\n'.join(f'<div style="display: grid; grid-template-columns: 56px minmax(0, 1fr) auto; gap: 8px; font-size: 13px; padding: 6px 0"><strong style="color: {AMBER}">{d}</strong><span>{x}</span><strong>{v}</strong></div>' for d, x, v in cal)
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 10px; display: flex; flex-direction: column; gap: 12px; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: center"><h1 style="margin: 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px">Mi plan de vida</h1>{TAG_INFO}</div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; justify-content: space-between; align-items: baseline"><strong style="font-size: 15px">Tu pensión, el ancla</strong><span style="font-size: 12px; color: #B8CCC4">hoy 36 → 57 años</span></div>
<span style="font-size: 13px; color: #DCE6E2; line-height: 1.4">Vas para unos <strong style="color: #FFFFFF">$2,3 M al mes</strong>; tu meta son <strong style="color: #FFFFFF">$3,0 M</strong>. Estimado con las reglas que rigen desde abril de 2027.</span>
<span style="height: 8px; border-radius: 4px; background: #2C4A41"><span style="display: block; width: 77%; height: 8px; border-radius: 4px; background: {GOLD}"></span></span>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">
{chr(10).join(rows)}
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 12px 16px; display: flex; flex-direction: column">
<strong style="font-size: 14px; padding-bottom: 4px">Tu año en dinero</strong>
{calrows}
</div>
</div>
{tabbar('plan')}
</div>
'''
write('H-Plan.dc.html', 'Mi plan de vida', body)

# ---------- H-Meta (casa, interactive) ----------
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 12px; display: flex; flex-direction: column; gap: 12px">
{back('H-Plan.dc.html', TAG_INFO)}
<div style="background: {SGREEN}; border-radius: 22px; padding: 18px; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; gap: 12px">
<span aria-hidden="true" style="width: 48px; height: 48px; border-radius: 14px; background: #FFFFFF; display: flex; align-items: center; justify-content: center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path></svg></span>
<div style="display: flex; flex-direction: column"><h1 style="margin: 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 24px">Tu casa</h1><span style="font-size: 13px; color: #2E403A">Cuota inicial de $45 M · meta en 10 años</span></div>
</div>
<div style="display: flex; justify-content: space-between; font-size: 13px"><span><strong>$9,4 M</strong> llevas</span><span><strong>21%</strong></span></div>
<span style="height: 10px; border-radius: 5px; background: #FFFFFF"><span style="display: block; width: 21%; height: 10px; border-radius: 5px; background: {GREEN}"></span></span>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<strong style="font-size: 14px">Con qué la estás construyendo</strong>
<div style="display: flex; justify-content: space-between; font-size: 13px"><span>Tus cesantías</span><strong>$9,4 M</strong></div>
<div style="display: flex; justify-content: space-between; font-size: 13px"><span>30% de cada prima (si apruebas tu propuesta)</span><strong>$780 mil</strong></div>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px">
<strong style="font-size: 14px">¿Y si además separas cada mes…?</strong>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px">
<sc-for list="{{{{montos}}}}" as="m" hint-placeholder-count="4">
<button type="button" onClick="{{{{m.pick}}}}" style="{{{{m.style}}}}">{{{{m.label}}}}</button>
</sc-for>
</div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 16px; padding: 14px; display: flex; flex-direction: column; gap: 4px">
<span style="font-size: 13px; color: #B8CCC4">Llegas a tu cuota inicial hacia</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 30px; font-weight: 700">{{{{anio}}}}</span>
<span style="font-size: 12px; color: #DCE6E2">{{{{lectura}}}}</span>
</div>
<span style="font-size: 11px; color: {MUTED}; line-height: 1.4">Supone una rentabilidad real de 4% al año, ya descontadas comisiones, y no cuenta tus cesantías futuras, que son tu respaldo si pierdes el empleo. Estimado; no es una promesa.</span>
</div>
<div style="flex-grow: 1"></div>
<a href="H-Decision.dc.html" style="min-height: 50px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; text-decoration: none">Ver mi propuesta para la prima</a>
</div>
</div>
'''
meta_script = '''class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { mensual: 100000 };
}
anios(m) {
var b = 9400000, r = Math.pow(1.04, 1 / 12) - 1, meses = 0;
while (b < 45000000 && meses < 600) {
b = b * (1 + r) + m;
if (meses % 12 === 5 || meses % 12 === 11) { b += 780000; }
meses++;
}
return meses / 12;
}
renderVals() {
var self = this, m = this.state.mensual;
var opts = [0, 100000, 200000, 300000];
var t = this.anios(m);
var anio = 2026 + Math.ceil(t);
var lectura = t <= 10 ? 'Dentro de los 10 años que te pusiste.' : 'Después de los 10 años que te pusiste: con un poco más al mes llegas a tiempo.';
return {
montos: opts.map(function (v) {
var sel = v === m;
return {
label: v === 0 ? '$0' : '$' + (v / 1000) + ' mil',
pick: function () { self.setState({ mensual: v }); },
style: 'min-height: 44px; border-radius: 12px; font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; border: 2px solid ' + (sel ? '#0E6A4E' : '#E7E2D6') + '; background: ' + (sel ? '#E3EFEA' : '#FFFFFF') + '; color: #12241F'
};
}),
anio: String(anio),
lectura: lectura
};
}
}'''
write('H-Meta.dc.html', 'Tu casa', body, meta_script)

# ---------- H-Decision (interactive) ----------
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 14px; display: flex; flex-direction: column; gap: 12px">
{back('H-Revision.dc.html', TAG_REC)}
<sc-if value="{{{{pendiente}}}}" hint-placeholder-val="{{{{ true }}}}">
<div style="display: flex; flex-direction: column; gap: 12px">
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">Tu propuesta para la prima</h1>
<div style="background: {SGREEN}; border-radius: 18px; padding: 14px 16px; display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; justify-content: space-between; gap: 8px"><strong style="font-size: 15px">$1.820.000 a tu colchón</strong><span style="font-size: 11px; font-weight: 700; color: {GREEN}; text-align: right">PASO DEL PLAN · NO ES UN PRODUCTO</span></div>
<span style="font-size: 13px; line-height: 1.45; color: #2E403A">Sepáralo en tu cuenta de ahorros. Pasas de 1,2 a 1,9 meses de colchón.</span>
</div>
<div style="background: #FFFFFF; border-radius: 18px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; justify-content: space-between; gap: 8px"><strong style="font-size: 15px">$780.000 a tu casa</strong><span style="font-size: 11px; font-weight: 700; color: {AMBER}; text-align: right">PORTAFOLIO MODERADO</span></div>
<span style="font-size: 13px; line-height: 1.45; color: #2E403A"><strong>Por qué:</strong> tu meta es a 10 años y tu perfil es moderado; con ese plazo puedes aguantar las bajas.</span>
<span style="font-size: 13px; background: {SAMBER}; border-radius: 10px; padding: 8px 10px; line-height: 1.4"><strong>En un mal año</strong> podría bajar unos $90.000. Por eso tu colchón no va ahí.</span>
<details style="font-size: 12.5px; line-height: 1.5; color: #2E403A">
<summary style="font-weight: 700; font-size: 13px; color: {INK}; cursor: pointer; min-height: 24px">Quién te asesora y cuánto cuesta</summary>
Recomendación de [Administradora] hecha por una herramienta que la entidad supervisa, con tu perfil del 15 de junio. Asesoría no independiente: recibimos una comisión de [X]% al año. Otras opciones: tu cuenta de ahorros, un CDT o fondos de otras entidades.
</details>
</div>
<a href="H-Equipo.dc.html" style="background: #FFFFFF; border-radius: 18px; padding: 12px 14px; display: flex; align-items: center; gap: 12px; text-decoration: none; color: {INK}">{avatar('DR', GOLD, INK, 40, 13)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 14px">¿Lo vemos con Daniela?</strong><span style="font-size: 12.5px; color: {MUTED}">Mañana 10:00 a. m. o 4:00 p. m. · 15 minutos por video</span></span></a>
<button type="button" onClick="{{{{aprobar}}}}" style="min-height: 52px; border: 0; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-family: inherit; font-weight: 700; font-size: 16px; cursor: pointer">Aprobar con mi huella</button>
<span style="font-size: 11px; color: {MUTED}; text-align: center">El 30 de junio te pido confirmar antes de mover cualquier peso.</span>
</div>
</sc-if>
<sc-if value="{{{{listo}}}}" hint-placeholder-val="{{{{ false }}}}">
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 14px; justify-content: center">
<span aria-hidden="true" style="width: 68px; height: 68px; border-radius: 34px; background: {SGREEN}; display: flex; align-items: center; justify-content: center"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"></path></svg></span>
<h1 style="margin: 0; font-family: 'Newsreader', serif; font-size: 28px; font-weight: 600; line-height: 1.15">Listo, Laura. Tu prima ya tiene rumbo.</h1>
<span style="font-size: 15px; line-height: 1.5; color: #2E403A">El 30 de junio, cuando llegue, te pido confirmar. Tu plan pasa de 520 a <strong>610</strong> (estimado) y tu colchón a 1,9 meses.</span>
<div style="background: #FFFFFF; border-radius: 18px; padding: 14px 16px; font-size: 14px; line-height: 1.45">¿Quieres que en diciembre te lo proponga igual, con aviso un día antes?</div>
<a href="L5-Reglas.dc.html" style="min-height: 50px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; text-decoration: none">Sí, déjalo como regla</a>
<a href="H-Inicio.dc.html" style="text-align: center; font-size: 14px; font-weight: 700; padding: 8px">Volver a mi inicio</a>
</div>
</sc-if>
</div>
</div>
'''
dec_script = '''class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { listo: false };
}
renderVals() {
var self = this;
return {
pendiente: !this.state.listo,
listo: this.state.listo,
aprobar: function () { self.setState({ listo: true }); }
};
}
}'''
write('H-Decision.dc.html', 'Tu propuesta para la prima', body, dec_script)

# ---------- H-Patrimonio ----------
def fila(n, v, estado, cb, cf):
    return f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid {LINE}"><span style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><strong style="font-size: 14px">{n}</strong><span style="font-size: 12.5px; color: #2E403A">{v}</span></span><span style="font-size: 11px; font-weight: 700; color: {cf}; background: {cb}; padding: 3px 8px; border-radius: 8px; flex-shrink: 0">{estado}</span></div>'
S, C, P = ('Sabemos', SGREEN, GREEN), ('Nos contaste', SAMBER, AMBER), ('Por completar', '#ECE8DE', '#3F3F3F')
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 10px; display: flex; flex-direction: column; gap: 12px; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: center"><h1 style="margin: 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px">Mi patrimonio</h1>{TAG_INFO}</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 16px; display: flex; flex-direction: column; gap: 10px">
<span style="font-size: 13px; color: {MUTED}">Todo lo tuyo, en un solo lugar</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 32px; font-weight: 700">$90,4 M</span>
<div role="img" aria-label="Pensión 86%, cesantías 10%, ahorro 3%" style="display: flex; height: 12px; border-radius: 6px; overflow: hidden; gap: 2px"><span style="width: 86%; background: {INK}"></span><span style="width: 10%; background: {GREEN}"></span><span style="width: 4%; background: #B9721C"></span></div>
<div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: #2E403A"><span>Pensión 86%</span><span>Cesantías 10%</span><span>Ahorro 3%</span></div>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">
{fila('Pensión obligatoria', '$78 M · 14 años cotizados', *S)}
{fila('Cesantías', '$9,4 M · hoy construyen tu casa', *S)}
{fila('Ahorro', '$3,0 M en una cuenta de ahorros', *C)}
{fila('Deudas', 'Tarjeta al día; sin deudas caras', *C)}
{fila('Protección de tu familia', 'Tu hija · beneficiaria por confirmar', *P)}
{fila('Impuestos', 'No pagas renta (estimado); si debes declarar depende de tus ingresos', *S)}
</div>
<div style="background: {SAMBER}; border-radius: 18px; padding: 12px 14px; font-size: 13px; line-height: 1.45"><strong>¿Tienes algo en otras entidades?</strong> Cuéntanos o sube un extracto, y lo sumamos a tu plan. Cuando las finanzas abiertas estén disponibles, podrás conectarlo.</div>
</div>
{tabbar('patrimonio')}
</div>
'''
write('H-Patrimonio.dc.html', 'Mi patrimonio', body)

# ---------- H-Equipo ----------
cuando = ['Siempre que lo pidas', 'Aportes que solo sirven para tu pensión', 'Traslados y tu forma de pensionarte', 'Un retiro que te hace perder un beneficio']
cuando_html = '\n'.join(f'<span style="display: flex; gap: 8px; align-items: flex-start; font-size: 13px; line-height: 1.4"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink: 0; margin-top: 2px"><path d="M5 12l5 5L20 7"></path></svg>{c}</span>' for c in cuando)
body = f'''{ROOT}
<div style="flex-grow: 1; padding: 22px 16px 10px; display: flex; flex-direction: column; gap: 12px; overflow: hidden">
<h1 style="margin: 0; font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px">Tu equipo</h1>
<div style="background: #FFFFFF; border-radius: 22px; padding: 16px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; gap: 12px; align-items: center">{avatar('DR', GOLD, INK, 56, 18)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 16px">Daniela R.</strong><span style="font-size: 12px; color: {MUTED}; line-height: 1.35">Tu consultora · certificada por el Autorregulador del Mercado de Valores · datos ficticios</span></span></div>
<span style="font-size: 13px; line-height: 1.45; color: #2E403A">Ve tu mismo plan y tu historia. No tienes que repetirle nada.</span>
<span style="font-size: 12px; font-weight: 700; color: {MUTED}">AGENDA 15 MINUTOS POR VIDEO</span>
<div style="display: flex; gap: 8px; flex-wrap: wrap">
<button type="button" style="min-height: 44px; padding: 0 14px; border-radius: 12px; border: 2px solid {GREEN}; background: {SGREEN}; font-family: inherit; font-weight: 700; font-size: 13px; color: {INK}; cursor: pointer">Mañana 10:00 a. m.</button>
<button type="button" style="min-height: 44px; padding: 0 14px; border-radius: 12px; border: 2px solid {LINE}; background: #FFFFFF; font-family: inherit; font-weight: 700; font-size: 13px; color: {INK}; cursor: pointer">Mañana 4:00 p. m.</button>
<button type="button" style="min-height: 44px; padding: 0 14px; border-radius: 12px; border: 2px solid {LINE}; background: #FFFFFF; font-family: inherit; font-weight: 700; font-size: 13px; color: {INK}; cursor: pointer">Escribirle</button>
</div>
</div>
<div style="background: #FFFFFF; border-radius: 22px; padding: 16px; display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; gap: 12px; align-items: center">{avatar('A', GREEN, '#FFFFFF', 44, 16)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 15px">Tu arquitecto digital</strong><span style="font-size: 12px; color: {MUTED}">Herramienta de [Administradora], supervisada por la entidad</span></span></div>
<span style="font-size: 13px; line-height: 1.45; color: #2E403A">Arma y vigila tu plan todos los días y te avisa antes de los momentos que importan. Te propone; nunca decide por ti. La asesoría es no independiente: te recomienda alternativas nuestras y recibimos una comisión.</span>
</div>
<div style="background: {SAMBER}; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<strong style="font-size: 14px">Cuándo te proponemos hablar con Daniela</strong>
{cuando_html}
</div>
<a href="T1-ComoFunciona.dc.html" style="font-size: 13px; font-weight: 700; text-align: center">Cómo funciona tu arquitecto y tus permisos</a>
</div>
{tabbar('equipo')}
</div>
'''
write('H-Equipo.dc.html', 'Tu equipo', body)
print('ok')
