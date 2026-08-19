import arcade
import asyncio
import hashlib
import json
import os
import math
import random
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent

# Tamaño de la ventana y velocidades del personaje
ANCHO = 800
ALTO = 600
TITULO = "REMINENCE OF GRACIA"

VELOCIDAD_CAMINAR = 3
VELOCIDAD_CORRER = 6
ESCALA_PERSONAJE = 0.35
VOLUMEN_MUSICA_FONDO = 0.15

# Rutas a todas las imágenes/audios usados (sprite sheet, fondos, personajes, etc.)
SPRITE_SHEET = str(BASE_DIR / "assets_juicio" / "sprite_sheet.png")
SPRITE_FRAME_W = 104
SPRITE_FRAME_H = 200
SPRITE_SHEET_COLS = 4
SPRITE_SHEET_ROWS = 3
ANIM_FPS = 8

FONDO_ESTANCIA = str(BASE_DIR / "assets_estancia" / "estancia_jesuitica_principal.jpg")
CURA_IDLE = str(BASE_DIR / "assets_estancia" / "cura_idle.png")
CURA_DIALOGO = str(BASE_DIR / "assets_estancia" / "cura_dialogo.png")
CURA_SENALANDO = str(BASE_DIR / "assets_estancia" / "cura_senalando.png")
CRUZ_ESTANCIA_IMG = str(BASE_DIR / "assets_estancia" / "cruz_estancia.png")

LOGO_FUTURISTA = str(BASE_DIR / "assets_intro" / "logo_futurista.png")
LOGO_CAMBIO = str(BASE_DIR / "assets_intro" / "logo_cambio.png")
LOGO_ANTIGUO = str(BASE_DIR / "assets_intro" / "logo_antiguo.png")
MENU_INICIO = str(BASE_DIR / "assets_intro" / "menu_inicio.png")
MUSICA_FONDO = str(BASE_DIR / "assets_intro" / "musica_fondo.wav")

JUICIO_FONDO_INICIO = str(BASE_DIR / "assets_juicio" / "juicio_inicio.jpeg")
JUICIO_FONDO_ACTIVO = str(BASE_DIR / "assets_juicio" / "juicio_activo.jpeg")
JUICIO_FONDO_CERRADO = str(BASE_DIR / "assets_juicio" / "juicio_cerrado.jpeg")

HOTEL_SIERRAS_FONDO = str(BASE_DIR / "assets_juicio" / "hotel_sierras_fondo.png")
HOTEL_WALTER_LEDO_IDLE = str(BASE_DIR / "assets_juicio" / "walter_ledo_pies_t.png")
HOTEL_WALTER_LEDO_AFK = str(BASE_DIR / "assets_juicio" / "walter_ledo_afk_t.png")
HOTEL_WALTER_LEDO_DLG = str(BASE_DIR / "assets_juicio" / "walter_ledo_dialogo_t.png")

VITRINA_FONDO = str(BASE_DIR / "assets_juicio" / "vitrina_fondo.jpeg")
VITRINA_ABIERTA = str(BASE_DIR / "assets_juicio" / "vitrina_abierta.jpeg")
CRONOSCOPIO_IMG = str(BASE_DIR / "assets_juicio" / "cronoscopio.png")

# Nivel 2: "Senderos de Paravachasca" (dialogo con el Indio + esquivar lanzas)
FONDO_SUBNIVEL1 = str(BASE_DIR / "assets_paravachasca" / "fondo_subnivel1.jpg")
INDIO_IDLE_IMG = str(BASE_DIR / "assets_paravachasca" / "indio_idle.png")
INDIO_DIALOGO_IMG = str(BASE_DIR / "assets_paravachasca" / "indio_dialogo.png")
LANZA_IMG = str(BASE_DIR / "assets_paravachasca" / "lanza_proyectil.png")

# Nivel 3: "La Guardiana del Museo" (dialogo con Gabriel Dubois + duelo con el angel)
FONDO_MUSEO = str(BASE_DIR / "assets_dubois" / "fondo_museo.jpg")
DUBOIS_IDLE_IMG = str(BASE_DIR / "assets_dubois" / "dubois_idle.png")
DUBOIS_DIALOGO_IMG = str(BASE_DIR / "assets_dubois" / "dubois_dialogo.png")
ANGEL_IDLE_IMG = str(BASE_DIR / "assets_dubois" / "angel_idle.png")
ANGEL_CARGA_IMG = str(BASE_DIR / "assets_dubois" / "angel_carga.png")
ANGEL_LANZA_IMG = str(BASE_DIR / "assets_dubois" / "angel_lanza.png")
BOLA_FUEGO_ATAQUE_IMG = str(BASE_DIR / "assets_dubois" / "bola_fuego_ataque.png")
BOLA_FUEGO_DEFENSA_IMG = str(BASE_DIR / "assets_dubois" / "bola_fuego_defensa.png")

SAVE_FILE = str(BASE_DIR / "partida_guardada.json")

FRENTE = 0
ESPALDA = 1
IZQUIERDA = 2
DERECHA = 3

# Posibles "modos" en los que puede estar la escena de la Estancia (caminando, hablando, en la trivia, etc.)
ESTADO_JUGANDO = 0
ESTADO_HABLANDO = 1
ESTADO_INTRO_CURA = 2
ESTADO_TRIVIA = 3
ESTADO_CIERRE_CURA = 4
ESTADO_FIN_DEMO = 5

FONDO_INICIO = "inicio"
FONDO_ACTIVO = "activo"
FONDO_CERRADO = "cerrado"

MEDALLA_HISTORIADOR = "Historiador de la Estancia"
XP_RECOMPENSA_TRIVIA = 100
PREGUNTAS_MINIMAS_PARA_GANAR = 5

# --- Nivel 2: "Senderos de Paravachasca" ---
TITULO_NIVEL2 = "NIVEL 2 - SENDEROS DE PARAVACHASCA"
MEDALLA_PARAVACHASCA = "Guardian de Paravachasca"
XP_RECOMPENSA_NIVEL2 = 100
NIVEL2_DURACION_SEGUNDOS = 120.0   # 2 minutos para ganar el nivel
NIVEL2_VIDAS = 3                   # golpes de lanza permitidos antes de perder
NIVEL2_ESCALA_LANZA = 0.18
NIVEL2_VELOCIDAD_LANZA_MIN = 220   # px/seg al arrancar el nivel
NIVEL2_VELOCIDAD_LANZA_MAX = 400   # px/seg cerca del final (mas dificil)
NIVEL2_INTERVALO_SPAWN_INICIAL = 1.15  # segundos entre lanzas al arrancar
NIVEL2_INTERVALO_SPAWN_MINIMO = 0.45   # segundos entre lanzas en lo mas dificil
NIVEL2_TIEMPO_INVULNERABLE = 1.2   # segundos de "respiro" despues de un golpe

# --- Nivel 3: "La Guardiana del Museo" ---
TITULO_NIVEL3 = "NIVEL 3 - LA GUARDIANA DEL MUSEO"
MEDALLA_MUSEO = "Guardian del Museo"
XP_RECOMPENSA_NIVEL3 = 120
NIVEL3_VIDAS_JUGADOR = 5
NIVEL3_VIDA_ANGEL = 5               # golpes de bola azul necesarios para vencerlo
NIVEL3_FUEGOS_RONDA_BASE = 3        # cantidad de bolas de fuego en la primera ronda
NIVEL3_FUEGOS_RONDA_MAX = 7         # tope de bolas de fuego por ronda
NIVEL3_VELOCIDAD_FUEGO_MIN = 190
NIVEL3_VELOCIDAD_FUEGO_MAX = 340
NIVEL3_INTERVALO_FUEGO = 0.85       # segundos entre cada bola de fuego dentro de una ronda
NIVEL3_VELOCIDAD_BOLA_AZUL = 420
NIVEL3_TIEMPO_INVULNERABLE = 1.1
NIVEL3_ESCALA_ATAQUE = 0.12
NIVEL3_ESCALA_DEFENSA = 0.10
NIVEL3_ESCALA_ANGEL = 0.68
NIVEL3_ANGEL_X = 640                # posicion fija del angel (pedestal vacio del museo)
NIVEL3_ANGEL_Y = 370
NIVEL3_TIEMPO_CARGA = 0.6           # segundos que el angel se queda "cargando" antes de tirar

DURACION_LOGO_FUTURISTA = 2.5
DURACION_TRANSICION = 0.4
DURACION_LOGO_ANTIGUO = 2.5

# Tiempo (en segundos) que tarda en terminar de "escribirse" cada línea de
# diálogo en pantalla, efecto cinemática.
DURACION_TEXTO_DIALOGO = 8.0

ETAPA_LOGO_FUTURISTA = 0
ETAPA_TRANSICION = 1
ETAPA_LOGO_ANTIGUO = 2
ETAPA_MENU = 3

# Voz de Edge TTS asignada a cada personaje (usada por generar_voces.py
# para generar los audios). El nombre de la voz tiene que terminar en
# "Neural" -- podés listar las disponibles con: edge-tts --list-voices
VOCES_PERSONAJE = {
    "JUEZ"      : "es-ES-AlvaroNeural",
    "ABOGADO"   : "es-US-AlonsoNeural",
    "WALTER"    : "es-AR-TomasNeural",
    "LEDO"      : "es-BO-MarceloNeural",
    "LEDIAGO"   : "es-CL-LorenzoNeural",
    "CIUDADANOS": "es-MX-JorgeNeural",
    "NARRADOR"  : "es-ES-XabierNeural",
    "CURA"      : "es-CR-JuanNeural",
    "WALEDO"    : "es-CL-LorenzoNeural",
    "INDIO"     : "es-EC-LuisNeural",
    "GABRIEL"   : "es-VE-SebastianNeural",
}
VOZ_POR_DEFECTO = "es-AR-ElenaNeural"


# Datos de cada personaje que puede hablar (nombre a mostrar y color de sus cuadros de diálogo)
HABLANTES = {
    "JUEZ": {"nombre": "JUEZ DEL TRIBUNAL", "color_nombre": arcade.color.GOLD, "color_borde": arcade.color.GOLD},
    "ABOGADO": {"nombre": "ABOGADO DE LA CORPORACION", "color_nombre": arcade.color.RED_DEVIL, "color_borde": arcade.color.RED_DEVIL},
    "WALTER": {"nombre": "WALTER", "color_nombre": arcade.color.CYAN, "color_borde": arcade.color.CYAN},
    "LEDO": {"nombre": "LEDO", "color_nombre": arcade.color.GREEN_YELLOW, "color_borde": arcade.color.GREEN_YELLOW},
    "LEDIAGO": {"nombre": "LEDIAGO WALEDO", "color_nombre": arcade.color.LIGHT_PASTEL_PURPLE, "color_borde": arcade.color.LIGHT_PASTEL_PURPLE},
    "CIUDADANOS": {"nombre": "CIUDADANOS", "color_nombre": arcade.color.LIGHT_GRAY, "color_borde": arcade.color.LIGHT_GRAY},
    "NARRADOR": {"nombre": "", "color_nombre": arcade.color.WHITE, "color_borde": arcade.color.WHITE},
    "WALEDO": {"nombre": "LEDIAGO WALEDO", "color_nombre": arcade.color.LIGHT_PASTEL_PURPLE, "color_borde": arcade.color.LIGHT_PASTEL_PURPLE},
    "INDIO": {"nombre": "SABIO COMECHINGON", "color_nombre": arcade.color.ORANGE, "color_borde": arcade.color.ORANGE},
    "GABRIEL": {"nombre": "GABRIEL DUBOIS", "color_nombre": arcade.color.AO, "color_borde": arcade.color.AO},
}

# A partir de acá: guiones de diálogo (listas de tuplas "quién habla" + "qué dice")
# usados en las distintas escenas del juego
GUION_INTRO_CURA = [
    ("CURA", "La paz sea contigo, hijo! Veo curiosidad en tus ojos... No todos los dias alguien se detiene a observar la historia de este lugar."),
    ("WALEDO", "Estoy recorriendo Alta Gracia y tratando de descubrir los secretos que esconde cada epoca."),
    ("CURA", "Entonces has llegado al sitio indicado. Esta antigua Estancia guarda casi cuatro siglos de historia, desde la llegada de los jesuitas hasta convertirse en uno de los mayores tesoros culturales del pais."),
    ("WALEDO", "Eso suena interesante! Pero... como se si aprendi lo suficiente?"),
    ("CURA", "Muy sencillo. Prepare un pequenio desafio. Son siete preguntas sobre la Estancia Jesuitica. Si respondes correctamente la mayoria, demostraras que estas listo para continuar tu viaje por el tiempo."),
    ("WALEDO", "Acepto el reto!"),
    ("CURA", "Muy bien. Lee con atencion y piensa antes de responder. La historia siempre recompensa a quienes observan."),
]

