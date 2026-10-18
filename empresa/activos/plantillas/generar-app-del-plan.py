"""v5.1 · La app del arquitecto para Laura (vuelve el 15 de junio) y Juliana (23 de noviembre).
Cada persona tiene sus propias pantallas; ningún enlace cruza de una persona a otra."""
import sys
from pantallas_asesoria import *
set_out(sys.argv[1])

L = dict(sfx='', nombre='Laura', fecha='Lunes 15 de junio · datos ficticios', cons='Daniela', cons_full='Daniela R.', cons_ini='DR',
         cons_rol='tu consultora', perfil='moderado · del 1 de junio', cert='Certificada por el Autorregulador del Mercado de Valores e inscrita en el Registro Nacional de Profesionales del Mercado de Valores')
J = dict(sfx='Juliana', nombre='Juliana', fecha='Lunes 23 de noviembre · datos ficticios', cons='Camilo', cons_full='Camilo V.', cons_ini='CV',
         cons_rol='tu consultor', perfil='moderado · del 3 de marzo', cert='Certificado por el Autorregulador del Mercado de Valores e inscrito en el Registro Nacional de Profesionales del Mercado de Valores')

def metas_tiles(persona, tiles):
    out = []
    for nombre, pct, estado, color, cb, cf, href in tiles:
        out.append(f'''<a href="{href}" style="flex: 0 0 148px; min-height: 124px; box-sizing: border-box; background: #FFFFFF; border-radius: 18px; padding: 13px; display: flex; flex-direction: column; gap: 7px; text-decoration: none; color: {INK}">
<span style="font-size: 14px; font-weight: 700; line-height: 1.25">{nombre}</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 23px; font-weight: 700">{pct}%</span>
{bar(pct, color)}
<span style="align-self: flex-start">{tag(estado, cf, cb)}</span></a>''')
    return '\n'.join(out)

def inicio(P, total, desglose, puntaje, nota_t, nota_x, nota_cta, nota_href, tiles):
    s = P['sfx']
    body = f'''{root(False)}
{inner(13, '20px 16px 10px')}
<div style="display: flex; justify-content: space-between; align-items: center">
<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 13px; color: {MUTED}">{P['fecha']}</span>{h1('Hola, ' + P['nombre'], False, 26)}</div>
<a href="{f('H-Equipo', s)}" aria-label="Tu equipo: tu arquitecto y {P['cons']}" style="display: flex; text-decoration: none; min-height: 44px; align-items: center">{avatar('A', GREEN)}<span style="margin-left: -10px; display: flex">{avatar(P['cons_ini'], GOLD, INK)}</span></a>
</div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 22px; padding: 16px 18px; display: flex; flex-direction: column; gap: 10px">
<a href="{f('H-Patrimonio', s)}" style="display: flex; flex-direction: column; gap: 4px; text-decoration: none; color: #FFFFFF">
<span style="font-size: 13px; color: #B8CCC4">Tu patrimonio hoy</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 32px; font-weight: 700; line-height: 1.05">{total}</span>
<span style="font-size: 12px; color: #B8CCC4; line-height: 1.4">{desglose}</span></a>
<a href="{f('H-Pilares', s)}" style="display: flex; justify-content: space-between; align-items: center; gap: 10px; min-height: 44px; border-top: 1px solid #2C4A41; padding-top: 8px; text-decoration: none; color: #FFFFFF">
<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px"><strong style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 20px; color: {GOLD}">{puntaje}</strong> de 1.000 · salud de tu plan</span><span style="font-size: 11.5px; color: #B8CCC4">Información, no una recomendación ni una calificación de crédito</span></span>
<span style="font-size: 13px; font-weight: 700; color: {GOLD}; flex-shrink: 0">Ver pilares</span></a>
</div>
<div style="background: #FFFFFF; border-radius: 22px; padding: 15px 18px; display: flex; flex-direction: column; gap: 9px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px">{eyebrow('Nota de tu arquitecto', AMBER)}{TAG_INFO}</div>
<span style="font-family: 'Newsreader', serif; font-size: 22px; font-weight: 600; line-height: 1.2">{nota_t}</span>
{p(nota_x)}
<a href="{nota_href}" style="min-height: 46px; border-radius: 14px; background: {GREEN}; color: #FFFFFF; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; text-decoration: none">{nota_cta}</a>
</div>
<div style="display: flex; justify-content: space-between; align-items: center"><h2 style="margin: 0; font-size: 16px">Tus metas</h2>{link(f('H-Plan', s), 'Ver mi plan', False)}</div>
<div style="display: flex; gap: 10px; overflow-x: auto; margin-right: -16px; padding-right: 16px">
{metas_tiles(s, tiles)}
</div>
</div>
{ask_bar(s)}
{tabbar('inicio', s)}
</div>'''
    write(f('H-Inicio', s), f'Inicio de {P["nombre"]}', body)

