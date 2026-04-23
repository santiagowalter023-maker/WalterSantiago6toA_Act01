#Ejercicio 7
#Desarrollar un programa que conste de una clase padre Cuenta y dos subclases PlazoFijo y CajaAhorro. Definir
#los atributos titular y cantidad y un método para imprimir los datos en la clase Cuenta. La clase CajaAhorro
#tendrá un método para heredar los datos y uno para mostrar la información.
#La clase PlazoFijo tendrá dos atributos propios, plazo e interés. Tendrá un método para obtener el importe del
#interés (cantidad*interés/100) y otro método para mostrar la información, datos del titular plazo, interés y total
#de interés.
#Crear al menos un objeto de cada subclase.

class Cuenta:
    def __init__(self,titlr,cant):
        self.titular  = titlr
        self.cantidad = cant

    def mostrasdatos(self):
        print("El titular  es :",self.titular)
        print("La cantidad es :",self.cantidad)

class CajaAhorro(Cuenta):
    def __init__(self,titlr,cant):
        super().__init__(titlr, cant)

    def datosmostar(self):
        self.mostrasdatos()

class PlazoFijo(Cuenta):
    def __init__(self,titlr,cant,plaz,intrs):
        super().__init__(titlr,cant)
        self.interes = intrs
        self.plazo   = plaz

    def calculintrs(self):
        return (self.cantidad * self.interes / 100)
    
    def datos(self):
        self.mostrasdatos()
        print("Interest   :",self.interes)
        print("Plazo Fijo :",self.plazo)
        print("Total es   :",self.calculintrs())

fondo = CajaAhorro("Messi", 40000)
fondo.datosmostar()

plazo = PlazoFijo("Cristiano", 50000, 30, 10)
plazo.datos()

         


     




