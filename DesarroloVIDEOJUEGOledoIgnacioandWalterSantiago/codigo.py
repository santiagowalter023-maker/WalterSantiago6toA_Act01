#python "e:/Programacion 3/01Heladeria WalterSantiago/Python-Reposity/DesarroloVIDEOJUEGOledoIgnacioandWalterSantiago/codigo.py"
# ============================================================
# REMINENCE OF GRACIA - PUNTO DE ENTRADA PRINCIPAL DEL JUEGO
# ============================================================
# Este archivo une las 3 partes que estaban sueltas en el proyecto:
#   - codigosb.py                  -> configuracion (tamaño ventana, velocidades, rutas)
#   - animacion_correrycamonar.py  -> referencia del sistema de movimiento/animacion
#   - codigo_textointeractivo.py   -> referencia del sistema de dialogo con NPC
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
    def __init__(self) -> None:
        super().__init__()

        self.estado_actual = ESTADO_JUGANDO

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


def main():
    window = arcade.Window(codigosb.ANCHO, codigosb.ALTO, codigosb.TITULO)
    window.center_window()
    juego = GameView()
    window.show_view(juego)
    arcade.run()


if __name__ == "__main__":
    main()
