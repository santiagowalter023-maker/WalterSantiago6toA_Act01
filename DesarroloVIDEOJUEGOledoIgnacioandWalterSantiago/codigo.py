# python "DesarroloVIDEOJUEGOledoIgnacioandWalterSantiago/codigo.py"
# ============================================================
# REMINENCE OF GRACIA - PUNTO DE ENTRADA PRINCIPAL DEL JUEGO
# ============================================================
# Modulos incluidos:
#   codigosb.py         -> configuracion (tamanio ventana, velocidades, rutas)
#   Inventario          -> sistema de objetos recolectados + guardado de partida
#   Lediago             -> personaje principal con sprite sheet animado
#   GameView            -> escena de la Estancia Jesuitica (libre)
#   JuicioView          -> escena del juicio (novela visual)
#   HotelSierrasView    -> escena interior Hotel Sierras con Walter y Ledo
#   VitrinaView         -> vitrina de objetos recolectados + Cronoscopio
# Todo corre sobre Arcade 3.x
import arcade
import json
import os
import codigosb

# ============================================================
# DIRECCIONES DEL PERSONAJE
# ============================================================
FRENTE    = 0
ESPALDA   = 1
IZQUIERDA = 2
DERECHA   = 3

# ============================================================
# ESTADOS GENERALES
# ============================================================
ESTADO_JUGANDO  = 0
ESTADO_HABLANDO = 1
ESTADO_INTRO_CURA = 2
ESTADO_TRIVIA      = 3
ESTADO_CIERRE_CURA = 4
ESTADO_FIN_DEMO    = 5


