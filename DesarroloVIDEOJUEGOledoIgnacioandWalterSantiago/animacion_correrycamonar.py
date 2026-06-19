import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Reminiscence of Gracia - Movimiento Avanzado"

CHARACTER_SCALING = 2
VELOCIDAD_CAMINAR = 3
VELOCIDAD_CORRER = 6
FRENTE = 0
ESPALDA = 1
IZQUIERDA = 2
DERECHA = 3
class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.direccion_actual = FRENTE
        self.esta_corriendo = False
        self.frame_actual = 0
        self.tiempo_desde_ultimo_frame = 0
        self.cambio_frame_rate = 0.1 
        self.texturas_caminar_frente = [
            arcade.load_texture("lediago_frente_idle.png"),
            arcade.load_texture("lediago_frente_paso1.png"),
            arcade.load_texture("lediago_frente_paso2.png")
        ]
        self.texturas_caminar_espalda = [
            arcade.load_texture("lediago_espalda_idle.png"),
            arcade.load_texture("lediago_espalda_paso1.png"),
            arcade.load_texture("lediago_espalda_paso2.png")
        ]
        self.texturas_caminar_derecha = [
            arcade.load_texture("lediago_perfil_idle.png"),
            arcade.load_texture("lediago_perfil_paso1.png"),
            arcade.load_texture("lediago_perfil_paso2.png")
        ]
        self.texturas_caminar_izquierda = [
            arcade.load_texture("lediago_perfil_idle.png", flipped_horizontally=True),
            arcade.load_texture("lediago_perfil_paso1.png", flipped_horizontally=True),
            arcade.load_texture("lediago_perfil_paso2.png", flipped_horizontally=True)
        ]
        self.texturas_correr_frente = [arcade.load_texture("lediago_run_frente1.png"), arcade.load_texture("lediago_run_frente2.png")]
        self.texturas_correr_espalda = [arcade.load_texture("lediago_run_espalda1.png"), arcade.load_texture("lediago_run_espalda2.png")]
        self.texturas_correr_derecha = [arcade.load_texture("lediago_run_perfil1.png"), arcade.load_texture("lediago_run_perfil2.png")]
        self.texturas_correr_izquierda = [arcade.load_texture("lediago_run_perfil1.png", flipped_horizontally=True), arcade.load_texture("lediago_run_perfil2.png", flipped_horizontally=True)]
        self.texture = self.texturas_caminar_frente[0]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0:
            self.direccion_actual = IZQUIERDA
        elif self.change_x > 0:
            self.direccion_actual = DERECHA
        elif self.change_y < 0:
            self.direccion_actual = FRENTE
        elif self.change_y > 0:
            self.direccion_actual = ESPALDA
        if self.change_x == 0 and self.change_y == 0:
            if self.direccion_actual == FRENTE: self.texture = self.texturas_caminar_frente[0]
            elif self.direccion_actual == ESPALDA: self.texture = self.texturas_caminar_espalda[0]
            elif self.direccion_actual == IZQUIERDA: self.texture = self.texturas_caminar_izquierda[0]
            elif self.direccion_actual == DERECHA: self.texture = self.texturas_caminar_derecha[0]
            return
        self.tiempo_desde_ultimo_frame += delta_time
        # Si corre, los pies se mueven más rápido
        anim_speed = self.cambio_frame_rate / 2 if self.esta_corriendo else self.cambio_frame_rate
        if self.tiempo_desde_ultimo_frame > anim_speed:
            self.tiempo_desde_ultimo_frame = 0
            self.frame_actual += 1
            if self.esta_corriendo:
                if self.direccion_actual == FRENTE: lista = self.texturas_correr_frente
                elif self.direccion_actual == ESPALDA: lista = self.texturas_correr_espalda
                elif self.direccion_actual == IZQUIERDA: lista = self.texturas_correr_izquierda
                else: lista = self.texturas_correr_derecha
            else:
                if self.direccion_actual == FRENTE: lista = self.texturas_caminar_frente
                elif self.direccion_actual == ESPALDA: lista = self.texturas_caminar_espalda
                elif self.direccion_actual == IZQUIERDA: lista = self.texturas_caminar_izquierda
                else: lista = self.texturas_caminar_derecha
            self.frame_actual %= len(lista)
            self.texture = lista[self.frame_actual]

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.w_apretada = False
        self.s_apretada = False
        self.a_apretada = False
        self.d_apretada = False
        self.shift_apretado = False
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, arcade.SpriteList())
    def on_draw(self):
        self.clear()
        self.player_list.draw()
    def evaluar_movimiento(self):
        """ Calcula la velocidad final combinando dirección y Shift """
        velocidad = VELOCIDAD_CORRER if self.shift_apretado else VELOCIDAD_CAMINAR
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
    def on_key_press(self, key, modifiers):
        # Detectar direcciones
        if key == arcade.key.W: self.w_apretada = True
        elif key == arcade.key.S: self.s_apretada = True
        elif key == arcade.key.A: self.a_apretada = True
        elif key == arcade.key.D: self.d_apretada = True
        elif key in [arcade.key.KEY_MOD_SHIFT, arcade.key.LSHIFT, arcade.key.RSHIFT]:
            self.shift_apretado = True

        self.evaluar_movimiento()

    def on_key_release(self, key, modifiers):
        # Detectar cuando suelta las teclas
        if key == arcade.key.W: self.w_apretada = False
        elif key == arcade.key.S: self.s_apretada = False
        elif key == arcade.key.A: self.a_apretada = False
        elif key == arcade.key.D: self.d_apretada = False
        
        elif key in [arcade.key.KEY_MOD_SHIFT, arcade.key.LSHIFT, arcade.key.RSHIFT]:
            self.shift_apretado = False

        self.evaluar_movimiento()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update_animation(delta_time)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()