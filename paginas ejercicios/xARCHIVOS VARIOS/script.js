// Menú móvil
var toggle = document.querySelector('.nav-toggle');
var menu = document.getElementById('nav-menu');

toggle.addEventListener('click', function () {
  var abierto = menu.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(abierto));
});

menu.querySelectorAll('a').forEach(function (enlace) {
  enlace.addEventListener('click', function () {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  });
});

// Filtro de proyectos
var filtros = document.querySelectorAll('.filter');
var proyectos = document.querySelectorAll('.project-card');

filtros.forEach(function (btn) {
  btn.addEventListener('click', function () {
    var filtro = btn.getAttribute('data-filter');
    filtros.forEach(function (b) { b.classList.remove('is-active'); });
    btn.classList.add('is-active');
    proyectos.forEach(function (p) {
      var categoria = p.getAttribute('data-category');
      p.hidden = !(filtro === 'todos' || categoria === filtro);
    });
  });
});

// Formulario de contacto: genera un .txt con los datos
function p2(n) { return String(n).padStart(2, '0'); }

var form = document.getElementById('form-contacto');

function etiqueta(campo) {
  var lbl = document.querySelector('label[for="' + campo.id + '"]');
  return lbl ? lbl.textContent.trim() : campo.name;
}

form.addEventListener('submit', function (e) {
  e.preventDefault();
  var ahora = new Date();
  var fecha = p2(ahora.getDate()) + '/' + p2(ahora.getMonth() + 1) + '/' + ahora.getFullYear() +
    ' ' + p2(ahora.getHours()) + ':' + p2(ahora.getMinutes()) + ':' + p2(ahora.getSeconds());
  var pagina = window.location.pathname.split('/').pop() || 'index.html';

  var lineas = [];
  lineas.push('CONTACTO RECIBIDO');
  lineas.push('==============================');
  lineas.push('Fecha y hora: ' + fecha);
  lineas.push('Pagina de origen: ' + document.title + ' (' + pagina + ')');
  lineas.push('');
  lineas.push('DATOS DEL CONTACTO');
  lineas.push('------------------------------');

  Array.prototype.forEach.call(form.elements, function (campo) {
    if (!campo.name || campo.type === 'submit') return;
    var valor = campo.value.trim();
    if (valor === '') return;
    lineas.push(etiqueta(campo) + ': ' + valor);
  });

  var nombreArchivo = 'contacto_' + ahora.getFullYear() + p2(ahora.getMonth() + 1) +
    p2(ahora.getDate()) + '_' + p2(ahora.getHours()) + p2(ahora.getMinutes()) +
    p2(ahora.getSeconds()) + '.txt';

  var blob = new Blob([lineas.join('\r\n')], { type: 'text/plain;charset=utf-8' });
  var url = URL.createObjectURL(blob);
  var enlace = document.createElement('a');
  enlace.href = url;
  enlace.download = nombreArchivo;
  document.body.appendChild(enlace);
  enlace.click();
  document.body.removeChild(enlace);
  setTimeout(function () { URL.revokeObjectURL(url); }, 1000);

  alert('Mensaje enviado. Se generó el archivo ' + nombreArchivo);
  form.reset();
});
