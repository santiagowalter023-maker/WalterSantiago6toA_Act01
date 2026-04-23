#02

#Ejercicio 2
#Realizar un programa que tenga una clase Persona con las siguientes características. La clase tendrá como
#atributos el nombre y la edad de una persona. Implementar los métodos necesarios para inicializar los
#♥atributos, mostrar los datos e indicar si la persona es mayor de edad o no.#&'"3☺ →"

class Persona:
    
    def __init__(self, nom, edd):
        self.nombre = nom
        self.edad = edd
             

    def Mostrar(self):
        print("Nombre :",self.nombre)
        print("Edad   :",self.edad)
        
    def Verficacion(self):
        if self.edad >= 18:
            print("SI es mayor de edad")
        
        else :
            print("NO es menor de edad")
           
        
persona01 = Persona( "MAX vertapen",26)
persona01.Mostrar()
persona01.Verficacion()
        