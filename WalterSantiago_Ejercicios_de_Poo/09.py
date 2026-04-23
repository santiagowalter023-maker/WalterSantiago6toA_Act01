#Ejercicio 9: EL TESORO ESCONDIDO
#Un explorador se adentra en una cueva en busca de tesoros. En su camino encuentra cofres que pueden estar
#cerrados o abiertos, y que contienen cierta cantidad de monedas.
#El usuario deberá decidir qué hacer en cada momento: intentar abrir cofres, recolectar monedas o continuar
#explorando.
#El sistema debe permitir visualizar el estado del cofre y la cantidad de recursos acumulados por el jugador
#hasta finalizar la exploración.

import random

class Tesoro:
    def __init__(self):
        self.tesoroo = []
        self.total_monedas = 0
    
    def Moneda(self,cant):
        cant = random.randint(1,999)
        
        monedas = [cant]
        self.tesoroo.append(monedas)
        
        self.total_monedas = self.total_monedas + cant
        
    def Bicho(self):
        lagartija = random.randint(1,10)
        araña     = random.randint(1,20)
        serpiente = random.randint(1,5)
        
        bichos = [lagartija,araña,serpiente]
        
        self.tesoroo.append(bichos)
        
    def valioso(self):
        obj01 = input("Encontre algo valioso y es : ")
        obj02 = input("Ademas y otra cosa y es : ")
        obj03 = input("OO hoy estoy de suerte y es : ")
        
        objetos = [obj01,obj02,obj03]
        
        self.tesoroo.append(objetos)
    
    def Mostrar(self):
        print("----- ESTADO ACTUAL -----")
        print("Contenido encontrado:", self.tesoroo)
        print("Monedas acumuladas :", self.total_monedas)


class Exploracion(Tesoro):
    
    def Menu(self):
        op = 0
        
        while op != 4:
            print("1 - Abrir Cofre")
            print("2 - Recolectar Monedas")
            print("3 - Ver estado")
            print("4 - Salir")
            
            op = int(input("Opcion: "))
            
            if op == 1:
                print("Intentando abrir cofre...")
                
                estado = random.randint(0,1)
                
                if estado == 1:
                    print("El cofre estaba ABIERTO")
                    
                    tipo = random.randint(1,3)
                    
                    if tipo == 1:
                        self.Moneda(0)
                    if tipo == 2:
                        self.Bicho()
                    if tipo == 3:
                        self.valioso()
                
                if estado == 0:
                    print("El cofre estaba CERRADO")
            
            if op == 2:
                print("Recolectando monedas...")
                self.Moneda(0)
            
            if op == 3:
                self.Mostrar()
            
            if op == 4:
                print("Exploracion finalizada")
                self.Mostrar()


# PROGRAMA PRINCIPAL
juego = Exploracion()
juego.Menu()
        
    