GUION_CIERRE_CURA_EXITO = [
    ("CURA", "Excelente! Has demostrado conocer la historia de este lugar. El conocimiento tambien es una forma de viajar en el tiempo."),
    ("WALEDO", "Gracias, padre. Ahora entiendo mucho mejor la importancia de la Estancia."),
    ("CURA", "Que esta sabiduria te acompanie en los proximos viajes del Cronoscopio."),
]

GUION_CIERRE_CURA_FALLO = [
    ("CURA", "No te desanimes. La historia siempre ofrece una segunda oportunidad. Recorre nuevamente la Estancia y vuelve cuando estes preparado."),
    ("WALEDO", "Volvere. Todavia me queda mucho por aprender."),
]

# Preguntas de la trivia: (enunciado, lista de opciones, índice de la opción correcta)
PREGUNTAS_ESTANCIA = [
    ("Que anio comenzo a organizarse la Estancia Jesuitica de Alta Gracia?",
     ["1588", "1643", "1767", "1810"], 1),
    ("Que orden religiosa administro la Estancia?",
     ["Franciscanos", "Dominicos", "Jesuitas", "Benedictinos"], 2),
    ("Que reconocimiento internacional recibio la Estancia?",
     ["Patrimonio Natural", "Monumento Provincial", "Patrimonio Mundial de la UNESCO", "Capital Cultural Americana"], 2),
    ("Que importante personaje historico vivio sus ultimos dias en esta residencia?",
     ["Manuel Belgrano", "Jose de San Martin", "Juan Bautista Alberdi", "Santiago de Liniers"], 3),
    ("Que construccion de la Estancia permitia almacenar agua para la comunidad?",
     ["El campanario", "La biblioteca", "El Tajamar", "El cabildo"], 2),
    ("Cual de estas partes todavia forma parte del conjunto historico?",
     ["La iglesia y la residencia jesuitica", "El fuerte militar", "El puerto", "El teatro colonial"], 0),
    ("Cual era uno de los principales objetivos de las estancias jesuiticas?",
     ["Construir fortalezas militares.", "Extraer oro.",
      "Sostener economicamente las obras educativas y religiosas de los jesuitas mediante la produccion agricola y ganadera.",
      "Fabricar barcos."], 2),
]

GUION_JUICIO = [
    ("JUEZ", "Se abre la sesion extraordinaria del Tribunal de Legado Cultural. Procedan con sus argumentos.", FONDO_INICIO),
    ("ABOGADO", "Honorables miembros del tribunal, los edificios antiguos no generan progreso. Nuestra propuesta traera inversion, turismo y empleo. La ciudad necesita avanzar.", FONDO_INICIO),
    ("WALTER", "Avanzar destruyendo todo lo que la hace unica?", FONDO_INICIO),
    ("ABOGADO", "La historia esta en los libros, senor. No en piedras viejas.", FONDO_INICIO),
    ("LEDO", "Entonces nunca entendio lo que significa Alta Gracia.", FONDO_INICIO),
    ("JUEZ", "Tienen pruebas concretas para refutar el proyecto?", FONDO_INICIO),
    ("ABOGADO", "Exactamente. Emociones y recuerdos no son evidencia legal.", FONDO_INICIO),
    ("NARRADOR", "(Las puertas del hotel se abren.)", FONDO_ACTIVO),
    ("WALTER", "Llego.", FONDO_ACTIVO),
    ("LEDO", "Sabia que volveria.", FONDO_ACTIVO),
    ("JUEZ", "Quien es usted?", FONDO_ACTIVO),
    ("LEDIAGO", "Mi nombre es Lediago Waledo. Y traigo la memoria de esta ciudad.", FONDO_ACTIVO),
    ("ABOGADO", "Esto es absurdo.", FONDO_ACTIVO),
    ("LEDIAGO", "Absurdo?", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca la Piedra de Moler sobre la mesa.)", FONDO_ACTIVO),
    ("LEDIAGO", "Antes de las calles hubo un pueblo que escuchaba hablar al viento.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca la Herramienta Jesuita.)", FONDO_ACTIVO),
    ("LEDIAGO", "Antes de los hoteles hubo hombres que levantaron estos muros piedra por piedra.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca la Llave Maestra.)", FONDO_ACTIVO),
    ("LEDIAGO", "Antes del nombre existio el suenio de una ciudad.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca el Sello Real.)", FONDO_ACTIVO),
    ("LEDIAGO", "Antes de la nacion hubo quienes protegieron estas tierras en tiempos inciertos.", FONDO_ACTIVO),
    ("NARRADOR", "(Los presentes observan en silencio.)", FONDO_ACTIVO),
    ("ABOGADO", "Objetos antiguos. Nada mas.", FONDO_ACTIVO),
    ("LEDIAGO", "Nada mas?", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca el Cincel del Cantero.)", FONDO_ACTIVO),
    ("LEDIAGO", "Miles de golpes construyeron cada calle que hoy pisan.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca el Quijote.)", FONDO_ACTIVO),
    ("LEDIAGO", "Un ninio curioso aprendio aqui a cuestionar el mundo.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca el Metronomo.)", FONDO_ACTIVO),
    ("LEDIAGO", "Un compositor encontro inspiracion entre estas montanias.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca la Cantimplora.)", FONDO_ACTIVO),
    ("LEDIAGO", "Miles de peregrinos buscaron esperanza en estas tierras.", FONDO_ACTIVO),
    ("NARRADOR", "(Coloca la Espatula de Dubois.)", FONDO_ACTIVO),
    ("LEDIAGO", "Y artistas transformaron la materia en memoria.", FONDO_ACTIVO),
    ("ABOGADO", "Todo eso sigue siendo pasado.", FONDO_ACTIVO),
    ("LEDIAGO", "No.", FONDO_ACTIVO),
    ("LEDIAGO", "El pasado es lo que sostiene el presente.", FONDO_ACTIVO),
    ("JUEZ", "Y como pretende demostrarlo?", FONDO_ACTIVO),
    ("WALTER", "Activemos el Cronoscopio.", FONDO_ACTIVO),
    ("LEDO", "Es momento de que la ciudad hable por si misma.", FONDO_ACTIVO),
    ("NARRADOR", "(El Cronoscopio comienza a iluminarse.)", FONDO_ACTIVO),
    ("ABOGADO", "Que es eso?", FONDO_ACTIVO),
    ("LEDIAGO", "Escuche.", FONDO_ACTIVO),
    ("NARRADOR", "(Se oye el sonido del agua del Tajamar.)", FONDO_ACTIVO),
    ("CIUDADANOS", "...", FONDO_ACTIVO),
    ("NARRADOR", "(Se escuchan martillos de los canteros.)", FONDO_ACTIVO),
    ("CIUDADANOS", "...", FONDO_ACTIVO),
    ("NARRADOR", "(Comienza a sonar un piano lejano.)", FONDO_ACTIVO),
    ("CIUDADANOS", "...", FONDO_ACTIVO),
    ("NARRADOR", "(Voces indigenas, campanas jesuitas y cantos de peregrinos llenan el salon.)", FONDO_ACTIVO),
    ("JUEZ", "Que esta ocurriendo?", FONDO_ACTIVO),
    ("WALTER", "La memoria de Alta Gracia.", FONDO_ACTIVO),
    ("LEDO", "La historia que aun vive entre nosotros.", FONDO_ACTIVO),
    ("ABOGADO", "Esto... esto no puede ser posible.", FONDO_ACTIVO),
    ("LEDIAGO", "La ciudad no es un conjunto de edificios.", FONDO_ACTIVO),
    ("LEDIAGO", "Es la suma de todas las vidas que la construyeron.", FONDO_ACTIVO),
    ("JUEZ", "He escuchado suficiente.", FONDO_ACTIVO),
    ("NARRADOR", "(Silencio absoluto.)", FONDO_ACTIVO),
    ("JUEZ", "Este tribunal determina que el patrimonio historico y cultural de Alta Gracia posee un valor excepcional e irremplazable.", FONDO_CERRADO),
    ("ABOGADO", "Protesto!", FONDO_CERRADO),
    ("JUEZ", "Protesta denegada.", FONDO_CERRADO),
]

GUION_HOTEL = [
    ("WALTER", "Por fin despertaste!"),
    ("LEDIAGO", "Donde estoy?"),
    ("LEDO", "En el Hotel Sierras. O mejor dicho... en lo que queda de el."),
    ("LEDIAGO", "No entiendo nada. Quienes son ustedes?"),
    ("WALTER", "Mi nombre es Walter."),
    ("LEDO", "Y yo soy Ledo. Somos los guardianes del Archivo Historico de Alta Gracia."),
    ("LEDIAGO", "Y por que me trajeron aqui?"),
    ("WALTER", "Porque la ciudad esta en peligro. Muy pronto todo esto podria desaparecer."),
    ("LEDIAGO", "Desaparecer?"),
    ("LEDO", "Una corporacion quiere demoler los lugares historicos para construir algo nuevo."),
    ("LEDIAGO", "Y que esperan que haga yo?"),
    ("NARRADOR", "(Walter senala una extrana maquina llena de engranajes y luces.)"),
    ("WALTER", "Necesitamos que uses el Cronoscopio."),
    ("LEDIAGO", "Cronoscopio?"),
    ("LEDO", "Una maquina capaz de abrir puertas hacia distintas epocas de Alta Gracia."),
    ("LEDIAGO", "Me estan diciendo que viaje en el tiempo?"),
    ("WALTER", "Exactamente."),
    ("LEDIAGO", "Eso suena imposible."),
    ("LEDO", "Tambien sonaba imposible perder toda la historia de una ciudad."),
    ("WALTER", "Tu mision sera viajar al pasado, conocer a quienes construyeron esta tierra y recuperar fragmentos de su memoria."),
    ("LEDIAGO", "Y si algo sale mal?"),
    ("LEDO", "No cambiaras la historia."),
    ("WALTER", "Solo la observaras... y traeras pruebas de que sigue viva."),
    ("NARRADOR", "(El Cronoscopio comienza a iluminarse.)"),
    ("LEDIAGO", "Supongo que no tengo muchas opciones."),
    ("LEDO", "Ninguna."),
    ("WALTER", "Preparate, viajero."),
    ("LEDO", "Tu primera parada te espera hace cientos de anios."),
]

# Dialogo del Nivel 2 ("Senderos de Paravachasca"): Waledo habla con el Indio
# antes de enfrentar el desafio de esquivar las lanzas.
GUION_INDIO_NIVEL2 = [
    ("WALEDO", "Saludos, sabio del monte. Dime, como era este valle de Paravachasca mucho antes de que la ciudad de Alta Gracia fuera lo que conocemos hoy?"),
    ("INDIO", "Ah, Waledo... Escucha el murmullo del viento entre los algarrobos. Antes de que existieran las murallas de piedra, los caminos trazados y las luces de la ciudad, esta tierra nos pertenecia a nosotros, los comechingones. Viviamos en casas semisubterraneas para protegernos del frio y del calor, alimentandonos de los frutos del monte y cazando con respeto. Para nosotros, los cerros y los rios de agua clara no eran solo paisaje, eran vida y espiritu sagrado."),
    ("WALEDO", "He leido sobre su pueblo y sobre como la llegada de los conquistadores y la posterior instalacion de las estancias jesuitas transformaron por completo la region. Como vivieron esa transicion?"),
    ("INDIO", "Fue un cambio profundo y doloroso, Waledo. Con la llegada de los jesuitas en el siglo XVII, el valle cambio su rostro para siempre. Ellos levantaron la gran Estancia de Alta Gracia, construyeron el Tajamar para canalizar el agua, fundaron la iglesia y trajeron nuevos oficios y culturas. Aunque transformaron el valle en un centro productivo y de fe, la huella de nuestros antepasados jamas se borro. La piedra, el mortero tallado en la roca y la tierra misma conservan nuestro legado."),
    ("WALEDO", "Es una historia de transformacion increible. Caminar por Alta Gracia hoy me hace sentir que el pasado y el presente conviven en cada rincon. Siento que apenas estoy empezando a entender los misterios de este lugar."),
    ("INDIO", "Y no te equivocas, Waledo. Tu travesia por estas tierras recien comienza. Si de verdad deseas descifrar los antiguos secretos de Paravachasca y estar preparado para avanzar al Nivel 3, aun debes completar 2 niveles mas. No apresures tu marcha; observa con atencion, escucha al monte y supera las pruebas que te aguardan. Solo asi seras digno del conocimiento ancestral."),
]