# ============================================================
#  INVENTARIO  -  objetos recolectados + guardado de partida
# ============================================================
class Inventario:
    """
    Objeto central que hereda entre escenas.
    Todos los objetos que Lediago recolecta viajan en este inventario.
    Al usar el Cronoscopio se llama a guardar() para persistir la partida.

    Uso tipico:
        inv = Inventario()          # partida nueva
        inv.agregar("Piedra de Moler", "Herramienta usada por los indigenas")
        inv.guardar()               # guarda en JSON

        inv2 = Inventario.cargar()  # retoma partida guardada
    """

    # Objetos que se pueden guardar en la vitrina (nombre -> descripcion)
    OBJETOS_POSIBLES = {
        "Piedra de Moler":    "Herramienta indigena anterior a la colonizacion.",
        "Herramienta Jesuita":"Utensilio usado para construir la iglesia y la estancia.",
        "Llave Maestra":      "Llave que abria las puertas del Sierras Hotel en 1901.",
        "Sello Real":         "Sello oficial de la corona espaniola en tierras de Gracia.",
        "Cincel del Cantero": "Cincel con el que se tallaron las piedras de la plaza.",
        "Quijote":            "Ejemplar que Sarmiento leyo en Alta Gracia de niino.",
        "Metronomo":          "Metronomo de Manuel de Falla, compositor en el Villa.",
        "Cantimplora":        "Cantimplora de peregrino del siglo XIX.",
        "Espatula de Dubois": "Herramienta del escultor Dubois, residente en Gracia.",
        "Cronoscopio":        "Dispositivo que permite viajar por el tiempo.",
        "Cruz de la Estancia": "Cruz bendecida por el cura de la Estancia Jesuitica, "
                                "entregada a quien demuestra conocer su historia.",
    }

    def __init__(self):
        # dict: nombre_objeto -> True/False (recolectado o no)
        self.objetos = {nombre: False for nombre in self.OBJETOS_POSIBLES}
        self.turno_viaje   = 0       # cuantas veces se uso el Cronoscopio
        self.nombre_jugador = "Lediago Waledo"
        self.experiencia = 0         # puntos de experiencia acumulados
        self.medallas    = []        # nombres de medallas obtenidas

    # --------------------------------------------------------
    # EXPERIENCIA Y MEDALLAS
    # --------------------------------------------------------
    def sumar_experiencia(self, puntos: int):
        self.experiencia += puntos

    def otorgar_medalla(self, nombre_medalla: str) -> bool:
        """Agrega la medalla si todavia no la tiene. Devuelve True si es nueva."""
        if nombre_medalla not in self.medallas:
            self.medallas.append(nombre_medalla)
            return True
        return False

    def tiene_medalla(self, nombre_medalla: str) -> bool:
        return nombre_medalla in self.medallas

    # --------------------------------------------------------
    # GESTION DE OBJETOS
    # --------------------------------------------------------
    def agregar(self, nombre_objeto: str) -> bool:
        """Marca el objeto como recolectado. Devuelve True si existia."""
        if nombre_objeto in self.objetos:
            self.objetos[nombre_objeto] = True
            return True
        return False

    def tiene(self, nombre_objeto: str) -> bool:
        return self.objetos.get(nombre_objeto, False)

    def recolectados(self) -> list:
        """Lista de nombres de objetos ya recolectados."""
        return [n for n, v in self.objetos.items() if v]

    def faltantes(self) -> list:
        return [n for n, v in self.objetos.items() if not v]

    # --------------------------------------------------------
    # GUARDAR / CARGAR
    # --------------------------------------------------------
    def guardar(self):
        """Serializa el inventario a JSON en disco."""
        datos = {
            "nombre_jugador": self.nombre_jugador,
            "turno_viaje": self.turno_viaje,
            "objetos": self.objetos,
            "experiencia": self.experiencia,
            "medallas": self.medallas,
        }
        try:
            with open(codigosb.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    @classmethod
    def cargar(cls):
        """Intenta cargar una partida guardada. Si no existe, devuelve None."""
        if not os.path.exists(codigosb.SAVE_FILE):
            return None
        try:
            with open(codigosb.SAVE_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
            inv = cls()
            inv.nombre_jugador = datos.get("nombre_jugador", "Lediago Waledo")
            inv.turno_viaje    = datos.get("turno_viaje", 0)
            inv.experiencia    = datos.get("experiencia", 0)
            inv.medallas       = datos.get("medallas", [])
            for nombre, valor in datos.get("objetos", {}).items():
                if nombre in inv.objetos:
                    inv.objetos[nombre] = valor
            return inv
        except (OSError, json.JSONDecodeError):
            return None


# ============================================================
#  LEDIAGO  -  personaje principal con sprite sheet animado
# ============================================================
class Lediago(arcade.Sprite):
    """
    Personaje principal con animacion de caminar suave usando el sprite sheet.

    Sprite sheet (sprite_sheet.png): 416x600 px, 4 cols x 3 filas
        Fila 0: caminar hacia ABAJO  (frente)
        Fila 1: caminar de LADO      (derecha)
        Fila 2: caminar hacia ARRIBA (espalda)
    Para izquierda se espeja la fila 1.
    Frame 0 de cada fila = pose en reposo.
    """

    ANIM_FPS = codigosb.ANIM_FPS

    def __init__(self, escala=0.35):
        super().__init__(scale=escala)

        self.direccion_actual = FRENTE
        self.esta_corriendo   = False

        # -------------------------------------------------------
        # Cargar los 12 frames del sprite sheet de una sola vez.
        # Arcade 3.x: load_spritesheet() devuelve un SpriteSheet;
        # get_texture_grid(size, columns, count) los corta en orden
        # de izquierda-a-derecha, arriba-a-abajo.
        # Sheet: 416x600, 4 cols x 3 filas de 104x200 cada una.
        #   frames  0-3  -> fila 0 (caminar hacia ABAJO  / frente)
        #   frames  4-7  -> fila 1 (caminar de LADO      / derecha)
        #   frames 8-11  -> fila 2 (caminar hacia ARRIBA / espalda)
        # -------------------------------------------------------
        _ss = arcade.load_spritesheet(codigosb.SPRITE_SHEET)
        _todos = _ss.get_texture_grid(
            size=(codigosb.SPRITE_FRAME_W, codigosb.SPRITE_FRAME_H),
            columns=codigosb.SPRITE_SHEET_COLS,
            count=codigosb.SPRITE_SHEET_COLS * codigosb.SPRITE_SHEET_ROWS,
        )

        self._frames_frente    = _todos[0:4]
        self._frames_lado      = _todos[4:8]
        self._frames_espalda   = _todos[8:12]
        self._frames_izquierda = [t.flip_left_right() for t in self._frames_lado]

        # Textura inicial: frame 0 de frente (pose en reposo)
        self.texture = self._frames_frente[0]

        # Estado de animacion
        self._anim_frame    = 0
        self._anim_timer    = 0.0
        self._seg_por_frame = 1.0 / self.ANIM_FPS

    # --------------------------------------------------------
    # ACTUALIZACION DE DIRECCION Y ANIMACION
    # --------------------------------------------------------
    def actualizar_direccion(self):
        """Elige el set de frames segun hacia donde se mueve."""
        if self.change_x < 0:
            self.direccion_actual = IZQUIERDA
        elif self.change_x > 0:
            self.direccion_actual = DERECHA
        elif self.change_y > 0:
            self.direccion_actual = ESPALDA
        elif self.change_y < 0:
            self.direccion_actual = FRENTE

    def _frames_actuales(self) -> list:
        if self.direccion_actual == FRENTE:
            return self._frames_frente
        elif self.direccion_actual == ESPALDA:
            return self._frames_espalda
        elif self.direccion_actual == IZQUIERDA:
            return self._frames_izquierda
        else:
            return self._frames_lado

    def update_animation(self, delta_time: float = 1/60):
        """Avanza la animacion de caminar. Llamar desde on_update de la View."""
        esta_quieto = (self.change_x == 0 and self.change_y == 0)

        if esta_quieto:
            # Frame 0 = pose de reposo
            self._anim_frame = 0
            self._anim_timer = 0.0
            self.texture = self._frames_actuales()[0]
            return

        # Ajustar velocidad segun si corre o camina
        fps = self.ANIM_FPS * (1.8 if self.esta_corriendo else 1.0)
        seg_por_frame = 1.0 / fps

        self._anim_timer += delta_time
        if self._anim_timer >= seg_por_frame:
            self._anim_timer -= seg_por_frame
            frames = self._frames_actuales()
            self._anim_frame = (self._anim_frame + 1) % len(frames)
            self.texture = frames[self._anim_frame]


# ============================================================
# DIALOGO Y MINIJUEGO DEL CURA - "El Desafio de la Estancia"
# ============================================================
# Hablante simple: (nombre_mostrado, texto). Se dibuja con el mismo
# cuadro de dialogo generico que ya usa GameView.
GUION_INTRO_CURA = [
    ("CURA",   "La paz sea contigo, hijo! Veo curiosidad en tus ojos... "
               "No todos los dias alguien se detiene a observar la "
               "historia de este lugar."),
    ("WALEDO", "Estoy recorriendo Alta Gracia y tratando de descubrir "
               "los secretos que esconde cada epoca."),
    ("CURA",   "Entonces has llegado al sitio indicado. Esta antigua "
               "Estancia guarda casi cuatro siglos de historia, desde "
               "la llegada de los jesuitas hasta convertirse en uno de "
               "los mayores tesoros culturales del pais."),
    ("WALEDO", "Eso suena interesante! Pero... como se si aprendi lo "
               "suficiente?"),
    ("CURA",   "Muy sencillo. Prepare un pequenio desafio. Son siete "
               "preguntas sobre la Estancia Jesuitica. Si respondes "
               "correctamente la mayoria, demostraras que estas listo "
               "para continuar tu viaje por el tiempo."),
    ("WALEDO", "Acepto el reto!"),
    ("CURA",   "Muy bien. Lee con atencion y piensa antes de responder. "
               "La historia siempre recompensa a quienes observan."),
]

GUION_CIERRE_CURA_EXITO = [
    ("CURA",   "Excelente! Has demostrado conocer la historia de este "
               "lugar. El conocimiento tambien es una forma de viajar "
               "en el tiempo."),
    ("WALEDO", "Gracias, padre. Ahora entiendo mucho mejor la "
               "importancia de la Estancia."),
    ("CURA",   "Que esta sabiduria te acompanie en los proximos viajes "
               "del Cronoscopio."),
]

GUION_CIERRE_CURA_FALLO = [
    ("CURA",   "No te desanimes. La historia siempre ofrece una "
               "segunda oportunidad. Recorre nuevamente la Estancia y "
               "vuelve cuando estes preparado."),
    ("WALEDO", "Volvere. Todavia me queda mucho por aprender."),
]

MEDALLA_HISTORIADOR = "Historiador de la Estancia"
XP_RECOMPENSA_TRIVIA = 100
PREGUNTAS_MINIMAS_PARA_GANAR = 5

# Cada pregunta: (texto, [4 opciones A-D], indice_correcto 0-3)
PREGUNTAS_ESTANCIA = [
    ("Que anio comenzo a organizarse la Estancia Jesuitica de Alta Gracia?",
     ["1588", "1643", "1767", "1810"], 1),
    ("Que orden religiosa administro la Estancia?",
     ["Franciscanos", "Dominicos", "Jesuitas", "Benedictinos"], 2),
    ("Que reconocimiento internacional recibio la Estancia?",
     ["Patrimonio Natural", "Monumento Provincial",
      "Patrimonio Mundial de la UNESCO", "Capital Cultural Americana"], 2),
    ("Que importante personaje historico vivio sus ultimos dias en esta "
     "residencia?",
     ["Manuel Belgrano", "Jose de San Martin", "Juan Bautista Alberdi",
      "Santiago de Liniers"], 3),
    ("Que construccion de la Estancia permitia almacenar agua para la "
     "comunidad?",
     ["El campanario", "La biblioteca", "El Tajamar", "El cabildo"], 2),
    ("Cual de estas partes todavia forma parte del conjunto historico?",
     ["La iglesia y la residencia jesuitica", "El fuerte militar",
      "El puerto", "El teatro colonial"], 0),
    ("Cual era uno de los principales objetivos de las estancias "
     "jesuiticas?",
     ["Construir fortalezas militares.", "Extraer oro.",
      "Sostener economicamente las obras educativas y religiosas de los "
      "jesuitas mediante la produccion agricola y ganadera.",
      "Fabricar barcos."], 2),
]


class GameView(arcade.View):
    """
    Escena libre de la Estancia Jesuitica.

    El Cura espera del lado izquierdo de la pantalla. Al acercarse y
    hablar con el se desbloquea el minijuego "El Desafio de la
    Estancia": siete preguntas de opcion multiple sobre la historia
    del lugar. Respondiendo 5 o mas correctamente se obtiene la Cruz
    de la Estancia, experiencia y una medalla; ademas se muestra el
    cartel de fin de demo.
    """

    # Posicion del Cura (lado izquierdo del patio). Se dibuja con
    # draw_texture_rect (no SpriteList/atlas) porque el atlas de
    # sprites genera un halo blanco en el contorno por sangrado de
    # color entre el padding transparente y el sprite vecino.
    CURA_CX = 150
    CURA_CY = 230
    CURA_ESCALA = 0.65

    def __init__(self, musica_fondo=None, reproductor_musica=None,
                 inventario: Inventario = None) -> None:
        super().__init__()

        self.estado_actual = ESTADO_JUGANDO
        self.inventario = inventario or Inventario()

        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(
                volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True
            )

        self.fondo = arcade.load_texture(codigosb.FONDO_ESTANCIA)

        self.player_sprite = Lediago(escala=codigosb.ESCALA_PERSONAJE)
        self.player_sprite.center_x = codigosb.ANCHO // 2
        self.player_sprite.center_y = codigosb.ALTO  // 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Texturas del Cura (idle / hablando / senalando). Ya vienen
        # pre-escaladas (PIL + NEAREST) al tamanio final de pantalla.
        self.tex_cura_idle      = arcade.load_texture(codigosb.CURA_IDLE)
        self.tex_cura_dialogo   = arcade.load_texture(codigosb.CURA_DIALOGO)
        self.tex_cura_senalando = arcade.load_texture(codigosb.CURA_SENALANDO)
        self.tex_cruz           = arcade.load_texture(codigosb.CRUZ_ESTANCIA_IMG)
        self.tex_cura_actual    = self.tex_cura_idle

        self.w_ap = self.s_ap = self.a_ap = self.d_ap = self.shift_ap = False

        # Dialogo generico (bienvenida libre, ya existente)
        self.dialogo_lineas = []
        self.indice_linea_actual = 0

        # Dialogo del Cura (intro / cierre), reutiliza el mismo cuadro
        self.guion_cura_actual = []
        self.indice_cura = 0

        # Minijuego de trivia
        self.indice_pregunta   = 0
        self.respuestas_ok     = 0
        self.opcion_hover      = None   # 0-3, para resaltar al pasar el mouse
        self.feedback_visible  = False
        self.feedback_correcta = False
        self._ultima_opcion_elegida = -1

        # Recompensa / cartel de fin de demo
        self._mostrar_recompensa = False

    # --------------------------------------------------------
    # HELPERS DE PROXIMIDAD / FLUJO
    # --------------------------------------------------------
    def _cerca_del_cura(self) -> bool:
        dx = self.player_sprite.center_x - self.CURA_CX
        dy = self.player_sprite.center_y - self.CURA_CY
        return (dx*dx + dy*dy) < 110*110

    def _iniciar_intro_cura(self):
        self.guion_cura_actual = GUION_INTRO_CURA
        self.indice_cura = 0
        self.estado_actual = ESTADO_INTRO_CURA
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def _avanzar_intro_cura(self):
        self.indice_cura += 1
        if self.indice_cura >= len(self.guion_cura_actual):
            self._iniciar_trivia()

    def _iniciar_trivia(self):
        self.indice_pregunta  = 0
        self.respuestas_ok    = 0
        self.feedback_visible = False
        self.estado_actual    = ESTADO_TRIVIA

    def _responder(self, opcion_idx: int):
        if self.feedback_visible:
            return  # ya se esta mostrando el resultado de esta pregunta
        _, opciones, correcta = PREGUNTAS_ESTANCIA[self.indice_pregunta]
        if opcion_idx < 0 or opcion_idx >= len(opciones):
            return
        self.feedback_correcta = (opcion_idx == correcta)
        if self.feedback_correcta:
            self.respuestas_ok += 1
        self.feedback_visible = True

    def _siguiente_pregunta(self):
        self.indice_pregunta += 1
        self.feedback_visible = False
        if self.indice_pregunta >= len(PREGUNTAS_ESTANCIA):
            self._terminar_trivia()

    def _terminar_trivia(self):
        gano = self.respuestas_ok >= PREGUNTAS_MINIMAS_PARA_GANAR
        if gano:
            self.guion_cura_actual = GUION_CIERRE_CURA_EXITO
            ya_tenia_cruz = self.inventario.tiene("Cruz de la Estancia")
            self.inventario.agregar("Cruz de la Estancia")
            self.inventario.sumar_experiencia(XP_RECOMPENSA_TRIVIA)
            self.inventario.otorgar_medalla(MEDALLA_HISTORIADOR)
            self.inventario.guardar()
            self._mostrar_recompensa = not ya_tenia_cruz
        else:
            self.guion_cura_actual    = GUION_CIERRE_CURA_FALLO
            self._mostrar_recompensa = False
        self.indice_cura   = 0
        self.estado_actual = ESTADO_CIERRE_CURA

    def _avanzar_cierre_cura(self):
        self.indice_cura += 1
        if self.indice_cura >= len(self.guion_cura_actual):
            self.estado_actual = ESTADO_FIN_DEMO

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.fondo, arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO))

        # Pose del cura segun el momento
        if self.estado_actual in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA):
            self.tex_cura_actual = self.tex_cura_dialogo
        elif self.estado_actual == ESTADO_TRIVIA:
            self.tex_cura_actual = self.tex_cura_senalando
        else:
            self.tex_cura_actual = self.tex_cura_idle

        ancho_cura = int(self.tex_cura_actual.width  * self.CURA_ESCALA)
        alto_cura  = int(self.tex_cura_actual.height * self.CURA_ESCALA)
        arcade.draw_texture_rect(
            self.tex_cura_actual,
            arcade.LBWH(
                self.CURA_CX - ancho_cura // 2,
                self.CURA_CY - alto_cura // 2,
                ancho_cura,
                alto_cura,
            )
        )
        self.player_list.draw()

        if self.estado_actual == ESTADO_JUGANDO and self._cerca_del_cura():
            arcade.draw_text(
                "[ ESPACIO / CLICK ] Hablar con el Cura",
                codigosb.ANCHO // 2, self.CURA_CY + 160,
                arcade.color.YELLOW, font_size=11,
                anchor_x="center", bold=True)

        if self.estado_actual == ESTADO_HABLANDO:
            self.dibujar_cuadro_dialogo()
        elif self.estado_actual in (ESTADO_INTRO_CURA, ESTADO_CIERRE_CURA):
            self._dibujar_cuadro_cura()
        elif self.estado_actual == ESTADO_TRIVIA:
            self._dibujar_trivia()
        elif self.estado_actual == ESTADO_FIN_DEMO:
            self._dibujar_fin_demo()

    def dibujar_cuadro_dialogo(self):
        arcade.draw_rect_filled(
            arcade.LRBT(20, codigosb.ANCHO-20, 20, 140), arcade.color.BLACK)
        arcade.draw_rect_outline(
            arcade.LRBT(20, codigosb.ANCHO-20, 20, 140),
            arcade.color.WHITE, border_width=3)
        arcade.draw_text(
            self.dialogo_lineas[self.indice_linea_actual],
            40, 90, arcade.color.WHITE, font_size=16,
            width=codigosb.ANCHO-80, multiline=True)
        arcade.draw_text("[Espacio] Siguiente...",
            codigosb.ANCHO-220, 35, arcade.color.GRAY, font_size=12)

    def _dibujar_cuadro_cura(self):
        """Cuadro de dialogo con nombre del hablante (Cura / Waledo)."""
        nombre, texto = self.guion_cura_actual[self.indice_cura]
        m = 20
        alto_caja = 150
        color = arcade.color.GOLD if nombre == "CURA" else \
            arcade.color.LIGHT_PASTEL_PURPLE
        arcade.draw_rect_filled(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja), (0, 0, 0, 210))
        arcade.draw_rect_outline(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja),
            color, border_width=3)
        arcade.draw_rect_filled(
            arcade.LRBT(m, m+170, alto_caja-4, alto_caja+26), (0, 0, 0, 230))
        arcade.draw_rect_outline(
            arcade.LRBT(m, m+170, alto_caja-4, alto_caja+26),
            color, border_width=2)
        etiqueta = "CURA DE LA ESTANCIA" if nombre == "CURA" else "LEDIAGO WALEDO"
        arcade.draw_text(etiqueta, m+14, alto_caja+3,
            color, font_size=12, bold=True, anchor_y="center")
        arcade.draw_text(texto, m+20, alto_caja-30, arcade.color.WHITE,
            font_size=15, width=codigosb.ANCHO-(m*2)-40,
            multiline=True, anchor_y="top")
        es_ultima = self.indice_cura >= len(self.guion_cura_actual) - 1
        pista = "[Espacio] Continuar..." if not es_ultima else \
            "[Espacio] Continuar..."
        arcade.draw_text(pista, codigosb.ANCHO-m-10, m+8,
            arcade.color.GRAY, font_size=11, anchor_x="right")

    def _dibujar_trivia(self):
        """Pantalla de pregunta con 4 opciones clickeables."""
        texto, opciones, correcta = PREGUNTAS_ESTANCIA[self.indice_pregunta]
        m = 50
        y_top = codigosb.ALTO - 60

        arcade.draw_rect_filled(
            arcade.LRBT(m, codigosb.ANCHO-m, codigosb.ALTO-180, y_top+20),
            (10, 10, 30, 230))
        arcade.draw_rect_outline(
            arcade.LRBT(m, codigosb.ANCHO-m, codigosb.ALTO-180, y_top+20),
            arcade.color.GOLD, border_width=2)
        arcade.draw_text(
            f"Pregunta {self.indice_pregunta+1}/{len(PREGUNTAS_ESTANCIA)}",
            codigosb.ANCHO//2, y_top, arcade.color.GOLD,
            font_size=12, bold=True, anchor_x="center")
        arcade.draw_text(
            texto, m+20, y_top-26, arcade.color.WHITE, font_size=14,
            width=codigosb.ANCHO-(m*2)-40, multiline=True, anchor_y="top")

        letras = ["A", "B", "C", "D"]
        for i, op in enumerate(opciones):
            x1, y1, x2, y2 = self._rect_opcion(i)
            if self.feedback_visible:
                if i == correcta:
                    color_fondo = (40, 130, 40, 235)
                elif i != correcta and not self.feedback_correcta and \
                        i == self._ultima_opcion_elegida:
                    color_fondo = (150, 30, 30, 235)
                else:
                    color_fondo = (25, 25, 45, 200)
            else:
                color_fondo = (60, 50, 20, 235) if self.opcion_hover == i \
                    else (25, 25, 45, 200)
            arcade.draw_rect_filled(arcade.LRBT(x1, x2, y1, y2), color_fondo)
            arcade.draw_rect_outline(
                arcade.LRBT(x1, x2, y1, y2), arcade.color.GOLD, border_width=1)
            arcade.draw_text(
                f"{letras[i]}) {op}",
                x1+14, (y1+y2)//2, arcade.color.WHITE, font_size=13,
                anchor_y="center", width=x2-x1-24, multiline=True)

        # Franja fija al pie para feedback / ayuda (nunca se solapa
        # con las opciones, que terminan por encima de FRANJA_PIE_Y2).
        if self.feedback_visible:
            msg = "Correcto!" if self.feedback_correcta else "Incorrecto."
            col = arcade.color.GREEN_YELLOW if self.feedback_correcta \
                else arcade.color.RED_DEVIL
            arcade.draw_text(msg, codigosb.ANCHO//2, 22, col,
                font_size=14, bold=True, anchor_x="center")
        else:
            arcade.draw_text(
                "[1-4] o [Click] para responder",
                codigosb.ANCHO//2, 22, arcade.color.GRAY,
                font_size=11, anchor_x="center")

    def _rect_opcion(self, i: int):
        """Devuelve (x1, y1, x2, y2) del boton de la opcion i (0-3).
        Ancladas debajo del cuadro de pregunta, de arriba hacia abajo,
        dejando siempre una franja libre de pie para el feedback."""
        m = 60
        alto_opcion = 42
        espacio     = 8
        y_tope = codigosb.ALTO - 210   # justo debajo del cuadro de pregunta
        y2 = y_tope - i * (alto_opcion + espacio)
        y1 = y2 - alto_opcion
        return (m, y1, codigosb.ANCHO - m, y2)

    def _dibujar_fin_demo(self):
        """Cartel final: recompensa obtenida + fin de la demo."""
        arcade.draw_rect_filled(
            arcade.LRBT(0, codigosb.ANCHO, 0, codigosb.ALTO), (0, 0, 0, 215))

        if self._mostrar_recompensa:
            arcade.draw_texture_rect(
                self.tex_cruz,
                arcade.LBWH(codigosb.ANCHO//2 - 55, 440, 110, 110))

            arcade.draw_text("Cruz de la Estancia obtenida",
                codigosb.ANCHO//2, 425, arcade.color.GOLD,
                font_size=15, bold=True, anchor_x="center")
            arcade.draw_text(
                f"+{XP_RECOMPENSA_TRIVIA} Experiencia   -   Medalla: "
                f"\"{MEDALLA_HISTORIADOR}\"",
                codigosb.ANCHO//2, 397, arcade.color.LIGHT_PASTEL_PURPLE,
                font_size=12, anchor_x="center")
        else:
            arcade.draw_text("Podras intentarlo de nuevo...",
                codigosb.ANCHO//2, 430, arcade.color.LIGHT_GRAY,
                font_size=14, anchor_x="center")

        arcade.draw_text("FIN DE LA DEMO",
            codigosb.ANCHO//2, 260, arcade.color.WHITE,
            font_size=30, bold=True, anchor_x="center")
        arcade.draw_text("Gracias por jugar Reminiscence of Gracia",
            codigosb.ANCHO//2, 210, arcade.color.LIGHT_GRAY,
            font_size=13, anchor_x="center")
        arcade.draw_text("[Espacio] Cerrar",
            codigosb.ANCHO//2, 60, arcade.color.GRAY,
            font_size=11, anchor_x="center")

    # --------------------------------------------------------
    # MOVIMIENTO
    # --------------------------------------------------------
    def evaluar_movimiento(self):
        vel = codigosb.VELOCIDAD_CORRER if self.shift_ap else codigosb.VELOCIDAD_CAMINAR
        self.player_sprite.esta_corriendo = self.shift_ap
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        if self.w_ap and not self.s_ap:
            self.player_sprite.change_y = vel
        elif self.s_ap and not self.w_ap:
            self.player_sprite.change_y = -vel
        if self.a_ap and not self.d_ap:
            self.player_sprite.change_x = -vel
        elif self.d_ap and not self.a_ap:
            self.player_sprite.change_x = vel
        self.player_sprite.actualizar_direccion()

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if key == arcade.key.W:     self.w_ap = True
            elif key == arcade.key.S:   self.s_ap = True
            elif key == arcade.key.A:   self.a_ap = True
            elif key == arcade.key.D:   self.d_ap = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = True
            elif key == arcade.key.SPACE:
                if self._cerca_del_cura():
                    self._iniciar_intro_cura()
            elif key == arcade.key.J:
                self.iniciar_juicio()
            self.evaluar_movimiento()

        elif self.estado_actual == ESTADO_HABLANDO:
            if key == arcade.key.SPACE:
                self.indice_linea_actual += 1
                if self.indice_linea_actual >= len(self.dialogo_lineas):
                    self.estado_actual = ESTADO_JUGANDO

        elif self.estado_actual == ESTADO_INTRO_CURA:
            if key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_intro_cura()

        elif self.estado_actual == ESTADO_TRIVIA:
            if not self.feedback_visible:
                tecla_a_opcion = {
                    arcade.key.KEY_1: 0, arcade.key.KEY_2: 1,
                    arcade.key.KEY_3: 2, arcade.key.KEY_4: 3,
                }
                if key in tecla_a_opcion:
                    self._ultima_opcion_elegida = tecla_a_opcion[key]
                    self._responder(tecla_a_opcion[key])
            elif key in (arcade.key.SPACE, arcade.key.ENTER):
                self._siguiente_pregunta()

        elif self.estado_actual == ESTADO_CIERRE_CURA:
            if key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_cierre_cura()

        elif self.estado_actual == ESTADO_FIN_DEMO:
            if key == arcade.key.SPACE:
                pass  # el cartel queda visible; se podria cerrar el juego aqui

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:     self.w_ap = False
        elif key == arcade.key.S:   self.s_ap = False
        elif key == arcade.key.A:   self.a_ap = False
        elif key == arcade.key.D:   self.d_ap = False
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_ap = False
        if self.estado_actual == ESTADO_JUGANDO:
            self.evaluar_movimiento()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.estado_actual == ESTADO_TRIVIA and not self.feedback_visible:
            self.opcion_hover = None
            for i in range(4):
                x1, y1, x2, y2 = self._rect_opcion(i)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.opcion_hover = i
                    break

    def on_mouse_press(self, x, y, button, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if self._cerca_del_cura():
                self._iniciar_intro_cura()

        elif self.estado_actual == ESTADO_INTRO_CURA:
            self._avanzar_intro_cura()

        elif self.estado_actual == ESTADO_TRIVIA:
            if not self.feedback_visible:
                for i in range(4):
                    x1, y1, x2, y2 = self._rect_opcion(i)
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        self._ultima_opcion_elegida = i
                        self._responder(i)
                        break
            else:
                self._siguiente_pregunta()

        elif self.estado_actual == ESTADO_CIERRE_CURA:
            self._avanzar_cierre_cura()

    def on_update(self, delta_time):
        if self.estado_actual == ESTADO_JUGANDO:
            nueva_x = self.player_sprite.center_x + self.player_sprite.change_x
            nueva_y = self.player_sprite.center_y + self.player_sprite.change_y
            mw = self.player_sprite.width  / 2
            mh = self.player_sprite.height / 2
            self.player_sprite.center_x = max(mw, min(codigosb.ANCHO-mw, nueva_x))
            self.player_sprite.center_y = max(mh, min(codigosb.ALTO-mh,  nueva_y))
            self.player_sprite.update_animation(delta_time)

    def disparar_dialogo(self, lineas):
        self.dialogo_lineas = lineas
        self.indice_linea_actual = 0
        self.estado_actual = ESTADO_HABLANDO
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def iniciar_juicio(self):
        self.window.show_view(JuicioView(vista_siguiente=self))


# ============================================================
# COLORES / DATOS DE HABLANTES (compartido por JuicioView y HotelSierrasView)
# ============================================================
FONDO_INICIO  = "inicio"
FONDO_ACTIVO  = "activo"
FONDO_CERRADO = "cerrado"

HABLANTES = {
    "JUEZ": {
        "nombre": "JUEZ DEL TRIBUNAL",
        "color_nombre": arcade.color.GOLD,
        "color_borde":  arcade.color.GOLD,
    },
    "ABOGADO": {
        "nombre": "ABOGADO DE LA CORPORACION",
        "color_nombre": arcade.color.RED_DEVIL,
        "color_borde":  arcade.color.RED_DEVIL,
    },
    "WALTER": {
        "nombre": "WALTER",
        "color_nombre": arcade.color.CYAN,
        "color_borde":  arcade.color.CYAN,
    },
    "LEDO": {
        "nombre": "LEDO",
        "color_nombre": arcade.color.GREEN_YELLOW,
        "color_borde":  arcade.color.GREEN_YELLOW,
    },
    "LEDIAGO": {
        "nombre": "LEDIAGO WALEDO",
        "color_nombre": arcade.color.LIGHT_PASTEL_PURPLE,
        "color_borde":  arcade.color.LIGHT_PASTEL_PURPLE,
    },
    "CIUDADANOS": {
        "nombre": "CIUDADANOS",
        "color_nombre": arcade.color.LIGHT_GRAY,
        "color_borde":  arcade.color.LIGHT_GRAY,
    },
    "NARRADOR": {
        "nombre": "",
        "color_nombre": arcade.color.WHITE,
        "color_borde":  arcade.color.WHITE,
    },
}


# ============================================================
# GUION DEL JUICIO
# ============================================================
GUION_JUICIO = [
    ("JUEZ",      "Se abre la sesion extraordinaria del Tribunal de Legado Cultural. "
                  "Procedan con sus argumentos.", FONDO_INICIO),
    ("ABOGADO",   "Honorables miembros del tribunal, los edificios antiguos no "
                  "generan progreso. Nuestra propuesta traera inversion, turismo "
                  "y empleo. La ciudad necesita avanzar.", FONDO_INICIO),
    ("WALTER",    "Avanzar destruyendo todo lo que la hace unica?", FONDO_INICIO),
    ("ABOGADO",   "La historia esta en los libros, senor. No en piedras viejas.", FONDO_INICIO),
    ("LEDO",      "Entonces nunca entendio lo que significa Alta Gracia.", FONDO_INICIO),
    ("JUEZ",      "Tienen pruebas concretas para refutar el proyecto?", FONDO_INICIO),
    ("ABOGADO",   "Exactamente. Emociones y recuerdos no son evidencia legal.", FONDO_INICIO),
    ("NARRADOR",  "(Las puertas del hotel se abren.)", FONDO_ACTIVO),
    ("WALTER",    "Llego.", FONDO_ACTIVO),
    ("LEDO",      "Sabia que volveria.", FONDO_ACTIVO),
    ("JUEZ",      "Quien es usted?", FONDO_ACTIVO),
    ("LEDIAGO",   "Mi nombre es Lediago Waledo. Y traigo la memoria de esta ciudad.", FONDO_ACTIVO),
    ("ABOGADO",   "Esto es absurdo.", FONDO_ACTIVO),
    ("LEDIAGO",   "Absurdo?", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca la Piedra de Moler sobre la mesa.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Antes de las calles hubo un pueblo que escuchaba hablar al viento.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca la Herramienta Jesuita.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Antes de los hoteles hubo hombres que levantaron estos muros "
                  "piedra por piedra.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca la Llave Maestra.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Antes del nombre existio el suenio de una ciudad.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca el Sello Real.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Antes de la nacion hubo quienes protegieron estas tierras en "
                  "tiempos inciertos.", FONDO_ACTIVO),
    ("NARRADOR",  "(Los presentes observan en silencio.)", FONDO_ACTIVO),
    ("ABOGADO",   "Objetos antiguos. Nada mas.", FONDO_ACTIVO),
    ("LEDIAGO",   "Nada mas?", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca el Cincel del Cantero.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Miles de golpes construyeron cada calle que hoy pisan.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca el Quijote.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Un ninio curioso aprendio aqui a cuestionar el mundo.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca el Metronomo.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Un compositor encontro inspiracion entre estas montanias.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca la Cantimplora.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Miles de peregrinos buscaron esperanza en estas tierras.", FONDO_ACTIVO),
    ("NARRADOR",  "(Coloca la Espatula de Dubois.)", FONDO_ACTIVO),
    ("LEDIAGO",   "Y artistas transformaron la materia en memoria.", FONDO_ACTIVO),
    ("ABOGADO",   "Todo eso sigue siendo pasado.", FONDO_ACTIVO),
    ("LEDIAGO",   "No.", FONDO_ACTIVO),
    ("LEDIAGO",   "El pasado es lo que sostiene el presente.", FONDO_ACTIVO),
    ("JUEZ",      "Y como pretende demostrarlo?", FONDO_ACTIVO),
    ("WALTER",    "Activemos el Cronoscopio.", FONDO_ACTIVO),
    ("LEDO",      "Es momento de que la ciudad hable por si misma.", FONDO_ACTIVO),
    ("NARRADOR",  "(El Cronoscopio comienza a iluminarse.)", FONDO_ACTIVO),
    ("ABOGADO",   "Que es eso?", FONDO_ACTIVO),
    ("LEDIAGO",   "Escuche.", FONDO_ACTIVO),
    ("NARRADOR",  "(Se oye el sonido del agua del Tajamar.)", FONDO_ACTIVO),
    ("CIUDADANOS","...", FONDO_ACTIVO),
    ("NARRADOR",  "(Se escuchan martillos de los canteros.)", FONDO_ACTIVO),
    ("CIUDADANOS","...", FONDO_ACTIVO),
    ("NARRADOR",  "(Comienza a sonar un piano lejano.)", FONDO_ACTIVO),
    ("CIUDADANOS","...", FONDO_ACTIVO),
    ("NARRADOR",  "(Voces indigenas, campanas jesuitas y cantos de peregrinos "
                  "llenan el salon.)", FONDO_ACTIVO),
    ("JUEZ",      "Que esta ocurriendo?", FONDO_ACTIVO),
    ("WALTER",    "La memoria de Alta Gracia.", FONDO_ACTIVO),
    ("LEDO",      "La historia que aun vive entre nosotros.", FONDO_ACTIVO),
    ("ABOGADO",   "Esto... esto no puede ser posible.", FONDO_ACTIVO),
    ("LEDIAGO",   "La ciudad no es un conjunto de edificios.", FONDO_ACTIVO),
    ("LEDIAGO",   "Es la suma de todas las vidas que la construyeron.", FONDO_ACTIVO),
    ("JUEZ",      "He escuchado suficiente.", FONDO_ACTIVO),
    ("NARRADOR",  "(Silencio absoluto.)", FONDO_ACTIVO),
    ("JUEZ",      "Este tribunal determina que el patrimonio historico y cultural "
                  "de Alta Gracia posee un valor excepcional e irremplazable.", FONDO_CERRADO),
    ("ABOGADO",   "Protesto!", FONDO_CERRADO),
    ("JUEZ",      "Protesta denegada.", FONDO_CERRADO),
]


# ============================================================
# ESCENA DEL JUICIO
# ============================================================
class JuicioView(arcade.View):
    def __init__(self, vista_siguiente=None) -> None:
        super().__init__()
        self.vista_siguiente = vista_siguiente
        self.texturas_fondo = {
            FONDO_INICIO:  arcade.load_texture(codigosb.JUICIO_FONDO_INICIO),
            FONDO_ACTIVO:  arcade.load_texture(codigosb.JUICIO_FONDO_ACTIVO),
            FONDO_CERRADO: arcade.load_texture(codigosb.JUICIO_FONDO_CERRADO),
        }
        self.indice_linea_actual = 0
        self.escena_terminada    = False

    def on_draw(self):
        self.clear()
        hablante_clave, texto, fondo_clave = GUION_JUICIO[self.indice_linea_actual]
        arcade.draw_texture_rect(
            self.texturas_fondo[fondo_clave],
            arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO))
        self._dibujar_cuadro(hablante_clave, texto)
        if self.escena_terminada:
            arcade.draw_text("FIN DE LA ESCENA",
                codigosb.ANCHO//2, codigosb.ALTO-30,
                arcade.color.WHITE, font_size=14, bold=True, anchor_x="center")

    def _dibujar_cuadro(self, hablante_clave, texto):
        info = HABLANTES[hablante_clave]
        alto_caja = 150
        m = 20
        arcade.draw_rect_filled(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja), (0,0,0,210))
        arcade.draw_rect_outline(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja),
            info["color_borde"], border_width=3)
        if hablante_clave != "NARRADOR":
            arcade.draw_rect_filled(
                arcade.LRBT(m, m+230, alto_caja-4, alto_caja+26), (0,0,0,230))
            arcade.draw_rect_outline(
                arcade.LRBT(m, m+230, alto_caja-4, alto_caja+26),
                info["color_borde"], border_width=2)
            arcade.draw_text(info["nombre"], m+14, alto_caja+3,
                info["color_nombre"], font_size=13, bold=True, anchor_y="center")
        color_texto = (arcade.color.LIGHT_GRAY if hablante_clave == "NARRADOR"
                       else arcade.color.WHITE)
        arcade.draw_text(texto, m+20, alto_caja-30, color_texto,
            font_size=15, width=codigosb.ANCHO-(m*2)-40,
            multiline=True, anchor_y="top")
        arcade.draw_text(
            f"{self.indice_linea_actual+1}/{len(GUION_JUICIO)}   "
            "[Espacio] Siguiente...",
            codigosb.ANCHO-m-230, m+8,
            arcade.color.GRAY, font_size=11)

    def avanzar_dialogo(self):
        if self.escena_terminada:
            self._terminar_escena()
            return
        self.indice_linea_actual += 1
        if self.indice_linea_actual >= len(GUION_JUICIO):
            self.indice_linea_actual = len(GUION_JUICIO) - 1
            self.escena_terminada = True

    def _terminar_escena(self):
        if self.vista_siguiente is None:
            return
        siguiente = self.vista_siguiente() if callable(self.vista_siguiente) \
                    else self.vista_siguiente
        self.window.show_view(siguiente)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.ENTER):
            self.avanzar_dialogo()

    def on_mouse_press(self, x, y, button, modifiers):
        self.avanzar_dialogo()


