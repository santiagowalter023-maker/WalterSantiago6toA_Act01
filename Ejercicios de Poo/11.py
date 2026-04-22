#Ejercicio 11: BATALLA DE HECHICEROS
#Dos hechiceros se enfrentan en un duelo mágico. Uno será controlado por el usuario, quien podrá tomar
#decisiones estratégicas durante el combate.
#Cada acción tiene consecuencias sobre los recursos disponibles del personaje, por lo que será necesario
#administrarlos correctamente.
#El enfrentamiento continúa hasta que uno de los participantes ya no pueda seguir luchando.
import random

class Hechicerocontrolado:
    def atributos(self,nom):
        self.nombre = input("Ingrese su nombre mago :")

    def __init__(self):
        self.poderfuego01 = int(input("Cuanto poder de fuego tenes (0 -100) :"))
        self.poderagua01  = int(input("Cuanto poder de agua tenes (0 - 100) :"))

        self.vida01 = 100

    def daño(self, op):
        if op == 1:
           return self.poderagua01 / 10
        else:
           return self.poderfuego01/ 10

    def mostrar(self):
        print("se llama : ",self.nombre)
        #-----------------------------------------
        print("tiene fuego a : ",self.poderfuego)
        #
        print("tiene agua  a : ",self.poderagua)
        #
        print("Su vida es  a : ",self.daño())

class HechiceroBoot:
    def __init__(self):
        self.poderfuego02 = random.randint(100,102)
        self.poderagua02  = random.randint(100,105)

        self.vida02 = 100

    def daño(self, opi):
        opi = random.randint(1,2)
        if opi == 1:
           return self.poderagua02 / 10
        else:
           return self.poderfuego02/ 10
        
a = Hechicerocontrolado()
a.atributos("")

b = HechiceroBoot()

while a.vida01 > 0 and b.vida02 > 0:
    print("Tu vida ",a.vida01)
    print("Su vida ",b.vida02)

    print(" 1Ataque fuego")
    print(" 2Ataque agua")

    op = int(input(" : "))

    daño = a.daño(op)
    b.vida02 = b.vida02 - daño
    print("daño :",daño)

    if b.vida02 > 0:
        daño = b.daño(0)
        b.vida02 = b.vida02 - daño
        print("daño :",daño)

if a.vida01 > 0:
    print("winnn")
else:
    print("la proxima sera")


    


        
        

    