def pil_rows(rows):
    out = []
    for n, v, t in rows:
        c = GREEN if v >= 65 else (WARN if v >= 45 else '#9A2B1E')
        out.append(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 8px 0; border-bottom: 1px solid {LINE}"><span style="display: flex; justify-content: space-between"><strong style="font-size: 14px">{n}</strong><strong style="font-size: 13px">{v} / 100</strong></span>{bar(v, c, GREY, 8)}<span style="font-size: 12.5px; color: {BODY}">{t}</span></div>')
    return ''.join(out)

def pilares(P, score, rows, mueve, cta_href, cta_txt):
    s = P['sfx']
    body = f'''{root(False)}
{inner(11, '20px 16px 14px')}
{back(f('H-Inicio', s), TAG_INFO)}
<div style="display: flex; align-items: baseline; gap: 8px"><span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 44px; font-weight: 700; line-height: 1">{score}</span><span style="font-size: 14px; color: {MUTED}">de 1.000 · la salud de tu plan</span></div>
{p('Seis pilares, con tu pensión adentro. Es el promedio de los seis.', 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">{pil_rows(rows)}</div>
<div style="background: {SAMBER}; border-radius: 16px; padding: 12px 14px; font-size: 13.5px; line-height: 1.45"><strong>Lo que más lo mueve hoy:</strong> {mueve}</div>
<div style="flex-grow: 1"></div>
{cta(cta_href, cta_txt)}
{small('Información de tu plan. No es una recomendación profesional ni una calificación de crédito. Puntaje simulado.', True)}
</div>
</div>'''
    write(f('H-Pilares', s), 'La salud de tu plan', body)

def revision(P, titulo, sub, como, cambio, propongo, nopropongo, cta_href, cta_txt):
    s = P['sfx']
    li = lambda xs: ''.join(p(x, 13.5) for x in xs)
    body = f'''{root(False)}
{inner(9, '18px 16px 12px')}
{back(f('H-Inicio', s), TAG_INFO)}
<div style="background: #FFFFFF; border-radius: 22px; padding: 14px 16px; display: flex; flex-direction: column; gap: 9px">
<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 12px; color: {MUTED}">{sub}</span>{h1(titulo, True, 24)}</div>
<div style="display: flex; flex-direction: column; gap: 5px">{eyebrow('Cómo vas')}{li(como)}</div>
<div style="height: 1px; background: {LINE}"></div>
<div style="display: flex; flex-direction: column; gap: 5px">{eyebrow('Qué cambió')}{li(cambio)}</div>
<div style="height: 1px; background: {LINE}"></div>
<div style="display: flex; flex-direction: column; gap: 7px">{eyebrow('Lo que te propongo')}{li(propongo)}</div>
<div style="background: {SAMBER}; border-radius: 14px; padding: 10px 12px; font-size: 13px; line-height: 1.45"><strong>Lo que no te propongo todavía:</strong> {nopropongo}</div>
</div>
<div style="flex-grow: 1"></div>
{cta(cta_href, cta_txt)}
{link(f('H-Equipo', s), avatar(P['cons_ini'], GOLD, INK, 28, 11) + f'Verla con {P["cons"]}, {P["cons_rol"]}')}
{small('Preparada por tu arquitecto digital. Cifras estimadas; no son promesas.', True)}
</div>
</div>'''
    write(f('H-Revision', s), titulo, body)

def plan(P, ancla, sup, metas_html, sugerencia, cal):
    s = P['sfx']
    calrows = ''.join(f'<div style="display: grid; grid-template-columns: 54px minmax(0, 1fr) auto; gap: 8px; font-size: 13px; padding: 5px 0"><strong style="color: {AMBER}">{d}</strong><span>{x}</span><strong>{v}</strong></div>' for d, x, v in cal)
    body = f'''{root(False)}
{inner(11, '20px 16px 10px')}
<div style="display: flex; justify-content: space-between; align-items: center">{h1('Mi plan de vida', False, 26)}{TAG_INFO}</div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 20px; padding: 13px 16px 4px; display: flex; flex-direction: column; gap: 7px">
<strong style="font-size: 15px">Tu pensión, el ancla</strong>
<span style="font-size: 13px; color: #DCE6E2; line-height: 1.45">{ancla}</span>
<details style="font-size: 12px; line-height: 1.5; color: #DCE6E2"><summary style="min-height: 44px; display: flex; align-items: center; font-weight: 700; font-size: 13.5px; color: {GOLD}; cursor: pointer">Ver supuestos</summary>{sup}</details>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">{metas_html}</div>
{sugerencia}
<div style="background: #FFFFFF; border-radius: 20px; padding: 10px 16px; display: flex; flex-direction: column"><strong style="font-size: 14px; padding-bottom: 2px">Tu año en dinero</strong>{calrows}</div>
</div>
{ask_bar(s)}
{tabbar('plan', s)}
</div>'''
    write(f('H-Plan', s), 'Mi plan de vida', body)

def meta_row(nombre, estado, txt, pct, color, ok, href=None):
    fg, bg = (GREEN, SGREEN) if ok == 'g' else ((AMBER, SAMBER) if ok == 'a' else ('#3F3F3F', GREY))
    chev = f'<span style="font-size: 12.5px; font-weight: 700; color: {GREEN}">Ver detalle ›</span>' if href else ''
    inner_ = (f'<span style="display: flex; justify-content: space-between; gap: 8px; align-items: center"><strong style="font-size: 14px">{nombre}</strong>{tag(estado, fg, bg)}</span>'
              f'<span style="font-size: 12.5px; color: {BODY}">{txt}</span>{bar(pct, color)}{chev}')
    st = f'display: flex; flex-direction: column; gap: 5px; padding: 10px 0; border-bottom: 1px solid {LINE}; text-decoration: none; color: {INK}'
    return f'<a href="{href}" style="{st}">{inner_}</a>' if href else f'<div style="{st}">{inner_}</div>'

def fila(n, v, k):
    return f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid {LINE}"><span style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><strong style="font-size: 13.5px">{n}</strong><span style="font-size: 12.5px; color: {BODY}">{v}</span></span>{origen(k)}</div>'

def patrimonio(P, total, segs, filas):
    s = P['sfx']
    barra = ''.join(f'<span style="width: {w}%; background: {c}"></span>' for _, w, c in segs)
    leyenda = ''.join(f'<span>{n} {round(w)}%</span>' for n, w, _ in segs)
    aria = ', '.join(f'{n} {round(w)}%' for n, w, _ in segs)
    body = f'''{root(False)}
{inner(9, '18px 16px 8px')}
<div style="display: flex; justify-content: space-between; align-items: center">{h1('Mi patrimonio', False, 26)}{TAG_INFO}</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px">
<span style="font-size: 13px; color: {MUTED}">Tus 8 dimensiones, en un solo lugar</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 30px; font-weight: 700">{total}</span>
<div role="img" aria-label="{aria}" style="display: flex; height: 12px; border-radius: 6px; overflow: hidden; gap: 2px">{barra}</div>
<div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: {BODY}">{leyenda}</div>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 0 16px">{''.join(fila(*x) for x in filas)}</div>
{small('¿Tienes algo en otras entidades? Cuéntanos o sube un extracto. Cuando las finanzas abiertas estén disponibles, podrás conectarlo.')}
</div>
{ask_bar(s)}
{tabbar('patrimonio', s)}
</div>'''
    write(f('H-Patrimonio', s), 'Mi patrimonio', body)

def equipo(P, cuando, nota_rnpmv='Supuesto por decidir: si el consultor con nombre aplica a todos los segmentos'):
    s = P['sfx']
    ch = ''.join(f'<span style="display: flex; gap: 8px; align-items: flex-start; font-size: 13px; line-height: 1.4"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink: 0; margin-top: 2px"><path d="M5 12l5 5L20 7"></path></svg>{c}</span>' for c in cuando)
    body = f'''{root(False)}
{inner(10, '20px 16px 8px')}
{h1('Tu equipo', False, 26)}
<div style="background: #FFFFFF; border-radius: 22px; padding: 14px 16px; display: flex; flex-direction: column; gap: 9px">
<div style="display: flex; gap: 12px; align-items: center">{avatar(P['cons_ini'], GOLD, INK, 52, 17)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 16px">{P['cons_full']} · {P['cons_rol']}</strong><span style="font-size: 11.5px; color: {MUTED}; line-height: 1.35">{P['cert']} · datos ficticios</span></span></div>
{p('Ve tu mismo plan y tu historia: no tienes que repetirle nada. Agenda 15 minutos por video:', 13)}
<div style="display: flex; gap: 8px; flex-wrap: wrap">
<sc-for list="{{{{slots}}}}" as="c" hint-placeholder-count="2"><button type="button" aria-pressed="{{{{c.on}}}}" onClick="{{{{c.pick}}}}" style="{{{{c.style}}}}">{{{{c.label}}}}</button></sc-for>
</div>
<sc-if value="{{{{agendado}}}}" hint-placeholder-val="{{{{ false }}}}"><span style="font-size: 13px; font-weight: 700; color: {GREEN}">{{{{agendadoTxt}}}}</span></sc-if>
</div>
<div style="background: #FFFFFF; border-radius: 22px; padding: 12px 16px; display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; gap: 12px; align-items: center">{avatar('A', GREEN, '#FFFFFF', 40, 15)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 15px">Tu arquitecto digital</strong><span style="font-size: 11.5px; color: {MUTED}">Herramienta de tu administradora de fondos, supervisada por la entidad</span></span></div>
{p('Arma y vigila tu plan y te avisa antes de los momentos que importan. Te propone; nunca decide por ti. Asesoría no independiente: te recomienda alternativas nuestras y recibimos una comisión.', 12.5)}
</div>
<div style="background: {SAMBER}; border-radius: 20px; padding: 12px 16px; display: flex; flex-direction: column; gap: 6px"><strong style="font-size: 14px">Cuándo te proponemos hablar con {P['cons']}</strong>{ch}</div>
<div style="background: #FFFFFF; border-radius: 18px; padding: 0 16px; display: flex; flex-direction: column">
<a href="{f('H-Perfil', s)}" style="min-height: 44px; display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: {INK}; font-size: 14px; border-bottom: 1px solid {LINE}"><span>Tu perfil: {P['perfil']}</span><strong style="color: {GREEN}">Ver o cambiar</strong></a>
<a href="{f('H-Reglas', s)}" style="min-height: 44px; display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: {INK}; font-size: 14px; border-bottom: 1px solid {LINE}"><span>Mis reglas y permisos</span><strong style="color: {GREEN}">Ver</strong></a>
<a href="{f('H-ComoFunciona', s)}" style="min-height: 44px; display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: {INK}; font-size: 14px"><span>Cómo funciona tu arquitecto</span><strong style="color: {GREEN}">Ver</strong></a>
</div>
</div>
{tabbar('equipo', s)}
</div>'''
    sc = script("{ slot: '' }", extra=(
        "slots: ['Mañana 10:00 a. m.', 'Mañana 4:00 p. m.'].map(function (o) { var on = s.slot === o; return { label: o, on: on ? 'true' : 'false', style: st(on, false).replace('border-radius: 22px', 'border-radius: 12px'), pick: function () { self.setState({ slot: o }); } }; }), "
        f"agendado: s.slot !== '', agendadoTxt: 'Agendado: ' + s.slot + '. {P['cons']} ya tiene tu plan a la vista.'"))
    write(f('H-Equipo', s), 'Tu equipo', body, sc)

def perfil(P, respuestas, cambiar_href=None):
    s = P['sfx']
    rows = ''.join(f'<div style="display: flex; justify-content: space-between; gap: 10px; padding: 8px 0; border-bottom: 1px solid {LINE}"><span style="font-size: 13px">{a}</span><strong style="font-size: 13px; text-align: right; max-width: 150px">{b}</strong></div>' for a, b in respuestas)
    accion = cta(cambiar_href, 'Cambiar mis respuestas') if cambiar_href else link(f('H-Equipo', s), f'Cambiarlo con {P["cons"]}')
    body = f'''{root(False)}
{inner(11, '20px 16px 14px')}
{back(f('H-Equipo', s), TAG_INFO)}
{h1('Tu perfil: moderado', True, 27)}
{p(f'Tus respuestas del {P["perfil"].split("del ")[1]}. Con ellas sabemos qué te podemos recomendar y qué no. Vence en un año o cuando tu vida cambie.', 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">{rows}</div>
<div style="flex-grow: 1"></div>
{accion}
</div>
</div>'''
    write(f('H-Perfil', s), 'Tu perfil', body)

def como_funciona(P):
    s = P['sfx']
    bloques = [('Tu plan primero', 'Partimos de tus metas, no de nuestros productos. A veces tu siguiente paso no es un producto: tu colchón en tu cuenta, pagar una deuda cara o confirmar a tus beneficiarios.'),
               ('Información o recomendación', 'Tu patrimonio, tu puntaje y tu plan son información. Cuando te recomendamos un producto lo marcamos como Recomendación profesional, con su porqué, su riesgo en pesos y su costo.'),
               ('Quién te asesora', 'Una herramienta tecnológica de tu administradora de fondos, supervisada por la entidad, con tu perfil. Asesoría no independiente: te recomendamos alternativas nuestras y recibimos una comisión.'),
               ('Cuándo entra un asesor', f'Siempre que lo pidas. Y te proponemos ver con {P["cons"]} las decisiones que lo piden: aportes que solo sirven para tu pensión, traslados, tu forma de pensionarte o un retiro que te hace perder un beneficio.'),
               ('Tus permisos', 'Usamos el salario con el que cotizas porque lo autorizaste; puedes retirar ese permiso con una frase. Nada se mueve sin tu confirmación o una regla que tú fijaste.')]
    b = ''.join(f'<div style="display: flex; flex-direction: column; gap: 3px; padding: 9px 0; border-bottom: 1px solid {LINE}"><strong style="font-size: 14px">{t}</strong><span style="font-size: 13px; line-height: 1.45; color: {BODY}">{x}</span></div>' for t, x in bloques)
    body = f'''{root(False)}
{inner(10, '20px 16px 14px')}
{back(f('H-Equipo', s), tag('Reglamento de uso', GREEN, SGREEN))}
{h1('Cómo funciona tu arquitecto', True, 27)}
{p('Lo que antes era un servicio de banca privada, en tu bolsillo, con un asesor cuando la decisión lo pide.', 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">{b}</div>
<div style="flex-grow: 1"></div>
{small('El reglamento completo y la comisión de cada producto están en Mis documentos. Datos ficticios.', True)}
</div>
</div>'''
    write(f('H-ComoFunciona', s), 'Cómo funciona tu arquitecto', body)

def chat(P, pregunta, respuesta, link_href, link_txt):
    s = P['sfx']
    body = f'''{root(False)}
{inner(12, '20px 16px 10px')}
{back(f('H-Inicio', s), '<span style="font-size: 13px; font-weight: 700; color: ' + MUTED + '">Tu arquitecto · responde aquí; tu plan vive en la app</span>')}
<div style="flex-grow: 1"></div>
<div style="align-self: flex-end; max-width: 82%; background: {GREEN}; color: #FFFFFF; border-radius: 18px 18px 4px 18px; padding: 11px 14px; font-size: 14px; line-height: 1.45">{pregunta}</div>
<div style="display: flex; gap: 8px; align-items: flex-end">{avatar('A', GREEN, '#FFFFFF', 30, 12)}
<div style="max-width: 84%; background: #FFFFFF; border-radius: 18px 18px 18px 4px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px">{TAG_INFO}{p(respuesta)}
<a href="{link_href}" style="min-height: 44px; display: flex; align-items: center; font-weight: 700; font-size: 14px">{link_txt}</a></div></div>
{link(f('H-Equipo', s), avatar(P['cons_ini'], GOLD, INK, 28, 11) + f'Prefiero hablar con {P["cons"]}')}
<label for="msg" style="font-size: 0; position: absolute">Escribe tu pregunta</label>
<input id="msg" type="text" placeholder="Escribe tu pregunta" style="min-height: 48px; border-radius: 24px; border: 1px solid {LINE}; padding: 0 16px; font-family: inherit; font-size: 14px; background: #FFFFFF">
</div>
{tabbar('inicio', s)}
</div>'''
    write(f('H-Chat', s), 'Pregúntale a tu arquitecto', body)

def reglas(P, nombre, estado_ini, campos, nota, intro='Lo que dejaste andando solo, con su tope, su vigencia y su aviso. Lo pausas o lo cancelas en un toque.', pausable=True):
    s = P['sfx']
    filas = ''.join(f'<div style="display: grid; grid-template-columns: 78px minmax(0, 1fr); gap: 8px; font-size: 13px; line-height: 1.4; padding: 6px 0; border-bottom: 1px solid {LINE}"><span style="color: {MUTED}; font-weight: 700">{a}</span><span>{b}</span></div>' for a, b in campos)
    body = f'''{root(False)}
{inner(11, '20px 16px 10px')}
{back(f('H-Equipo', s), TAG_INFO)}
{h1('Mis reglas', False, 26)}
{p(intro, 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px"><strong style="font-size: 15px">{nombre}</strong><span style="font-size: 11.5px; font-weight: 700; color: {GREEN}; background: {SGREEN}; padding: 3px 8px; border-radius: 8px">{{{{estado}}}}</span></div>
{filas}
<div style="display: flex; gap: 8px; padding-top: 4px">
<button type="button" onClick="{{{{pausar}}}}" style="display: {'block' if pausable else 'none'}; flex: 1; min-height: 44px; border-radius: 12px; border: 2px solid {GREEN}; background: #FFFFFF; color: {GREEN}; font-family: inherit; font-weight: 700; font-size: 14px; cursor: pointer">{{{{botonPausa}}}}</button>
<button type="button" onClick="{{{{cancelar}}}}" style="flex: 1; min-height: 44px; border-radius: 12px; border: 2px solid {LINE}; background: #FFFFFF; color: #9A2B1E; font-family: inherit; font-weight: 700; font-size: 14px; cursor: pointer">{'Cancelar regla' if pausable else 'No la quiero'}</button>
</div></div>
{nota}
<div style="flex-grow: 1"></div>
{small('Nada se mueve sin que tú lo confirmes o lo hayas autorizado. Cada cambio te llega por correo y queda en Mis documentos.', True)}
</div>
{tabbar('equipo', s)}
</div>'''
    sc = script(f"{{ estado: '{estado_ini}' }}", extra=(
        "estado: s.estado, botonPausa: s.estado === 'En pausa' ? 'Reanudar' : 'Pausar', "
        f"pausar: function () {{ self.setState({{ estado: s.estado === 'En pausa' ? '{estado_ini}' : 'En pausa' }}); }}, "
        "cancelar: function () { self.setState({ estado: 'Cancelada' }); }"))
    write(f('H-Reglas', s), 'Mis reglas', body, sc)

# ======================= LAURA =======================
set_momento('Laura · 15 de junio · vuelve')
inicio(L, '$90,4 M', 'Pensión $78 M · Cesantías $9,4 M · Ahorro $3,0 M', '535',
       'Tu prima llega en 15 días',
       'Preparé tu revisión de junio: cómo vas desde tu plan del 1 de junio y una propuesta para tu prima. Tú decides; te toma 2 minutos.',
       'Ver mi revisión de junio', 'H-Revision.dc.html',
       [('Colchón de 3 meses', 40, 'Lo primero', WARN, SAMBER, AMBER, 'H-Plan.dc.html'),
        ('Tu casa en 10 años', 21, 'Con brecha', WARN, SAMBER, AMBER, 'H-Meta.dc.html'),
        ('Tu pensión a los 57', 77, 'Con brecha', WARN, SAMBER, AMBER, 'H-Plan.dc.html'),
        ('Proteger a tu hija', 50, 'En camino', GREEN, SGREEN, GREEN, 'H-Plan.dc.html')])

pilares(L, '535', [('Colchón', 40, 'Cubres 1,2 meses; lo sano son 3'), ('Suficiencia', 55, 'Vas para $2,3 M; tu meta, $3,0 M'),
                   ('Protección', 44, 'Tu hija ya es tu beneficiaria; falta revisar tu seguro de vida'), ('Riesgo a la medida', 70, 'Tu pensión va en el fondo para tu edad'),
                   ('Eficiencia', 62, 'Comisión de 1,2% al año (ficticia); cesantías con meta'), ('Constancia', 50, 'Aportas sin falta a tu pensión; tus primas aún no tienen meta')],
        'llevar tu colchón a 3 meses. Si separas para él la mayor parte de tu prima de junio, tu puntaje sube a unos 575 (estimado).',
        'H-Revision.dc.html', 'Ver mi revisión de junio')

revision(L, 'Tu revisión de junio', 'Preparada para Laura · 15 de junio',
         ['Tu colchón cubre 1,2 meses de gastos; lo sano son 3.', 'Tu casa va en 21%: $9,4 M de tus $45 M. Solo con tus primas llegarías hacia 2040, no en 10 años.', 'Tu pensión va para unos $2,3 M de los $3,0 M que quieres (estimado).', 'Tu hija ya es tu beneficiaria: lo hiciste el 1 de junio.'],
         ['El 30 de junio llega tu prima, unos $2.600.000 (estimado con tu salario de cotización).'],
         ['<strong>1.</strong> Separa $1.820.000, el 70%, para tu colchón en tu cuenta de ahorros. Es un paso de tu plan, no un producto.',
          '<strong>2.</strong> Pon $780.000, el 30%, a tu casa. Para eso te hago una recomendación profesional, con su porqué, su riesgo y su costo: la ves en el siguiente paso.'],
         'invertir para tu pensión. Tu casa sí avanza porque es tu meta más importante, su plazo es de 10 años y solo usa el 30% de la prima. Tu pensión la vemos en diciembre, con tu colchón más completo.',
         'H-Decision.dc.html', 'Ver mi propuesta')

SUP_L = ('Estimado con tu salario de cotización de hoy, cotizando hasta los 57 y una rentabilidad real supuesta de 4% al año, neta de comisiones. '
         'Tienes unas 730 semanas cotizadas: si sigues cotizando, llegas a 750 antes del 1 de abril de 2027 y conservarías las reglas de hoy (régimen de transición de la reforma pensional). '
         'Supone 13 mesadas al año durante 30 años. Lo confirmamos con tu historia laboral. No es una promesa ni una rentabilidad garantizada; algunos años puede ser negativa.')
plan(L, 'Vas para unos <strong style="color: #FFFFFF">$2,3 M al mes</strong> a los 57 (estimado); quieres <strong style="color: #FFFFFF">$3,0 M</strong>. Te faltan unos $0,7 M.' + bar(77, GOLD, '#2C4A41', 8), SUP_L,
     meta_row('Colchón de 3 meses', 'Lo primero', 'Tienes $3,0 M de $7,5 M · en tu cuenta de ahorros', 40, WARN, 'a') +
     meta_row('Tu casa en 10 años', 'Con brecha', '$45 M · llevas $9,4 M · a tiempo con unos $100 mil más al mes', 21, WARN, 'a', 'H-Meta.dc.html') +
     meta_row('Proteger a tu hija', 'En camino', 'Beneficiaria confirmada · falta revisar tu seguro de vida', 50, GREEN, 'g'),
     f'''<div style="background: #FFFFFF; border-radius: 18px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; gap: 10px"><span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 13.5px">¿Sumamos la educación de tu hija?</strong><span style="font-size: 12px; color: {MUTED}">No la elegiste; tiene 8 años.</span></span><button type="button" onClick="{{{{sumar}}}}" style="min-height: 44px; padding: 0 12px; border-radius: 12px; border: 2px solid {GREEN}; background: #FFFFFF; color: {GREEN}; font-family: inherit; font-weight: 700; font-size: 13px; cursor: pointer; flex-shrink: 0">{{{{sumarTxt}}}}</button></div>''',
     [('30 jun', 'Prima de mitad de año', '$2,6 M'), ('20 dic', 'Prima de fin de año', '$2,6 M'), ('31 ene', 'Intereses de tus cesantías', '$624 mil'), ('14 feb', 'Tu empresa consigna tus cesantías', '$5,2 M')])
# plan de Laura con el botón de sugerencia
import re as _re
_p = open(f'{sys.argv[1]}/H-Plan.dc.html', encoding='utf-8').read()
_p = _p.replace(EMPTY, script("{ sumada: false }", extra="sumar: function () { self.setState({ sumada: true }); }, sumarTxt: s.sumada ? 'En tu próxima revisión' : 'Sumarla'"))
open(f'{sys.argv[1]}/H-Plan.dc.html', 'w', encoding='utf-8').write(_p)

patrimonio(L, '$90,4 M', [('Pensión', 86.3, INK), ('Cesantías', 10.4, GREEN), ('Ahorro', 3.3, WARN)],
           [('Pensión obligatoria', '$78 M · 14 años cotizados', 's'), ('Cesantías', '$9,4 M · cuentan para tu casa', 's'),
            ('Ahorro e inversión', '$3,0 M en tu cuenta de ahorros', 'c'), ('Vivienda', 'En arriendo · meta: tu casa en 10 años', 'c'),
            ('Deudas', 'Tarjeta que pagas completa; sin deudas caras', 'c'), ('Protección de tu familia', 'Tu hija, beneficiaria · seguro de vida por revisar', 'p'),
            ('Impuestos', 'No pagas renta; si debes declarar depende de tus ingresos del año', 'e'), ('Legado', 'Tu hija es tu beneficiaria · lo demás, por conversar', 'p')])

equipo(L, ['Siempre que lo pidas', 'Aportes que solo sirven para tu pensión', 'Traslados y tu forma de pensionarte', 'Un retiro que te hace perder un beneficio'])
perfil(L, [('1 · Tu horizonte', 'Más de 5 años'), ('2 · Tus objetivos', 'Que crezca para mi meta'), ('3 · Tu conocimiento', 'Lo básico'),
           ('4 · Tu experiencia', 'Nunca, además de pensión y cesantías'), ('5 · Cuánto puedes perder', 'Hasta 15 de cada 100 pesos'), ('6 · Cómo reaccionas', 'Espero')],
       'H-PerfilCambiar.dc.html')
body = f'''{root(True, 1420)}
{back('H-Perfil.dc.html', TAG_INFO)}
{h1('Actualiza tu perfil', True, 27)}
{p('Lunes 15 de junio. Cambia lo que ya no sea cierto: tu plan y lo que te podemos recomendar se ajustan.', 13.5)}
{perfil_cards()}
<div style="flex-grow: 1"></div>
{cta('H-Perfil.dc.html', 'Guardar mi perfil')}
</div>'''
write('H-PerfilCambiar.dc.html', 'Actualiza tu perfil', body, perfil_script(), h=1420)
como_funciona(L)
chat(L, '¿Puedo usar mis cesantías para la cuota inicial de mi casa?',
     'Sí. Tus cesantías se pueden usar para tu vivienda; si las usas, dejan de ser tu respaldo si pierdes el empleo. Por eso en tu plan tu colchón va aparte. Hoy tienes $9,4 M y ya cuentan para tu casa.',
     'H-Meta.dc.html', 'Ver tu casa en tu plan')
reglas(L, 'Prima con rumbo', 'Activa',
       [('Cuando', 'Llegue tu prima (próxima: diciembre)'), ('Qué hago', '70% a tu colchón, en tu cuenta, hasta llegar a 3 meses; 30% a tu casa'),
        ('Tope', '$1.000.000 a inversión por prima'), ('Vigencia', 'Hasta junio de 2027'), ('Aviso', 'Un día antes, con opción de saltar esa vez'), ('Control', 'Te propongo y tú confirmas')],
       f'<div style="background: {SAMBER}; border-radius: 16px; padding: 12px 14px; font-size: 13px; line-height: 1.45"><strong>Te puede servir:</strong> en enero te llegan los intereses de tus cesantías, unos $624.000. En tu revisión de enero te propongo su rumbo.</div>')

# ---------- H-Meta (Laura, casa) ----------
body = f'''{root(False)}
{inner(11, '20px 16px 12px')}
{back('H-Plan.dc.html', TAG_INFO)}
<div style="background: {SGREEN}; border-radius: 22px; padding: 16px; display: flex; flex-direction: column; gap: 9px">
<div style="display: flex; align-items: center; gap: 12px">
<span aria-hidden="true" style="width: 46px; height: 46px; border-radius: 14px; background: #FFFFFF; display: flex; align-items: center; justify-content: center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path></svg></span>
<div style="display: flex; flex-direction: column">{h1('Tu casa', False, 24)}<span style="font-size: 13px; color: {BODY}">Cuota inicial de $45 M en 10 años · la que elegiste</span></div></div>
<div style="display: flex; justify-content: space-between; font-size: 13px"><span><strong>$9,4 M</strong> llevas</span><strong>21%</strong></div>
{bar(21, GREEN, '#FFFFFF', 10)}
</div>
{card('<strong style="font-size: 14px">Con qué la estás construyendo</strong>' + row('Tus cesantías de hoy', '$9,4 M') + row('30% de cada prima, si apruebas tu propuesta', '$780 mil') + small('Tus cesantías se pueden usar para tu vivienda; si las usas, dejan de ser tu respaldo si pierdes el empleo. Por eso tu colchón va aparte.'), gap=6)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 9px">
<strong style="font-size: 14px">¿Y si además separas cada mes…?</strong>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px">
<sc-for list="{{{{montos}}}}" as="m" hint-placeholder-count="4"><button type="button" aria-pressed="{{{{m.on}}}}" onClick="{{{{m.pick}}}}" style="{{{{m.style}}}}">{{{{m.label}}}}</button></sc-for>
</div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 16px; padding: 12px 14px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 12px; color: #B8CCC4">Si rinde 4% real al año</span><span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px; font-weight: 700">{{{{anio}}}}</span></span>
<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 12px; color: #B8CCC4">Si los mercados van mal (0%)</span><span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 26px; font-weight: 700; color: {GOLD}">{{{{anioMalo}}}}</span></span>
<span style="grid-column: 1 / 3; font-size: 12px; color: #DCE6E2">{{{{lectura}}}}</span>
</div>
{small('Rentabilidades supuestas, netas de comisiones. Cuenta tus cesantías de hoy y tus primas; no tus cesantías futuras. No es una promesa ni una rentabilidad garantizada; algunos años puede ser negativa.')}
</div>
<div style="flex-grow: 1"></div>
{cta('H-Revision.dc.html', 'Ver mi revisión de junio', 50)}
</div>
</div>'''
meta_script = '''class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { mensual: 100000 };
}
anios(m, tasa) {
var b = 9400000, r = Math.pow(1 + tasa, 1 / 12) - 1, meses = 0;
while (b < 45000000 && meses < 600) {
b = b * (1 + r) + m;
if (meses % 12 === 5 || meses % 12 === 11) { b += 780000; }
meses++;
}
return meses / 12;
}
renderVals() {
var self = this, m = this.state.mensual;
var t = this.anios(m, 0.04), tm = this.anios(m, 0);
return {
montos: [0, 100000, 200000, 300000].map(function (v) {
var sel = v === m;
return { label: v === 0 ? '$0' : '$' + (v / 1000) + ' mil', on: sel ? 'true' : 'false', pick: function () { self.setState({ mensual: v }); },
style: 'min-height: 44px; border-radius: 12px; font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; border: 2px solid ' + (sel ? '#0E6A4E' : '#E7E2D6') + '; background: ' + (sel ? '#E3EFEA' : '#FFFFFF') + '; color: #12241F' };
}),
anio: String(2026 + Math.ceil(t)),
anioMalo: String(2026 + Math.ceil(tm)),
lectura: t <= 10 ? 'Con 4% llegas dentro de los 10 años que te pusiste; en un mal escenario, más tarde.' : 'Después de los 10 años que te pusiste: con un poco más al mes llegas a tiempo.'
};
}
}'''
write('H-Meta.dc.html', 'Tu casa', body, meta_script)

# ---------- H-Decision (Laura) ----------
def decision(P, back_href, titulo, pendiente_html, listo_html, aprobar_txt, nota, entiendo=None):
    s = P['sfx']
    chk = (f'<label style="display: flex; gap: 10px; align-items: center; min-height: 44px; font-size: 13px; line-height: 1.35; cursor: pointer"><input type="checkbox" onChange="{{{{toggle}}}}" style="width: 22px; height: 22px; accent-color: {GREEN}; flex-shrink: 0">{entiendo}</label>') if entiendo else ''
    body = f'''{root(False)}
{inner(10, '20px 16px 12px')}
{back(back_href, TAG_REC)}
<sc-if value="{{{{pendiente}}}}" hint-placeholder-val="{{{{ true }}}}">
<div style="display: flex; flex-direction: column; gap: 10px">
{h1(titulo, True, 26)}
{pendiente_html}
{chk}
<button type="button" onClick="{{{{aprobar}}}}" aria-disabled="{{{{bloqueado}}}}" style="min-height: 52px; border: 0; border-radius: 14px; background: {{{{btnBg}}}}; color: #FFFFFF; font-family: inherit; font-weight: 700; font-size: 16px; cursor: pointer">{aprobar_txt}</button>
{small(nota, True)}
</div>
</sc-if>
<sc-if value="{{{{listo}}}}" hint-placeholder-val="{{{{ false }}}}">
<div style="display: flex; flex-direction: column; gap: 11px">
{listo_html}
</div>
</sc-if>
</div>
</div>'''
    ok0 = 'false' if entiendo else 'true'
    sc = ('class Component extends DCLogic {\nconstructor(props) {\nsuper(props);\nthis.state = { listo: false, ok: ' + ok0 + ' };\n}\nrenderVals() {\nvar self = this, s = this.state;\n'
          "return { pendiente: !s.listo, listo: s.listo, bloqueado: s.ok ? 'false' : 'true', btnBg: s.ok ? '#0E6A4E' : '#7C8A85', "
          'toggle: function () { self.setState({ ok: !s.ok }); }, aprobar: function () { if (s.ok) { self.setState({ listo: true }); } } };\n}\n}')
    write(f('H-Decision', s), titulo, body, sc)

TRANSP_L = details('Quién te asesora y cuánto cuesta', 'Recomendación de tu administradora de fondos hecha por una herramienta que la entidad supervisa, con tu perfil del 1 de junio. Lo retiras cuando quieras, en pocos días hábiles; su valor puede variar. Asesoría no independiente: recibimos una comisión de 1,2% al año (ficticia). Otras opciones: tu cuenta de ahorros, un certificado de depósito a término o fondos de otras entidades. Te enviamos esta recomendación a tu correo y queda en Mis documentos.')
check = f'<span aria-hidden="true" style="width: 60px; height: 60px; border-radius: 30px; background: {SGREEN}; display: flex; align-items: center; justify-content: center"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"></path></svg></span>'
decision(L, 'H-Revision.dc.html', 'Tu propuesta para la prima',
    f'''<div style="background: {SGREEN}; border-radius: 18px; padding: 12px 16px; display: flex; flex-direction: column; gap: 4px">
<div style="display: flex; justify-content: space-between; gap: 8px"><strong style="font-size: 15px">$1.820.000 a tu colchón</strong><span style="font-size: 11.5px; font-weight: 700; color: {GREEN}; text-align: right">PASO DEL PLAN · NO ES UN PRODUCTO</span></div>
<span style="font-size: 13px; line-height: 1.45; color: {BODY}">Sepáralo en tu cuenta de ahorros. Pasas de 1,2 a 1,9 meses de colchón.</span></div>
<div style="background: #FFFFFF; border-radius: 18px; padding: 12px 16px; display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; justify-content: space-between; gap: 8px"><strong style="font-size: 15px">$780.000 a tu casa</strong><span style="font-size: 11.5px; font-weight: 700; color: {AMBER}; text-align: right">FONDO DE INVERSIÓN COLECTIVA · MODERADO</span></div>
<span style="font-size: 13px; line-height: 1.45; color: {BODY}"><strong>Por qué:</strong> tu casa es tu meta más importante, es a 10 años y tu perfil es moderado: con ese plazo puedes esperar las bajas.</span>
<span style="font-size: 13px; background: {SAMBER}; border-radius: 10px; padding: 8px 10px; line-height: 1.4"><strong>En un mal año</strong> esta parte podría bajar unos $94.000 (estimado con una caída de 12%). Por eso tu colchón no va ahí.</span>
{TRANSP_L}</div>
<a href="H-Equipo.dc.html" style="background: #FFFFFF; border-radius: 18px; padding: 10px 14px; display: flex; align-items: center; gap: 12px; text-decoration: none; color: {INK}; min-height: 44px">{avatar('DR', GOLD, INK, 38, 13)}<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 14px">¿Lo vemos con Daniela?</strong><span style="font-size: 12.5px; color: {MUTED}">15 minutos por video, con tu plan a la vista</span></span></a>''',
    f'''{check}
{h1('Listo, Laura. Tu prima ya tiene rumbo.', True, 27)}
{p('El 30 de junio, cuando llegue, te pido confirmar antes de mover cualquier peso. Tu colchón pasa a 1,9 meses y tu puntaje a unos 575 (estimado).', 15)}
{card(p('¿Quieres que en diciembre te lo proponga igual, con aviso un día antes? Lo pausas o lo cancelas cuando quieras.', 14, INK), gap=4)}
{cta('H-Reglas.dc.html', 'Sí, déjalo como regla', 50)}
{link('H-Inicio.dc.html', 'No por ahora, volver a mi inicio')}
{small('Te enviamos el resumen a tu correo y queda en Mis documentos.', True)}''',
    'Aprobar con mi huella', 'Aprobar no mueve dinero: el 30 de junio te pido confirmar.')

# ======================= JULIANA =======================
set_momento('Juliana · 23 de noviembre')
inicio(J, '$257 M', 'Pensión $185 M · Pensión voluntaria $24 M · Ahorro $34 M · Cesantías $14 M', '640',
       'Cierre de año: tu casa y tu impuesto',
       'Tu casa en la costa va en 27%. Preparé tu revisión de cierre de año: cómo vas y una propuesta para tu prima de diciembre que avanza tu casa y, como pagas renta, también baja tu impuesto. Las condiciones van con la propuesta.',
       'Ver mi revisión de cierre de año', 'H-RevisionJuliana.dc.html',
       [('Colchón de 4 meses', 100, 'Completo', GREEN, SGREEN, GREEN, 'H-PlanJuliana.dc.html'),
        ('Casa en la costa a los 55', 27, 'En camino', GREEN, SGREEN, GREEN, 'H-PlanJuliana.dc.html'),
        ('Tu pensión a los 57', 60, 'Con brecha', WARN, SAMBER, AMBER, 'H-PlanJuliana.dc.html')])

pilares(J, '640', [('Colchón', 100, '4 meses de gastos, separado y disponible'), ('Suficiencia', 60, 'Vas para $3,0 M; tu meta, $5,0 M'),
                   ('Protección', 70, 'Beneficiarios confirmados; seguro de vida con tu empresa'), ('Riesgo a la medida', 65, 'Tu casa y tu pensión, según tu perfil moderado'),
                   ('Eficiencia', 48, 'Te faltan $6,65 M para tu punto óptimo de este año'), ('Constancia', 41, 'Aportas para tu casa solo a fin de año')],
        'completar el aporte de este año para tu casa y aportar cada mes. Con las dos cosas, tu puntaje sube a unos 733 (estimado).',
        'H-RevisionJuliana.dc.html', 'Ver mi revisión de cierre de año')

revision(J, 'Tu revisión de cierre de año', 'Preparada para Juliana · 23 de noviembre',
         ['Tu colchón está completo: 4 meses.', 'Tu casa en la costa va en 27%: $24 M de tus $90 M.', 'Tu pensión va para unos $3,0 M de los $5,0 M que quieres (estimado): es tu brecha más grande.'],
         ['A más tardar el 20 de diciembre llega tu prima, unos $4.250.000.', 'Este año aportaste $6,0 M a tu pensión voluntaria; tu punto óptimo es $12,65 M.'],
         ['<strong>1.</strong> Completa $6,65 M para tu casa antes del 31 de diciembre: tu prima y $2,40 M de tu ahorro por encima de tu colchón. Es una recomendación profesional, con su beneficio y su condición: la ves en el siguiente paso.',
          '<strong>2.</strong> Tu colchón no se toca.'],
         'cómo cerrar la brecha de tu pensión. Es una decisión que solo sirve para tu pensión: la vemos con Camilo en enero. El aporte de este año no compite: vence el 31 de diciembre y también puede ir a tu pensión.',
         'H-ImpuestoJuliana.dc.html', 'Ver cómo cambia mi impuesto')

# ---------- H-ImpuestoJuliana ----------
cmp = ''.join(f'<div style="display: flex; justify-content: space-between; font-size: 13.5px; padding: 7px 0; border-bottom: 1px solid {LINE}"><span>{a}</span><strong>{b}</strong></div>' for a, b in [('Si no hubieras aportado', '$3,59 M'), ('Con los $6,0 M que llevas', '$2,74 M'), ('Si completas $12,65 M al 31 de diciembre', '$1,79 M')])
body = f'''{root(False)}
{inner(11, '20px 16px 12px')}
{back('H-RevisionJuliana.dc.html', TAG_INFO)}
{h1('Tu impuesto de 2026, con y sin tu casa', True, 26)}
{p('Pagas renta y declaras: tus ingresos del año superan el tope para declarar. Este es tu impuesto estimado:', 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 4px 16px">{cmp}</div>
<div style="background: {SGREEN}; border-radius: 18px; padding: 12px 16px; font-size: 14px; line-height: 1.45">Por cada $100 que aportes hasta tu punto óptimo, pagas unos <strong>$14 menos</strong> de impuesto (estimado).</div>
{card('<strong style="font-size: 14px">La condición, antes que el beneficio</strong>' + p('El beneficio se conserva si dejas cada aporte 10 años, o lo usas para tu vivienda o tu pensión. Si lo retiras antes para otra cosa, ese retiro suma a tus ingresos del año y te retenemos el 7% al retirarlo.', 13), gap=5)}
{details('Supuestos de este cálculo', 'Salario de $8.500.000 y prima, sin dependientes ni otras deducciones, cesantías exentas, unidad de valor tributario de 2026 de $52.374. Es un estimado: si tienes otros ingresos, deducciones o dependientes, cambia. Es un cálculo informativo, no asesoría tributaria; si tu caso es complejo, lo ves con Camilo.')}
<div style="flex-grow: 1"></div>
{cta('H-DecisionJuliana.dc.html', 'Ver mi propuesta')}
</div>
</div>'''
write('H-ImpuestoJuliana.dc.html', 'Tu impuesto de 2026', body)

TRANSP_J = details('Quién te asesora y cuánto cuesta', 'Recomendación de tu administradora de fondos hecha por una herramienta que la entidad supervisa, con tu perfil del 3 de marzo. Asesoría no independiente: recibimos una comisión de 1,2% al año (ficticia). Otras opciones: una cuenta de ahorro para el fomento a la construcción en un banco, o fondos de otras entidades. Te enviamos esta recomendación a tu correo y queda en Mis documentos.')
regla_j = ''.join(f'<div style="display: grid; grid-template-columns: 66px minmax(0, 1fr); gap: 8px; font-size: 12.5px; line-height: 1.35; padding: 3px 0"><span style="color: {MUTED}; font-weight: 700">{a}</span><span>{b}</span></div>' for a, b in [
    ('Cuando', 'Cada pago de nómina, desde enero de 2027'), ('Qué', 'Tu empresa descuenta $1.060.000 y lo aporta a tu pensión voluntaria para tu casa'),
    ('Ganas', 'Te retiene unos $151.000 menos al mes (estimado)'), ('Tope', 'Tu punto óptimo de 2027; si tu salario cambia, te propongo el nuevo monto y tú confirmas'),
    ('Vigencia', 'Hasta diciembre de 2027; entonces te pregunto si la renuevas'), ('Aviso', 'Cada mes, el día de pago, te cuento cuánto se aportó'),
    ('Control', 'Tú firmas la autorización ante tu empresa; yo solo te la preparo. La cambias o la cancelas cuando quieras')])
decision(J, 'H-ImpuestoJuliana.dc.html', 'Cierra tu año con tu casa',
    f'''<div style="background: #FFFFFF; border-radius: 18px; padding: 12px 16px; display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; justify-content: space-between; gap: 8px"><strong style="font-size: 15px">$6,65 M a tu casa</strong><span style="font-size: 11.5px; font-weight: 700; color: {AMBER}; text-align: right">PENSIÓN VOLUNTARIA · PORTAFOLIO MODERADO</span></div>
<span style="font-size: 13px; color: {BODY}">$4,25 M de tu prima (a más tardar el 20 de diciembre) y $2,40 M de tu ahorro, sin tocar tu colchón.</span>
<span style="font-size: 13px; line-height: 1.45; color: {BODY}"><strong>Por qué:</strong> avanza tu casa a 34% y, si queda acreditado a más tardar el 31 de diciembre, pagas unos $950.000 menos de renta (estimado).</span>
<span style="font-size: 12.5px; line-height: 1.4; color: {BODY}"><strong>Condición:</strong> el beneficio se conserva si dejas cada aporte 10 años, o lo usas para tu vivienda o tu pensión. Si lo retiras antes para otra cosa, ese retiro suma a tus ingresos del año y te retenemos el 7% al retirarlo. Que el retiro para una segunda vivienda conserve el beneficio está por validar con el experto tributario.</span>
<span style="font-size: 12.5px; background: {SAMBER}; border-radius: 10px; padding: 7px 10px; line-height: 1.4"><strong>En un mal año</strong> esta parte podría bajar unos $800.000 (estimado con una caída de 12%). Por eso tu colchón no va ahí.</span>
{TRANSP_J}</div>''',
    f'''<div style="display: flex; gap: 12px; align-items: center">{check}{h1('Listo, Juliana.', True, 26)}</div>
{p('Cuando tu aporte quede acreditado, llegas a tu punto óptimo; te lo confirmamos antes del 31.', 14)}
<div style="background: #FFFFFF; border-radius: 18px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 14px">¿Y si el próximo año no esperas a diciembre?</strong>{regla_j}</div>
{cta('H-ReglasJuliana.dc.html', 'Prepárame la autorización', 50)}
{link('H-EquipoJuliana.dc.html', avatar('CV', GOLD, INK, 28, 11) + 'Ver el aporte a mi pensión obligatoria con Camilo')}''',
    'Confirmar con mi huella', 'Confirmar no mueve dinero de otra cuenta: te pido cada transferencia. Te enviamos la recomendación a tu correo.',
    entiendo='Entiendo la condición del beneficio y que el cálculo es un estimado.')

SUP_J = ('Estimado con tu salario de cotización de hoy, cotizando hasta los 57 y una rentabilidad real supuesta de 4% al año, neta de comisiones. '
         'Con tus 18 años cotizados superas las 750 semanas: conservarías las reglas de hoy (régimen de transición de la reforma pensional, que rige desde el 1 de abril de 2027). '
         'Supone 13 mesadas al año durante 30 años. Lo confirmamos con tu historia laboral. No es una promesa ni una rentabilidad garantizada; algunos años puede ser negativa.')
plan(J, 'Vas para unos <strong style="color: #FFFFFF">$3,0 M al mes</strong> a los 57 (estimado); quieres <strong style="color: #FFFFFF">$5,0 M</strong>. Te faltan unos $2,0 M: la vemos con Camilo en enero.' + bar(60, GOLD, '#2C4A41', 8), SUP_J,
     meta_row('Colchón de 4 meses', 'Completo', '$20 M de tu ahorro, separado y disponible', 100, GREEN, 'g') +
     meta_row('Casa en la costa a los 55', 'En camino', '$90 M · llevas $24 M en tu pensión voluntaria', 27, GREEN, 'g', 'H-RevisionJuliana.dc.html') +
     meta_row('Tu pensión con $5,0 M al mes', 'Con brecha', 'Te faltan unos $2,0 M al mes (estimado) · la ves con Camilo en enero', 60, WARN, 'a'),
     '',
     [('20 dic', 'Prima de fin de año', '$4,25 M'), ('31 dic', 'Último día para que tu aporte cuente en 2026', ''), ('31 ene', 'Intereses de tus cesantías', '$1,02 M'), ('14 feb', 'Tu empresa consigna tus cesantías', '$8,5 M')])

patrimonio(J, '$257 M', [('Pensión', 72, INK), ('Pensión voluntaria', 9.3, '#3A3F7A'), ('Ahorro', 13.2, WARN), ('Cesantías', 5.5, GREEN)],
           [('Pensión obligatoria', '$185 M · 18 años cotizados', 's'), ('Pensión voluntaria', '$24 M · para tu casa en la costa', 's'),
            ('Ahorro e inversión', '$34 M: tu colchón de $20 M y $14 M más', 'c'), ('Cesantías', '$14 M', 's'),
            ('Vivienda', 'Propia, sin crédito · meta: casa en la costa', 'c'), ('Deudas', 'Ninguna', 'c'),
            ('Protección y legado', 'Beneficiarios confirmados · seguro de vida con tu empresa', 'c'), ('Impuestos', 'Pagas renta y declaras: unos $2,74 M este año', 'e')])

equipo(J, ['Siempre que lo pidas', 'Aportes que solo sirven para tu pensión, como el voluntario a tu pensión obligatoria', 'Traslados y tu forma de pensionarte', 'Un retiro que te hace perder un beneficio'])
perfil(J, [('1 · Tu horizonte', 'Más de 10 años'), ('2 · Tus objetivos', 'Mi casa y mi pensión'), ('3 · Tu conocimiento', 'Intermedio'),
           ('4 · Tu experiencia', 'Fondos y pensión voluntaria'), ('5 · Cuánto puedes perder', 'Hasta 1 de cada 10 pesos'), ('6 · Cómo reaccionas', 'Espero')])
como_funciona(J)
chat(J, '¿Y si necesito esa plata antes de 10 años?',
     'Siempre puedes retirarla. Si es para tu vivienda o tu pensión, conservas el beneficio. Si la retiras antes para otra cosa, ese retiro suma a tus ingresos del año y te retenemos el 7% al retirarlo; antes de hacerlo te muestro cuánto pierdes.',
     'H-DecisionJuliana.dc.html', 'Volver a mi propuesta')
reglas(J, 'Aporte mensual para tu casa', 'Por firmar',
       [('Cuando', 'Cada pago de nómina, desde enero de 2027'), ('Qué', 'Tu empresa descuenta $1.060.000 y lo aporta a tu pensión voluntaria'),
        ('Tope', 'Tu punto óptimo de 2027'), ('Vigencia', 'Hasta diciembre de 2027'), ('Aviso', 'Cada mes, el día de pago'),
        ('Control', 'Tú firmas ante tu empresa; nosotros no ejecutamos el descuento')],
       f'<div style="background: {SAMBER}; border-radius: 16px; padding: 12px 14px; font-size: 13px; line-height: 1.45"><strong>Siguiente paso:</strong> te enviamos a tu correo la autorización lista para que la firmes y la entregues a tu empresa. Si prefieres, Camilo te ayuda.</div>',
       intro='El descuento lo hace tu empresa con la autorización que tú firmas. Para cancelarlo después, revocas esa autorización ante tu empresa; te preparamos la carta en una frase.', pausable=False)
print('app ok')
