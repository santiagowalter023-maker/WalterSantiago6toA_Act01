// Formulario de reserva: genera un .txt con los datos al enviar
function p2(n) { return String(n).padStart(2, '0'); }

var form = document.getElementById('form-reserva');

function etiqueta(campo) {
  var lbl = document.querySelector('label[for="' + campo.id + '"]');
  return lbl ? lbl.textContent.trim() : campo.name;
}

form.addEventListener('submit', function (e) {
  e.preventDefault();
  var ahora = new Date();
  var fecha = p2(ahora.getDate()) + '/' + p2(ahora.getMonth() + 1) + '/' + ahora.getFullYear() +
    ' ' + p2(ahora.getHours()) + ':' + p2(ahora.getMinutes()) + ':' + p2(ahora.getSeconds());
  var pagina = window.location.pathname.split('/').pop() || 'agenciaviajes.html';

  var lineas = [];
  lineas.push('SOLICITUD DE RESERVA');
  lineas.push('==============================');
  lineas.push('Fecha y hora: ' + fecha);
  lineas.push('Pagina de origen: ' + document.title + ' (' + pagina + ')');
  lineas.push('');
  lineas.push('DATOS DEL CLIENTE');
  lineas.push('------------------------------');

  Array.prototype.forEach.call(form.elements, function (campo) {
    if (!campo.name || campo.type === 'submit') return;
    var valor = campo.value.trim();
    if (valor === '') return;
    lineas.push(etiqueta(campo) + ': ' + valor);
  });

  var nombreArchivo = 'reserva_' + ahora.getFullYear() + p2(ahora.getMonth() + 1) +
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

  alert('Solicitud enviada. Se generó el archivo ' + nombreArchivo);
  form.reset();
});
