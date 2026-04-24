#Ejercicio 14: ÚLTIMA DEFENSA
#Una torre protege un territorio de ataques constantes. El usuario podrá decidir cómo actuar frente a cada
#situación. A medida que transcurre el tiempo, la torre recibe daños que afectan su estado. El sistema debe
#permitir observar su condición en cada momento.
#El juego finaliza cuando la torre ya no puede resistir más ataques.

import time
import random

class Torre:
    def __init__(self):
        self.vida = 100

    def atributos(self):
        self.nombre = input("Como te llamas?")

    def ataque(self):
        daños = 20
        print("Daño hecho ;",daños)

    
    def defensa(self):
        defensa = 10
        
        self.vida = self.vida + defensa
        print("La vida de la torre es de ",self.vida)

    def daño(self,daños):
        self.vida = self.vida - daños

        if self.vida < 0:
            self.vida = 0

        print("La torre sufrio daño :",daños)

    def mostrarVida(self):
        objt = int(self.vida / 5)
        linea = ""

        for i in range(objt):
            linea = linea + "♥"
            
        print("VIDA",linea,":","(",self.vida,")")



    def mostrar(self):
        print("Hola ",self.nombre)
        self.mostrarVida()

class Enemigo(Torre):
    def __init__(self):
        self.vida = 100

    def combate(self):
        daño = random.randint(15,20)
        print("Te atacaron e hicieron ",daño)
        return daño


    
torre = Torre()
torre.atributos()

enemigo = Enemigo()

op = 0

while torre.vida >0:
    print("Que desea hecer ?")
    print("1 - Atacar")
    print("2 - Defender")

    op = int(input("Ingrese opcion : "))

    time.sleep(2)

    if op == 1:
        time.sleep(2)
        torre.ataque()


    if op == 2:
        time.sleep(2)
        torre.defensa()

    if op != 1 and op != 2:
        print("elija una opcion valida")

    dañor = enemigo.combate()
    torre.daño(dañor)

    torre.mostrar()
    time.sleep(2)

print("LA TORRE AH SIDO DESTRUIDA")
    





    