# ============================================================
# GUION DEL HOTEL SIERRAS
# ============================================================
GUION_HOTEL = [
    ("WALTER",   "Por fin despertaste!"),
    ("LEDIAGO",  "Donde estoy?"),
    ("LEDO",     "En el Hotel Sierras. O mejor dicho... en lo que queda de el."),
    ("LEDIAGO",  "No entiendo nada. Quienes son ustedes?"),
    ("WALTER",   "Mi nombre es Walter."),
    ("LEDO",     "Y yo soy Ledo. Somos los guardianes del Archivo Historico de Alta Gracia."),
    ("LEDIAGO",  "Y por que me trajeron aqui?"),
    ("WALTER",   "Porque la ciudad esta en peligro. Muy pronto todo esto podria desaparecer."),
    ("LEDIAGO",  "Desaparecer?"),
    ("LEDO",     "Una corporacion quiere demoler los lugares historicos para construir algo nuevo."),
    ("LEDIAGO",  "Y que esperan que haga yo?"),
    ("NARRADOR", "(Walter senala una extrana maquina llena de engranajes y luces.)"),
    ("WALTER",   "Necesitamos que uses el Cronoscopio."),
    ("LEDIAGO",  "Cronoscopio?"),
    ("LEDO",     "Una maquina capaz de abrir puertas hacia distintas epocas de Alta Gracia."),
    ("LEDIAGO",  "Me estan diciendo que viaje en el tiempo?"),
    ("WALTER",   "Exactamente."),
    ("LEDIAGO",  "Eso suena imposible."),
    ("LEDO",     "Tambien sonaba imposible perder toda la historia de una ciudad."),
    ("WALTER",   "Tu mision sera viajar al pasado, conocer a quienes construyeron esta tierra "
                 "y recuperar fragmentos de su memoria."),
    ("LEDIAGO",  "Y si algo sale mal?"),
    ("LEDO",     "No cambiaras la historia."),
    ("WALTER",   "Solo la observaras... y traeras pruebas de que sigue viva."),
    ("NARRADOR", "(El Cronoscopio comienza a iluminarse.)"),
    ("LEDIAGO",  "Supongo que no tengo muchas opciones."),
    ("LEDO",     "Ninguna."),
    ("WALTER",   "Preparate, viajero."),
    ("LEDO",     "Tu primera parada te espera hace cientos de anios."),
]