# Dialogo del Nivel 3 ("La Guardiana del Museo"): Waledo se reencuentra con
# Gabriel Dubois y le explica el duelo contra el angel de piedra.
GUION_DUBOIS_NIVEL3 = [
    ("NARRADOR", "Los pasos de Gabriel Dubois resuenan por el patio del museo. Waledo lo espera de pie junto a las viejas reliquias, bajo la sombra del gran arbol."),
    ("WALEDO", "Al fin llegas, Gabriel. Pense que las sombras de los pasillos te habrian desviado del camino."),
    ("NARRADOR", "(Gabriel se ajusta los punios de la chaqueta y da un paso al frente, alzando una ceja.)"),
    ("GABRIEL", "Sabes perfectamente que no soy de los que se pierden facilmente, Waledo. Pero dejate de rodeos. Me mandaste a llamar con urgencia y no creo que haya sido solo para disfrutar de tu compania. Que esta pasando?"),
    ("NARRADOR", "(Waledo baja la mirada y suspira suavemente.)"),
    ("WALEDO", "Lo que pasa, Gabriel, es que la historia que nos contaron a todos sobre este lugar es una mentira piadosa. Y ha llegado el momento de que conozcas la verdad antes de que sea demasiado tarde."),
    ("GABRIEL", "Soy todo oidos. Habla."),
    ("WALEDO", "Hace tres siglos, este valle no estaba gobernado por reyes ni senores feudales, sino por los Guardianes del Umbral. Eran tres artefactos antiguos capaces de mantener en equilibrio la magia pura y la realidad. Durante anios, la paz reino porque los guardianes permanecian escondidos, conectados solo por sellos mistico-elementales."),
    ("GABRIEL", "Y supones que alguien decidio jugar a ser Dios y romper el sello?"),
    ("WALEDO", "Exactamente. Un traidor dentro de la propia orden rompio el equilibrio para reclamar el poder del Umbral para si mismo. La magia comenzo a colapsar. Para evitar el fin absoluto, los sabios supervivientes no destruyeron el poder... lo fragmentaron y lo encerraron tras un complejo mecanismo de pruebas."),
    ("NARRADOR", "(Gabriel se senala a si mismo con una sonrisa amarga.)"),
    ("GABRIEL", "Y por la forma en que me estas mirando, me huelo que ese alguien no vas a ser tu."),
    ("WALEDO", "Mis dias de campo quedaron atras, Gabriel. El equilibrio se esta debilitando de nuevo y las sombras estan despertando. Vos sos el unico que posee la habilidad necesaria para atravesar esta barrera."),
    ("NARRADOR", "(Gabriel se cruza de brazos.)"),
    ("GABRIEL", "Bien. Iluminame. A que me enfrento exactamente?"),
    ("WALEDO", "En este salon duerme una guardiana de piedra: un angel que protege la Espatula de Dubois desde hace generaciones. Solo despierta cuando alguien intenta acercarse a la reliquia."),
    ("GABRIEL", "Un angel de piedra que despierta... Como se supone que la enfrente?"),
    ("WALEDO", "En cuanto despierte te va a lanzar bolas de fuego, una tras otra. Vas a tener que esquivarlas moviendote sin parar. Cuando se quede sin aliento al final de cada ronda, vas a tener un instante para responder con esta energia."),
    ("NARRADOR", "(Waledo le entrega un glifo que brilla con una luz azul.)"),
    ("GABRIEL", "Y si el fuego me alcanza?"),
    ("WALEDO", "Vas a perder parte de tus fuerzas. Si te quedas sin ellas antes de vencerla, la guardiana va a volver a dormir y vamos a tener que empezar de nuevo. Pero si logras apagar su fuego las veces necesarias, la Espatula va a ser tuya."),
    ("NARRADOR", "(Gabriel pierde la sonrisa progresivamente, adoptando una postura seria.)"),
    ("GABRIEL", "Entendido. Esquivar, resistir y atacar en el momento justo. Como en los viejos tiempos."),
    ("WALEDO", "Cuando estes listo, acercate a la guardiana."),
]


