# ============================================================
# REMINENCE OF GRACIA - ESCENA DEL JUICIO (SIERRAS HOTEL)
# ============================================================
# Esta vista reproduce la escena "EL JUICIO EN EL SIERRAS HOTEL" como una
# secuencia de dialogo tipo novela visual, arriba de los 3 fondos del
# Tribunal Superior de Gracia:
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
# Como entrar a esta vista desde el resto del juego:
#   from juicio import JuicioView
#   window.show_view(JuicioView())
#
# Se puede probar este archivo solo (python juicio.py) sin pasar por el
# menu/intro del resto del proyecto.
import arcade
import codigosb

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
        "color_nombre": arcade.color.LIGHT_VIOLET,
        "color_borde": arcade.color.LIGHT_VIOLET,
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
# entre parentesis, que se muestran en cursiva-like, sin etiqueta de color).
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

    ("JUEZ", "Se cancela inmediatamente toda orden de demolición.", FONDO_CERRADO),

    ("NARRADOR", "(Los ciudadanos estallan en aplausos.)", FONDO_CERRADO),

    ("WALTER", "Lo logramos.", FONDO_CERRADO),

    ("LEDO", "Alta Gracia está a salvo.", FONDO_CERRADO),

    ("LEDIAGO", "No fui yo.", FONDO_CERRADO),

    ("WALTER", "¿Entonces quién?", FONDO_CERRADO),

    ("LEDIAGO", "Todos los que vivieron aquí antes que nosotros.", FONDO_CERRADO),

    ("LEDO", "Y todos los que vivirán después.", FONDO_CERRADO),

    ("JUEZ", "La sesión queda cerrada.", FONDO_CERRADO),

    ("NARRADOR", "(Las luces del Cronoscopio se apagan lentamente.)", FONDO_CERRADO),

    ("WALTER", "¿Y ahora qué harás?", FONDO_CERRADO),

    ("LEDIAGO", "Creo que por primera vez...", FONDO_CERRADO),

    ("LEDIAGO", "Me voy a quedar en casa.", FONDO_CERRADO),
]


class JuicioView(arcade.View):
    """ Reproduce la escena completa del juicio como una secuencia de
    dialogo. Avanza linea por linea con [Espacio] o click, cambiando el
    fondo y la caja de dialogo (nombre + color) segun quien habla. """

    def __init__(self, vista_siguiente=None) -> None:
        super().__init__()

        # Vista a la que se pasa al terminar la escena (por ejemplo
        # GameView). Si queda en None, simplemente no hace nada al
        # terminar el ultimo dialogo (se queda en la ultima linea).
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
        """ Si se definio una vista siguiente (por ejemplo GameView), se
        pasa a ella al volver a apretar [Espacio] despues del FIN. """
        if self.vista_siguiente is not None:
            self.window.show_view(self.vista_siguiente)

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ENTER:
            self.avanzar_dialogo()

    def on_mouse_press(self, x, y, button, modifiers):
        self.avanzar_dialogo()


def main():
    """ Permite correr unicamente la escena del juicio, sin pasar por
    el menu/intro del resto del juego (util para probarla suelta). """
    window = arcade.Window(codigosb.ANCHO, codigosb.ALTO, "El Juicio - Reminiscence of Gracia")
    window.center_window()
    window.show_view(JuicioView())
    arcade.run()


if __name__ == "__main__":
    main()
