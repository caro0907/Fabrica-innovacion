"""v5.1 · Primero te conozco (Laura, 1 de junio) y Tu plan de primera vez."""
import sys
from pantallas_asesoria import *
set_out(sys.argv[1])

def chipcard(title, key, sub='', col=False):
    s = small(sub) if sub else ''
    return card(f'<strong style="font-size: 15px">{title}</strong>{s}{chips(key, col)}', gap=9)

# ---------- D1 Bienvenida ----------
sab = ''.join(row(a, b) for a, b in [('Tu pensión obligatoria', '$78 M · 14 años cotizados'), ('Tus cesantías', '$9,4 M'), ('Tu salario de cotización', 'unos $5,2 M al mes'), ('Tus primas', 'junio y diciembre')])
agenda = ['Lo que quieres lograr, con números', 'Tu vida y tu dinero hoy', 'Cómo te sientes con el riesgo', 'Lo que entendí de ti']
ag = ''.join(f'<div style="display: flex; gap: 10px; align-items: center; font-size: 14px"><span style="width: 26px; height: 26px; border-radius: 13px; background: {SGREEN}; color: {GREEN}; font-weight: 700; font-size: 13px; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{k+1}</span>{t}</div>' for k, t in enumerate(agenda))
body = f'''{root()}
<div style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 12px; font-weight: 600; color: {MUTED}">Lunes 1 de junio · datos ficticios</span><span style="display: flex">{avatar('A', GREEN)}<span style="margin-left: -10px; display: flex">{avatar('DR', GOLD, INK)}</span></span></div>
{h1('Laura, armemos tu plan como en una primera reunión con tu asesor', size=29)}
{p('Así empieza una buena asesoría: primero tu vida, después los productos, y solo si te sirven. Son cuatro temas y unos 7 minutos.')}
{card('<strong style="font-size: 15px">Lo que ya sabemos, para no preguntártelo</strong>' + small('Lo usamos porque nos autorizaste. Si algo no está bien, lo corriges al final.') + sab, gap=6)}
{card('<strong style="font-size: 15px">De qué vamos a hablar</strong>' + ag, gap=9)}
<div style="flex-grow: 1"></div>
{cta('D2-Metas.dc.html', 'Empecemos')}
{link('H-Equipo.dc.html', avatar('DR', GOLD, INK, 28, 11) + 'Prefiero hacerla con Daniela por video')}
</div>'''
write('D1-Bienvenida.dc.html', 'Tu primera reunión', body)

# ---------- D2 Metas y prioridad ----------
METAS = ['Tener tranquilidad', 'Comprar mi casa', 'Educar a mis hijos', 'Pensionarme bien', 'Salir de deudas', 'Viajar', 'Emprender']
body = f'''{root()}
{top('D1-Bienvenida.dc.html', 1, 4)}
{h1('¿Qué te gustaría lograr en los próximos años?')}
{p('Elige las que sean tuyas. En la siguiente pantalla les ponemos fecha y números.')}
{chipcard('Tus metas', 'metas')}
{chipcard('¿Cuál es la más importante para ti?', 'prioridad', 'Por esa empezamos tu plan.')}
<div style="flex-grow: 1"></div>
{cta('D2b-Numeros.dc.html', 'Siguiente')}
</div>'''
d2 = script("{ metas: ['Tener tranquilidad', 'Comprar mi casa', 'Pensionarme bien'], prioridad: 'Comprar mi casa' }",
            [('metas', METAS, True, False)],
            extra="prioridad: s.metas.map(function (o) { var on = s.prioridad === o; return { label: o, on: on ? 'true' : 'false', style: st(on, false), pick: function () { self.setState({ prioridad: o }); } }; })")
write('D2-Metas.dc.html', 'Tus metas', body, d2)

# ---------- D2b Números de las metas ----------
body = f'''{root()}
{top('D2-Metas.dc.html', 1, 4)}
{h1('Pongámosle números a tus metas', size=27)}
{p('Te propongo una cifra para empezar. Muévela hasta que se parezca a lo que quieres.')}
{chipcard('Tu casa, ¿para cuándo?', 'plazo')}
{slider('casa', 'Tu cuota inicial', 10000000, 150000000, 5000000, 'Te propongo $45 M: el 30% de una vivienda de $150 M.')}
{slider('pension', 'Tu pensión, ¿con cuánto al mes quieres vivir?', 1800000, 6000000, 100000, 'Te propongo $3,0 M: unos 6 de cada 10 pesos de tu salario de hoy.')}
{small('Tu tranquilidad la calculamos con tus gastos, en el siguiente tema.')}
<div style="flex-grow: 1"></div>
{cta('D3-Vida.dc.html', 'Siguiente')}
</div>'''
write('D2b-Numeros.dc.html', 'Tus metas con números', body,
      script("{ plazo: 'En 10 años', casa: 45000000, pension: 3000000 }", [('plazo', ['En 3 años', 'En 5 años', 'En 10 años', 'Más de 10'], False, False)], ['casa', 'pension']))

