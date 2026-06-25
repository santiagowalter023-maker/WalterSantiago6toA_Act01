# CONFIGURACION GENERAL DEL JUEGO
# Este modulo centraliza constantes compartidas por codigo.py
# para que todo el proyecto use los mismos valores.

from pathlib import Path

# Carpeta donde esta este archivo (la carpeta del proyecto).
# Usamos esto para armar rutas ABSOLUTAS a los assets. Si dejamos las rutas
# relativas ("disenos/001.jpeg"), Arcade las resuelve con pathlib.resolve()
# tomando como base la carpeta desde donde se ejecuta python, y en Windows
# eso puede fallar o deformar la ruta cuando el path tiene espacios
# (por ejemplo "Programacion 3"). Con BASE_DIR evitamos ese problema.
BASE_DIR = Path(__file__).resolve().parent

ANCHO = 800
ALTO = 600
TITULO = "REMINENCE OF GRACIA"

# Velocidades de movimiento del personaje
VELOCIDAD_CAMINAR = 3
VELOCIDAD_CORRER = 6

# Escala del sprite del personaje (las imagenes originales son grandes)
ESCALA_PERSONAJE = 0.35

# Rutas de assets (absolutas, calculadas a partir de BASE_DIR)
# OJO: el fondo vive en la carpeta "disenos_estancia" (copia de la carpeta
# original "diseños", renombrada sin eñe para evitar problemas de
# codificacion de nombres de archivo en Windows/zip).
FONDO_ESTANCIA = str(BASE_DIR / "disenos_estancia" / "001.jpeg")
SPRITE_FRENTE = str(BASE_DIR / "waledo03.png")
SPRITE_ESPALDA = str(BASE_DIR / "waledo02.png")
SPRITE_PERFIL = str(BASE_DIR / "waledo01.png")

# Assets de la intro (logos, transicion, menu de inicio y musica de fondo)
LOGO_FUTURISTA = str(BASE_DIR / "assets_intro" / "logo_futurista.png")
LOGO_CAMBIO = str(BASE_DIR / "assets_intro" / "logo_cambio.png")
LOGO_ANTIGUO = str(BASE_DIR / "assets_intro" / "logo_antiguo.png")
MENU_INICIO = str(BASE_DIR / "assets_intro" / "menu_inicio.png")
MUSICA_FONDO = str(BASE_DIR / "assets_intro" / "musica_fondo.wav")

# Volumen bajo para que la musica de fondo no tape los dialogos (0.0 a 1.0)
VOLUMEN_MUSICA_FONDO = 0.15

# Assets de la escena del juicio (Tribunal Superior de Gracia, Sierras Hotel)
# Tres fondos distintos segun el momento de la escena:
#   INICIO  -> sala con el juez presentando el caso (arranque del juicio)
#   ACTIVO  -> el juez de pie, "¡Orden en la sala!" (momento de tension)
#   CERRADO -> mazo golpeado, "CASO CERRADO" (veredicto final)
JUICIO_FONDO_INICIO = str(BASE_DIR / "assets_juicio" / "juicio_inicio.jpeg")
JUICIO_FONDO_ACTIVO = str(BASE_DIR / "assets_juicio" / "juicio_activo.jpeg")
JUICIO_FONDO_CERRADO = str(BASE_DIR / "assets_juicio" / "juicio_cerrado.jpeg")