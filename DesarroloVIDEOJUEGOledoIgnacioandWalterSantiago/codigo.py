#python "e:/Programacion 3/01Heladeria WalterSantiago/Python-Reposity/DesarroloVIDEOJUEGOledoIgnacioandWalterSantiago/codigo.py"
# ============================================================
# REMINENCE OF GRACIA - PUNTO DE ENTRADA PRINCIPAL DEL JUEGO
# ============================================================
# Este archivo une las partes que estaban sueltas en el proyecto:
#   - codigosb.py                  -> configuracion (tamaño ventana, velocidades, rutas)
#   - animacion_correrycamonar.py  -> referencia del sistema de movimiento/animacion
#   - codigo_textointeractivo.py   -> referencia del sistema de dialogo con NPC
#   - JuicioView (mas abajo)       -> escena del juicio en el Sierras Hotel
# Todo corre sobre Arcade 3.x (las funciones de dibujo viejas de Arcade 2.x
# como draw_xywh_rectangle_filled / draw_rectangle_filled ya no existen).
import arcade
import codigosb

# ------------------------------------------------------------
# DIRECCIONES POSIBLES DEL PERSONAJE
# ------------------------------------------------------------
FRENTE = 0
ESPALDA = 1
IZQUIERDA = 2
DERECHA = 3

# ------------------------------------------------------------
# ESTADOS DEL JUEGO
# ------------------------------------------------------------
ESTADO_JUGANDO = 0
ESTADO_HABLANDO = 1


class Lediago(arcade.Sprite):
    """ Personaje principal. Usa los 3 sprites reales del proyecto
    (frente, espalda y perfil) y espeja el perfil para mirar a la izquierda,
    ya que no existen hojas de animacion (spritesheets) todavia. """

    def __init__(self):
        super().__init__(codigosb.SPRITE_FRENTE, scale=codigosb.ESCALA_PERSONAJE)
        self.direccion_actual = FRENTE
        self.esta_corriendo = False

        self.textura_frente = arcade.load_texture(codigosb.SPRITE_FRENTE)
        self.textura_espalda = arcade.load_texture(codigosb.SPRITE_ESPALDA)
        self.textura_derecha = arcade.load_texture(codigosb.SPRITE_PERFIL)
        self.textura_izquierda = self.textura_derecha.flip_left_right()
        self.texture = self.textura_frente

    def actualizar_direccion(self):
        """ Elige la textura segun hacia donde se mueve el personaje. """
        if self.change_x < 0:
            self.direccion_actual = IZQUIERDA
        elif self.change_x > 0:
            self.direccion_actual = DERECHA
        elif self.change_y > 0:
            self.direccion_actual = ESPALDA
        elif self.change_y < 0:
            self.direccion_actual = FRENTE

        if self.direccion_actual == FRENTE:
            self.texture = self.textura_frente
        elif self.direccion_actual == ESPALDA:
            self.texture = self.textura_espalda
        elif self.direccion_actual == IZQUIERDA:
            self.texture = self.textura_izquierda
        elif self.direccion_actual == DERECHA:
            self.texture = self.textura_derecha