# Guarda qué objetos juntó el jugador, su experiencia y medallas.
# También sabe guardar/cargar esos datos en un archivo JSON (el "save").
class Inventario:
    OBJETOS_POSIBLES = {
        "Piedra de Moler": "Herramienta indigena anterior a la colonizacion.",
        "Herramienta Jesuita": "Utensilio usado para construir la iglesia y la estancia.",
        "Llave Maestra": "Llave que abria las puertas del Sierras Hotel en 1901.",
        "Sello Real": "Sello oficial de la corona espaniola en tierras de Gracia.",
        "Cincel del Cantero": "Cincel con el que se tallaron las piedras de la plaza.",
        "Quijote": "Ejemplar que Sarmiento leyo en Alta Gracia de niino.",
        "Metronomo": "Metronomo de Manuel de Falla, compositor en el Villa.",
        "Cantimplora": "Cantimplora de peregrino del siglo XIX.",
        "Espatula de Dubois": "Herramienta del escultor Dubois, residente en Gracia.",
        "Cronoscopio": "Dispositivo que permite viajar por el tiempo.",
        "Cruz de la Estancia": "Cruz bendecida por el cura de la Estancia Jesuitica, entregada a quien demuestra conocer su historia.",
    }

    def __init__(self):
        self.objetos = {nombre: False for nombre in self.OBJETOS_POSIBLES}
        self.turno_viaje = 0
        self.nombre_jugador = "Lediago Waledo"
        self.experiencia = 0
        self.medallas = []

    def agregar(self, nombre):
        if nombre in self.objetos:
            self.objetos[nombre] = True
            return True
        return False

    def tiene(self, nombre):
        return self.objetos.get(nombre, False)

    def recolectados(self):
        return [n for n, v in self.objetos.items() if v]

    def sumar_experiencia(self, puntos):
        self.experiencia += puntos

    def otorgar_medalla(self, nombre):
        if nombre not in self.medallas:
            self.medallas.append(nombre)
            return True
        return False

    def guardar(self):
        datos = {
            "nombre_jugador": self.nombre_jugador,
            "turno_viaje": self.turno_viaje,
            "objetos": self.objetos,
            "experiencia": self.experiencia,
            "medallas": self.medallas,
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    @classmethod
    def cargar(cls):
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
            inv = cls()
            inv.nombre_jugador = datos.get("nombre_jugador", "Lediago Waledo")
            inv.turno_viaje = datos.get("turno_viaje", 0)
            inv.experiencia = datos.get("experiencia", 0)
            inv.medallas = datos.get("medallas", [])
            for nombre, valor in datos.get("objetos", {}).items():
                if nombre in inv.objetos:
                    inv.objetos[nombre] = valor
            return inv
        except (OSError, json.JSONDecodeError):
            return None


# El personaje jugable. Carga el sprite sheet y elige qué cuadro de animación
# mostrar según hacia dónde se mueve (frente/espalda/izquierda/derecha).
class Lediago(arcade.Sprite):
    def __init__(self, escala=0.35):
        super().__init__(scale=escala)
        self.direccion_actual = FRENTE
        self.esta_corriendo = False

        ss = arcade.load_spritesheet(SPRITE_SHEET)
        todos = ss.get_texture_grid(
            size=(SPRITE_FRAME_W, SPRITE_FRAME_H),
            columns=SPRITE_SHEET_COLS,
            count=SPRITE_SHEET_COLS * SPRITE_SHEET_ROWS,
        )

        self._frames_frente = todos[0:4]
        self._frames_lado = todos[4:8]
        self._frames_espalda = todos[8:12]
        self._frames_izquierda = [t.flip_left_right() for t in self._frames_lado]

        self.texture = self._frames_frente[0]
        self._anim_frame = 0
        self._anim_timer = 0.0

    def actualizar_direccion(self):
        if self.change_x < 0:
            self.direccion_actual = IZQUIERDA
        elif self.change_x > 0:
            self.direccion_actual = DERECHA
        elif self.change_y > 0:
            self.direccion_actual = ESPALDA
        elif self.change_y < 0:
            self.direccion_actual = FRENTE

    def _frames_actuales(self):
        if self.direccion_actual == FRENTE:
            return self._frames_frente
        elif self.direccion_actual == ESPALDA:
            return self._frames_espalda
        elif self.direccion_actual == IZQUIERDA:
            return self._frames_izquierda
        else:
            return self._frames_lado

    def update_animation(self, delta_time=1/60):
        if self.change_x == 0 and self.change_y == 0:
            self._anim_frame = 0
            self._anim_timer = 0.0
            self.texture = self._frames_actuales()[0]
            return

        fps = ANIM_FPS * (1.8 if self.esta_corriendo else 1.0)
        self._anim_timer += delta_time
        if self._anim_timer >= 1.0 / fps:
            self._anim_timer -= 1.0 / fps
            frames = self._frames_actuales()
            self._anim_frame = (self._anim_frame + 1) % len(frames)
            self.texture = frames[self._anim_frame]


# Funciones sueltas que usan varias pantallas: calcular distancia (para saber si
# el jugador está cerca de un NPC) y mover al personaje según las teclas W/A/S/D.
def distancia(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)


def mover_personaje(player, w_ap, s_ap, a_ap, d_ap, shift_ap):
    velocidad = VELOCIDAD_CORRER if shift_ap else VELOCIDAD_CAMINAR
    player.esta_corriendo = shift_ap
    player.change_x = 0
    player.change_y = 0
    if w_ap and not s_ap:
        player.change_y = velocidad
    elif s_ap and not w_ap:
        player.change_y = -velocidad
    if a_ap and not d_ap:
        player.change_x = -velocidad
    elif d_ap and not a_ap:
        player.change_x = velocidad
    player.actualizar_direccion()


# Dibuja el cajón de diálogo (nombre + texto + "siguiente") que reutilizan varias escenas
# --- Sistema de voces (edge-tts) -------------------------------------------
# Todo vive en este mismo archivo: la generación (con edge_tts, necesita
# internet) corre una sola vez al arrancar el juego -normalmente instantánea,
# porque solo genera lo que falta- y deja los audios en la carpeta voces/.
# La reproducción después solo busca esos archivos y los pasa por arcade.Sound.
CARPETA_VOCES = BASE_DIR / "voces"
VOLUMEN_VOCES = 1.0

_cache_sonidos_voz = {}
_reproductor_voz_actual = None


def _clave_voz(hablante, texto):
    contenido = f"{hablante}|{texto}".encode("utf-8")
    return hashlib.md5(contenido).hexdigest()[:12]


def _lineas_de_guion(guion):
    """(hablante, texto) de un guion, sin importar si trae un 3er campo (fondo)."""
    for fila in guion:
        yield fila[0], fila[1]


def _todas_las_lineas_de_dialogo():
    guiones = [GUION_INTRO_CURA, GUION_CIERRE_CURA_EXITO, GUION_CIERRE_CURA_FALLO, GUION_JUICIO, GUION_HOTEL, GUION_INDIO_NIVEL2, GUION_DUBOIS_NIVEL3]
    lineas = {}
    for guion in guiones:
        for hablante, texto in _lineas_de_guion(guion):
            lineas[_clave_voz(hablante, texto)] = (hablante, texto)
    return lineas


async def _generar_una_voz(clave, hablante, texto):
    destino = CARPETA_VOCES / f"{clave}.mp3"
    if destino.exists():
        return
    voz = VOCES_PERSONAJE.get(hablante, VOZ_POR_DEFECTO)
    comunicador = edge_tts.Communicate(texto, voz)
    await comunicador.save(str(destino))


async def _generar_voces_faltantes_async():
    CARPETA_VOCES.mkdir(exist_ok=True)
    lineas = _todas_las_lineas_de_dialogo()
    faltantes = {c: ht for c, ht in lineas.items() if not (CARPETA_VOCES / f"{c}.mp3").exists() and not (CARPETA_VOCES / f"{c}.wav").exists()}
    if not faltantes:
        return
    print(f"Generando voces ({len(faltantes)} lineas nuevas, puede tardar un momento)...")
    for clave, (hablante, texto) in faltantes.items():
        try:
            await _generar_una_voz(clave, hablante, texto)
        except Exception as e:
            print(f"  No se pudo generar la voz de {hablante!r}: {e}")
    print("Voces listas.")


def generar_voces_faltantes():
    """Se llama una vez al arrancar el juego (ver main()). Necesita internet
    la primera vez; después no vuelve a tocar los archivos que ya existen."""
    try:
        asyncio.run(_generar_voces_faltantes_async())
    except Exception as e:
        print(f"No se pudieron generar las voces (¿sin internet?): {e}")
        print("El juego va a seguir funcionando, solo que sin voz en las lineas que falten.")


def _sonido_voz(hablante, texto):
    clave = _clave_voz(hablante, texto)
    ruta = CARPETA_VOCES / f"{clave}.wav"
    if not ruta.exists():
        ruta = CARPETA_VOCES / f"{clave}.mp3"
    if not ruta.exists():
        return None
    if ruta not in _cache_sonidos_voz:
        try:
            _cache_sonidos_voz[ruta] = arcade.Sound(str(ruta), streaming=False)
        except Exception:
            _cache_sonidos_voz[ruta] = None
    return _cache_sonidos_voz[ruta]


def reproducir_voz(hablante, texto):
    """Corta la voz que esté sonando y reproduce la de la línea actual.
    Si todavía no se generó el audio de esa línea, no hace nada
    (el juego sigue funcionando igual, solo sin voz en esa línea)."""
    global _reproductor_voz_actual
    if _reproductor_voz_actual is not None:
        try:
            _reproductor_voz_actual.pause()
        except Exception:
            pass
        _reproductor_voz_actual = None
    sonido = _sonido_voz(hablante, texto)
    if sonido is not None:
        _reproductor_voz_actual = sonido.play(volume=VOLUMEN_VOCES)
# -----------------------------------------------------------------------------


def texto_progresivo(texto, tiempo_transcurrido, duracion=DURACION_TEXTO_DIALOGO):
    """Corta el texto según cuánto tiempo pasó, para el efecto de cinemática
    donde las letras van apareciendo de a poco hasta completarse en
    `duracion` segundos."""
    if duracion <= 0 or tiempo_transcurrido >= duracion:
        return texto
    progreso = max(0.0, tiempo_transcurrido / duracion)
    return texto[:int(len(texto) * progreso)]


def dibujar_boton_saltar(x=ANCHO - 160, y=ALTO - 34, w=140, h=26):
    """Botón simple de 'Saltar escena'. Devuelve su rectángulo (x1, y1, x2, y2)
    para poder detectar el click sobre él."""
    arcade.draw_rect_filled(arcade.LRBT(x, x + w, y, y + h), (20, 20, 20, 215))
    arcade.draw_rect_outline(arcade.LRBT(x, x + w, y, y + h), arcade.color.LIGHT_GRAY, border_width=1)
    arcade.draw_text("Saltar escena >>", x + w / 2, y + h / 2, arcade.color.WHITE,
                      font_size=10, anchor_x="center", anchor_y="center", bold=True)
    return (x, y, x + w, y + h)


def click_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2


def dibujar_cuadro_dialogo_generico(hablante_clave, texto, indice, total, fin=False):
    info = HABLANTES[hablante_clave]
    m = 20
    alto_caja = 150
    arcade.draw_rect_filled(arcade.LRBT(m, ANCHO - m, m, alto_caja), (0, 0, 0, 210))
    arcade.draw_rect_outline(arcade.LRBT(m, ANCHO - m, m, alto_caja), info["color_borde"], border_width=3)
    if hablante_clave != "NARRADOR":
        arcade.draw_rect_filled(arcade.LRBT(m, m + 230, alto_caja - 4, alto_caja + 26), (0, 0, 0, 230))
        arcade.draw_rect_outline(arcade.LRBT(m, m + 230, alto_caja - 4, alto_caja + 26), info["color_borde"], border_width=2)
        arcade.draw_text(info["nombre"], m + 14, alto_caja + 3, info["color_nombre"], font_size=13, bold=True, anchor_y="center")
    color_texto = arcade.color.LIGHT_GRAY if hablante_clave == "NARRADOR" else arcade.color.WHITE
    arcade.draw_text(texto, m + 20, alto_caja - 30, color_texto, font_size=15, width=ANCHO - (m * 2) - 40, multiline=True, anchor_y="top")
    if fin:
        pista = "- FIN -  [Espacio] Continuar..."
    else:
        pista = f"{indice + 1}/{total}   [Espacio] Siguiente..."
    arcade.draw_text(pista, ANCHO - m - 10, m + 8, arcade.color.GRAY, font_size=11, anchor_x="right")


# Pantalla inicial: logos animados y después el menú de "presiona cualquier tecla".
# Al arrancar, revisa si hay una partida guardada.
class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tex_futurista = arcade.load_texture(LOGO_FUTURISTA)
        self.tex_cambio = arcade.load_texture(LOGO_CAMBIO)
        self.tex_antiguo = arcade.load_texture(LOGO_ANTIGUO)
        self.tex_menu = arcade.load_texture(MENU_INICIO)
        self.etapa = ETAPA_LOGO_FUTURISTA
        self.tiempo = 0.0
        self.musica = arcade.Sound(MUSICA_FONDO, streaming=False)
        self.reproductor = self.musica.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)
        inv_guardado = Inventario.cargar()
        self._partida_guardada = inv_guardado is not None
        self._inventario = inv_guardado if inv_guardado else Inventario()

    def on_draw(self):
        self.clear()
        if self.etapa == ETAPA_LOGO_FUTURISTA:
            self._dibujar_centrada(self.tex_futurista)
        elif self.etapa == ETAPA_TRANSICION:
            self._dibujar_centrada(self.tex_cambio)
        elif self.etapa == ETAPA_LOGO_ANTIGUO:
            self._dibujar_centrada(self.tex_antiguo)
        elif self.etapa == ETAPA_MENU:
            self._dibujar_centrada(self.tex_menu)
            if int(self.tiempo * 2) % 2 == 0:
                arcade.draw_text("Presiona cualquier tecla o click para comenzar", ANCHO // 2, 40, arcade.color.WHITE, font_size=16, anchor_x="center", bold=True)
            if self._partida_guardada:
                arcade.draw_text("Partida guardada encontrada", ANCHO // 2, 70, arcade.color.GREEN_YELLOW, font_size=12, anchor_x="center")

    def _dibujar_centrada(self, tex):
        escala = min(ANCHO / tex.width, ALTO / tex.height)
        w = tex.width * escala
        h = tex.height * escala
        arcade.draw_texture_rect(tex, arcade.LBWH((ANCHO - w) / 2, (ALTO - h) / 2, w, h))

    def on_update(self, delta_time):
        self.tiempo += delta_time
        limites = {ETAPA_LOGO_FUTURISTA: DURACION_LOGO_FUTURISTA, ETAPA_TRANSICION: DURACION_TRANSICION, ETAPA_LOGO_ANTIGUO: DURACION_LOGO_ANTIGUO}
        if self.etapa in limites and self.tiempo >= limites[self.etapa]:
            self.etapa += 1
            self.tiempo = 0.0

    def on_key_press(self, key, modifiers):
        if self.etapa == ETAPA_MENU:
            self._arrancar()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.etapa == ETAPA_MENU:
            self._arrancar()

    def _arrancar(self):
        juicio = JuicioView(musica_fondo=self.musica, reproductor_musica=self.reproductor, inventario=self._inventario)
        self.window.show_view(juicio)


# Escena del juicio: solo va mostrando el GUION_JUICIO línea por línea
# y cambia el fondo según en qué parte del guion estemos.
class JuicioView(arcade.View):
    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        self.inventario = inventario
        self.texturas_fondo = {
            FONDO_INICIO: arcade.load_texture(JUICIO_FONDO_INICIO),
            FONDO_ACTIVO: arcade.load_texture(JUICIO_FONDO_ACTIVO),
            FONDO_CERRADO: arcade.load_texture(JUICIO_FONDO_CERRADO),
        }
        self.indice = 0
        self.terminado = False
        self.tiempo_linea = 0.0
        self._rect_saltar = None
        reproducir_voz(*GUION_JUICIO[0][:2])

    def on_draw(self):
        self.clear()
        hablante, texto, fondo = GUION_JUICIO[self.indice]
        arcade.draw_texture_rect(self.texturas_fondo[fondo], arcade.LBWH(0, 0, ANCHO, ALTO))
        texto_visible = texto_progresivo(texto, self.tiempo_linea)
        dibujar_cuadro_dialogo_generico(hablante, texto_visible, self.indice, len(GUION_JUICIO), fin=self.terminado)
        if self.terminado:
            arcade.draw_text("FIN DE LA ESCENA", ANCHO // 2, ALTO - 30, arcade.color.WHITE, font_size=14, bold=True, anchor_x="center")
        self._rect_saltar = dibujar_boton_saltar()

    def on_update(self, delta_time):
        self.tiempo_linea += delta_time

    def avanzar(self):
        if self.terminado:
            siguiente_vista = HotelSierrasView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario)
            self.window.show_view(siguiente_vista)
            return
        self.indice += 1
        if self.indice >= len(GUION_JUICIO):
            self.indice = len(GUION_JUICIO) - 1
            self.terminado = True
        self.tiempo_linea = 0.0
        reproducir_voz(*GUION_JUICIO[self.indice][:2])

    def _saltar_escena(self):
        siguiente_vista = HotelSierrasView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario)
        self.window.show_view(siguiente_vista)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            self._saltar_escena()
        elif key in (arcade.key.SPACE, arcade.key.ENTER):
            self.avanzar()

    def on_mouse_press(self, x, y, button, modifiers):
        if self._rect_saltar and click_en_rect(x, y, self._rect_saltar):
            self._saltar_escena()
            return
        self.avanzar()


# Escena del hotel: el jugador camina libremente y, al acercarse al NPC (Walter/Ledo),
# se abre el diálogo del GUION_HOTEL.
class HotelSierrasView(arcade.View):
    FASE_GAMEPLAY = 0
    FASE_DIALOGO = 1

    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.fase = HotelSierrasView.FASE_GAMEPLAY
        self.inventario = inventario or Inventario()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)

        self.tex_fondo = arcade.load_texture(HOTEL_SIERRAS_FONDO)
        self.tex_idle = arcade.load_texture(HOTEL_WALTER_LEDO_IDLE)
        self.tex_afk = arcade.load_texture(HOTEL_WALTER_LEDO_AFK)
        self.tex_dlg = arcade.load_texture(HOTEL_WALTER_LEDO_DLG)

        npc_escala = 155 / 1536
        self.npc_w = int(1024 * npc_escala)
        self.npc_h = int(1536 * npc_escala)
        self.npc_cx = int(ANCHO * 0.74)
        self.npc_cy = int(ALTO * 0.42)

        self.player = Lediago(escala=0.28)
        self.player.center_x = ANCHO * 0.30
        self.player.center_y = 90
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.w_ap = self.s_ap = self.a_ap = self.d_ap = self.shift_ap = False
        self.dialogo_idx = 0
        self.dialogo_fin = False
        self.anim_timer = 0.0
        self.npc_pose_afk = False
        self.tiempo_linea = 0.0
        self._rect_saltar = None

    def _mover_player(self):
        mover_personaje(self.player, self.w_ap, self.s_ap, self.a_ap, self.d_ap, self.shift_ap)

    def _cerca_npc(self):
        d = distancia(self.player.center_x, self.player.center_y, self.npc_cx, self.npc_cy)
        return d < 180

    def _iniciar_dialogo(self):
        self.dialogo_idx = 0
        self.dialogo_fin = False
        self.fase = HotelSierrasView.FASE_DIALOGO
        self.player.change_x = 0
        self.player.change_y = 0
        self.tiempo_linea = 0.0
        reproducir_voz(*GUION_HOTEL[0])

    def _avanzar_dialogo(self):
        if self.dialogo_fin:
            self.window.show_view(VitrinaView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario))
            return
        self.dialogo_idx += 1
        if self.dialogo_idx >= len(GUION_HOTEL):
            self.dialogo_idx = len(GUION_HOTEL) - 1
            self.dialogo_fin = True
        self.tiempo_linea = 0.0
        reproducir_voz(*GUION_HOTEL[self.dialogo_idx])

    def _saltar_dialogo(self):
        self.window.show_view(VitrinaView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario))

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.tex_fondo, arcade.LBWH(0, 0, ANCHO, ALTO))

        if self.fase == HotelSierrasView.FASE_DIALOGO:
            hab = GUION_HOTEL[self.dialogo_idx][0]
            tex_npc = self.tex_dlg if hab in ("WALTER", "LEDO") else self.tex_idle
        else:
            tex_npc = self.tex_afk if self.npc_pose_afk else self.tex_idle

        arcade.draw_texture_rect(tex_npc, arcade.LBWH(self.npc_cx - self.npc_w // 2, self.npc_cy - self.npc_h // 2, self.npc_w, self.npc_h))
        self.player_list.draw()

        if self.fase == HotelSierrasView.FASE_GAMEPLAY and self._cerca_npc():
            arcade.draw_text("[ ESPACIO / CLICK ] Hablar", self.npc_cx, self.npc_cy + self.npc_h // 2 + 14, arcade.color.YELLOW, font_size=11, anchor_x="center", bold=True)

        self._rect_saltar = None
        if self.fase == HotelSierrasView.FASE_DIALOGO:
            hablante, texto = GUION_HOTEL[self.dialogo_idx]
            texto_visible = texto_progresivo(texto, self.tiempo_linea)
            dibujar_cuadro_dialogo_generico(hablante, texto_visible, self.dialogo_idx, len(GUION_HOTEL), fin=self.dialogo_fin)
            self._rect_saltar = dibujar_boton_saltar()

    def on_key_press(self, key, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            if key == arcade.key.W:
                self.w_ap = True
            elif key == arcade.key.S:
                self.s_ap = True
            elif key == arcade.key.A:
                self.a_ap = True
            elif key == arcade.key.D:
                self.d_ap = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = True
            elif key == arcade.key.SPACE and self._cerca_npc():
                self._iniciar_dialogo()
            self._mover_player()
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            if key == arcade.key.TAB:
                self._saltar_dialogo()
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_dialogo()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_ap = False
        elif key == arcade.key.S:
            self.s_ap = False
        elif key == arcade.key.A:
            self.a_ap = False
        elif key == arcade.key.D:
            self.d_ap = False
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_ap = False
        self._mover_player()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fase == HotelSierrasView.FASE_DIALOGO and self._rect_saltar and click_en_rect(x, y, self._rect_saltar):
            self._saltar_dialogo()
            return
        if self.fase == HotelSierrasView.FASE_GAMEPLAY and self._cerca_npc():
            self._iniciar_dialogo()
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            self._avanzar_dialogo()

    def on_update(self, delta_time):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            nueva_x = self.player.center_x + self.player.change_x
            nueva_y = self.player.center_y + self.player.change_y
            mw = self.player.width / 2
            mh = self.player.height / 2
            self.player.center_x = max(mw, min(ANCHO - mw, nueva_x))
            self.player.center_y = max(mh, min(ALTO - mh, nueva_y))
            self.player.update_animation(delta_time)
            self.anim_timer += delta_time
            if self.anim_timer >= 3.5:
                self.anim_timer = 0.0
                self.npc_pose_afk = not self.npc_pose_afk
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            self.tiempo_linea += delta_time


# Escena de la vitrina: permite abrir/cerrar la vitrina, guardar la partida
# y usar el Cronoscopio para pasar a la escena de la Estancia (GameView).
class VitrinaView(arcade.View):
    FASE_CERRADA = "cerrada"
    FASE_ABIERTA = "abierta"

    CRONO_X = 205
    CRONO_Y = 390
    CRONO_W = 100
    CRONO_H = 140

    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.inventario = inventario or Inventario()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)

        self.tex_cerrada = arcade.load_texture(VITRINA_FONDO)
        self.tex_abierta = arcade.load_texture(VITRINA_ABIERTA)
        self.tex_crono = arcade.load_texture(CRONOSCOPIO_IMG)
        self.fase = VitrinaView.FASE_CERRADA

        if not self.inventario.tiene("Cronoscopio"):
            self.inventario.agregar("Cronoscopio")

        self.msg = ""
        self.msg_timer = 0.0
        self.obj_seleccionado = None
        self.desc_visible = False

    def _mostrar_msg(self, texto):
        self.msg = texto
        self.msg_timer = 2.5

    def _guardar(self):
        if self.inventario.guardar():
            self._mostrar_msg("Partida guardada correctamente.")
        else:
            self._mostrar_msg("Error al guardar la partida.")

    def _usar_cronoscopio(self):
        if not self.inventario.tiene("Cronoscopio"):
            self._mostrar_msg("No tienes el Cronoscopio todavia.")
            return
        self.inventario.turno_viaje += 1
        self.inventario.guardar()
        self.window.show_view(GameView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario))

    def _volver_hotel(self):
        self.window.show_view(HotelSierrasView(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario))

    def on_draw(self):
        self.clear()
        if self.fase == VitrinaView.FASE_CERRADA:
            arcade.draw_texture_rect(self.tex_cerrada, arcade.LBWH(0, 0, ANCHO, ALTO))
        else:
            arcade.draw_texture_rect(self.tex_abierta, arcade.LBWH(0, 0, ANCHO, ALTO))
            if self.inventario.tiene("Cronoscopio"):
                arcade.draw_texture_rect(self.tex_crono, arcade.LBWH(self.CRONO_X - self.CRONO_W // 2, self.CRONO_Y - self.CRONO_H // 2, self.CRONO_W, self.CRONO_H))
                arcade.draw_rect_outline(arcade.LRBT(self.CRONO_X - self.CRONO_W // 2 - 3, self.CRONO_X + self.CRONO_W // 2 + 3, self.CRONO_Y - self.CRONO_H // 2 - 3, self.CRONO_Y + self.CRONO_H // 2 + 3), (80, 200, 255, 180), border_width=2)
            self._dibujar_lista_objetos()

        self._dibujar_controles()

        if self.desc_visible and self.obj_seleccionado:
            self._dibujar_descripcion()

        if self.msg_timer > 0:
            arcade.draw_rect_filled(arcade.LRBT(80, ANCHO - 80, 260, 320), (0, 0, 0, 210))
            arcade.draw_rect_outline(arcade.LRBT(80, ANCHO - 80, 260, 320), arcade.color.CYAN, border_width=2)
            arcade.draw_text(self.msg, ANCHO // 2, 290, arcade.color.WHITE, font_size=13, anchor_x="center", anchor_y="center", width=ANCHO - 200, multiline=True)

    def _dibujar_controles(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, 54), (0, 0, 0, 200))
        estado = "Abrir vitrina" if self.fase == VitrinaView.FASE_CERRADA else "Cerrar vitrina"
        controles = [("[E] Salir al Hotel", arcade.color.YELLOW), (f"[V] {estado}", arcade.color.CYAN), ("[G] Guardar partida", arcade.color.GREEN_YELLOW), ("[C] Usar Cronoscopio", arcade.color.LIGHT_PASTEL_PURPLE)]
        paso = ANCHO // len(controles)
        for i, (texto, color) in enumerate(controles):
            arcade.draw_text(texto, paso * i + paso // 2, 20, color, font_size=11, bold=True, anchor_x="center", anchor_y="center")

    def _dibujar_lista_objetos(self):
        recolectados = self.inventario.recolectados()
        if not recolectados:
            return
        x = 510
        y = 530
        arcade.draw_rect_filled(arcade.LRBT(x - 10, ANCHO - 8, 60, y + 10), (0, 0, 0, 170))
        arcade.draw_rect_outline(arcade.LRBT(x - 10, ANCHO - 8, 60, y + 10), arcade.color.GOLD, border_width=1)
        arcade.draw_text("OBJETOS RECOLECTADOS", x + 120, y, arcade.color.GOLD, font_size=10, bold=True, anchor_x="center")
        for idx, nombre in enumerate(recolectados):
            y_item = y - 22 - idx * 18
            if y_item < 70:
                break
            arcade.draw_text(f"• {nombre}", x, y_item, arcade.color.WHITE, font_size=10)

    def _dibujar_descripcion(self):
        nombre = self.obj_seleccionado
        desc = Inventario.OBJETOS_POSIBLES.get(nombre, "")
        m = 60
        arcade.draw_rect_filled(arcade.LRBT(m, ANCHO - m, 200, 420), (10, 10, 30, 230))
        arcade.draw_rect_outline(arcade.LRBT(m, ANCHO - m, 200, 420), arcade.color.GOLD, border_width=2)
        arcade.draw_text(nombre, ANCHO // 2, 405, arcade.color.GOLD, font_size=16, bold=True, anchor_x="center")
        arcade.draw_text(desc, m + 20, 380, arcade.color.WHITE, font_size=13, width=ANCHO - m * 2 - 40, multiline=True, anchor_y="top")
        arcade.draw_text("[Click] Cerrar", ANCHO // 2, 215, arcade.color.GRAY, font_size=11, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.desc_visible:
            self.desc_visible = False
            self.obj_seleccionado = None
            return
        if key == arcade.key.E:
            self._volver_hotel()
        elif key == arcade.key.V:
            self.fase = VitrinaView.FASE_ABIERTA if self.fase == VitrinaView.FASE_CERRADA else VitrinaView.FASE_CERRADA
        elif key == arcade.key.G:
            self._guardar()
        elif key == arcade.key.C:
            self._usar_cronoscopio()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.desc_visible:
            self.desc_visible = False
            self.obj_seleccionado = None
            return
        if self.inventario.tiene("Cronoscopio") and self.fase == VitrinaView.FASE_ABIERTA:
            hw, hh = self.CRONO_W // 2, self.CRONO_H // 2
            if (self.CRONO_X - hw <= x <= self.CRONO_X + hw) and (self.CRONO_Y - hh <= y <= self.CRONO_Y + hh):
                self.obj_seleccionado = "Cronoscopio"
                self.desc_visible = True

    def on_update(self, delta_time):
        if self.msg_timer > 0:
            self.msg_timer = max(0, self.msg_timer - delta_time)


# Escena de la Estancia: caminar, hablar con el Cura, responder la trivia
# de 7 preguntas y, si aprueba, recibir la Cruz de la Estancia (fin de la demo).
class GameView(arcade.View):
    CURA_CX = 150
    CURA_CY = 230
    CURA_ESCALA = 0.65

    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.estado = ESTADO_JUGANDO
        self.inventario = inventario or Inventario()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)

        self.fondo = arcade.load_texture(FONDO_ESTANCIA)
        self.tex_cura_idle = arcade.load_texture(CURA_IDLE)
        self.tex_cura_dlg = arcade.load_texture(CURA_DIALOGO)
        self.tex_cura_sen = arcade.load_texture(CURA_SENALANDO)
        self.tex_cruz = arcade.load_texture(CRUZ_ESTANCIA_IMG)

        self.player = Lediago(escala=ESCALA_PERSONAJE)
        self.player.center_x = ANCHO // 2
        self.player.center_y = ALTO // 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.w_ap = self.s_ap = self.a_ap = self.d_ap = self.shift_ap = False

        self.guion_cura = []
        self.indice_cura = 0
        self.indice_pregunta = 0
        self.respuestas_ok = 0
        self.opcion_hover = None
        self.feedback_visible = False
        self.feedback_correcta = False
        self.ultima_opcion = -1
        self.mostrar_recompensa = False
        self.tiempo_linea = 0.0
        self._rect_saltar = None

    def _cerca_cura(self):
        d = distancia(self.player.center_x, self.player.center_y, self.CURA_CX, self.CURA_CY)
        return d < 110

    def _mover_player(self):
        mover_personaje(self.player, self.w_ap, self.s_ap, self.a_ap, self.d_ap, self.shift_ap)

    def _iniciar_intro_cura(self):
        self.guion_cura = GUION_INTRO_CURA
        self.indice_cura = 0
        self.estado = ESTADO_INTRO_CURA
        self.player.change_x = 0
        self.player.change_y = 0
        self.tiempo_linea = 0.0
        reproducir_voz(*self.guion_cura[0])

    def _avanzar_intro(self):
        self.indice_cura += 1
        self.tiempo_linea = 0.0
        if self.indice_cura >= len(self.guion_cura):
            self.estado = ESTADO_TRIVIA
            self.indice_pregunta = 0
            self.respuestas_ok = 0
            self.feedback_visible = False
        else:
            reproducir_voz(*self.guion_cura[self.indice_cura])

    def _saltar_dialogo_cura(self):
        """Salta el resto del diálogo actual del Cura (intro o cierre)."""
        if self.estado == ESTADO_INTRO_CURA:
            self.estado = ESTADO_TRIVIA
            self.indice_pregunta = 0
            self.respuestas_ok = 0
            self.feedback_visible = False
        elif self.estado == ESTADO_CIERRE_CURA:
            self.estado = ESTADO_FIN_DEMO

    # Revisa si la opción elegida es la correcta y guarda el resultado para mostrar feedback
    def _responder(self, opcion):
        if self.feedback_visible:
            return
        _, opciones, correcta = PREGUNTAS_ESTANCIA[self.indice_pregunta]
        if opcion < 0 or opcion >= len(opciones):
            return
        self.feedback_correcta = (opcion == correcta)
        if self.feedback_correcta:
            self.respuestas_ok += 1
        self.ultima_opcion = opcion
        self.feedback_visible = True

    def _siguiente_pregunta(self):
        self.indice_pregunta += 1
        self.feedback_visible = False
        if self.indice_pregunta >= len(PREGUNTAS_ESTANCIA):
            gano = self.respuestas_ok >= PREGUNTAS_MINIMAS_PARA_GANAR
            if gano:
                self.guion_cura = GUION_CIERRE_CURA_EXITO
                ya_tenia = self.inventario.tiene("Cruz de la Estancia")
                self.inventario.agregar("Cruz de la Estancia")
                self.inventario.sumar_experiencia(XP_RECOMPENSA_TRIVIA)
                self.inventario.otorgar_medalla(MEDALLA_HISTORIADOR)
                self.inventario.guardar()
                self.mostrar_recompensa = not ya_tenia
            else:
                self.guion_cura = GUION_CIERRE_CURA_FALLO
                self.mostrar_recompensa = False
            self.indice_cura = 0
            self.estado = ESTADO_CIERRE_CURA
            self.tiempo_linea = 0.0
            reproducir_voz(*self.guion_cura[0])

    def _avanzar_cierre(self):
        self.indice_cura += 1
        self.tiempo_linea = 0.0
        if self.indice_cura >= len(self.guion_cura):
            self.estado = ESTADO_FIN_DEMO
        else:
            reproducir_voz(*self.guion_cura[self.indice_cura])

    def _rect_opcion(self, i):
        m = 60
        alto = 42
        espacio = 8
        y_tope = ALTO - 210
        y2 = y_tope - i * (alto + espacio)
        y1 = y2 - alto
        return (m, y1, ANCHO - m, y2)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, ANCHO, ALTO))

        if self.estado in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA):
            tex_cura = self.tex_cura_dlg
        elif self.estado == ESTADO_TRIVIA:
            tex_cura = self.tex_cura_sen
        else:
            tex_cura = self.tex_cura_idle

        cw = int(tex_cura.width * self.CURA_ESCALA)
        ch = int(tex_cura.height * self.CURA_ESCALA)
        arcade.draw_texture_rect(tex_cura, arcade.LBWH(self.CURA_CX - cw // 2, self.CURA_CY - ch // 2, cw, ch))
        self.player_list.draw()

        if self.estado == ESTADO_JUGANDO and self._cerca_cura():
            arcade.draw_text("[ ESPACIO / CLICK ] Hablar con el Cura", ANCHO // 2, self.CURA_CY + 160, arcade.color.YELLOW, font_size=11, anchor_x="center", bold=True)

        self._rect_saltar = None
        if self.estado in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA):
            nombre, texto = self.guion_cura[self.indice_cura]
            texto_visible = texto_progresivo(texto, self.tiempo_linea)
            hablante_key = "CURA" if nombre == "CURA" else "LEDIAGO"
            m = 20
            alto_caja = 150
            color = arcade.color.GOLD if nombre == "CURA" else arcade.color.LIGHT_PASTEL_PURPLE
            arcade.draw_rect_filled(arcade.LRBT(m, ANCHO - m, m, alto_caja), (0, 0, 0, 210))
            arcade.draw_rect_outline(arcade.LRBT(m, ANCHO - m, m, alto_caja), color, border_width=3)
            arcade.draw_rect_filled(arcade.LRBT(m, m + 170, alto_caja - 4, alto_caja + 26), (0, 0, 0, 230))
            arcade.draw_rect_outline(arcade.LRBT(m, m + 170, alto_caja - 4, alto_caja + 26), color, border_width=2)
            etiqueta = "CURA DE LA ESTANCIA" if nombre == "CURA" else "LEDIAGO WALEDO"
            arcade.draw_text(etiqueta, m + 14, alto_caja + 3, color, font_size=12, bold=True, anchor_y="center")
            arcade.draw_text(texto_visible, m + 20, alto_caja - 30, arcade.color.WHITE, font_size=15, width=ANCHO - (m * 2) - 40, multiline=True, anchor_y="top")
            arcade.draw_text("[Espacio] Continuar...", ANCHO - m - 10, m + 8, arcade.color.GRAY, font_size=11, anchor_x="right")
            self._rect_saltar = dibujar_boton_saltar()

        elif self.estado == ESTADO_TRIVIA:
            self._dibujar_trivia()

        elif self.estado == ESTADO_FIN_DEMO:
            self._dibujar_fin_demo()

    def _dibujar_trivia(self):
        texto, opciones, correcta = PREGUNTAS_ESTANCIA[self.indice_pregunta]
        m = 50
        y_top = ALTO - 60
        arcade.draw_rect_filled(arcade.LRBT(m, ANCHO - m, ALTO - 180, y_top + 20), (10, 10, 30, 230))
        arcade.draw_rect_outline(arcade.LRBT(m, ANCHO - m, ALTO - 180, y_top + 20), arcade.color.GOLD, border_width=2)
        arcade.draw_text(f"Pregunta {self.indice_pregunta + 1}/{len(PREGUNTAS_ESTANCIA)}", ANCHO // 2, y_top, arcade.color.GOLD, font_size=12, bold=True, anchor_x="center")
        arcade.draw_text(texto, m + 20, y_top - 26, arcade.color.WHITE, font_size=14, width=ANCHO - (m * 2) - 40, multiline=True, anchor_y="top")

        letras = ["A", "B", "C", "D"]
        for i, op in enumerate(opciones):
            x1, y1, x2, y2 = self._rect_opcion(i)
            if self.feedback_visible:
                if i == correcta:
                    color_fondo = (40, 130, 40, 235)
                elif i == self.ultima_opcion and not self.feedback_correcta:
                    color_fondo = (150, 30, 30, 235)
                else:
                    color_fondo = (25, 25, 45, 200)
            else:
                color_fondo = (60, 50, 20, 235) if self.opcion_hover == i else (25, 25, 45, 200)
            arcade.draw_rect_filled(arcade.LRBT(x1, x2, y1, y2), color_fondo)
            arcade.draw_rect_outline(arcade.LRBT(x1, x2, y1, y2), arcade.color.GOLD, border_width=1)
            arcade.draw_text(f"{letras[i]}) {op}", x1 + 14, (y1 + y2) // 2, arcade.color.WHITE, font_size=13, anchor_y="center", width=x2 - x1 - 24, multiline=True)

        if self.feedback_visible:
            msg = "Correcto!" if self.feedback_correcta else "Incorrecto."
            col = arcade.color.GREEN_YELLOW if self.feedback_correcta else arcade.color.RED_DEVIL
            arcade.draw_text(msg, ANCHO // 2, 22, col, font_size=14, bold=True, anchor_x="center")
        else:
            arcade.draw_text("[1-4] o [Click] para responder", ANCHO // 2, 22, arcade.color.GRAY, font_size=11, anchor_x="center")

    def _dibujar_fin_demo(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, ALTO), (0, 0, 0, 215))

        if self.mostrar_recompensa:
            arcade.draw_texture_rect(self.tex_cruz, arcade.LBWH(ANCHO // 2 - 55, 440, 110, 110))
            arcade.draw_text("*** DESBLOQUEASTE LA CRUZ DE LA ESTANCIA ***", ANCHO // 2, 430, arcade.color.GOLD, font_size=16, bold=True, anchor_x="center")
            arcade.draw_text("Cruz de la Estancia agregada a tu inventario", ANCHO // 2, 400, arcade.color.WHITE, font_size=13, anchor_x="center")
            arcade.draw_text(f"+{XP_RECOMPENSA_TRIVIA} Experiencia   |   Medalla: \"{MEDALLA_HISTORIADOR}\"", ANCHO // 2, 375, arcade.color.LIGHT_PASTEL_PURPLE, font_size=12, anchor_x="center")
        else:
            arcade.draw_text("Podras intentarlo de nuevo...", ANCHO // 2, 430, arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center")

        arcade.draw_text("FIN DE LA DEMO", ANCHO // 2, 280, arcade.color.WHITE, font_size=32, bold=True, anchor_x="center")
        arcade.draw_text("El Cronoscopio ya detecta tu proximo destino...", ANCHO // 2, 235, arcade.color.LIGHT_GRAY, font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Continuar tu viaje", ANCHO // 2, 60, arcade.color.GRAY, font_size=11, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.estado == ESTADO_JUGANDO:
            if key == arcade.key.W:
                self.w_ap = True
            elif key == arcade.key.S:
                self.s_ap = True
            elif key == arcade.key.A:
                self.a_ap = True
            elif key == arcade.key.D:
                self.d_ap = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = True
            elif key == arcade.key.SPACE and self._cerca_cura():
                self._iniciar_intro_cura()
            self._mover_player()

        elif self.estado in (ESTADO_INTRO_CURA,):
            if key == arcade.key.TAB:
                self._saltar_dialogo_cura()
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_intro()

        elif self.estado == ESTADO_TRIVIA:
            if not self.feedback_visible:
                mapa = {arcade.key.KEY_1: 0, arcade.key.KEY_2: 1, arcade.key.KEY_3: 2, arcade.key.KEY_4: 3}
                if key in mapa:
                    self.ultima_opcion = mapa[key]
                    self._responder(mapa[key])
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._siguiente_pregunta()

        elif self.estado == ESTADO_CIERRE_CURA:
            if key == arcade.key.TAB:
                self._saltar_dialogo_cura()
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_cierre()

        elif self.estado == ESTADO_FIN_DEMO:
            if key == arcade.key.SPACE:
                siguiente_vista = Nivel2View(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario)
                self.window.show_view(siguiente_vista)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_ap = False
        elif key == arcade.key.S:
            self.s_ap = False
        elif key == arcade.key.A:
            self.a_ap = False
        elif key == arcade.key.D:
            self.d_ap = False
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_ap = False
        if self.estado == ESTADO_JUGANDO:
            self._mover_player()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.estado == ESTADO_TRIVIA and not self.feedback_visible:
            self.opcion_hover = None
            for i in range(4):
                x1, y1, x2, y2 = self._rect_opcion(i)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.opcion_hover = i
                    break

    def on_mouse_press(self, x, y, button, modifiers):
        if self.estado in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA) and self._rect_saltar and click_en_rect(x, y, self._rect_saltar):
            self._saltar_dialogo_cura()
            return
        if self.estado == ESTADO_JUGANDO and self._cerca_cura():
            self._iniciar_intro_cura()
        elif self.estado == ESTADO_INTRO_CURA:
            self._avanzar_intro()
        elif self.estado == ESTADO_TRIVIA:
            if not self.feedback_visible:
                for i in range(4):
                    x1, y1, x2, y2 = self._rect_opcion(i)
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        self.ultima_opcion = i
                        self._responder(i)
                        break
            else:
                self._siguiente_pregunta()
        elif self.estado == ESTADO_CIERRE_CURA:
            self._avanzar_cierre()

    def on_update(self, delta_time):
        if self.estado == ESTADO_JUGANDO:
            nueva_x = self.player.center_x + self.player.change_x
            nueva_y = self.player.center_y + self.player.change_y
            mw = self.player.width / 2
            mh = self.player.height / 2
            self.player.center_x = max(mw, min(ANCHO - mw, nueva_x))
            self.player.center_y = max(mh, min(ALTO - mh, nueva_y))
            self.player.update_animation(delta_time)
        elif self.estado in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA):
            self.tiempo_linea += delta_time


# Nivel 2 - "Senderos de Paravachasca": primero Waledo conversa con el Indio
# (dialogo con voz, igual que las demas escenas) y despues tiene que esquivar,
# durante 2 minutos, las lanzas que van cayendo desde arriba de la pantalla.
# Si una lanza lo toca pierde una vida; si se queda sin vidas, pierde el nivel.
# Si aguanta los 2 minutos completos, gana la Piedra de Moler.
class Nivel2View(arcade.View):
    FASE_DIALOGO = 0
    FASE_JUEGO = 1
    FASE_VICTORIA = 2
    FASE_DERROTA = 3

    JUGADOR_Y = 90  # altura fija donde se mueve el jugador (solo izquierda/derecha)

    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.inventario = inventario or Inventario()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)

        self.fondo = arcade.load_texture(FONDO_SUBNIVEL1)
        self.tex_indio_dlg = arcade.load_texture(INDIO_DIALOGO_IMG)
        self.tex_indio_idle = arcade.load_texture(INDIO_IDLE_IMG)
        self.tex_lanza = arcade.load_texture(LANZA_IMG)

        # --- fase de dialogo ---
        self.fase = Nivel2View.FASE_DIALOGO
        self.indice_dialogo = 0
        self.tiempo_linea = 0.0
        self._rect_saltar = None
        reproducir_voz(*GUION_INDIO_NIVEL2[0])

        # --- jugador ---
        self.player = Lediago(escala=ESCALA_PERSONAJE)
        self.player.center_x = ANCHO // 2
        self.player.center_y = Nivel2View.JUGADOR_Y
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.a_ap = self.d_ap = False

        # --- minijuego de esquivar lanzas ---
        self.lanza_list = arcade.SpriteList()
        self.tiempo_restante = NIVEL2_DURACION_SEGUNDOS
        self.vidas = NIVEL2_VIDAS
        self.tiempo_spawn = 0.0
        self.invulnerable_seg = 0.0
        self.mostro_recompensa = False

    # ---------------- fase de dialogo ----------------
    def _avanzar_dialogo(self):
        self.indice_dialogo += 1
        self.tiempo_linea = 0.0
        if self.indice_dialogo >= len(GUION_INDIO_NIVEL2):
            self._iniciar_juego()
        else:
            reproducir_voz(*GUION_INDIO_NIVEL2[self.indice_dialogo])

    def _iniciar_juego(self):
        self.fase = Nivel2View.FASE_JUEGO
        self.player.center_x = ANCHO // 2
        self.player.center_y = Nivel2View.JUGADOR_Y
        self.player.change_x = 0
        self.player.change_y = 0

    # ---------------- fase del minijuego ----------------
    def _spawn_lanza(self):
        lanza = arcade.Sprite(scale=NIVEL2_ESCALA_LANZA)
        lanza.texture = self.tex_lanza
        lanza.center_x = random.randint(40, ANCHO - 40)
        lanza.bottom = ALTO + 10
        progreso = 1.0 - (self.tiempo_restante / NIVEL2_DURACION_SEGUNDOS)
        velocidad = NIVEL2_VELOCIDAD_LANZA_MIN + (NIVEL2_VELOCIDAD_LANZA_MAX - NIVEL2_VELOCIDAD_LANZA_MIN) * progreso
        lanza.change_y = -velocidad
        self.lanza_list.append(lanza)

    def _intervalo_spawn_actual(self):
        progreso = 1.0 - (self.tiempo_restante / NIVEL2_DURACION_SEGUNDOS)
        intervalo = NIVEL2_INTERVALO_SPAWN_INICIAL - (NIVEL2_INTERVALO_SPAWN_INICIAL - NIVEL2_INTERVALO_SPAWN_MINIMO) * progreso
        return max(NIVEL2_INTERVALO_SPAWN_MINIMO, intervalo)

    def _mover_player_horizontal(self):
        velocidad = VELOCIDAD_CORRER
        self.player.change_x = 0
        if self.a_ap and not self.d_ap:
            self.player.change_x = -velocidad
        elif self.d_ap and not self.a_ap:
            self.player.change_x = velocidad
        self.player.actualizar_direccion()

    def _actualizar_juego(self, delta_time):
        self._mover_player_horizontal()
        mw = self.player.width / 2
        nueva_x = self.player.center_x + self.player.change_x
        self.player.center_x = max(mw, min(ANCHO - mw, nueva_x))
        self.player.update_animation(delta_time)

        if self.invulnerable_seg > 0:
            self.invulnerable_seg = max(0.0, self.invulnerable_seg - delta_time)
        self.player.alpha = 130 if (self.invulnerable_seg > 0 and int(self.invulnerable_seg * 12) % 2 == 0) else 255

        self.tiempo_restante -= delta_time
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self._ganar()
            return

        self.tiempo_spawn += delta_time
        if self.tiempo_spawn >= self._intervalo_spawn_actual():
            self.tiempo_spawn = 0.0
            self._spawn_lanza()

        for lanza in self.lanza_list:
            lanza.center_y += lanza.change_y * delta_time
        for lanza in list(self.lanza_list):
            if lanza.top < 0:
                lanza.remove_from_sprite_lists()

        if self.invulnerable_seg <= 0:
            golpes = arcade.check_for_collision_with_list(self.player, self.lanza_list)
            if golpes:
                for l in golpes:
                    l.remove_from_sprite_lists()
                self.vidas -= 1
                self.invulnerable_seg = NIVEL2_TIEMPO_INVULNERABLE
                if self.vidas <= 0:
                    self._perder()

    def _ganar(self):
        self.fase = Nivel2View.FASE_VICTORIA
        self.lanza_list.clear()
        ya_tenia = self.inventario.tiene("Piedra de Moler")
        self.inventario.agregar("Piedra de Moler")
        self.inventario.sumar_experiencia(XP_RECOMPENSA_NIVEL2)
        self.inventario.otorgar_medalla(MEDALLA_PARAVACHASCA)
        self.inventario.guardar()
        self.mostro_recompensa = not ya_tenia

    def _perder(self):
        self.fase = Nivel2View.FASE_DERROTA
        self.lanza_list.clear()

    def _reintentar_juego(self):
        self.fase = Nivel2View.FASE_JUEGO
        self.tiempo_restante = NIVEL2_DURACION_SEGUNDOS
        self.vidas = NIVEL2_VIDAS
        self.tiempo_spawn = 0.0
        self.invulnerable_seg = 0.0
        self.lanza_list.clear()
        self.player.alpha = 255
        self.player.center_x = ANCHO // 2
        self.player.center_y = Nivel2View.JUGADOR_Y

    # ---------------- dibujado ----------------
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, ANCHO, ALTO))
        arcade.draw_text(TITULO_NIVEL2, 14, ALTO - 22, arcade.color.WHITE, font_size=11, bold=True)

        if self.fase == Nivel2View.FASE_DIALOGO:
            self._dibujar_dialogo()
        elif self.fase == Nivel2View.FASE_JUEGO:
            self._dibujar_indio_espectador()
            self.lanza_list.draw()
            self.player_list.draw()
            self._dibujar_hud_juego()
        elif self.fase == Nivel2View.FASE_VICTORIA:
            self._dibujar_victoria()
        elif self.fase == Nivel2View.FASE_DERROTA:
            self._dibujar_derrota()

    def _dibujar_dialogo(self):
        iw = int(self.tex_indio_dlg.width * 0.48)
        ih = int(self.tex_indio_dlg.height * 0.48)
        arcade.draw_texture_rect(self.tex_indio_dlg, arcade.LBWH(ANCHO - iw - 30, 165, iw, ih))

        hablante, texto = GUION_INDIO_NIVEL2[self.indice_dialogo]
        texto_visible = texto_progresivo(texto, self.tiempo_linea)
        es_ultima = self.indice_dialogo == len(GUION_INDIO_NIVEL2) - 1
        fin = es_ultima and texto_visible == texto
        dibujar_cuadro_dialogo_generico(hablante, texto_visible, self.indice_dialogo, len(GUION_INDIO_NIVEL2), fin=fin)
        self._rect_saltar = dibujar_boton_saltar()

    def _dibujar_indio_espectador(self):
        """El Indio observa la prueba desde un costado (solo decorativo)."""
        iw = int(self.tex_indio_idle.width * 0.35)
        ih = int(self.tex_indio_idle.height * 0.35)
        arcade.draw_texture_rect(self.tex_indio_idle, arcade.LBWH(20, Nivel2View.JUGADOR_Y - ih // 2, iw, ih))

    def _dibujar_hud_juego(self):
        m = 14
        segundos = max(0, int(self.tiempo_restante))
        mm, ss = divmod(segundos, 60)
        arcade.draw_text(f"Tiempo: {mm:01d}:{ss:02d}", ANCHO - m, ALTO - 22, arcade.color.WHITE, font_size=13, bold=True, anchor_x="right")
        arcade.draw_text(f"Vidas: {'*' * self.vidas}{'.' * (NIVEL2_VIDAS - self.vidas)}", ANCHO - m, ALTO - 44, arcade.color.RED_DEVIL, font_size=13, bold=True, anchor_x="right")
        arcade.draw_text("[A] [D] para moverte - Esquiva las lanzas!", ANCHO // 2, 20, arcade.color.LIGHT_GRAY, font_size=11, anchor_x="center")

    def _dibujar_victoria(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, ALTO), (0, 0, 0, 215))
        if self.mostro_recompensa:
            arcade.draw_text("*** SUPERASTE EL NIVEL 2 ***", ANCHO // 2, 430, arcade.color.GOLD, font_size=18, bold=True, anchor_x="center")
            arcade.draw_text("Piedra de Moler agregada a tu inventario", ANCHO // 2, 400, arcade.color.WHITE, font_size=13, anchor_x="center")
            arcade.draw_text(f"+{XP_RECOMPENSA_NIVEL2} Experiencia   |   Medalla: \"{MEDALLA_PARAVACHASCA}\"", ANCHO // 2, 375, arcade.color.LIGHT_PASTEL_PURPLE, font_size=12, anchor_x="center")
        else:
            arcade.draw_text("Resististe la prueba del monte una vez mas.", ANCHO // 2, 400, arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center")
        arcade.draw_text("SENDEROS DE PARAVACHASCA SUPERADO", ANCHO // 2, 300, arcade.color.WHITE, font_size=24, bold=True, anchor_x="center")
        arcade.draw_text("Gabriel Dubois te espera en el museo...", ANCHO // 2, 255, arcade.color.LIGHT_GRAY, font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Continuar tu viaje", ANCHO // 2, 60, arcade.color.GRAY, font_size=11, anchor_x="center")

    def _dibujar_derrota(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, ALTO), (0, 0, 0, 215))
        arcade.draw_text("Una lanza te alcanzo...", ANCHO // 2, 340, arcade.color.RED_DEVIL, font_size=18, bold=True, anchor_x="center")
        arcade.draw_text("El sabio del monte todavia no te considera listo.", ANCHO // 2, 300, arcade.color.LIGHT_GRAY, font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Reintentar", ANCHO // 2, 60, arcade.color.GRAY, font_size=11, anchor_x="center")

    # ---------------- input ----------------
    def on_key_press(self, key, modifiers):
        if self.fase == Nivel2View.FASE_DIALOGO:
            if key == arcade.key.TAB:
                self._iniciar_juego()
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_dialogo()

        elif self.fase == Nivel2View.FASE_JUEGO:
            if key == arcade.key.A:
                self.a_ap = True
            elif key == arcade.key.D:
                self.d_ap = True

        elif self.fase == Nivel2View.FASE_VICTORIA:
            if key == arcade.key.SPACE:
                siguiente_vista = Nivel3View(musica_fondo=self.musica_fondo, reproductor_musica=self.reproductor_musica, inventario=self.inventario)
                self.window.show_view(siguiente_vista)

        elif self.fase == Nivel2View.FASE_DERROTA:
            if key == arcade.key.SPACE:
                self._reintentar_juego()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_ap = False
        elif key == arcade.key.D:
            self.d_ap = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fase == Nivel2View.FASE_DIALOGO:
            if self._rect_saltar and click_en_rect(x, y, self._rect_saltar):
                self._iniciar_juego()
                return
            self._avanzar_dialogo()

    def on_update(self, delta_time):
        if self.fase == Nivel2View.FASE_DIALOGO:
            self.tiempo_linea += delta_time
        elif self.fase == Nivel2View.FASE_JUEGO:
            self._actualizar_juego(delta_time)


# Nivel 3 - "La Guardiana del Museo": Waledo se reencuentra con Gabriel Dubois
# (dialogo con voz) y despues Dubois se enfrenta al angel de piedra que
# custodia la Espatula de Dubois: primero hay que esquivar sus bolas de
# fuego y despues, cuando el angel se queda sin aliento, hay una ventana
# para responder con una bola de energia azul. Se repite por rondas hasta
# vaciar la vida del angel.
class Nivel3View(arcade.View):
    FASE_DIALOGO = 0
    FASE_ESQUIVAR = 1
    FASE_ATAQUE = 2
    FASE_VICTORIA = 3
    FASE_DERROTA = 4

    JUGADOR_Y = 90

    def __init__(self, musica_fondo=None, reproductor_musica=None, inventario=None):
        super().__init__()
        self.inventario = inventario or Inventario()
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(volume=VOLUMEN_MUSICA_FONDO, loop=True)

        self.fondo = arcade.load_texture(FONDO_MUSEO)
        self.tex_dubois_dlg = arcade.load_texture(DUBOIS_DIALOGO_IMG)
        self.tex_angel_idle = arcade.load_texture(ANGEL_IDLE_IMG)
        self.tex_angel_carga = arcade.load_texture(ANGEL_CARGA_IMG)
        self.tex_angel_lanza = arcade.load_texture(ANGEL_LANZA_IMG)
        self.tex_fuego_ataque = arcade.load_texture(BOLA_FUEGO_ATAQUE_IMG)
        self.tex_fuego_defensa = arcade.load_texture(BOLA_FUEGO_DEFENSA_IMG)

        # --- fase de dialogo ---
        self.fase = Nivel3View.FASE_DIALOGO
        self.indice_dialogo = 0
        self.tiempo_linea = 0.0
        self._rect_saltar = None
        reproducir_voz(*GUION_DUBOIS_NIVEL3[0])

        # --- jugador (Gabriel Dubois entra en accion) ---
        self.player = Lediago(escala=ESCALA_PERSONAJE)
        self.player.center_x = ANCHO // 2
        self.player.center_y = Nivel3View.JUGADOR_Y
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.a_ap = self.d_ap = False

        # --- el angel (guardiana) ---
        self.angel = arcade.Sprite(scale=NIVEL3_ESCALA_ANGEL)
        self.angel.texture = self.tex_angel_idle
        self.angel.center_x = NIVEL3_ANGEL_X
        self.angel.center_y = NIVEL3_ANGEL_Y
        self.angel_list = arcade.SpriteList()
        self.angel_list.append(self.angel)
        self.angel_vida = NIVEL3_VIDA_ANGEL
        self.angel_invulnerable_seg = 0.0

        # --- proyectiles ---
        self.fuegos_list = arcade.SpriteList()
        self.bolas_azules_list = arcade.SpriteList()

        # --- estado de rondas ---
        self.ronda = 1
        self.tiempo_carga_restante = 0.0
        self.fuegos_por_lanzar = 0
        self.tiempo_spawn = 0.0
        self.vidas = NIVEL3_VIDAS_JUGADOR
        self.invulnerable_seg = 0.0
        self.mostro_recompensa = False

    # ---------------- fase de dialogo ----------------
    def _avanzar_dialogo(self):
        self.indice_dialogo += 1
        self.tiempo_linea = 0.0
        if self.indice_dialogo >= len(GUION_DUBOIS_NIVEL3):
            self._iniciar_ronda()
        else:
            reproducir_voz(*GUION_DUBOIS_NIVEL3[self.indice_dialogo])

    # ---------------- rondas del duelo ----------------
    def _iniciar_ronda(self):
        self.fase = Nivel3View.FASE_ESQUIVAR
        self.player.center_x = ANCHO // 2
        self.player.center_y = Nivel3View.JUGADOR_Y
        self.angel.texture = self.tex_angel_carga
        self.tiempo_carga_restante = NIVEL3_TIEMPO_CARGA
        self.fuegos_por_lanzar = min(NIVEL3_FUEGOS_RONDA_MAX, NIVEL3_FUEGOS_RONDA_BASE + (self.ronda - 1))
        self.tiempo_spawn = 0.0

    def _spawn_fuego(self):
        progreso = min(1.0, (self.ronda - 1) / 5.0)
        velocidad = NIVEL3_VELOCIDAD_FUEGO_MIN + (NIVEL3_VELOCIDAD_FUEGO_MAX - NIVEL3_VELOCIDAD_FUEGO_MIN) * progreso
        objetivo_x = random.randint(40, ANCHO - 40)
        dx = objetivo_x - self.angel.center_x
        dy = Nivel3View.JUGADOR_Y - self.angel.center_y
        dist = max(1.0, math.hypot(dx, dy))
        fuego = arcade.Sprite(scale=NIVEL3_ESCALA_ATAQUE)
        fuego.texture = self.tex_fuego_ataque
        fuego.center_x = self.angel.center_x
        fuego.center_y = self.angel.center_y
        fuego.change_x = dx / dist * velocidad
        fuego.change_y = dy / dist * velocidad
        self.fuegos_list.append(fuego)

    def _lanzar_bola_azul(self):
        bola = arcade.Sprite(scale=NIVEL3_ESCALA_DEFENSA)
        bola.texture = self.tex_fuego_defensa
        bola.center_x = self.player.center_x
        bola.center_y = self.player.center_y + 20
        dx = self.angel.center_x - bola.center_x
        dy = self.angel.center_y - bola.center_y
        dist = max(1.0, math.hypot(dx, dy))
        bola.change_x = dx / dist * NIVEL3_VELOCIDAD_BOLA_AZUL
        bola.change_y = dy / dist * NIVEL3_VELOCIDAD_BOLA_AZUL
        self.bolas_azules_list.append(bola)

    def _mover_player_horizontal(self):
        velocidad = VELOCIDAD_CORRER
        self.player.change_x = 0
        if self.a_ap and not self.d_ap:
            self.player.change_x = -velocidad
        elif self.d_ap and not self.a_ap:
            self.player.change_x = velocidad
        self.player.actualizar_direccion()

    def _actualizar_esquivar(self, delta_time):
        self._mover_player_horizontal()
        mw = self.player.width / 2
        nueva_x = self.player.center_x + self.player.change_x
        self.player.center_x = max(mw, min(ANCHO - mw, nueva_x))
        self.player.update_animation(delta_time)

        if self.invulnerable_seg > 0:
            self.invulnerable_seg = max(0.0, self.invulnerable_seg - delta_time)
        self.player.alpha = 130 if (self.invulnerable_seg > 0 and int(self.invulnerable_seg * 12) % 2 == 0) else 255

        if self.tiempo_carga_restante > 0:
            self.tiempo_carga_restante -= delta_time
            if self.tiempo_carga_restante <= 0:
                self.angel.texture = self.tex_angel_lanza
        else:
            self.tiempo_spawn += delta_time
            if self.fuegos_por_lanzar > 0 and self.tiempo_spawn >= NIVEL3_INTERVALO_FUEGO:
                self.tiempo_spawn = 0.0
                self.fuegos_por_lanzar -= 1
                self._spawn_fuego()

        for fuego in self.fuegos_list:
            fuego.center_x += fuego.change_x * delta_time
            fuego.center_y += fuego.change_y * delta_time
        for fuego in list(self.fuegos_list):
            if fuego.top < 0 or fuego.right < 0 or fuego.left > ANCHO:
                fuego.remove_from_sprite_lists()

        if self.invulnerable_seg <= 0:
            golpes = arcade.check_for_collision_with_list(self.player, self.fuegos_list)
            if golpes:
                for f in golpes:
                    f.remove_from_sprite_lists()
                self.vidas -= 1
                self.invulnerable_seg = NIVEL3_TIEMPO_INVULNERABLE
                if self.vidas <= 0:
                    self._perder()
                    return

        # la ronda termina cuando ya no quedan fuegos por lanzar ni en vuelo
        if self.tiempo_carga_restante <= 0 and self.fuegos_por_lanzar <= 0 and len(self.fuegos_list) == 0:
            self._iniciar_ataque()

    def _iniciar_ataque(self):
        self.fase = Nivel3View.FASE_ATAQUE
        self.angel.texture = self.tex_angel_idle

    def _actualizar_ataque(self, delta_time):
        self.player.update_animation(delta_time)
        if self.angel_invulnerable_seg > 0:
            self.angel_invulnerable_seg = max(0.0, self.angel_invulnerable_seg - delta_time)
            self.angel.alpha = 130 if int(self.angel_invulnerable_seg * 12) % 2 == 0 else 255
        else:
            self.angel.alpha = 255

        for bola in self.bolas_azules_list:
            bola.center_x += bola.change_x * delta_time
            bola.center_y += bola.change_y * delta_time
        for bola in list(self.bolas_azules_list):
            if bola.bottom > ALTO or bola.right < 0 or bola.left > ANCHO:
                bola.remove_from_sprite_lists()

        impactos = arcade.check_for_collision_with_list(self.angel, self.bolas_azules_list)
        if impactos:
            for b in impactos:
                b.remove_from_sprite_lists()
            self.angel_vida -= 1
            self.angel_invulnerable_seg = 0.5
            if self.angel_vida <= 0:
                self._ganar()
            else:
                self.ronda += 1
                self._iniciar_ronda()

    def _ganar(self):
        self.fase = Nivel3View.FASE_VICTORIA
        self.fuegos_list.clear()
        self.bolas_azules_list.clear()
        ya_tenia = self.inventario.tiene("Espatula de Dubois")
        self.inventario.agregar("Espatula de Dubois")
        self.inventario.sumar_experiencia(XP_RECOMPENSA_NIVEL3)
        self.inventario.otorgar_medalla(MEDALLA_MUSEO)
        self.inventario.guardar()
        self.mostro_recompensa = not ya_tenia

    def _perder(self):
        self.fase = Nivel3View.FASE_DERROTA
        self.fuegos_list.clear()
        self.bolas_azules_list.clear()

    def _reintentar_duelo(self):
        self.fase = Nivel3View.FASE_ESQUIVAR
        self.vidas = NIVEL3_VIDAS_JUGADOR
        self.angel_vida = NIVEL3_VIDA_ANGEL
        self.ronda = 1
        self.invulnerable_seg = 0.0
        self.angel_invulnerable_seg = 0.0
        self.player.alpha = 255
        self.angel.alpha = 255
        self.fuegos_list.clear()
        self.bolas_azules_list.clear()
        self._iniciar_ronda()

    # ---------------- dibujado ----------------
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.fondo, arcade.LBWH(0, 0, ANCHO, ALTO))
        arcade.draw_text(TITULO_NIVEL3, 14, ALTO - 22, arcade.color.WHITE, font_size=11, bold=True)

        if self.fase == Nivel3View.FASE_DIALOGO:
            self._dibujar_dialogo()
        elif self.fase in (Nivel3View.FASE_ESQUIVAR, Nivel3View.FASE_ATAQUE):
            self.angel_list.draw()
            self.fuegos_list.draw()
            self.bolas_azules_list.draw()
            self.player_list.draw()
            self._dibujar_hud_duelo()
        elif self.fase == Nivel3View.FASE_VICTORIA:
            self._dibujar_victoria()
        elif self.fase == Nivel3View.FASE_DERROTA:
            self._dibujar_derrota()

    def _dibujar_dialogo(self):
        iw = int(self.tex_dubois_dlg.width * 0.85)
        ih = int(self.tex_dubois_dlg.height * 0.85)
        arcade.draw_texture_rect(self.tex_dubois_dlg, arcade.LBWH(ANCHO - iw - 30, 165, iw, ih))

        hablante, texto = GUION_DUBOIS_NIVEL3[self.indice_dialogo]
        texto_visible = texto_progresivo(texto, self.tiempo_linea)
        es_ultima = self.indice_dialogo == len(GUION_DUBOIS_NIVEL3) - 1
        fin = es_ultima and texto_visible == texto
        dibujar_cuadro_dialogo_generico(hablante, texto_visible, self.indice_dialogo, len(GUION_DUBOIS_NIVEL3), fin=fin)
        self._rect_saltar = dibujar_boton_saltar()

    def _dibujar_hud_duelo(self):
        m = 14
        arcade.draw_text(f"Tus fuerzas: {'*' * self.vidas}{'.' * (NIVEL3_VIDAS_JUGADOR - self.vidas)}", ANCHO - m, ALTO - 22, arcade.color.RED_DEVIL, font_size=13, bold=True, anchor_x="right")
        arcade.draw_text(f"Guardiana: {'#' * self.angel_vida}{'.' * (NIVEL3_VIDA_ANGEL - self.angel_vida)}", ANCHO - m, ALTO - 44, arcade.color.LIGHT_BLUE, font_size=13, bold=True, anchor_x="right")
        arcade.draw_text(f"Ronda {self.ronda}", ANCHO - m, ALTO - 66, arcade.color.LIGHT_GRAY, font_size=11, anchor_x="right")

        if self.fase == Nivel3View.FASE_ESQUIVAR:
            arcade.draw_text("[A] [D] para moverte - Esquiva el fuego!", ANCHO // 2, 20, arcade.color.LIGHT_GRAY, font_size=11, anchor_x="center")
        elif self.fase == Nivel3View.FASE_ATAQUE:
            arcade.draw_text("La guardiana se quedo sin aliento...", ANCHO // 2, 44, arcade.color.LIGHT_BLUE, font_size=12, anchor_x="center")
            arcade.draw_text("[Espacio] Atacar con la energia azul!", ANCHO // 2, 20, arcade.color.WHITE, font_size=12, bold=True, anchor_x="center")

    def _dibujar_victoria(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, ALTO), (0, 0, 0, 215))
        if self.mostro_recompensa:
            arcade.draw_text("*** SUPERASTE EL NIVEL 3 ***", ANCHO // 2, 430, arcade.color.GOLD, font_size=18, bold=True, anchor_x="center")
            arcade.draw_text("Espatula de Dubois agregada a tu inventario", ANCHO // 2, 400, arcade.color.WHITE, font_size=13, anchor_x="center")
            arcade.draw_text(f"+{XP_RECOMPENSA_NIVEL3} Experiencia   |   Medalla: \"{MEDALLA_MUSEO}\"", ANCHO // 2, 375, arcade.color.LIGHT_BLUE, font_size=12, anchor_x="center")
        else:
            arcade.draw_text("La guardiana vuelve a dormir, en paz.", ANCHO // 2, 400, arcade.color.LIGHT_GRAY, font_size=14, anchor_x="center")
        arcade.draw_text("LA GUARDIANA DEL MUSEO SUPERADA", ANCHO // 2, 300, arcade.color.WHITE, font_size=22, bold=True, anchor_x="center")
        arcade.draw_text("El resto de los objetos todavia te esperan...", ANCHO // 2, 255, arcade.color.LIGHT_GRAY, font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Cerrar", ANCHO // 2, 60, arcade.color.GRAY, font_size=11, anchor_x="center")

    def _dibujar_derrota(self):
        arcade.draw_rect_filled(arcade.LRBT(0, ANCHO, 0, ALTO), (0, 0, 0, 215))
        arcade.draw_text("El fuego de la guardiana te alcanzo...", ANCHO // 2, 340, arcade.color.RED_DEVIL, font_size=18, bold=True, anchor_x="center")
        arcade.draw_text("Gabriel respira hondo y se prepara para volver a intentarlo.", ANCHO // 2, 300, arcade.color.LIGHT_GRAY, font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Reintentar", ANCHO // 2, 60, arcade.color.GRAY, font_size=11, anchor_x="center")

    # ---------------- input ----------------
    def on_key_press(self, key, modifiers):
        if self.fase == Nivel3View.FASE_DIALOGO:
            if key == arcade.key.TAB:
                self._iniciar_ronda()
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_dialogo()

        elif self.fase == Nivel3View.FASE_ESQUIVAR:
            if key == arcade.key.A:
                self.a_ap = True
            elif key == arcade.key.D:
                self.d_ap = True

        elif self.fase == Nivel3View.FASE_ATAQUE:
            if key == arcade.key.SPACE and len(self.bolas_azules_list) == 0:
                self._lanzar_bola_azul()

        elif self.fase == Nivel3View.FASE_VICTORIA:
            if key == arcade.key.SPACE:
                arcade.exit()

        elif self.fase == Nivel3View.FASE_DERROTA:
            if key == arcade.key.SPACE:
                self._reintentar_duelo()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.a_ap = False
        elif key == arcade.key.D:
            self.d_ap = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fase == Nivel3View.FASE_DIALOGO:
            if self._rect_saltar and click_en_rect(x, y, self._rect_saltar):
                self._iniciar_ronda()
                return
            self._avanzar_dialogo()

    def on_update(self, delta_time):
        if self.fase == Nivel3View.FASE_DIALOGO:
            self.tiempo_linea += delta_time
        elif self.fase == Nivel3View.FASE_ESQUIVAR:
            self._actualizar_esquivar(delta_time)
        elif self.fase == Nivel3View.FASE_ATAQUE:
            self._actualizar_ataque(delta_time)


# Punto de entrada: crea la ventana y arranca mostrando la IntroView
def main():
    generar_voces_faltantes()
    window = arcade.Window(ANCHO, ALTO, TITULO)
    window.center_window()
    window.show_view(IntroView())
    arcade.run()


if __name__ == "__main__":
    main()