#Ejercicio 10: GRAN CARRERA
#Se está llevando a cabo una carrera entre varios autos. Uno de ellos será controlado por el usuario, quien podrá
#decidir cómo actuar en cada turno.
#Cada acción influirá en el desempeño del vehículo, afectando su avance en la pista. Mientras tanto, los demás
#competidores avanzarán automáticamente. El programa debe permitir observar la evolución de la carrera y
#determinar el resultado final.

import random

class Autocrtl:
    def atributos(self):
        self.nombre = input("Nombre del piloto(vos) :")

    def __init__(self):
        self.vel01 = int(input("Ingrese velocidad del auto(250km - 300,km) :"))
        self.alc01 = int(input("Ingrese aceleracion del auto :(250sgm2 - 300sgm2)"))
        self.distancia = 0

    def carrera(self,op):
        if op == 1:
            self.distancia = self.distancia + (self.vel01 * 0.25) #Mas LENTO
        
        if op == 2:
            self.distancia = self.distancia + self.vel01

        if op == 3:
            self.distancia = self.distancia + (self.vel01 * 2) #MAS rapido

    def mostrar(self):
        print("USTED SE LLAMA :",self.nombre)
        print("SU velocida es :",self.vel01)
        print("SU aceleracion :",self.alc01)

class Autosbot:
    def __init__(self):
        self.vel02 = random.randint(250,300)
        self.alc02 = random.randint(250,300)
        self.distancia = 0

    def avanzar(self):

        op = random.randint(1,3)
        
        if op == 1:
            self.distancia = self.distancia + (self.vel02 * 0.25) #Mas LENTO
        
        if op == 2:
            self.distancia = self.distancia + self.vel02

        if op == 3:
            self.distancia = self.distancia + (self.vel02 * 2) #MAS rapido

automio = Autocrtl()
automio.atributos()
automio.mostrar()

bott01 = Autosbot()
bott02 = Autosbot()

cuadros = 10000
fin = 0
turno = 1

while fin == 0:
    print(turno)

    print("1 LENTO")
    print("2 NORMAL")
    print("3 FRANCHESCO VIRGULINI FIUN")
    op = int(input("Elige estrategia :"))

    automio.carrera(op)

    bott01.avanzar()
    bott02.avanzar()

    print("distancia:", automio.distancia)
    print("Bot1 distancia:", bott01.distancia)
    print("Bot2 distancia:", bott02.distancia)

    if automio.distancia >= cuadros:
        print("GANASTE!")
        fin = 1

    if bott01.distancia >= cuadros:
        print("GANO BOT1")
        fin = 1

    if bott02.distancia >= cuadros:
        print("GANO BOT2")
        fin = 1

    turno = turno + 1



