// Mejoras progresivas: todo funciona sin JavaScript; esto solo actualiza cifras en vivo.
(function () {
  function pesos(v) { return '$' + Math.round(v).toLocaleString('es-CO').replace(/,/g, '.'); }
  document.querySelectorAll('input[type=range][data-salida]').forEach(function (r) {
    var out = document.getElementById(r.dataset.salida);
    var actualizar = function () {
      if (out) out.textContent = pesos(Number(r.value));
      if (r.id === 'gastos_mensuales') {
        var c = document.getElementById('colchon-txt');
        if (c) c.textContent = pesos(Number(r.value) * 3);
      }
    };
    r.addEventListener('input', actualizar);
  });
  document.querySelectorAll('[data-numero]').forEach(function (caja) {
    var input = caja.querySelector('input');
    var out = caja.querySelector('output');
    caja.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = Math.max(0, Math.min(25, Number(input.value) + Number(b.dataset.paso)));
        input.value = v; out.textContent = v + ' años';
      });
    });
  });
  // Perfil: el botón se activa solo con las seis respuestas (H9). Sin JavaScript, el servidor lo valida.
  document.querySelectorAll('form[data-perfil]').forEach(function (f) {
    var boton = f.querySelector('[data-requiere-todas]');
    var ayuda = f.querySelector('[data-ayuda-perfil]');
    var nombres = Array.from(new Set(Array.from(f.querySelectorAll('input[type=radio]')).map(function (i) { return i.name; })));
    var revisar = function () {
      var completo = nombres.every(function (n) { return f.querySelector('input[name="' + n + '"]:checked'); });
      boton.disabled = !completo;
      if (ayuda) ayuda.hidden = completo;
    };
    f.addEventListener('change', revisar);
    revisar();
  });
  var sim = document.getElementById('simulador');
  if (sim) {
    var rango = sim.querySelector('input[type=range]');
    rango.addEventListener('input', function () {
      fetch('/api/simular/casa?mensual=' + rango.value, { credentials: 'same-origin' })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          document.getElementById('sim-mensual').textContent = d.mensual_txt;
          document.getElementById('sim-bueno').textContent = d.anio_bueno || 'más de 50 años';
          document.getElementById('sim-malo').textContent = d.anio_malo || 'más de 50 años';
          document.getElementById('sim-estado').textContent = d.a_tiempo ? 'Llegas a tiempo (estimado)' : 'Aún no llegas a tiempo';
          var caida = document.getElementById('sim-caida');
          if (caida) caida.textContent = d.caida_txt;
        });
    });
  }
})();