# ---------- D3 Vida ----------
body = f'''{root()}
{top('D2b-Numeros.dc.html', 2, 4)}
{h1('Cuéntame de tu vida hoy')}
{chipcard('¿Alguien depende de ti?', 'depende')}
<sc-if value="{{{{conHija}}}}" hint-placeholder-val="{{{{ true }}}}">
<div style="background: #FFFFFF; border-radius: 20px; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; gap: 10px">
<span style="display: flex; flex-direction: column; gap: 2px"><strong style="font-size: 15px">¿Qué edad tiene?</strong><span style="font-size: 12px; color: {MUTED}">Solo eso: para su educación y para protegerla.</span></span>
<span style="display: flex; align-items: center; gap: 6px">
<button type="button" aria-label="Menos" onClick="{{{{menos}}}}" style="width: 44px; height: 44px; border-radius: 22px; border: 2px solid {LINE}; background: #FFFFFF; font-size: 20px; font-weight: 700; color: {INK}; cursor: pointer">−</button>
<strong style="font-size: 17px; min-width: 64px; text-align: center">{{{{edadTxt}}}}</strong>
<button type="button" aria-label="Más" onClick="{{{{mas}}}}" style="width: 44px; height: 44px; border-radius: 22px; border: 2px solid {LINE}; background: #FFFFFF; font-size: 20px; font-weight: 700; color: {INK}; cursor: pointer">+</button>
</span></div>
</sc-if>
{chipcard('¿Dónde vives?', 'vivienda')}
{chipcard('¿Tienes deudas?', 'deudas', '', True)}
<div style="flex-grow: 1"></div>
{cta('D3b-Dinero.dc.html', 'Siguiente')}
</div>'''
write('D3-Vida.dc.html', 'Tu vida hoy', body, script(
    "{ depende: 'Mi hija', edad: 8, vivienda: 'En arriendo', deudas: 'Tarjeta que pago completa' }",
    [('depende', ['Nadie', 'Mi hija', 'Hijos', 'Mis padres'], False, False),
     ('vivienda', ['En arriendo', 'Con mi familia', 'Propia', 'Con crédito'], False, False),
     ('deudas', ['No tengo', 'Tarjeta que pago completa', 'Tarjeta o crédito que pago a cuotas'], False, True)],
    extra="conHija: s.depende === 'Mi hija' || s.depende === 'Hijos', edadTxt: s.edad + ' años', menos: function () { self.setState({ edad: Math.max(0, s.edad - 1) }); }, mas: function () { self.setState({ edad: Math.min(25, s.edad + 1) }); }"))

# ---------- D3b Dinero ----------
body = f'''{root()}
{top('D3-Vida.dc.html', 2, 4)}
{h1('Y tu dinero, más o menos')}
{p('No necesitas cifras exactas. Con esto vemos tu tranquilidad.')}
{slider('gastos', '¿Cuánto gastas al mes?', 1000000, 5000000, 100000, 'Tu colchón de 3 meses sería {{colchonTxt}}.')}
{slider('ahorro', '¿Cuánto tienes ahorrado o invertido, aquí o en otras entidades?', 0, 30000000, 500000)}
{chipcard('¿Dónde está?', 'donde')}
{chipcard('¿Tienes seguro de vida?', 'seguro')}
<div style="flex-grow: 1"></div>
{cta('D4-Riesgo.dc.html', 'Siguiente')}
</div>'''
write('D3b-Dinero.dc.html', 'Tu dinero hoy', body, script(
    "{ gastos: 2500000, ahorro: 3000000, donde: ['En mi cuenta de ahorros'], seguro: 'No sé' }",
    [('donde', ['En mi cuenta de ahorros', 'En inversiones', 'En otra entidad'], True, False),
     ('seguro', ['Sí', 'No', 'No sé'], False, False)],
    ['gastos', 'ahorro'], extra='colchonTxt: fmt(s.gastos * 3)'))

