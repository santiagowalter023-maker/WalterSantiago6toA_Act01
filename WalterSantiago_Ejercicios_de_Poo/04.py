#Ejercicio 4
#Realizar un programa en el cual se declaren dos valores enteros por teclado utilizando el método __init__.
#Calcular después la suma, resta, multiplicación y división. Utilizar un método para cada una e imprimir los
#resultados obtenidos. Llamar a la clase Calculadora.

class Calculadora:
    def __init__(self, n1, n2):
        self.numero1 = n1
        self.numero2 = n2

    def sumar(self):
        sumas = self.numero1 + self.numero2

        print("La suma es ", sumas)

    def restar(self):
        restas = self.numero1 - self.numero2

        print("La resta es ", restas)

    def multipicacion(self):
        multiplicar = self.numero1 * self.numero2

        print("La multiplicacion es ", multiplicar)

    def dividir(self):
        divicion = self.numero1 / self.numero2

        print("La division  es ", divicion)


A = int(input("Ingrese el 1re numero : "))
B = int(input("Ingrese el 2do numero : "))

operacion = Calculadora(A, B)
operacion.sumar()
operacion.restar()
operacion.multipicacion()
operacion.dividir()

    

    



        