#01

#Ejercicio 1
#Realizar un programa que conste de una clase llamada Alumno que tenga como atributos el nombre y la nota
#del alumno. Definir los métodos para inicializar sus atributos, imprimirlos y mostrar un mensaje con el
#resultado de la nota y si ha aprobado o no.

class Alumno:
    #Inicializamos la clase alumno
    
    def inicializar(self, nom):         
         self.nombre = nom 
         
    #♥ INICIALIZAMOS NT     
    def nota(self, nt):
         self.nota = nt  
    
    #MOstraMOS
    def Mostrar(self):
        print("Nombre",self.nombre)
        print("Nota :",self.nota)
        

#DEFINOS
alumno01 = Alumno()
alumno01.inicializar("MESSI")
alumno01.nota("Aprobado")
alumno01.Mostrar()

alumno02 = Alumno()
alumno02.inicializar("Mbappe")
alumno02.nota("Aprobado")
alumno02.Mostrar()

alumno03 = Alumno()
alumno03.inicializar("Tito Calderon")
alumno03.nota("REPROBADO")
alumno03.Mostrar()
    
    
    
    
        