# ---------- D4 Riesgo: las 6 preguntas ----------
preg = [('1 · Tu horizonte', '¿Para cuándo necesitas el dinero de tu meta?', 'En más de 5 años'),
        ('2 · Tus objetivos', '¿Qué buscas, sobre todo?', 'Que crezca para mi casa'),
        ('3 · Tu conocimiento', '¿Qué tanto sabes de inversiones?', 'Lo básico'),
        ('4 · Tu experiencia', '¿Has invertido antes?', 'Solo mi pensión y mis cesantías'),
        ('5 · Cuánto puedes perder', '¿Cuánto podría bajar en un año sin afectar tu vida?', 'Hasta 1 de cada 10 pesos')]
rows = ''.join(f'<div style="display: flex; justify-content: space-between; gap: 10px; align-items: center; padding: 7px 0; border-bottom: 1px solid {LINE}"><span style="display: flex; flex-direction: column; gap: 1px; min-width: 0"><span style="font-size: 11.5px; font-weight: 700; color: {MUTED}">{a.upper()}</span><span style="font-size: 13px">{b}</span></span><strong style="font-size: 12.5px; color: {GREEN}; text-align: right; max-width: 120px">{c}</strong></div>' for a, b, c in preg)
body = f'''{root()}
{top('D3b-Dinero.dc.html', 3, 4)}
{h1('¿Cómo te sientes con el riesgo?', size=27)}
{p('Seis preguntas, una por cada cosa que un asesor debe conocer antes de recomendarte. Tocas una para cambiar tu respuesta.', 13.5)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 4px 16px">{rows}</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 9px; border: 2px solid {GREEN}">
<span style="font-size: 11.5px; font-weight: 700; color: {MUTED}">6 · CÓMO REACCIONAS A LAS BAJAS</span>
<strong style="font-size: 15px; line-height: 1.4">Si pusieras $1.000.000 para tu casa y en un mal año bajara a $880.000, ¿qué harías?</strong>
{chips('resp', True)}
</div>
{small('No hay respuestas buenas o malas. Con esto sabemos qué te podemos recomendar y qué no; lo cambias cuando tu vida cambie.')}
<div style="flex-grow: 1"></div>
{cta('D5-Entendi.dc.html', 'Siguiente')}
</div>'''
write('D4-Riesgo.dc.html', 'Tu perfil', body, script("{ resp: 'Espero: mi meta es a 10 años' }",
      [('resp', ['Lo saco todo para no perder más', 'Espero: mi meta es a 10 años', 'Aprovecho y pongo más'], False, True)]))

# ---------- D5 Lo que entendí ----------
ent = [('Lo que quieres', 'Tu casa primero: $45 M de cuota inicial en 10 años. Pensionarte con unos $3,0 M al mes. Y tranquilidad: un colchón de 3 meses.'),
       ('Tu vida y tu dinero hoy', 'Vives en arriendo con tu hija de 8 años. Gastas unos $2,5 M al mes y tienes $3,0 M en tu cuenta de ahorros. Tu tarjeta la pagas completa.'),
       ('Tu perfil', 'Moderado: tu meta es a más de 5 años, aceptas bajas de hasta 1 de cada 10 pesos y esperas cuando el mercado baja.'),
       ('Lo que aún no sé', 'Si tienes seguro de vida. Lo revisamos en tu plan.')]
e = ''.join(f'<div style="display: flex; flex-direction: column; gap: 3px; padding: 9px 0; border-bottom: 1px solid {LINE}">{eyebrow(a)}<span style="font-size: 13.5px; line-height: 1.45">{b}</span></div>' for a, b in ent)
body = f'''{root()}
{top('D4-Riesgo.dc.html', 4, 4)}
{h1('Esto entendí de ti, Laura')}
{p('Revisa que esté bien antes de armar tu plan. Lo que corrijas cambia tus números.')}
<div style="background: #FFFFFF; border-radius: 20px; padding: 2px 16px">{e}</div>
{link('D2b-Numeros.dc.html', 'Corregir algo')}
<div style="flex-grow: 1"></div>
<div style="background: {INK}; color: #FFFFFF; border-radius: 18px; padding: 13px 16px; font-size: 13.5px; line-height: 1.5">Con esto y lo que ya sabemos de tu pensión y tus cesantías, armo tu plan: tu patrimonio, tus metas con números y el orden para lograrlas.</div>
{cta('H-TuPlan.dc.html', 'Ver mi plan')}
{small('Tus respuestas quedan como tu perfil del 1 de junio. Lo ves y lo cambias en Tu equipo.', True)}
</div>'''
write('D5-Entendi.dc.html', 'Esto entendí de ti', body)

