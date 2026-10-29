import os
import shutil
import subprocess
import sys

# Carpeta donde esta este archivo (junto a codigo.py)
CARPETA = os.path.dirname(os.path.abspath(__file__))
os.chdir(CARPETA)

# 1) Instalar las librerias necesarias
subprocess.check_call([sys.executable, "-m", "pip", "install", "arcade", "edge-tts", "pyinstaller"])

# 2) Borrar restos de generaciones anteriores
for carpeta in ["build", "dist"]:
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta)
for archivo in os.listdir(CARPETA):
    if archivo.endswith(".spec"):
        os.remove(archivo)

# 3) Ubicar la carpeta de recursos de Arcade instalada en esta PC
ruta_arcade = subprocess.check_output(
    [sys.executable, "-c", "import arcade, os; print(os.path.dirname(arcade.__file__))"],
    text=True).strip()
separador = ";" if os.name == "nt" else ":"

# 4) Recursos del juego que van DENTRO del .exe
RECURSOS = ["assets_intro", "assets_juicio", "assets_estancia", "assets_paravachasca",
            "assets_dubois", "assets_falla", "voces"]

# Arcade se empaqueta solo con su codigo y su carpeta resources (sin el archivo VERSION,
# que causaba el error "Failed to extract arcade\VERSION\VERSION")
comando = [sys.executable, "-m", "PyInstaller", "--onefile", "--windowed",
           "--name", "ReminenciaDeGracia",
           "--collect-submodules", "arcade",
           "--add-data", f"{os.path.join(ruta_arcade, 'resources')}{separador}arcade/resources",
           "--collect-all", "edge_tts"]
for carpeta in RECURSOS:
    comando += ["--add-data", f"{carpeta}{separador}{carpeta}"]
comando.append("codigo.py")

# 5) Generar el ejecutable
subprocess.check_call(comando)
print("Listo. El ejecutable esta en dist/ReminenciaDeGracia.exe (un solo archivo).")
