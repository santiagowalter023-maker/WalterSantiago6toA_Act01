# ============================================================
# REMINENCE OF GRACIA - INTRO Y MENU DE INICIO
# ============================================================
# Esta vista se muestra ANTES de entrar al juego (GameView en codigo.py).
# Secuencia:
#   1) Logo futurista (frame2logo.png)            -> se queda un rato
#   2) Transicion rapida con la imagen "cambio"    -> efecto de flash/cambio
#   3) Logo antiguo (frame1logo.png)               -> se queda un rato
#   4) Pantalla principal del juego (menudeinicio.png) -> espera input
#
# La musica de fondo arranca apenas se crea esta vista y queda sonando
# en volumen bajo durante toda la intro Y se la pasamos a GameView para
# que siga sonando sin cortes cuando se entra a jugar.
#
# Todo escrito con la API de Arcade 3.x (arcade.draw_texture_rect,
# arcade.LBWH), igual que el resto del proyecto.
import arcade
import codigosb

# ------------------------------------------------------------
# TIEMPOS DE LA SECUENCIA (en segundos)
# ------------------------------------------------------------
DURACION_LOGO_FUTURISTA = 2.5   # cuanto rato se queda el logo futurista
DURACION_TRANSICION = 0.4       # cuanto dura el "flash" de cambio (rapido)
DURACION_LOGO_ANTIGUO = 2.5     # cuanto rato se queda el logo antiguo

# ------------------------------------------------------------
# ETAPAS DE LA INTRO
# ------------------------------------------------------------
ETAPA_LOGO_FUTURISTA = 0
ETAPA_TRANSICION = 1
ETAPA_LOGO_ANTIGUO = 2
ETAPA_MENU = 3


class IntroView(arcade.View):
    """ Maneja el flujo completo: logos -> transicion -> menu de inicio. """

    def __init__(self) -> None:
        super().__init__()

        # --- Texturas de cada etapa ---
        self.textura_logo_futurista = arcade.load_texture(codigosb.LOGO_FUTURISTA)
        self.textura_cambio = arcade.load_texture(codigosb.LOGO_CAMBIO)
        self.textura_logo_antiguo = arcade.load_texture(codigosb.LOGO_ANTIGUO)
        self.textura_menu = arcade.load_texture(codigosb.MENU_INICIO)

        # --- Estado de la secuencia ---
        self.etapa_actual = ETAPA_LOGO_FUTURISTA
        self.tiempo_en_etapa = 0.0

        # --- Musica de fondo (suena bajo durante toda la intro y el juego) ---
        # Usamos un .wav (no .mp3) para que pyglet la decodifique con su
        # decodificador interno (WaveDecoder), sin depender de FFmpeg.
        # En Windows, sin FFmpeg instalado, pyglet se queda colgado buscando
        # los .dll de FFmpeg apenas intenta cargar un MP3 (FileNotFoundError:
        # avutil / cuelgue largo en la consola). Con WAV no hace falta FFmpeg
        # para nada. streaming=False: la carga entera en memoria (esta bien
        # para los ~10MB que pesa el wav comprimido a 22050Hz mono).
        self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
        self.reproductor_musica = self.musica_fondo.play(
            volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True
        )

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self) -> None:
        self.clear()

        if self.etapa_actual == ETAPA_LOGO_FUTURISTA:
            self._dibujar_textura_centrada(self.textura_logo_futurista)

        elif self.etapa_actual == ETAPA_TRANSICION:
            self._dibujar_textura_centrada(self.textura_cambio)

        elif self.etapa_actual == ETAPA_LOGO_ANTIGUO:
            self._dibujar_textura_centrada(self.textura_logo_antiguo)

        elif self.etapa_actual == ETAPA_MENU:
            self._dibujar_textura_centrada(self.textura_menu)
            self._dibujar_indicacion_inicio()

    def _dibujar_textura_centrada(self, textura):
        """ Dibuja una textura ocupando toda la ventana, manteniendo
        la proporcion (la encoge si es necesario para que no se deforme
        ni se corte). El fondo blanco de los logos hace que esto se vea
        bien aunque queden franjas a los costados. """
        ancho_ventana = codigosb.ANCHO
        alto_ventana = codigosb.ALTO

        escala = min(
            ancho_ventana / textura.width,
            alto_ventana / textura.height,
        )
        ancho_final = textura.width * escala
        alto_final = textura.height * escala

        x_izq = (ancho_ventana - ancho_final) / 2
        y_abajo = (alto_ventana - alto_final) / 2

        arcade.draw_texture_rect(
            textura,
            arcade.LBWH(x_izq, y_abajo, ancho_final, alto_final),
        )

    def _dibujar_indicacion_inicio(self):
        """ Texto parpadeante abajo de todo invitando a arrancar. """
        # Parpadeo simple basado en el tiempo (medio segundo prendido,
        # medio segundo apagado).
        if int(self.tiempo_en_etapa * 2) % 2 == 0:
            arcade.draw_text(
                "Presiona cualquier tecla o click para comenzar",
                codigosb.ANCHO // 2,
                40,
                arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                bold=True,
            )

    # --------------------------------------------------------
    # ACTUALIZACION POR FRAME (controla los tiempos de la secuencia)
    # --------------------------------------------------------
    def on_update(self, delta_time: float):
        self.tiempo_en_etapa += delta_time

        if self.etapa_actual == ETAPA_LOGO_FUTURISTA:
            if self.tiempo_en_etapa >= DURACION_LOGO_FUTURISTA:
                self._avanzar_a(ETAPA_TRANSICION)

        elif self.etapa_actual == ETAPA_TRANSICION:
            if self.tiempo_en_etapa >= DURACION_TRANSICION:
                self._avanzar_a(ETAPA_LOGO_ANTIGUO)

        elif self.etapa_actual == ETAPA_LOGO_ANTIGUO:
            if self.tiempo_en_etapa >= DURACION_LOGO_ANTIGUO:
                self._avanzar_a(ETAPA_MENU)

        # ETAPA_MENU se queda quieta esperando input del jugador.

    def _avanzar_a(self, nueva_etapa):
        self.etapa_actual = nueva_etapa
        self.tiempo_en_etapa = 0.0

    # --------------------------------------------------------
    # INPUT (solo hace algo una vez que se llego al menu)
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.etapa_actual == ETAPA_MENU:
            self._arrancar_juego()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.etapa_actual == ETAPA_MENU:
            self._arrancar_juego()

    def _arrancar_juego(self):
        """ Al apretar una tecla/click en el menu, primero se reproduce
        la escena del juicio (JuicioView) y SOLO cuando esa escena termina
        se crea HotelSierrasView (gameplay + dialogo con Walter y Ledo).

        OJO: le pasamos a JuicioView una FUNCION que crea la vista siguiente
        (en vez de una instancia ya creada) para diferir la carga de texturas
        hasta que el juicio realmente termine, evitando el "trabo" al apretar
        [Espacio]/click en el menu.
        """
        from codigo import JuicioView, HotelSierrasView

        def crear_hotel_view():
            return HotelSierrasView(
                musica_fondo=self.musica_fondo,
                reproductor_musica=self.reproductor_musica,
            )

        juicio = JuicioView(vista_siguiente=crear_hotel_view)
        self.window.show_view(juicio)