# ---------- H-TuPlan: el plan de primera vez (pantalla con desplazamiento) ----------
H = 2080
def meta_row(nombre, estado, txt, pct, color, ok, cond=''):
    fg, bg = (GREEN, SGREEN) if ok == 'g' else ((AMBER, SAMBER) if ok == 'a' else ('#3F3F3F', GREY))
    c = f'<span style="font-size: 12px; color: {MUTED}; line-height: 1.4">{cond}</span>' if cond else ''
    return (f'<div style="display: flex; flex-direction: column; gap: 5px; padding: 10px 0; border-bottom: 1px solid {LINE}">'
            f'<span style="display: flex; justify-content: space-between; gap: 8px; align-items: center"><strong style="font-size: 14px">{nombre}</strong>{tag(estado, fg, bg)}</span>'
            f'<span style="font-size: 13px; color: {BODY}; line-height: 1.4">{txt}</span>{bar(pct, color)}{c}</div>')
PIL = [('Colchón', 40, 'Cubres 1,2 meses; lo sano son 3'), ('Suficiencia', 55, 'Vas para $2,3 M; tu meta, $3,0 M'),
       ('Protección', 35, 'Tu hija aún no es tu beneficiaria confirmada'), ('Riesgo a la medida', 70, 'Tu pensión va en el fondo para tu edad'),
       ('Eficiencia', 62, 'Comisión de 1,2% al año (ficticia); cesantías con meta'), ('Constancia', 50, 'Aportas sin falta; tus primas se diluyen')]
def pil_rows(rows):
    out = []
    for n, v, t in rows:
        c = GREEN if v >= 65 else (WARN if v >= 45 else '#9A2B1E')
        out.append(f'<div style="display: grid; grid-template-columns: 128px minmax(0, 1fr) 30px; gap: 8px; align-items: center; padding: 4px 0"><span style="font-size: 13px; font-weight: 700">{n}</span>{bar(v, c, GREY, 8)}<strong style="font-size: 12.5px; text-align: right">{v}</strong></div><span style="font-size: 12px; color: {MUTED}; margin: -2px 0 4px">{t}</span>')
    return ''.join(out)
PENSION_SUP_L = ('Estimado con tu salario de cotización de hoy, cotizando hasta los 57 y una rentabilidad real supuesta de 4% al año, neta de comisiones. '
                 'Tienes unas 730 semanas cotizadas: si sigues cotizando, llegas a 750 antes del 1 de abril de 2027 y conservarías las reglas de hoy (régimen de transición de la reforma pensional). '
                 'Lo confirmamos con tu historia laboral. No es una promesa ni una rentabilidad garantizada; algunos años puede ser negativa.')