# ============================================================
# ESCENA DEL HOTEL SIERRAS (gameplay + dialogo con Walter y Ledo)
# ============================================================
class HotelSierrasView(arcade.View):
    """
    Lediago camina por el salon del Hotel Sierras.
    Al hacer click/espacio cerca de Walter y Ledo se dispara el dialogo.
    Al terminar el dialogo pasa a VitrinaView.
    """

    FASE_GAMEPLAY = 0
    FASE_DIALOGO  = 1

    def __init__(self, musica_fondo=None, reproductor_musica=None,
                 inventario: Inventario = None) -> None:
        super().__init__()

        self.fase       = HotelSierrasView.FASE_GAMEPLAY
        self.inventario = inventario or Inventario()

        # Musica heredada
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(
                volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True)

        # Fondo
        self.tex_fondo   = arcade.load_texture(codigosb.HOTEL_SIERRAS_FONDO)
        self.tex_npc_idle = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_IDLE)
        self.tex_npc_afk  = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_AFK)
        self.tex_npc_dlg  = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_DLG)

        # Proporciones de los NPCs
        self._npc_escala = 155 / 1536
        self._npc_ancho  = int(1024 * self._npc_escala)
        self._npc_alto   = int(1536 * self._npc_escala)
        self._npc_cx = int(codigosb.ANCHO * 0.74)
        self._npc_cy = int(codigosb.ALTO  * 0.42)
        self._npc_rect_x1 = self._npc_cx - self._npc_ancho//2 - 15
        self._npc_rect_x2 = self._npc_cx + self._npc_ancho//2 + 15
        self._npc_rect_y1 = self._npc_cy - self._npc_alto//2  - 10
        self._npc_rect_y2 = self._npc_cy + self._npc_alto//2  + 10

        # Personaje con sprite sheet
        self.player = Lediago(escala=0.28)
        self.player.center_x = codigosb.ANCHO * 0.30
        self.player.center_y = 90
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Teclas
        self.w_ap = self.s_ap = self.a_ap = self.d_ap = self.shift_ap = False

        # Dialogo
        self.dialogo_lineas = []
        self.dialogo_idx    = 0
        self.dialogo_fin    = False

        # Animacion idle NPCs
        self._anim_timer   = 0.0
        self._anim_periodo = 3.5
        self._npc_pose_afk = False

        # Indicador: si el jugador ya esta cerca de los NPCs
        self._hint_visible = False

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------
    def _evaluar_movimiento(self):
        vel = codigosb.VELOCIDAD_CORRER if self.shift_ap else codigosb.VELOCIDAD_CAMINAR
        self.player.esta_corriendo = self.shift_ap
        self.player.change_x = 0
        self.player.change_y = 0
        if self.w_ap and not self.s_ap:
            self.player.change_y = vel
        elif self.s_ap and not self.w_ap:
            self.player.change_y = -vel
        if self.a_ap and not self.d_ap:
            self.player.change_x = -vel
        elif self.d_ap and not self.a_ap:
            self.player.change_x = vel
        self.player.actualizar_direccion()

    def _click_en_npc(self, x, y):
        return (self._npc_rect_x1 <= x <= self._npc_rect_x2 and
                self._npc_rect_y1 <= y <= self._npc_rect_y2)

    def _cerca_de_npc(self):
        dx = self.player.center_x - self._npc_cx
        dy = self.player.center_y - self._npc_cy
        return (dx*dx + dy*dy) < 180*180

    def _iniciar_dialogo(self):
        self.dialogo_lineas = GUION_HOTEL
        self.dialogo_idx    = 0
        self.dialogo_fin    = False
        self.fase = HotelSierrasView.FASE_DIALOGO
        self.player.change_x = 0
        self.player.change_y = 0

    def _avanzar_dialogo(self):
        if self.dialogo_fin:
            self._ir_a_vitrina()
            return
        self.dialogo_idx += 1
        if self.dialogo_idx >= len(self.dialogo_lineas):
            self.dialogo_idx = len(self.dialogo_lineas) - 1
            self.dialogo_fin = True

    def _ir_a_vitrina(self):
        """Pasa a la VitrinaView llevando el inventario."""
        self.window.show_view(
            VitrinaView(
                musica_fondo=self.musica_fondo,
                reproductor_musica=self.reproductor_musica,
                inventario=self.inventario,
            )
        )

    def _npc_en_pose_dialogo(self):
        if self.dialogo_idx >= len(self.dialogo_lineas):
            return False
        hab, _ = self.dialogo_lineas[self.dialogo_idx]
        return hab in ("WALTER", "LEDO")

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.tex_fondo,
            arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO))

        # NPCs
        if self.fase == HotelSierrasView.FASE_DIALOGO:
            tex_npc = self.tex_npc_dlg if self._npc_en_pose_dialogo() else self.tex_npc_idle
        else:
            tex_npc = self.tex_npc_afk if self._npc_pose_afk else self.tex_npc_idle

        arcade.draw_texture_rect(
            tex_npc,
            arcade.LBWH(
                self._npc_cx - self._npc_ancho//2,
                self._npc_cy - self._npc_alto//2,
                self._npc_ancho, self._npc_alto))

        self.player_list.draw()

        if self.fase == HotelSierrasView.FASE_GAMEPLAY and self._cerca_de_npc():
            arcade.draw_text(
                "[ ESPACIO / CLICK ] Hablar",
                self._npc_cx,
                self._npc_cy + self._npc_alto//2 + 14,
                arcade.color.YELLOW, font_size=11,
                anchor_x="center", bold=True)

        if self.fase == HotelSierrasView.FASE_DIALOGO:
            self._dibujar_cuadro_dialogo()

    def _dibujar_cuadro_dialogo(self):
        if self.dialogo_idx >= len(self.dialogo_lineas):
            return
        hablante_clave, texto = self.dialogo_lineas[self.dialogo_idx]
        info = HABLANTES[hablante_clave]
        alto_caja = 150
        m = 20
        arcade.draw_rect_filled(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja), (0,0,0,210))
        arcade.draw_rect_outline(
            arcade.LRBT(m, codigosb.ANCHO-m, m, alto_caja),
            info["color_borde"], border_width=3)
        if hablante_clave != "NARRADOR":
            arcade.draw_rect_filled(
                arcade.LRBT(m, m+230, alto_caja-4, alto_caja+26), (0,0,0,230))
            arcade.draw_rect_outline(
                arcade.LRBT(m, m+230, alto_caja-4, alto_caja+26),
                info["color_borde"], border_width=2)
            arcade.draw_text(info["nombre"], m+14, alto_caja+3,
                info["color_nombre"], font_size=13, bold=True, anchor_y="center")
        color_texto = (arcade.color.LIGHT_GRAY if hablante_clave == "NARRADOR"
                       else arcade.color.WHITE)
        arcade.draw_text(texto, m+20, alto_caja-30, color_texto,
            font_size=15, width=codigosb.ANCHO-(m*2)-40,
            multiline=True, anchor_y="top")
        if not self.dialogo_fin:
            pista = (f"{self.dialogo_idx+1}/{len(self.dialogo_lineas)}   "
                     "[Espacio / Click] Siguiente...")
        else:
            pista = "- FIN -  [Espacio] Continuar al Estudio..."
        arcade.draw_text(pista, codigosb.ANCHO-m-10, m+8,
            arcade.color.GRAY, font_size=11, anchor_x="right")

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            if key == arcade.key.W:    self.w_ap = True
            elif key == arcade.key.S:  self.s_ap = True
            elif key == arcade.key.A:  self.a_ap = True
            elif key == arcade.key.D:  self.d_ap = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = True
            elif key == arcade.key.SPACE and self._cerca_de_npc():
                self._iniciar_dialogo()
            self._evaluar_movimiento()
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            if key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_dialogo()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:    self.w_ap = False
        elif key == arcade.key.S:  self.s_ap = False
        elif key == arcade.key.A:  self.a_ap = False
        elif key == arcade.key.D:  self.d_ap = False
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_ap = False
        self._evaluar_movimiento()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            if self._click_en_npc(x, y):
                self._iniciar_dialogo()
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            self._avanzar_dialogo()

    def on_update(self, delta_time):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            nueva_x = self.player.center_x + self.player.change_x
            nueva_y = self.player.center_y + self.player.change_y
            mw = self.player.width  / 2
            mh = self.player.height / 2
            self.player.center_x = max(mw, min(codigosb.ANCHO-mw, nueva_x))
            self.player.center_y = max(mh, min(codigosb.ALTO-mh,  nueva_y))
            self.player.update_animation(delta_time)

            # Animar NPCs entre idle y afk
            self._anim_timer += delta_time
            if self._anim_timer >= self._anim_periodo:
                self._anim_timer   = 0.0
                self._npc_pose_afk = not self._npc_pose_afk


