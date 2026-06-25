# CONFIGURACION GENERAL DEL JUEGO
# Este modulo centraliza constantes compartidas por codigo.py
# para que todo el proyecto use los mismos valores.

from pathlib import Path

# Carpeta donde esta este archivo (la carpeta del proyecto).
BASE_DIR = Path(__file__).resolve().parent

ANCHO = 800
ALTO = 600
TITULO = "REMINENCE OF GRACIA"

# Velocidades de movimiento del personaje
VELOCIDAD_CAMINAR = 3
VELOCIDAD_CORRER = 6

# Escala del sprite del personaje
ESCALA_PERSONAJE = 0.35

# ---------------------------------------------------------------
# SPRITE SHEET DEL PERSONAJE PRINCIPAL (Lediago)
# 4 columnas x 3 filas = 12 frames
#   Fila 0 (arriba): caminar hacia ABAJO  (frente) - 4 frames
#   Fila 1 (medio) : caminar de LADO      (derecha) - 4 frames
#   Fila 2 (abajo) : caminar hacia ARRIBA (espalda) - 4 frames
# Para caminar a la IZQUIERDA se espeja la fila 1.
# ---------------------------------------------------------------
SPRITE_SHEET      = str(BASE_DIR / "assets_juicio" / "sprite_sheet.png")
SPRITE_SHEET_COLS = 4
SPRITE_SHEET_ROWS = 3
SPRITE_FRAME_W    = 104   # 416 / 4
SPRITE_FRAME_H    = 200   # 600 / 3
ANIM_FPS          = 8     # frames por segundo de la animacion de caminar

# Rutas legadas (para retrocompatibilidad con GameView si se usa)
SPRITE_FRENTE  = str(BASE_DIR / "waledo03.png")
SPRITE_ESPALDA = str(BASE_DIR / "waledo02.png")
SPRITE_PERFIL  = str(BASE_DIR / "waledo01.png")

# Fondos
FONDO_ESTANCIA = str(BASE_DIR / "assets_estancia" / "estancia_jesuitica_principal.jpg")

# Assets del Cura y el minijuego de la Estancia
CURA_IDLE      = str(BASE_DIR / "assets_estancia" / "cura_idle.png")
CURA_DIALOGO   = str(BASE_DIR / "assets_estancia" / "cura_dialogo.png")
CURA_SENALANDO = str(BASE_DIR / "assets_estancia" / "cura_senalando.png")
CRUZ_ESTANCIA_IMG = str(BASE_DIR / "assets_estancia" / "cruz_estancia.png")

# Assets de la intro
LOGO_FUTURISTA = str(BASE_DIR / "assets_intro" / "logo_futurista.png")
LOGO_CAMBIO    = str(BASE_DIR / "assets_intro" / "logo_cambio.png")
LOGO_ANTIGUO   = str(BASE_DIR / "assets_intro" / "logo_antiguo.png")
MENU_INICIO    = str(BASE_DIR / "assets_intro" / "menu_inicio.png")
MUSICA_FONDO   = str(BASE_DIR / "assets_intro" / "musica_fondo.wav")

VOLUMEN_MUSICA_FONDO = 0.15

# Assets de la escena del juicio
JUICIO_FONDO_INICIO  = str(BASE_DIR / "assets_juicio" / "juicio_inicio.jpeg")
JUICIO_FONDO_ACTIVO  = str(BASE_DIR / "assets_juicio" / "juicio_activo.jpeg")
JUICIO_FONDO_CERRADO = str(BASE_DIR / "assets_juicio" / "juicio_cerrado.jpeg")

# Assets de la escena del Hotel Sierras (gameplay + dialogo)
HOTEL_SIERRAS_FONDO    = str(BASE_DIR / "assets_juicio" / "hotel_sierras_fondo.png")
HOTEL_WALTER_LEDO_IDLE = str(BASE_DIR / "assets_juicio" / "walter_ledo_pies_t.png")
HOTEL_WALTER_LEDO_AFK  = str(BASE_DIR / "assets_juicio" / "walter_ledo_afk_t.png")
HOTEL_WALTER_LEDO_DLG  = str(BASE_DIR / "assets_juicio" / "walter_ledo_dialogo_t.png")

# Assets de la Vitrina de Objetos (Estudio de Curiosidades)
VITRINA_FONDO    = str(BASE_DIR / "assets_juicio" / "vitrina_fondo.jpeg")
VITRINA_ABIERTA  = str(BASE_DIR / "assets_juicio" / "vitrina_abierta.jpeg")
CRONOSCOPIO_IMG  = str(BASE_DIR / "assets_juicio" / "cronoscopio.png")

# Archivo de guardado de partida
SAVE_FILE = str(BASE_DIR / "partida_guardada.json")
