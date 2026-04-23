#Ejercicio 13: DESAFÍO DE DADOS
#En un juego de azar participan varios jugadores. Uno de ellos será controlado por el usuario. En cada ronda,
#el usuario podrá lanzar un dado para obtener un valor que se acumulará en su puntaje total. Los demás
#jugadores también participarán automáticamente.
#Al finalizar varias rondas, se deberá determinar el resultado del juego.

import random

class JugadorCtr:
    def __init__(self):
        self.total = 0
        self.puntaje = []
        self.nombre = input("Ingrese su nombre :")

    def lanzamiento(self):
        
        dado = random.randint(1,6)
        self.puntaje.append(dado)
        self.total = self.total + dado

        print("Puntaje de  dado",dado)
        
    def mostrar(self):
        print("Vos sos :",self.nombre)
        print("Puntaje total : ",self.total)

class JugadorBoot:
    def __init__(self,nombre):
        self.total2 = 0
        self.puntaje2 = []
        self.nombre2 = nombre
        


    def lanzamiento(self):
        dado2 = random.randint(1,6)
        self.puntaje2.append(dado2)
        self.total2 = self.total2 + dado2

        print("Puntaje de  dado",dado2)
    
 
    def mostrar(self):
        print("EL siguiente jugador es ;",self.nombre2)
        print("Puntaje total : ",self.total2)

a = JugadorCtr()
b = JugadorBoot("MAQUINARDA")
c = JugadorBoot("VERTAPPEN")
d = JugadorBoot("LECRERC")

turnos = 0
op = 0

while turnos < 5:
    print("Que desea hacer ?")
    print("1 - Lanzar dado  ")
    print("2 -Mostrar puntos")

    turnos = turnos+ 1

    op = int(input("Ingrece mi opcion :"))

    if op == 1:
        a.lanzamiento()

        
        b.lanzamiento()

        
        c.lanzamiento()
  
        
        d.lanzamiento()


    if op == 2:
        a.mostrar()
        b.mostrar()
        c.mostrar()
        d.mostrar()
    
a.mostrar()
b.mostrar()
c.mostrar()
d.mostrar()

mayor = a.total
ganador = a.nombre

if b.total2 > mayor:
    mayor = b.total2
    ganador = b.nombre2

if c.total2 > mayor:
    mayor = c.total2
    ganador = c.nombre2

if d.total2 > mayor:
    mayor = d.total2
    ganador = d.nombre2

print("El ganador es:", ganador)
print("Con puntaje:", mayor)


    


    


