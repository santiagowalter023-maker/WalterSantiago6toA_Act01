// Guarda los datos del formulario en un archivo CSV (basado en el PDF "Guardar datos de un formulario en un archivo CSV")
(function () {
  var PAGINA = "Walter Santiago | Portfolio";
  var ARCHIVO_ORIGEN = "index.html";
  var PREFIJO = "contacto_portfolio";
  var form = document.querySelector("#form-contacto");
  if (!form) return;

  function p2(n) { return String(n).padStart(2, "0"); }

  function fechaTexto(d) {
    return p2(d.getDate()) + "/" + p2(d.getMonth() + 1) + "/" + d.getFullYear() +
      " " + p2(d.getHours()) + ":" + p2(d.getMinutes()) + ":" + p2(d.getSeconds());
  }

  function etiqueta(campo) {
    var lbl = campo.id ? document.querySelector('label[for="' + campo.id + '"]') : null;
    return lbl ? lbl.textContent.trim() : campo.name;
  }

  // Cada dato va entre comillas y las comillas internas se duplican (igual que en el PDF)
  function celda(valor) {
    return '"' + String(valor).replace(/"/g, '""') + '"';
  }

  // Columnas extra de esta página: devuelve pares [encabezado, valor]
  function columnasExtra() {
    return [];
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var ahora = new Date();
    var encabezados = ["Fecha", "Pagina de origen"];
    var fila = [fechaTexto(ahora), PAGINA + " (" + ARCHIVO_ORIGEN + ")"];

    Array.prototype.forEach.call(form.elements, function (campo) {
      if (!campo.name || campo.type === "submit" || campo.closest("table")) return;
      encabezados.push(etiqueta(campo));
      fila.push(campo.value.trim());
    });

    columnasExtra().forEach(function (par) {
      encabezados.push(par[0]);
      fila.push(par[1]);
    });

    var contenido = encabezados.map(celda).join(",") + "\r\n" + fila.map(celda).join(",") + "\r\n";
    var archivo = new Blob(["\uFEFF" + contenido], { type: "text/csv;charset=utf-8;" });
    var nombre = PREFIJO + "_" + ahora.getFullYear() + p2(ahora.getMonth() + 1) + p2(ahora.getDate()) +
      "_" + p2(ahora.getHours()) + p2(ahora.getMinutes()) + p2(ahora.getSeconds()) + ".csv";

    var enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(archivo);
    enlace.download = nombre;
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
    setTimeout(function () { URL.revokeObjectURL(enlace.href); }, 1000);

    alert("Se generó el archivo " + nombre);
    form.reset();
  });
})();
