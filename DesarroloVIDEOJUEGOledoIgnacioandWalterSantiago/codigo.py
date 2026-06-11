#python "e:/Programacion 3/01Heladeria WalterSantiago/Python-Reposity/DesarroloVIDEOJUEGOledoIgnacioandWalterSantiago/codigo.py"
# ACA VA ESTAR EL CODIGO PICHON
import arcade
import codigosb

# ACA VA ESTAR EL CODIGO PICHON

window = arcade.open_window(codigosb.ALTO, codigosb.ANCHO, "REMINENCE OF GRACIA")
window.center_window()

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        
    def on_draw(self) -> None:
        self.clear()
        
        #ACA VAMOS A RENDERIZAR
        
        #circulos
        arcade.draw_circle_filled(center_x=100, center_y=100, radius=30, color=(255, 0, 0))
        arcade.draw_circle_outline(center_x=150, center_y=150, radius=30, color=(255, 0, 0))
        #rectangulos
        arcade.draw_xywh_rectangle_filled(250, 250, 50, 90, (255, 0, 0))
        
        arcade.draw_xywh_rectangle_filled(250, 200, 50, 90, (255, 0, 0))
        
        arcade.draw_xywh_rectangle_outline(250, 50, 50, 80, (0, 0, 255))
        #arcos
        arcade.draw_arc_filled(500, 300, 100, 100, (0, 255, 0), start_angle=0, end_angle=100)
        
        arcade.draw_arc_outline(550, 350, 100, 100, color=(0, 255, 0), start_angle= 0, end_angle= 90)
        #parabolas
        
        #lineas
        
        
        
juego = GameView()
window.show_view(juego)
arcade.run()

print("Bienvenido")