class GameView(arcade.View):
    def __init__(self, musica_fondo=None, reproductor_musica=None) -> None:
        super().__init__()

        self.estado_actual = ESTADO_JUGANDO

        # Musica de fondo: si viene desde la IntroView, la seguimos usando
        # tal cual (sin reiniciarla, para que no se corte el loop). Si se
        # entra directo a GameView (por ejemplo en pruebas), la arrancamos
        # nosotros mismos en volumen bajo.
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(
                volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True
            )

        # Fondo de la Estancia Jesuitica
        self.fondo = arcade.load_texture(codigosb.FONDO_ESTANCIA)

        # Personaje
        self.player_sprite = Lediago()
        self.player_sprite.center_x = codigosb.ANCHO // 2
        self.player_sprite.center_y = codigosb.ALTO // 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # NPC con el que se puede hablar
        self.npc_sprite = arcade.SpriteSolidColor(32, 32, color=arcade.color.RED)
        self.npc_sprite.center_x = codigosb.ANCHO - 200
        self.npc_sprite.center_y = codigosb.ALTO // 2
        self.npc_list = arcade.SpriteList()
        self.npc_list.append(self.npc_sprite)

        # Teclas presionadas
        self.w_apretada = False
        self.s_apretada = False
        self.a_apretada = False
        self.d_apretada = False
        self.shift_apretado = False

        # Dialogo
        self.dialogo_lineas = []
        self.indice_linea_actual = 0

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self) -> None:
        self.clear()

        # Fondo de la Estancia, estirado a toda la ventana
        arcade.draw_texture_rect(
            self.fondo,
            arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO),
        )

        self.npc_list.draw()
        self.player_list.draw()

        if self.estado_actual == ESTADO_HABLANDO:
            self.dibujar_cuadro_dialogo()

    def dibujar_cuadro_dialogo(self):
        """ Dibuja el rectangulo del fondo y el texto actual del dialogo. """
        arcade.draw_rect_filled(
            arcade.LRBT(20, codigosb.ANCHO - 20, 20, 140),
            arcade.color.BLACK,
        )
        arcade.draw_rect_outline(
            arcade.LRBT(20, codigosb.ANCHO - 20, 20, 140),
            arcade.color.WHITE,
            border_width=3,
        )

        texto_a_mostrar = self.dialogo_lineas[self.indice_linea_actual]
        arcade.draw_text(
            texto_a_mostrar,
            40, 90,
            arcade.color.WHITE,
            font_size=16,
            width=codigosb.ANCHO - 80,
            multiline=True,
        )
        arcade.draw_text(
            "[Espacio] Siguiente...",
            codigosb.ANCHO - 220, 35,
            arcade.color.GRAY,
            font_size=12,
        )

    # --------------------------------------------------------
    # MOVIMIENTO
    # --------------------------------------------------------
    def evaluar_movimiento(self):
        """ Calcula la velocidad final combinando direccion y Shift (correr). """
        velocidad = codigosb.VELOCIDAD_CORRER if self.shift_apretado else codigosb.VELOCIDAD_CAMINAR
        self.player_sprite.esta_corriendo = self.shift_apretado

        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.w_apretada and not self.s_apretada:
            self.player_sprite.change_y = velocidad
        elif self.s_apretada and not self.w_apretada:
            self.player_sprite.change_y = -velocidad

        if self.a_apretada and not self.d_apretada:
            self.player_sprite.change_x = -velocidad
        elif self.d_apretada and not self.a_apretada:
            self.player_sprite.change_x = velocidad

        self.player_sprite.actualizar_direccion()

    # --------------------------------------------------------
    # DIALOGO
    # --------------------------------------------------------
    def disparar_dialogo(self, lineas_texto):
        """ Activa el cuadro de texto y congela el movimiento del jugador. """
        self.dialogo_lineas = lineas_texto
        self.indice_linea_actual = 0
        self.estado_actual = ESTADO_HABLANDO
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if key == arcade.key.W:
                self.w_apretada = True
            elif key == arcade.key.S:
                self.s_apretada = True
            elif key == arcade.key.A:
                self.a_apretada = True
            elif key == arcade.key.D:
                self.d_apretada = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_apretado = True
            elif key == arcade.key.SPACE:
                distancia = arcade.get_distance_between_sprites(
                    self.player_sprite, self.npc_sprite
                )
                if distancia < 80:
                    conversacion = [
                        "Hola Lediago... Bienvenido a la Estancia Jesuitica.",
                        "Necesitamos tu ayuda para resolver el misterio de Gracia.",
                        "Busca pistas en el ala norte del edificio antes de que sea tarde.",
                    ]
                    self.disparar_dialogo(conversacion)
            elif key == arcade.key.J:
                # Tecla de prueba: dispara la escena del juicio desde el
                # juego (pensada como evento de la historia mas adelante).
                self.iniciar_juicio()

            self.evaluar_movimiento()

        elif self.estado_actual == ESTADO_HABLANDO:
            if key == arcade.key.SPACE:
                self.indice_linea_actual += 1
                if self.indice_linea_actual >= len(self.dialogo_lineas):
                    self.estado_actual = ESTADO_JUGANDO

    def on_key_release(self, key, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if key == arcade.key.W:
                self.w_apretada = False
            elif key == arcade.key.S:
                self.s_apretada = False
            elif key == arcade.key.A:
                self.a_apretada = False
            elif key == arcade.key.D:
                self.d_apretada = False
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_apretado = False

            self.evaluar_movimiento()

    # --------------------------------------------------------
    # ACTUALIZACION POR FRAME
    # --------------------------------------------------------
    def on_update(self, delta_time: float):
        if self.estado_actual == ESTADO_JUGANDO:
            nueva_x = self.player_sprite.center_x + self.player_sprite.change_x
            nueva_y = self.player_sprite.center_y + self.player_sprite.change_y

            # No deja que el personaje salga de los limites de la ventana
            mitad_ancho = self.player_sprite.width / 2
            mitad_alto = self.player_sprite.height / 2
            nueva_x = max(mitad_ancho, min(codigosb.ANCHO - mitad_ancho, nueva_x))
            nueva_y = max(mitad_alto, min(codigosb.ALTO - mitad_alto, nueva_y))

            self.player_sprite.center_x = nueva_x
            self.player_sprite.center_y = nueva_y

    # --------------------------------------------------------
    # SALTO A LA ESCENA DEL JUICIO
    # --------------------------------------------------------
    def iniciar_juicio(self):
        """ Pasa de GameView a la escena del juicio (JuicioView, definida
        mas abajo en este mismo archivo). Le pasamos self (esta GameView)
        como vista_siguiente para que, al terminar la escena, se vuelva a
        este mismo punto del juego en vez de quedarse trabado en el FIN. """
        self.window.show_view(JuicioView(vista_siguiente=self))


# ============================================================
# ESCENA DEL JUICIO (SIERRAS HOTEL)
# ============================================================
# Reproduce la escena "EL JUICIO EN EL SIERRAS HOTEL" como una secuencia de
# dialogo tipo novela visual, arriba de los 3 fondos del Tribunal Superior
# de Gracia:
#   - JUICIO_FONDO_INICIO  -> arranca la sesion (juez sentado, presentando)
#   - JUICIO_FONDO_ACTIVO  -> el juez de pie gritando "¡Orden en la sala!"
#   - JUICIO_FONDO_CERRADO -> mazo golpeado, veredicto, "CASO CERRADO"
#
# Cada linea del guion sabe a que personaje pertenece (JUEZ, ABOGADO,
# WALTER, LEDO, LEDIAGO, CIUDADANOS o NARRADOR para las acotaciones entre
# parentesis) y el cuadro de dialogo de abajo cambia de color/etiqueta
# segun quien esta hablando, ademas de mostrar el fondo que corresponda
# a ese momento de la escena.
#
# Como entrar a esta vista desde cualquier otro punto del juego:
#   window.show_view(JuicioView())
# o, para volver a una vista concreta al terminar (por ejemplo GameView):
#   window.show_view(JuicioView(vista_siguiente=alguna_vista))

# ------------------------------------------------------------
# FONDOS POSIBLES DE LA ESCENA
# ------------------------------------------------------------
FONDO_INICIO = "inicio"
FONDO_ACTIVO = "activo"
FONDO_CERRADO = "cerrado"

# ------------------------------------------------------------
# COLOR DE CUADRO DE DIALOGO SEGUN QUIEN HABLA
# (nombre que se muestra, color de la etiqueta y color del borde
# del cuadro, para distinguir de un vistazo quien esta hablando)
# ------------------------------------------------------------
HABLANTES = {
    "JUEZ": {
        "nombre": "JUEZ DEL TRIBUNAL",
        "color_nombre": arcade.color.GOLD,
        "color_borde": arcade.color.GOLD,
    },
    "ABOGADO": {
        "nombre": "ABOGADO DE LA CORPORACIÓN",
        "color_nombre": arcade.color.RED_DEVIL,
        "color_borde": arcade.color.RED_DEVIL,
    },
    "WALTER": {
        "nombre": "WALTER",
        "color_nombre": arcade.color.CYAN,
        "color_borde": arcade.color.CYAN,
    },
    "LEDO": {
        "nombre": "LEDO",
        "color_nombre": arcade.color.GREEN_YELLOW,
        "color_borde": arcade.color.GREEN_YELLOW,
    },
    "LEDIAGO": {
        "nombre": "LEDIAGO WALEDO",
        # OJO: "LIGHT_VIOLET" no existe en arcade.color (eso tiraba el
        # AttributeError). LIGHT_PASTEL_PURPLE si existe y da el mismo
        # tono violeta clarito que se buscaba.
        "color_nombre": arcade.color.LIGHT_PASTEL_PURPLE,
        "color_borde": arcade.color.LIGHT_PASTEL_PURPLE,
    },
    "CIUDADANOS": {
        "nombre": "CIUDADANOS",
        "color_nombre": arcade.color.LIGHT_GRAY,
        "color_borde": arcade.color.LIGHT_GRAY,
    },
    "NARRADOR": {
        "nombre": "",
        "color_nombre": arcade.color.WHITE,
        "color_borde": arcade.color.WHITE,
    },
}


# ------------------------------------------------------------
# GUION COMPLETO DE LA ESCENA
# ------------------------------------------------------------
# Cada entrada es una tupla (hablante, texto, fondo).
# "hablante" es una clave de HABLANTES (o "NARRADOR" para las acotaciones
# entre parentesis, que se muestran sin etiqueta de color).
# "fondo" indica que imagen de fondo corresponde a esa linea: el fondo se
# mantiene hasta que aparece una linea con un fondo distinto.
GUION_JUICIO = [
    ("JUEZ", "Se abre la sesión extraordinaria del Tribunal de Legado Cultural. "
             "Procedan con sus argumentos.", FONDO_INICIO),

    ("ABOGADO", "Honorables miembros del tribunal, los edificios antiguos no "
                "generan progreso. Nuestra propuesta traerá inversión, turismo "
                "y empleo. La ciudad necesita avanzar.", FONDO_INICIO),

    ("WALTER", "¿Avanzar destruyendo todo lo que la hace única?", FONDO_INICIO),

    ("ABOGADO", "La historia está en los libros, señor. No en piedras viejas.", FONDO_INICIO),

    ("LEDO", "Entonces nunca entendió lo que significa Alta Gracia.", FONDO_INICIO),

    ("JUEZ", "¿Tienen pruebas concretas para refutar el proyecto?", FONDO_INICIO),

    ("ABOGADO", "Exactamente. Emociones y recuerdos no son evidencia legal.", FONDO_INICIO),

    ("NARRADOR", "(Las puertas del hotel se abren.)", FONDO_ACTIVO),

    ("WALTER", "Llegó.", FONDO_ACTIVO),

    ("LEDO", "Sabía que volvería.", FONDO_ACTIVO),

    ("JUEZ", "¿Quién es usted?", FONDO_ACTIVO),

    ("LEDIAGO", "Mi nombre es Lediago Waledo. Y traigo la memoria de esta ciudad.", FONDO_ACTIVO),

    ("ABOGADO", "Esto es absurdo.", FONDO_ACTIVO),

    ("LEDIAGO", "¿Absurdo?", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca la Piedra de Moler sobre la mesa.)", FONDO_ACTIVO),

    ("LEDIAGO", "Antes de las calles hubo un pueblo que escuchaba hablar al viento.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca la Herramienta Jesuita.)", FONDO_ACTIVO),

    ("LEDIAGO", "Antes de los hoteles hubo hombres que levantaron estos muros "
                "piedra por piedra.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca la Llave Maestra.)", FONDO_ACTIVO),

    ("LEDIAGO", "Antes del nombre existió el sueño de una ciudad.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca el Sello Real.)", FONDO_ACTIVO),

    ("LEDIAGO", "Antes de la nación hubo quienes protegieron estas tierras en "
                "tiempos inciertos.", FONDO_ACTIVO),

    ("NARRADOR", "(Los presentes observan en silencio.)", FONDO_ACTIVO),

    ("ABOGADO", "Objetos antiguos. Nada más.", FONDO_ACTIVO),

    ("LEDIAGO", "¿Nada más?", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca el Cincel del Cantero.)", FONDO_ACTIVO),

    ("LEDIAGO", "Miles de golpes construyeron cada calle que hoy pisan.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca el Quijote.)", FONDO_ACTIVO),

    ("LEDIAGO", "Un niño curioso aprendió aquí a cuestionar el mundo.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca el Metrónomo.)", FONDO_ACTIVO),

    ("LEDIAGO", "Un compositor encontró inspiración entre estas montañas.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca la Cantimplora.)", FONDO_ACTIVO),

    ("LEDIAGO", "Miles de peregrinos buscaron esperanza en estas tierras.", FONDO_ACTIVO),

    ("NARRADOR", "(Coloca la Espátula de Dubois.)", FONDO_ACTIVO),

    ("LEDIAGO", "Y artistas transformaron la materia en memoria.", FONDO_ACTIVO),

    ("ABOGADO", "Todo eso sigue siendo pasado.", FONDO_ACTIVO),

    ("LEDIAGO", "No.", FONDO_ACTIVO),

    ("LEDIAGO", "El pasado es lo que sostiene el presente.", FONDO_ACTIVO),

    ("JUEZ", "¿Y cómo pretende demostrarlo?", FONDO_ACTIVO),

    ("WALTER", "Activemos el Cronoscopio.", FONDO_ACTIVO),

    ("LEDO", "Es momento de que la ciudad hable por sí misma.", FONDO_ACTIVO),

    ("NARRADOR", "(El Cronoscopio comienza a iluminarse.)", FONDO_ACTIVO),

    ("ABOGADO", "¿Qué es eso?", FONDO_ACTIVO),

    ("LEDIAGO", "Escuche.", FONDO_ACTIVO),

    ("NARRADOR", "(Se oye el sonido del agua del Tajamar.)", FONDO_ACTIVO),

    ("CIUDADANOS", "...", FONDO_ACTIVO),

    ("NARRADOR", "(Se escuchan martillos de los canteros.)", FONDO_ACTIVO),

    ("CIUDADANOS", "...", FONDO_ACTIVO),

    ("NARRADOR", "(Comienza a sonar un piano lejano.)", FONDO_ACTIVO),

    ("CIUDADANOS", "...", FONDO_ACTIVO),

    ("NARRADOR", "(Voces indígenas, campanas jesuitas y cantos de peregrinos "
                 "llenan el salón.)", FONDO_ACTIVO),

    ("JUEZ", "¿Qué está ocurriendo?", FONDO_ACTIVO),

    ("WALTER", "La memoria de Alta Gracia.", FONDO_ACTIVO),

    ("LEDO", "La historia que aún vive entre nosotros.", FONDO_ACTIVO),

    ("ABOGADO", "Esto... esto no puede ser posible.", FONDO_ACTIVO),

    ("LEDIAGO", "La ciudad no es un conjunto de edificios.", FONDO_ACTIVO),

    ("LEDIAGO", "Es la suma de todas las vidas que la construyeron.", FONDO_ACTIVO),

    ("JUEZ", "He escuchado suficiente.", FONDO_ACTIVO),

    ("NARRADOR", "(Silencio absoluto.)", FONDO_ACTIVO),

    ("JUEZ", "Este tribunal determina que el patrimonio histórico y cultural "
             "de Alta Gracia posee un valor excepcional e irremplazable.", FONDO_CERRADO),

    ("ABOGADO", "¡Protesto!", FONDO_CERRADO),

    ("JUEZ", "Protesta denegada.", FONDO_CERRADO),
    ]



class JuicioView(arcade.View):
    """ Reproduce la escena completa del juicio como una secuencia de
    dialogo. Avanza linea por linea con [Espacio] o click, cambiando el
    fondo y la caja de dialogo (nombre + color) segun quien habla. """

    def __init__(self, vista_siguiente=None) -> None:
        super().__init__()

        # Vista a la que se pasa al terminar la escena. Acepta dos formas:
        #   - Una vista ya creada (instancia de arcade.View), como antes.
        #   - Una funcion sin argumentos que CREA y devuelve la vista
        #     (por ejemplo, una funcion que arma el GameView). Esto sirve
        #     para no construir esa vista -con toda su carga de texturas/
        #     sprites- hasta que el juicio realmente termine, en vez de
        #     crearla de entrada y dejarla esperando en memoria.
        # Si queda en None, simplemente no hace nada al terminar el
        # ultimo dialogo (se queda en la ultima linea).
        self.vista_siguiente = vista_siguiente

        # --- Texturas de los 3 fondos del tribunal ---
        self.texturas_fondo = {
            FONDO_INICIO: arcade.load_texture(codigosb.JUICIO_FONDO_INICIO),
            FONDO_ACTIVO: arcade.load_texture(codigosb.JUICIO_FONDO_ACTIVO),
            FONDO_CERRADO: arcade.load_texture(codigosb.JUICIO_FONDO_CERRADO),
        }

        # --- Estado de la escena ---
        self.indice_linea_actual = 0
        self.escena_terminada = False

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self) -> None:
        self.clear()

        hablante_clave, texto, fondo_clave = GUION_JUICIO[self.indice_linea_actual]

        # Fondo de la escena, estirado a toda la ventana
        arcade.draw_texture_rect(
            self.texturas_fondo[fondo_clave],
            arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO),
        )

        self.dibujar_cuadro_dialogo(hablante_clave, texto)

        if self.escena_terminada:
            self.dibujar_aviso_fin()

    def dibujar_cuadro_dialogo(self, hablante_clave, texto):
        """ Dibuja el cuadro de dialogo en la parte inferior de la pantalla,
        con el nombre del personaje que habla destacado en su color y el
        texto de la linea actual debajo. Las acotaciones de NARRADOR no
        llevan etiqueta de nombre (van solo el texto entre parentesis). """
        info_hablante = HABLANTES[hablante_clave]

        alto_caja = 150
        margen = 20

        arcade.draw_rect_filled(
            arcade.LRBT(margen, codigosb.ANCHO - margen, margen, alto_caja),
            (0, 0, 0, 210),
        )
        arcade.draw_rect_outline(
            arcade.LRBT(margen, codigosb.ANCHO - margen, margen, alto_caja),
            info_hablante["color_borde"],
            border_width=3,
        )

        # Etiqueta con el nombre de quien habla (no se dibuja para NARRADOR)
        if hablante_clave != "NARRADOR":
            arcade.draw_rect_filled(
                arcade.LRBT(margen, margen + 230, alto_caja - 4, alto_caja + 26),
                (0, 0, 0, 230),
            )
            arcade.draw_rect_outline(
                arcade.LRBT(margen, margen + 230, alto_caja - 4, alto_caja + 26),
                info_hablante["color_borde"],
                border_width=2,
            )
            arcade.draw_text(
                info_hablante["nombre"],
                margen + 14, alto_caja + 3,
                info_hablante["color_nombre"],
                font_size=13,
                bold=True,
                anchor_y="center",
            )

        # Texto de la linea actual. Las acotaciones de NARRADOR se pintan
        # en gris claro para diferenciarlas visualmente del dialogo hablado.
        color_texto = arcade.color.LIGHT_GRAY if hablante_clave == "NARRADOR" else arcade.color.WHITE
        arcade.draw_text(
            texto,
            margen + 20, alto_caja - 30,
            color_texto,
            font_size=15,
            width=codigosb.ANCHO - (margen * 2) - 40,
            multiline=True,
            anchor_y="top",
        )

        arcade.draw_text(
            f"{self.indice_linea_actual + 1}/{len(GUION_JUICIO)}   "
            "[Espacio] Siguiente...",
            codigosb.ANCHO - margen - 230, margen + 8,
            arcade.color.GRAY,
            font_size=11,
        )

    def dibujar_aviso_fin(self):
        """ Texto chico avisando que la escena termino, mientras se queda
        congelada en el ultimo fondo/dialogo. """
        arcade.draw_text(
            "FIN DE LA ESCENA",
            codigosb.ANCHO // 2, codigosb.ALTO - 30,
            arcade.color.WHITE,
            font_size=14,
            bold=True,
            anchor_x="center",
        )

    # --------------------------------------------------------
    # AVANCE DE DIALOGO
    # --------------------------------------------------------
    def avanzar_dialogo(self):
        if self.escena_terminada:
            self._terminar_escena()
            return

        self.indice_linea_actual += 1
        if self.indice_linea_actual >= len(GUION_JUICIO):
            self.indice_linea_actual = len(GUION_JUICIO) - 1
            self.escena_terminada = True

    def _terminar_escena(self):
        """ Si se definio una vista siguiente, se pasa a ella al volver a
        apretar [Espacio] despues del FIN. Si lo que se paso fue una
        funcion (callable) en vez de una vista ya creada, la llamamos
        recien en este momento para construir la vista (ver el comentario
        en __init__ sobre por que conviene diferir la creacion). """
        if self.vista_siguiente is None:
            return

        if callable(self.vista_siguiente):
            siguiente = self.vista_siguiente()
        else:
            siguiente = self.vista_siguiente

        self.window.show_view(siguiente)

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ENTER:
            self.avanzar_dialogo()

    def on_mouse_press(self, x, y, button, modifiers):
        self.avanzar_dialogo()



