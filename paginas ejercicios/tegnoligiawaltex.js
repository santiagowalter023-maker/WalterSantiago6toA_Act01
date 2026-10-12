// Guarda el pedido de WALTEX en un archivo .txt al enviar el formulario
(function () {
  var PAGINA = "Waltex | Tienda de Tecnología";
  var ARCHIVO_ORIGEN = "tegnoligiawaltex.html";
  var form = document.querySelector("form.pedido");
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

  function aNumero(texto) {
    return parseInt(texto.replace(/\D/g, ""), 10) || 0;
  }

  function formatear(n) {
    return "$ " + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
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
      if (campo.closest("table")) return;
      var valor = campo.value.trim();
      if (valor === "") return;
      lineas.push(etiqueta(campo) + ": " + valor);
    });

    lineas.push("");
    lineas.push("PRODUCTOS PEDIDOS");
    lineas.push("------------------------------");

    var total = 0;
    var hayProductos = false;
    Array.prototype.forEach.call(form.querySelectorAll("table input[type='number']"), function (input) {
      var cantidad = parseInt(input.value, 10) || 0;
      if (cantidad <= 0) return;
      var celdas = input.closest("tr").querySelectorAll("td");
      var precioUnitario = aNumero(celdas[1].textContent);
      var subtotal = precioUnitario * cantidad;
      total += subtotal;
      hayProductos = true;
      lineas.push("- " + celdas[0].textContent.trim() + " | Precio: " + formatear(precioUnitario) +
        " | Cantidad: " + cantidad + " | Subtotal: " + formatear(subtotal));
    });

    if (!hayProductos) {
      lineas.push("Ningún producto seleccionado");
    } else {
      lineas.push("");
      lineas.push("TOTAL: " + formatear(total));
    }

    var nombre = "pedido_waltex_" + ahora.getFullYear() + p2(ahora.getMonth() + 1) +
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
