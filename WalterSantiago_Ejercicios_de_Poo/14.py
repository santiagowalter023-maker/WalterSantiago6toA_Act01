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
        self.ataque = 20

        self.vida = self.vida - self.ataque
        print("La vida de la torre es de ",self.vida)

    
    def defensa(self):
        self.defensa = 10
        
        self.vida = self.vida + self.defensa
        print("La vida de la torre es de ",self.vida)

    def mostrar(self):
        print("Hola ",self.nombre)
        print("La vida que le queda es ;",self.vida)

class Enemigo(Torre):
    def __init__(self):
        super().__init__(self)
    
    op = 0




    