# ============================================================
# ESCENA DEL HOTEL SIERRAS - SALON PRINCIPAL (gameplay + dialogo)
# ============================================================
# Flujo:
#   1) El jugador controla a Lediago dentro del Salon Principal
#      del Hotel Sierras (fondo pixel-art del ecenario.png).
#   2) Walter y Ledo aparecen al fondo-derecha como NPCs visibles.
#   3) Al hacer CLICK sobre cualquiera de los dos NPCs se dispara
#      la escena de dialogo completa (guion GUION_HOTEL).
#   4) Una vez terminado el dialogo la pantalla se queda quieta
#      (fin de la demo de esta seccion).

# ------------------------------------------------------------
# GUION DE LA ESCENA DEL SALON PRINCIPAL
# Cada entrada: (hablante_clave, texto)
# Reutilizamos el diccionario HABLANTES ya definido arriba.
# ------------------------------------------------------------
GUION_HOTEL = [
    ("WALTER",   "¡Por fin despertaste!"),
    ("LEDIAGO",  "¿Dónde estoy?"),
    ("LEDO",     "En el Hotel Sierras. O mejor dicho... en lo que queda de él."),
    ("LEDIAGO",  "No entiendo nada. ¿Quiénes son ustedes?"),
    ("WALTER",   "Mi nombre es Walter."),
    ("LEDO",     "Y yo soy Ledo. Somos los guardianes del Archivo Histórico de Alta Gracia."),
    ("LEDIAGO",  "¿Y por qué me trajeron aquí?"),
    ("WALTER",   "Porque la ciudad está en peligro. Muy pronto todo esto podría desaparecer."),
    ("LEDIAGO",  "¿Desaparecer?"),
    ("LEDO",     "Una corporación quiere demoler los lugares históricos para construir algo nuevo."),
    ("LEDIAGO",  "¿Y qué esperan que haga yo?"),
    ("NARRADOR", "(Walter señala una extraña máquina llena de engranajes y luces.)"),
    ("WALTER",   "Necesitamos que uses el Cronoscopio."),
    ("LEDIAGO",  "¿Cronoscopio?"),
    ("LEDO",     "Una máquina capaz de abrir puertas hacia distintas épocas de Alta Gracia."),
    ("LEDIAGO",  "¿Me están diciendo que viaje en el tiempo?"),
    ("WALTER",   "Exactamente."),
    ("LEDIAGO",  "Eso suena imposible."),
    ("LEDO",     "También sonaba imposible perder toda la historia de una ciudad."),
    ("WALTER",   "Tu misión será viajar al pasado, conocer a quienes construyeron esta tierra "
                 "y recuperar fragmentos de su memoria."),
    ("LEDIAGO",  "¿Y si algo sale mal?"),
    ("LEDO",     "No cambiarás la historia."),
    ("WALTER",   "Solo la observarás... y traerás pruebas de que sigue viva."),
    ("NARRADOR", "(El Cronoscopio comienza a iluminarse.)"),
    ("LEDIAGO",  "Supongo que no tengo muchas opciones."),
    ("LEDO",     "Ninguna."),
    ("WALTER",   "Prepárate, viajero."),
    ("LEDO",     "Tu primera parada te espera hace cientos de años."),
]

