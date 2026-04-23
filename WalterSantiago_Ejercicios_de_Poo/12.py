#Ejercicio 12: AVENTURA Y OBJETOS
#Un aventurero recorre distintos escenarios recolectando objetos que encuentra en su camino. El usuario podrá
#decidir qué hacer con cada objeto: guardarlo, utilizarlo o descartarlo. Además, deberá poder consultar en todo
#momento qué elementos posee.
#El programa debe permitir gestionar esta información de forma dinámica durante la ejecución.

class Aventurero:
    def __init__(self):
        self.almacen = []

    def recoger(self,object):
        self.almacen.append(object)

        print("Tenes un nuevo objero :",object)

    def utilizar(self, object):
        for i in range(len(self.almacen)):
            if self.almacen[i]== object:
                self.almacen.remove(object)
                print("Usaste esto ",object)
                break
            else:
                print("No tenes esto ;",object)


    def descartar(self,object):
        for i in range(len(self.almacen)):
            if self.almacen[i] == object:
                self.almacen.remove(object)
                print("Sacaste este coso : ",object)
                break

            else:
                print("No tenes ese coso : ",object)

    def mostrar(self):
        print("Tenes en tu almacen :",self.almacen)

a = Aventurero()

op = 0
while op != 5:
    print("1 - Recoger Objeto")
    print("2 - Utilizar Objeto")
    print("3 - Descartar Objeto")
    print("4 - Mostar almacen")
    print("5 - Salir")

    op = int(input("Ingrese opcion :"))

    if op == 1:
        obje = input("Ingrese que objeto quiere recoger :")
        a.recoger(obje)

    if op == 2:
        obje = input("Ingrese objeto a utilizar :")
        a.utilizar(obje)

    if op == 3:
        obje = input("Ingrese objeto a borrar :")
        a.descartar(obje)

    if op == 4:
        a.mostrar()

print("desarrolla y crea (S.W)")

                        
    