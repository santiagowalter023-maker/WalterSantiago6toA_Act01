#Ejercicio 6
#En un banco tienen clientes que pueden hacer depósitos y extracciones de dinero. El banco requiere también al
#final del día calcular la cantidad de dinero que se ha depositado.
#Se deberán crear dos clases, la clase cliente y la clase banco. La clase cliente tendrá los atributos nombre y
#cantidad y los métodos __init__, depositar, extraer, mostrar_total.
#La clase banco tendrá como atributos 3 objetos de la clase cliente y los métodos __init__, operar y
#deposito_total.

class Cliente:
    def __init__(self,nom):

        self.nombre = nom
        
        self.cantidad = 0

    def depositar(self,dinerou):
        self.cantidad = dinerou + self.cantidad

    def extraer(self,dinerou):
        self.cantidad = self.cantidad - dinerou

    def mostrar(self):
        print("Nombre : ",self.nombre,"Cantidad : ",self.cantidad)

class Banco:
    def __init__(self):
        self.nombre01 = Cliente("MESSI")
        self.nombre02 = Cliente("FORD MUSTANG 1970")
        self.nombre03 = Cliente("DORITOS")
        self.nombre04 = Cliente("MARUITOS")

    def operar(self):
        self.nombre01.depositar(1)
        self.nombre02.depositar(9000000000000000000000000000000)
        self.nombre03.depositar(2)
        self.nombre04.depositar(2)
        self.nombre04.extraer(2)

    def deposito_total(self):
        total = self.nombre01.cantidad + self.nombre02.cantidad +self.nombre03.cantidad + self.nombre04.cantidad
         
        print("DINERO TOTAL ES : ",total)

        self.nombre01.mostrar()
        self.nombre02.mostrar()
        self.nombre03.mostrar()
        self.nombre04.mostrar()

bancos = Banco()
bancos.operar()
bancos.deposito_total()






    

    


 



       

    