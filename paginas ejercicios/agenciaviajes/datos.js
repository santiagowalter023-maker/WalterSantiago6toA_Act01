// Mini base de datos: lee el CSV indicado en data-archivo y lo muestra en #tabla-datos
var tabla = document.getElementById('tabla-datos');

if (tabla) {
  var archivo = tabla.getAttribute('data-archivo');

  fetch(archivo)
    .then(function (response) { return response.text(); })
    .then(function (data) {
      var filas = data.trim().split('\n');
      var tbody = tabla.querySelector('tbody');

      // La primera fila del CSV son los encabezados: ya están en el HTML, así que se omite
      filas.slice(1).forEach(function (fila) {
        var tr = document.createElement('tr');

        fila.split(',').forEach(function (col) {
          var td = document.createElement('td');
          td.textContent = col.trim();
          tr.appendChild(td);
        });

        tbody.appendChild(tr);
      });
    })
    .catch(function (error) { console.error('Error:', error); });
}
