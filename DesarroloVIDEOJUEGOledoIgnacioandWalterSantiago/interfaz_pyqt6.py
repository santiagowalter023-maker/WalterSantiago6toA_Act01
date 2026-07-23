import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Carpeta donde vive este archivo. Asi el boton "Jugar" encuentra
# codigo.py sin importar desde donde se ejecute el launcher.
BASE_DIR = Path(__file__).resolve().parent


# VENTANA PRINCIPAL
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminence of Gracia")
        self.setFixedSize(800, 600)

        # WIDGET Y LAYOUT CENTRAL
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # TITULO
        titulo = QLabel("Reminence of Gracia")
        titulo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Un juego de aventura")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo)

        # BOTONES
        btn_jugar = QPushButton(" Jugar")
        btn_jugar.setFixedHeight(50)
        btn_jugar.setFont(QFont("Arial", 13))
        btn_jugar.clicked.connect(self.iniciar_juego)
        layout.addWidget(btn_jugar)

        btn_salir = QPushButton("Salir")
        btn_salir.setFixedHeight(35)
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir)

        # ESTILOS
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QWidget      { background-color: #1e1e2e; color: #cdd6f4; }
            QLabel       { color: #cdd6f4; }
            QPushButton  {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover   { background-color: #74c7ec; }
            QPushButton:pressed { background-color: #89dceb; }
        """)

    # LOGICA DE BOTONES
    # Abre codigo.py como un proceso aparte (no se importa, se lanza el juego en su propia ventana)
    def iniciar_juego(self):
        codigo_path = BASE_DIR / "codigo.py"
        subprocess.Popen([sys.executable, str(codigo_path)], cwd=str(BASE_DIR))


# ARRANQUE
# Crea la aplicación Qt, muestra la ventana y queda esperando eventos (clicks, etc.)
# (en PyQt6 el método se llama exec(), no exec_() como en PyQt5)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
