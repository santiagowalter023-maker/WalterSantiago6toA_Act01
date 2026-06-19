import arcade
import codigosb

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sistema de Diálogos - Reminiscence of Gracia"
ESTADO_JUGANDO = 0
ESTADO_HABLANDO = 1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.estado_actual = ESTADO_JUGANDO
        self.dialogo_lineas = []      
        self.indice_linea_actual = 0  
        self.npc_sprite = arcade.SpriteSolidColor(32, 32, color=arcade.color.RED)
        self.npc_sprite.center_x = 500
        self.npc_sprite.center_y = 300
        self.player_sprite = arcade.Sprite(codigosb.SPRITE_FRENTE, scale=codigosb.ESCALA_PERSONAJE)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 300

    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.npc_sprite)
        arcade.draw_sprite(self.player_sprite)

        if self.estado_actual == ESTADO_HABLANDO:
            self.dibujar_cuadro_dialogo()

    def dibujar_cuadro_dialogo(self):
        """ Dibuja el rectángulo del fondo y el texto actual """
        arcade.draw_rect_filled(
            arcade.LRBT(20, SCREEN_WIDTH - 20, 20, 140),
            arcade.color.BLACK,
        )
        arcade.draw_rect_outline(
            arcade.LRBT(20, SCREEN_WIDTH - 20, 20, 140),
            arcade.color.WHITE,
            border_width=3,
        )
        texto_a_mostrar = self.dialogo_lineas[self.indice_linea_actual]
        
        arcade.draw_text(
            texto_a_mostrar,
            40, 90, 
            arcade.color.WHITE,
            font_size=16,
            width=SCREEN_WIDTH - 80, 
            multiline=True
        )
        arcade.draw_text(
            "[Espacio] Siguiente...",
            SCREEN_WIDTH - 220, 35,
            arcade.color.GRAY,
            font_size=12
        )
    def disparar_dialogo(self, lineas_texto):
        """ Activa el cuadro de texto y congela el juego """
        self.dialogo_lineas = lineas_texto
        self.indice_linea_actual = 0
        self.estado_actual = ESTADO_HABLANDO
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
    def on_key_press(self, key, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if key == arcade.key.W: self.player_sprite.change_y = 4
            elif key == arcade.key.S: self.player_sprite.change_y = -4
            elif key == arcade.key.A: self.player_sprite.change_x = -4
            elif key == arcade.key.D: self.player_sprite.change_x = 4
            
            elif key == arcade.key.SPACE:
                # Verificamos la distancia entre Lediago y el NPC
                distancia = arcade.get_distance_between_sprites(self.player_sprite, self.npc_sprite)
                if distancia < 60: # Si está lo suficientemente cerca...
                    conversacion = [
                        "Hola Lediago... Bienvenido a la Estancia Jesuítica.",
                        "Necesitamos tu ayuda para resolver el misterio de Gracia.",
                        "Busca pistas en el ala norte del edificio antes de que sea tarde."
                    ]
                    self.disparar_dialogo(conversacion)

        elif self.estado_actual == ESTADO_HABLANDO:
            if key == arcade.key.SPACE:
                self.indice_linea_actual += 1
            
                if self.indice_linea_actual >= len(self.dialogo_lineas):
                    self.estado_actual = ESTADO_JUGANDO

    def on_key_release(self, key, modifiers):
        if self.estado_actual == ESTADO_JUGANDO:
            if key in [arcade.key.W, arcade.key.S]: self.player_sprite.change_y = 0
            if key in [arcade.key.A, arcade.key.D]: self.player_sprite.change_x = 0
    def on_update(self, delta_time):
        if self.estado_actual == ESTADO_JUGANDO:
            self.player_sprite.center_x += self.player_sprite.change_x
            self.player_sprite.center_y += self.player_sprite.change_y
def main():
    game = MyGame()
    arcade.run()
if __name__ == "__main__":
    main()