from flask import Flask, send_from_directory, abort
import os

CARPETA = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

PAGINAS = [
    ("agenciaviajes/agenciaviajes.html", "Agencia de viajes"),
    ("arnold_gym/arnold_gym.html", "Arnold Schwarzenegger Gym"),
    ("waltex/tegnoligiawaltex.html", "WALTEX"),
    ("cafeteria/cafeteria_sidebar.html", "Cafetería"),
    ("portafolio/index.html", "Portafolio Walter Santiago"),
]

@app.route("/")
def inicio():
    links = "".join(f'<li><a href="/{ruta}">{nombre}</a></li>' for ruta, nombre in PAGINAS)
    return ("<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'>"
            "<title>Mis páginas</title></head><body>"
            f"<h1>Mis páginas</h1><ul>{links}</ul></body></html>")

@app.route("/<path:ruta>")
def archivo(ruta):
    if not os.path.isfile(os.path.join(CARPETA, ruta)):
        abort(404)
    return send_from_directory(CARPETA, ruta)

if __name__ == "__main__":
    print("Servidor activo en http://127.0.0.1:5000  (Ctrl + C para detener)")
    app.run(debug=True)
