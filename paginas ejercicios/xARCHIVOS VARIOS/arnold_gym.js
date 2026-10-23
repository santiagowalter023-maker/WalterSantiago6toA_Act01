// Guarda la reserva del gimnasio en un archivo .txt al enviar el formulario
(function () {
  var PAGINA = "Arnold Schwarzenegger Gym - Elite Fitness";
  var ARCHIVO_ORIGEN = "arnold_gym.html";
  var form = document.querySelector("form.booking-form");
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

    lineas.push("RESERVA RECIBIDA");
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

    var nombre = "reserva_arnold_gym_" + ahora.getFullYear() + p2(ahora.getMonth() + 1) +
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

    alert("Reserva enviada. Se generó el archivo " + nombre);
    form.reset();
  });
})();