# ============================================================
#  VITRINA DE OBJETOS RECOLECTADOS (Estudio de Curiosidades)
# ============================================================
class VitrinaView(arcade.View):
    """
    Escena del Estudio de Curiosidades - Vitrina de Objetos Recolectados.

    Casillas disponibles:
      [E]  Entrar / Salir del Sierras Hotel
      [V]  Abrir / Cerrar la vitrina
      [G]  Guardar partida y objetos (guarda el Inventario a JSON)
      [C]  Usar el Cronoscopio (requiere tenerlo en el inventario)
      Click sobre objeto -> ver descripcion

    El Cronoscopio aparece en el estante superior izquierdo
    (zona marcada con circulo azul en vitrina.jpeg) cuando esta
    en el inventario.
    """

    FASE_CERRADA  = "cerrada"
    FASE_ABIERTA  = "abierta"

    # Posicion y tamano del Cronoscopio en la vitrina (estante superior izq)
    CRONO_X  = 205    # centro horizontal en la pantalla de vitrina
    CRONO_Y  = 390    # centro vertical
    CRONO_W  = 100
    CRONO_H  = 140

    def __init__(self, musica_fondo=None, reproductor_musica=None,
                 inventario: Inventario = None) -> None:
        super().__init__()

        self.inventario = inventario or Inventario()

        # Musica heredada
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(
                volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True)

        # Fondos
        self.tex_fondo_cerrada = arcade.load_texture(codigosb.VITRINA_FONDO)
        self.tex_fondo_abierta = arcade.load_texture(codigosb.VITRINA_ABIERTA)
        self.tex_cronoscopio   = arcade.load_texture(codigosb.CRONOSCOPIO_IMG)

        self.fase_vitrina = VitrinaView.FASE_CERRADA

        # Al cargar, si el Cronoscopio aun no esta en el inventario,
        # se lo agregamos automaticamente porque acaba de terminar la
        # escena en la que Walter y Ledo se lo presentaron.
        if not self.inventario.tiene("Cronoscopio"):
            self.inventario.agregar("Cronoscopio")

        # Mensaje flotante de retroalimentacion (guardado, etc.)
        self._msg            = ""
        self._msg_timer      = 0.0
        self._msg_duracion   = 2.5

        # Objeto seleccionado para ver descripcion
        self._obj_seleccionado = None
        self._desc_visible     = False

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------
    def _mostrar_msg(self, texto: str):
        self._msg       = texto
        self._msg_timer = self._msg_duracion

    def _guardar(self):
        ok = self.inventario.guardar()
        if ok:
            self._mostrar_msg("Partida guardada correctamente.")
        else:
            self._mostrar_msg("Error al guardar la partida.")

    def _usar_cronoscopio(self):
        if not self.inventario.tiene("Cronoscopio"):
            self._mostrar_msg("No tienes el Cronoscopio todavia.")
            return
        self.inventario.turno_viaje += 1
        self.inventario.guardar()
        # El Cronoscopio abre una puerta en el tiempo: viaja a la
        # Estancia Jesuitica, donde espera el Cura con su desafio.
        self.window.show_view(
            GameView(
                musica_fondo=self.musica_fondo,
                reproductor_musica=self.reproductor_musica,
                inventario=self.inventario,
            )
        )

    def _volver_al_hotel(self):
        """Vuelve a la escena del Hotel Sierras conservando el inventario."""
        self.window.show_view(
            HotelSierrasView(
                musica_fondo=self.musica_fondo,
                reproductor_musica=self.reproductor_musica,
                inventario=self.inventario,
            )
        )

    def _click_en_cronoscopio(self, x, y) -> bool:
        """Devuelve True si el click cayo sobre el Cronoscopio en la vitrina."""
        if not self.inventario.tiene("Cronoscopio"):
            return False
        if self.fase_vitrina != VitrinaView.FASE_ABIERTA:
            return False
        cx, cy = self.CRONO_X, self.CRONO_Y
        hw, hh = self.CRONO_W//2, self.CRONO_H//2
        return (cx-hw <= x <= cx+hw) and (cy-hh <= y <= cy+hh)

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self):
        self.clear()

        # Fondo segun estado de vitrina
        if self.fase_vitrina == VitrinaView.FASE_CERRADA:
            arcade.draw_texture_rect(
                self.tex_fondo_cerrada,
                arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO))
        else:
            arcade.draw_texture_rect(
                self.tex_fondo_abierta,
                arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO))

            # Si tiene el Cronoscopio, mostrarlo en el estante sup izq
            if self.inventario.tiene("Cronoscopio"):
                arcade.draw_texture_rect(
                    self.tex_cronoscopio,
                    arcade.LBWH(
                        self.CRONO_X - self.CRONO_W//2,
                        self.CRONO_Y - self.CRONO_H//2,
                        self.CRONO_W,
                        self.CRONO_H,
                    )
                )
                # Brillo / indicador interactivo
                arcade.draw_rect_outline(
                    arcade.LRBT(
                        self.CRONO_X - self.CRONO_W//2 - 3,
                        self.CRONO_X + self.CRONO_W//2 + 3,
                        self.CRONO_Y - self.CRONO_H//2 - 3,
                        self.CRONO_Y + self.CRONO_H//2 + 3,
                    ),
                    (80, 200, 255, 180),
                    border_width=2,
                )

            # Mini-lista de objetos recolectados (lado derecho)
            self._dibujar_lista_objetos()

        # Panel de controles (siempre visible)
        self._dibujar_panel_controles()

        # Descripcion del objeto seleccionado
        if self._desc_visible and self._obj_seleccionado:
            self._dibujar_descripcion()

        # Mensaje flotante
        if self._msg_timer > 0:
            self._dibujar_mensaje()

    def _dibujar_panel_controles(self):
        """Franja de controles en la parte inferior."""
        m = 8
        y_panel = 50

        arcade.draw_rect_filled(
            arcade.LRBT(0, codigosb.ANCHO, 0, y_panel+4),
            (0, 0, 0, 200))

        estado_vitrina = "Abrir vitrina" if self.fase_vitrina == VitrinaView.FASE_CERRADA \
                         else "Cerrar vitrina"

        controles = [
            ("[E] Salir al Hotel",  arcade.color.YELLOW),
            (f"[V] {estado_vitrina}", arcade.color.CYAN),
            ("[G] Guardar partida", arcade.color.GREEN_YELLOW),
            ("[C] Usar Cronoscopio", arcade.color.LIGHT_PASTEL_PURPLE),
        ]

        paso = codigosb.ANCHO // len(controles)
        for i, (texto, color) in enumerate(controles):
            arcade.draw_text(
                texto,
                paso * i + paso//2, m + 12,
                color, font_size=11, bold=True,
                anchor_x="center", anchor_y="center")

    def _dibujar_lista_objetos(self):
        """Muestra los objetos recolectados en un panel lateral."""
        recolectados = self.inventario.recolectados()
        if not recolectados:
            return

        x_panel = 510
        y_ini   = 530
        arcade.draw_rect_filled(
            arcade.LRBT(x_panel - 10, codigosb.ANCHO - 8, 60, y_ini + 10),
            (0, 0, 0, 170))
        arcade.draw_rect_outline(
            arcade.LRBT(x_panel - 10, codigosb.ANCHO - 8, 60, y_ini + 10),
            arcade.color.GOLD, border_width=1)
        arcade.draw_text(
            "OBJETOS RECOLECTADOS",
            x_panel + 120, y_ini,
            arcade.color.GOLD, font_size=10, bold=True, anchor_x="center")

        for idx, nombre in enumerate(recolectados):
            y = y_ini - 22 - idx * 18
            if y < 70:
                break
            arcade.draw_text(
                f"• {nombre}",
                x_panel, y,
                arcade.color.WHITE, font_size=10)

    def _dibujar_descripcion(self):
        """Panel flotante con el nombre y descripcion del objeto seleccionado."""
        nombre = self._obj_seleccionado
        desc   = Inventario.OBJETOS_POSIBLES.get(nombre, "")
        m = 60
        arcade.draw_rect_filled(
            arcade.LRBT(m, codigosb.ANCHO-m, 200, 420),
            (10, 10, 30, 230))
        arcade.draw_rect_outline(
            arcade.LRBT(m, codigosb.ANCHO-m, 200, 420),
            arcade.color.GOLD, border_width=2)
        arcade.draw_text(nombre,
            codigosb.ANCHO//2, 405,
            arcade.color.GOLD, font_size=16, bold=True,
            anchor_x="center")
        arcade.draw_text(desc,
            m+20, 380,
            arcade.color.WHITE, font_size=13,
            width=codigosb.ANCHO-m*2-40,
            multiline=True, anchor_y="top")
        arcade.draw_text("[Click] Cerrar",
            codigosb.ANCHO//2, 215,
            arcade.color.GRAY, font_size=11, anchor_x="center")

    def _dibujar_mensaje(self):
        """Mensaje flotante centrado en pantalla."""
        arcade.draw_rect_filled(
            arcade.LRBT(80, codigosb.ANCHO-80, 260, 320),
            (0, 0, 0, 210))
        arcade.draw_rect_outline(
            arcade.LRBT(80, codigosb.ANCHO-80, 260, 320),
            arcade.color.CYAN, border_width=2)
        arcade.draw_text(
            self._msg,
            codigosb.ANCHO//2, 290,
            arcade.color.WHITE, font_size=13,
            anchor_x="center", anchor_y="center",
            width=codigosb.ANCHO-200, multiline=True)

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        # Si hay descripcion abierta, cualquier tecla la cierra
        if self._desc_visible:
            self._desc_visible     = False
            self._obj_seleccionado = None
            return

        if key == arcade.key.E:
            self._volver_al_hotel()
        elif key == arcade.key.V:
            if self.fase_vitrina == VitrinaView.FASE_CERRADA:
                self.fase_vitrina = VitrinaView.FASE_ABIERTA
            else:
                self.fase_vitrina = VitrinaView.FASE_CERRADA
        elif key == arcade.key.G:
            self._guardar()
        elif key == arcade.key.C:
            self._usar_cronoscopio()

    def on_mouse_press(self, x, y, button, modifiers):
        # Cerrar descripcion con click
        if self._desc_visible:
            self._desc_visible     = False
            self._obj_seleccionado = None
            return

        # Click sobre el Cronoscopio en la vitrina abierta
        if self._click_en_cronoscopio(x, y):
            self._obj_seleccionado = "Cronoscopio"
            self._desc_visible     = True

    def on_update(self, delta_time):
        if self._msg_timer > 0:
            self._msg_timer -= delta_time
            if self._msg_timer < 0:
                self._msg_timer = 0


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
def main():
    window = arcade.Window(codigosb.ANCHO, codigosb.ALTO, codigosb.TITULO)
    window.center_window()

    from intro import IntroView
    intro = IntroView()
    window.show_view(intro)
    arcade.run()


if __name__ == "__main__":
    main()
