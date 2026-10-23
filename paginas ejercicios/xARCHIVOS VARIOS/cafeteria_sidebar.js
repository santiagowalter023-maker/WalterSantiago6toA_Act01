// Guarda el pedido de la cafetería en un archivo .txt al enviar el formulario
(function () {
  var PAGINA = "Cafetería - Menú";
  var ARCHIVO_ORIGEN = "cafeteria_sidebar.html";
  var form = document.querySelector("form.order-form");
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

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var ahora = new Date();
    var lineas = [];

    lineas.push("PEDIDO RECIBIDO");
    lineas.push("==============================");
    lineas.push("Fecha y hora: " + fechaTexto(ahora));
    lineas.push("Pagina de origen: " + PAGINA + " (" + ARCHIVO_ORIGEN + ")");
    lineas.push("");
    lineas.push("DATOS DEL CLIENTE");
    lineas.push("------------------------------");

    Array.prototype.forEach.call(form.elements, function (campo) {
      if (!campo.name || campo.type === "submit" || campo.type === "button") return;
      var valor = campo.value.trim();
      if (valor === "") return;
      lineas.push(etiqueta(campo) + ": " + valor);
    });

    lineas.push("");
    lineas.push("BEBIDAS SELECCIONADAS");
    lineas.push("------------------------------");

    var seleccionadas = document.querySelectorAll("#tabla input[type='checkbox']:checked");
    if (seleccionadas.length === 0) {
      lineas.push("Ninguna bebida seleccionada");
    } else {
      Array.prototype.forEach.call(seleccionadas, function (cb) {
        var celdas = cb.closest("tr").querySelectorAll("td");
        lineas.push("- " + celdas[0].textContent.trim() +
          " | Pequeño: " + celdas[1].textContent.trim() +
          " | Mediano: " + celdas[2].textContent.trim() +
          " | Grande: " + celdas[3].textContent.trim());
      });
    }

    var nombre = "pedido_cafeteria_" + ahora.getFullYear() + p2(ahora.getMonth() + 1) +
      p2(ahora.getDate()) + "_" + p2(ahora.getHours()) + p2(ahora.getMinutes()) +
      p2(ahora.getSeconds()) + ".txt";

    var blob = new Blob([lineas.join("\r\n")], { type: "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var enlace = document.createElement("a");
    enlace.href = url;
    enlace.download = nombre;
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);

    alert("Pedido enviado. Se generó el archivo " + nombre);
    form.reset();
  });
})();