body = f'''{root(True, H)}
<div style="display: flex; justify-content: space-between; align-items: center">{back('D5-Entendi.dc.html')}{TAG_INFO}</div>
<span style="font-size: 12.5px; color: {MUTED}">Tu plan · lunes 1 de junio · datos ficticios</span>
{h1('Laura, este es tu plan')}
{p('Lo armé con tus metas, no con nuestros productos. Al final está el orden para lograrlo y tu primer paso.')}
<div style="background: {INK}; color: #FFFFFF; border-radius: 22px; padding: 16px 18px; display: flex; flex-direction: column; gap: 8px">
<span style="font-size: 13px; color: #B8CCC4">Tu patrimonio hoy</span>
<span style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 32px; font-weight: 700; line-height: 1.05">$90,4 M</span>
<div style="display: flex; flex-direction: column; gap: 3px; font-size: 13px; color: #DCE6E2">
<span>Pensión obligatoria $78 M · sabemos</span><span>Cesantías $9,4 M · sabemos</span><span>Ahorro $3,0 M · nos contaste</span><span>Vivienda: arriendo · deudas: ninguna cara · nos contaste</span></div>
<a href="H-Patrimonio.dc.html" style="color: {GOLD}; font-weight: 700; font-size: 14px; min-height: 44px; display: flex; align-items: center">Ver tus 8 dimensiones</a>
</div>
{card(eyebrow('Tu pensión, el ancla') + '<span style="font-size: 15px; line-height: 1.45">Vas para unos <strong>$2,3 M al mes</strong> a los 57 (estimado). Para la vida que quieres, <strong>$3,0 M</strong>, te faltan unos $0,7 M.</span>' + bar(77, GOLD, GREY, 8) + details('Ver supuestos', PENSION_SUP_L), gap=8)}
<div style="background: #FFFFFF; border-radius: 20px; padding: 6px 16px 4px">
<div style="padding-top: 8px">{eyebrow('Tus metas, con tus números')}</div>
{meta_row('Tranquilidad: colchón de 3 meses', 'Lo primero', '$7,5 M, 3 meses de tus gastos · tienes $3,0 M', 40, WARN, 'a', 'Puede quedarse en tu cuenta de ahorros: lo importante es que esté separado y disponible.')}
{meta_row('Tu casa en 10 años · tu meta más importante', 'En camino', 'Cuota inicial de $45 M · llevas $9,4 M en tus cesantías', 21, GREEN, 'g', 'Tus cesantías se pueden usar para tu vivienda; si las usas, dejan de ser tu respaldo si pierdes el empleo. Por eso tu colchón va aparte.')}
{meta_row('Tu pensión con $3,0 M al mes', 'Con brecha', 'Te faltan unos $0,7 M al mes (estimado)', 77, WARN, 'a')}
{meta_row('Proteger a tu hija', 'Por empezar', 'Confirmarla como beneficiaria y revisar si necesitas un seguro de vida', 0, GREY, 'p')}
<div style="padding: 10px 0; display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 13.5px">¿Sumamos la educación de tu hija?</strong>{small('No la elegiste, pero tiene 8 años: la universidad empieza en unos 10. Si quieres, la sumamos en tu próxima revisión.')}</div>
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 4px">
<div style="display: flex; justify-content: space-between; align-items: baseline">{eyebrow('La salud de tu plan')}<span><strong style="font-family: 'Bricolage Grotesque', sans-serif; font-size: 24px">520</strong><span style="font-size: 12px; color: {MUTED}"> de 1.000</span></span></div>
{pil_rows(PIL)}
{small('Lo que más lo mueve hoy: llevar tu colchón a 3 meses. Información de tu plan. No es una recomendación profesional ni una calificación de crédito.')}
</div>
<div style="background: #FFFFFF; border-radius: 20px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px">
{eyebrow('El orden de tu plan')}
<div style="display: flex; gap: 10px"><strong style="color: {GREEN}">1</strong><span style="display: flex; flex-direction: column; gap: 6px; flex-grow: 1"><strong style="font-size: 14px">Hoy: confirma a tu hija como beneficiaria</strong>{small('Es lo que la protege si algo te pasa. Toma 2 minutos y no es un producto.')}
<button type="button" onClick="{{{{confirmar}}}}" aria-pressed="{{{{confirmadaAria}}}}" style="{{{{btnStyle}}}}">{{{{btnTxt}}}}</button></span></div>
<div style="display: flex; gap: 10px"><strong style="color: {GREEN}">2</strong><span style="display: flex; flex-direction: column; gap: 3px"><strong style="font-size: 14px">30 de junio: tu prima, unos $2,6 M</strong>{small('Tu colchón primero y avanzar tu casa. Dos semanas antes te preparo tu revisión con una propuesta, y tú decides.')}</span></div>
<div style="display: flex; gap: 10px"><strong style="color: {GREEN}">3</strong><span style="display: flex; flex-direction: column; gap: 3px"><strong style="font-size: 14px">Diciembre: tu pensión</strong>{small('Cuando tu colchón esté completo, vemos cómo cerrar la brecha de tu pensión.')}</span></div>
</div>
<div style="flex-grow: 1"></div>
{cta('H-Inicio.dc.html', 'Guardar mi plan')}
{link('H-Equipo.dc.html', avatar('DR', GOLD, INK, 28, 11) + 'Revisarlo con Daniela, tu consultora')}
{small('Preparado por tu arquitecto digital con lo que sabemos y lo que nos contaste. Cifras estimadas; no son promesas. Te enviamos una copia a tu correo y queda en Mis documentos.', True)}
</div>'''
write('H-TuPlan.dc.html', 'Tu plan', body, script("{ ok: false }", extra=(
    "confirmar: function () { self.setState({ ok: true }); }, confirmadaAria: s.ok ? 'true' : 'false', "
    "btnTxt: s.ok ? 'Listo: tu hija es tu beneficiaria' : 'Confirmar a mi hija', "
    "btnStyle: 'align-self: flex-start; min-height: 44px; padding: 0 16px; border-radius: 12px; font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; border: 2px solid #0E6A4E; background: ' + (s.ok ? '#E3EFEA' : '#0E6A4E') + '; color: ' + (s.ok ? '#0E6A4E' : '#FFFFFF')")), h=H)
print('diag ok')
