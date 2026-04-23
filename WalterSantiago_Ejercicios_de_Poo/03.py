#Ejercicio 3
#Desarrollar un programa que cargue los datos de un triángulo. Implementar una clase con los métodos para
#inicializar los atributos, imprimir el valor del lado con un tamaño mayor y el tipo de triángulo que es
#(equilátero, isósceles o escaleno).

class Triangulo:

    def lados(self,lada,ladb,ladc):
        self.ladoA = lada
        self.ladoB = ladb
        self.ladoC = ladc

    def triangulomay(self):
        may = self.ladoA

        if self.ladoB > may:
            may = self.ladoB

        if self.ladoC > may:
            may = self.ladoC

        print("EL lado mayor es ", may)

    def tipotriangulo(self):
        if self.ladoA == self.ladoB and self.ladoA == self.ladoC:
            print("ES EQUILATERO")

        if self.ladoA == self.ladoB or self.ladoA == self.ladoC or self.ladoB == self.ladoC:
            print("ES ISOSELES")

        else:
            print("ES ESCALENO")

triangulos = Triangulo()
lad1 = float(input(""))
lad2 = float(input(""))
lad3 = float(input(""))
triangulos.lados(lad1,lad2,lad3)
triangulos.triangulomay()
triangulos.tipotriangulo()