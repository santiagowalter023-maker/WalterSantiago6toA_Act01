import subprocess
import sys

# Librerías que necesita el servidor
LIBRERIAS = ["flask"]

for libreria in LIBRERIAS:
    print(f"Instalando {libreria}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])

print("Listo. Para iniciar el servidor ejecutá: python servidor.py")