# Radio en pixeles de la zona clickeable sobre cada NPC
_RADIO_CLICK_NPC = 80


class HotelSierrasView(arcade.View):
    """Escena del Salon Principal del Hotel Sierras.

    Fases:
      FASE_GAMEPLAY  -> Lediago se mueve libremente; los NPCs estan visibles.
      FASE_DIALOGO   -> cuadro de dialogo estilo JuicioView; Lediago no se mueve.
    """

    FASE_GAMEPLAY = 0
    FASE_DIALOGO  = 1

    def __init__(self, musica_fondo=None, reproductor_musica=None) -> None:
        super().__init__()

        self.fase = HotelSierrasView.FASE_GAMEPLAY

        # --- Musica heredada del flujo anterior ---
        self.musica_fondo = musica_fondo
        self.reproductor_musica = reproductor_musica
        if self.musica_fondo is None:
            self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
            self.reproductor_musica = self.musica_fondo.play(
                volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True
            )

        # --- Fondo del Hotel Sierras ---
        self.tex_fondo = arcade.load_texture(codigosb.HOTEL_SIERRAS_FONDO)

        # --- Texturas de Walter+Ledo ---
        # idle: parados de frente (walteryledopies.png)
        # afk : postura "esperando" (walteyledoafk.png)
        # dlg : pose de dialogo - boca abierta (walterledodialogo.png)
        self.tex_npc_idle = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_IDLE)
        self.tex_npc_afk  = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_AFK)
        self.tex_npc_dlg  = arcade.load_texture(codigosb.HOTEL_WALTER_LEDO_DLG)

        # Posicion y tamaño de los NPCs en pantalla.
        # Imagen original ~1024 x 1536 px (los dos personajes juntos).
        # Queremos que se vean al FONDO del salon, mas chicos que Lediago
        # para dar sensacion de profundidad. ~155 px de alto = ~26% de 600.
        self._npc_escala = 155 / 1536          # ≈ 0.101
        self._npc_ancho  = int(1024 * self._npc_escala)   # ≈ 103
        self._npc_alto   = int(1536 * self._npc_escala)   # ≈ 155

        # Posicion: derecha del escenario, mas arriba para simular que estan
        # al fondo (perspectiva). El "suelo del fondo" en el ecenario.png
        # esta aprox al 42% de alto desde abajo.
        self._npc_cx = int(codigosb.ANCHO * 0.74)
        self._npc_cy = int(codigosb.ALTO  * 0.42)         # fondo del salon

        # Zona clickeable: un rect que abarca ambos personajes + algo de margen
        self._npc_rect_x1 = self._npc_cx - self._npc_ancho // 2 - 15
        self._npc_rect_x2 = self._npc_cx + self._npc_ancho // 2 + 15
        self._npc_rect_y1 = self._npc_cy - self._npc_alto // 2 - 10
        self._npc_rect_y2 = self._npc_cy + self._npc_alto // 2 + 10

        # --- Personaje jugable: Lediago ---
        # Escala reducida para que se note la perspectiva del salon:
        # los NPCs al fondo son ~155px, Lediago en primer plano ~210px.
        self.player = Lediago()
        self.player.scale = 0.28          # mas chico que el 0.35 del GameView
        self.player.center_x = codigosb.ANCHO * 0.30
        self.player.center_y = 90         # primer plano, cerca del borde inferior
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Teclas
        self.w_ap = self.s_ap = self.a_ap = self.d_ap = self.shift_ap = False

        # --- Estado del dialogo ---
        self.dialogo_lineas  = []    # lista de tuplas (hablante_clave, texto)
        self.dialogo_idx     = 0
        self.dialogo_fin     = False

        # Temporizador para animar los NPCs en idle (cambian entre idle y afk)
        self._anim_timer   = 0.0
        self._anim_periodo = 3.5     # segundos entre cambio de pose idle<->afk
        self._npc_pose_afk = False   # False=idle, True=afk

    # --------------------------------------------------------
    # HELPERS DE MOVIMIENTO (identico a GameView)
    # --------------------------------------------------------
    def _evaluar_movimiento(self):
        vel = codigosb.VELOCIDAD_CORRER if self.shift_ap else codigosb.VELOCIDAD_CAMINAR
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

    # --------------------------------------------------------
    # DIALOGO
    # --------------------------------------------------------
    def _iniciar_dialogo(self):
        self.dialogo_lineas = GUION_HOTEL
        self.dialogo_idx    = 0
        self.dialogo_fin    = False
        self.fase           = HotelSierrasView.FASE_DIALOGO
        self.player.change_x = 0
        self.player.change_y = 0

    def _avanzar_dialogo(self):
        if self.dialogo_fin:
            return   # la escena se queda en el ultimo frame (fin de demo)
        self.dialogo_idx += 1
        if self.dialogo_idx >= len(self.dialogo_lineas):
            self.dialogo_idx = len(self.dialogo_lineas) - 1
            self.dialogo_fin = True

    def _npc_en_pose_dialogo(self):
        """Devuelve True si el hablante actual es WALTER o LEDO."""
        if self.dialogo_idx >= len(self.dialogo_lineas):
            return False
        hab, _ = self.dialogo_lineas[self.dialogo_idx]
        return hab in ("WALTER", "LEDO")

    # --------------------------------------------------------
    # CLICK: comprueba si el click cayo sobre los NPCs
    # --------------------------------------------------------
    def _click_en_npc(self, x, y) -> bool:
        return (self._npc_rect_x1 <= x <= self._npc_rect_x2 and
                self._npc_rect_y1 <= y <= self._npc_rect_y2)

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self) -> None:
        self.clear()

        # Fondo estirado a toda la ventana
        arcade.draw_texture_rect(
            self.tex_fondo,
            arcade.LBWH(0, 0, codigosb.ANCHO, codigosb.ALTO),
        )

        # NPCs: textura segun fase y pose
        if self.fase == HotelSierrasView.FASE_DIALOGO:
            tex_npc = self.tex_npc_dlg if self._npc_en_pose_dialogo() else self.tex_npc_idle
        else:
            tex_npc = self.tex_npc_afk if self._npc_pose_afk else self.tex_npc_idle

        arcade.draw_texture_rect(
            tex_npc,
            arcade.LBWH(
                self._npc_cx - self._npc_ancho // 2,
                self._npc_cy - self._npc_alto  // 2,
                self._npc_ancho,
                self._npc_alto,
            ),
        )

        # Lediago
        self.player_list.draw()

        # Indicador de interaccion (solo en gameplay, NPCs visibles)
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            self._dibujar_hint_npc()

        # Cuadro de dialogo
        if self.fase == HotelSierrasView.FASE_DIALOGO:
            self._dibujar_cuadro_dialogo()

    def _dibujar_hint_npc(self):
        """Pequeño cartel sobre los NPCs indicando que son clicables."""
        arcade.draw_text(
            "[ Haz CLICK para hablar ]",
            self._npc_cx,
            self._npc_cy + self._npc_alto // 2 + 12,
            arcade.color.YELLOW,
            font_size=11,
            anchor_x="center",
            bold=True,
        )

    def _dibujar_cuadro_dialogo(self):
        """Caja de dialogo igual a la de JuicioView."""
        if self.dialogo_idx >= len(self.dialogo_lineas):
            return

        hablante_clave, texto = self.dialogo_lineas[self.dialogo_idx]
        info = HABLANTES[hablante_clave]

        alto_caja = 150
        margen    = 20

        # Fondo semitransparente
        arcade.draw_rect_filled(
            arcade.LRBT(margen, codigosb.ANCHO - margen, margen, alto_caja),
            (0, 0, 0, 210),
        )
        arcade.draw_rect_outline(
            arcade.LRBT(margen, codigosb.ANCHO - margen, margen, alto_caja),
            info["color_borde"],
            border_width=3,
        )

        # Etiqueta nombre (no para NARRADOR)
        if hablante_clave != "NARRADOR":
            arcade.draw_rect_filled(
                arcade.LRBT(margen, margen + 230, alto_caja - 4, alto_caja + 26),
                (0, 0, 0, 230),
            )
            arcade.draw_rect_outline(
                arcade.LRBT(margen, margen + 230, alto_caja - 4, alto_caja + 26),
                info["color_borde"],
                border_width=2,
            )
            arcade.draw_text(
                info["nombre"],
                margen + 14, alto_caja + 3,
                info["color_nombre"],
                font_size=13,
                bold=True,
                anchor_y="center",
            )

        # Texto del dialogo
        color_texto = (
            arcade.color.LIGHT_GRAY if hablante_clave == "NARRADOR"
            else arcade.color.WHITE
        )
        arcade.draw_text(
            texto,
            margen + 20, alto_caja - 30,
            color_texto,
            font_size=15,
            width=codigosb.ANCHO - (margen * 2) - 40,
            multiline=True,
            anchor_y="top",
        )

        # Contador y pista de avance
        if not self.dialogo_fin:
            pista = (f"{self.dialogo_idx + 1}/{len(self.dialogo_lineas)}   "
                     "[Espacio / Click] Siguiente...")
        else:
            pista = "— FIN DE LA ESCENA —"

        arcade.draw_text(
            pista,
            codigosb.ANCHO - margen - 10, margen + 8,
            arcade.color.GRAY,
            font_size=11,
            anchor_x="right",
        )

    # --------------------------------------------------------
    # INPUT – teclado
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            if key == arcade.key.W:     self.w_ap = True
            elif key == arcade.key.S:   self.s_ap = True
            elif key == arcade.key.A:   self.a_ap = True
            elif key == arcade.key.D:   self.d_ap = True
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = True
            self._evaluar_movimiento()

        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            if key in (arcade.key.SPACE, arcade.key.ENTER):
                self._avanzar_dialogo()

    def on_key_release(self, key, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            if key == arcade.key.W:     self.w_ap = False
            elif key == arcade.key.S:   self.s_ap = False
            elif key == arcade.key.A:   self.a_ap = False
            elif key == arcade.key.D:   self.d_ap = False
            elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
                self.shift_ap = False
            self._evaluar_movimiento()

    # --------------------------------------------------------
    # INPUT – mouse
    # --------------------------------------------------------
    def on_mouse_press(self, x, y, button, modifiers):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            # Click sobre los NPCs → dispara el dialogo
            if self._click_en_npc(x, y):
                self._iniciar_dialogo()
        elif self.fase == HotelSierrasView.FASE_DIALOGO:
            self._avanzar_dialogo()

    # --------------------------------------------------------
    # ACTUALIZACION POR FRAME
    # --------------------------------------------------------
    def on_update(self, delta_time: float):
        if self.fase == HotelSierrasView.FASE_GAMEPLAY:
            # Movimiento de Lediago con limites de ventana
            nueva_x = self.player.center_x + self.player.change_x
            nueva_y = self.player.center_y + self.player.change_y
            mw = self.player.width  / 2
            mh = self.player.height / 2
            nueva_x = max(mw, min(codigosb.ANCHO - mw, nueva_x))
            nueva_y = max(mh, min(codigosb.ALTO - mh, nueva_y))
            self.player.center_x = nueva_x
            self.player.center_y = nueva_y

            # Animacion idle/afk de los NPCs
            self._anim_timer += delta_time
            if self._anim_timer >= self._anim_periodo:
                self._anim_timer   = 0.0
                self._npc_pose_afk = not self._npc_pose_afk


def main():
    window = arcade.Window(codigosb.ANCHO, codigosb.ALTO, codigosb.TITULO)
    window.center_window()

    # Import diferido para evitar import circular (intro.py importa
    # GameView desde aca adentro de codigo.py).
    from intro import IntroView

    intro = IntroView()
    window.show_view(intro)
    arcade.run()


if __name__ == "__main__":
    main()
