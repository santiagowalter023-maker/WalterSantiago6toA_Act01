# ============================================================
# REMINENCE OF GRACIA - INTRO Y MENU DE INICIO
# ============================================================
# Secuencia:
#   1) Logo futurista  -> pausa
#   2) Flash de cambio -> rapido
#   3) Logo antiguo    -> pausa
#   4) Menu de inicio  -> espera input del jugador
# Al arrancar crea un Inventario nuevo (o carga uno guardado si existe)
# y lo pasa a todas las escenas siguientes.

import arcade
import codigosb

DURACION_LOGO_FUTURISTA = 2.5
DURACION_TRANSICION     = 0.4
DURACION_LOGO_ANTIGUO   = 2.5

ETAPA_LOGO_FUTURISTA = 0
ETAPA_TRANSICION     = 1
ETAPA_LOGO_ANTIGUO   = 2
ETAPA_MENU           = 3


class IntroView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.textura_logo_futurista = arcade.load_texture(codigosb.LOGO_FUTURISTA)
        self.textura_cambio         = arcade.load_texture(codigosb.LOGO_CAMBIO)
        self.textura_logo_antiguo   = arcade.load_texture(codigosb.LOGO_ANTIGUO)
        self.textura_menu           = arcade.load_texture(codigosb.MENU_INICIO)

        self.etapa_actual    = ETAPA_LOGO_FUTURISTA
        self.tiempo_en_etapa = 0.0

        self.musica_fondo = arcade.Sound(codigosb.MUSICA_FONDO, streaming=False)
        self.reproductor_musica = self.musica_fondo.play(
            volume=codigosb.VOLUMEN_MUSICA_FONDO, loop=True)

        # Intentar cargar partida guardada
        from codigo import Inventario
        inv_guardado = Inventario.cargar()
        self._partida_guardada = inv_guardado is not None
        self._inventario = inv_guardado if inv_guardado else Inventario()

    # --------------------------------------------------------
    # DIBUJADO
    # --------------------------------------------------------
    def on_draw(self):
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
        aw = codigosb.ANCHO
        ah = codigosb.ALTO
        escala     = min(aw / textura.width, ah / textura.height)
        ancho_f    = textura.width  * escala
        alto_f     = textura.height * escala
        arcade.draw_texture_rect(
            textura,
            arcade.LBWH((aw - ancho_f)/2, (ah - alto_f)/2, ancho_f, alto_f))

    def _dibujar_indicacion_inicio(self):
        if int(self.tiempo_en_etapa * 2) % 2 == 0:
            arcade.draw_text(
                "Presiona cualquier tecla o click para comenzar",
                codigosb.ANCHO//2, 40, arcade.color.WHITE,
                font_size=16, anchor_x="center", bold=True)
        # Indicador de partida guardada
        if self._partida_guardada:
            arcade.draw_text(
                "Partida guardada encontrada",
                codigosb.ANCHO//2, 70, arcade.color.GREEN_YELLOW,
                font_size=12, anchor_x="center")

    # --------------------------------------------------------
    # ACTUALIZACION
    # --------------------------------------------------------
    def on_update(self, delta_time):
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

    def _avanzar_a(self, nueva_etapa):
        self.etapa_actual    = nueva_etapa
        self.tiempo_en_etapa = 0.0

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if self.etapa_actual == ETAPA_MENU:
            self._arrancar_juego()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.etapa_actual == ETAPA_MENU:
            self._arrancar_juego()

    def _arrancar_juego(self):
        """
        Flujo:
          IntroView -> JuicioView -> HotelSierrasView -> VitrinaView
        El Inventario viaja desde aqui hasta VitrinaView sin romperse.
        """
        from codigo import JuicioView, HotelSierrasView

        inventario = self._inventario
        musica     = self.musica_fondo
        repro      = self.reproductor_musica

        def crear_hotel_view():
            return HotelSierrasView(
                musica_fondo=musica,
                reproductor_musica=repro,
                inventario=inventario,
            )

        juicio = JuicioView(vista_siguiente=crear_hotel_view)
        self.window.show_view(juicio)
