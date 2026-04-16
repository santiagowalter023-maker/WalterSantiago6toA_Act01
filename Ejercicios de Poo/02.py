#02

#Ejercicio 2
#Realizar un programa que tenga una clase Persona con las siguientes características. La clase tendrá como
#atributos el nombre y la edad de una persona. Implementar los métodos necesarios para inicializar los
#♥atributos, mostrar los datos e indicar si la persona es mayor de edad o no.#&'"3☺ →"

class viejo:
    
    def Nombre(self,nom):
        self.nombre = nom
        
    def Edad(self,edd):
        self.edad = edd
          

    def Mostrar(self):
        print("Nombre :",self.nombre)
        print("Edad   :",self.edad)
        
    def Verficacion(self):
        if self.edad >= 30:
            print("SI es mayor de edad")
            
        
        if self.edad <= 30:
            print("NO es menor de edad")
           
        
persona01 = viejo()
persona01.Nombre("MAXVerstappen")
persona01.Edad(50)
persona01.Mostrar()
        