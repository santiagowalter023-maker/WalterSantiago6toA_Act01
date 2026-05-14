#01

#Ejercicio 1
#Realizar un programa que conste de una clase llamada Alumno que tenga como atributos el nombre y la nota
#del alumno. Definir los métodos para inicializar sus atributos, imprimirlos y mostrar un mensaje con el
#resultado de la nota y si ha aprobado o no.

class Alumno:
    # Inicializamos la clase alumno
    def __init__(self, nom, nt):         
        self.nombre = nom 
        self.nota = nt     
    
    # Verificamos si aprobó o reprobó
    def verificar(self):
        if self.nota >= 7:
            print("Aprobó")
        else:
            print("Reprobado")
    
    # Mostramos los datos
    def mostrar(self):
        print(f"Nombre: {self.nombre}")
        print(f"Nota: {self.nota}")
        self.verificar()
        print("-" * 30)


# Creamos los alumnos
alumno01 = Alumno("MESSI", 8)
alumno01.mostrar()

alumno02 = Alumno("Mbappé", 9)
alumno02.mostrar()

alumno03 = Alumno("Tito Calderón", 5)
alumno03.mostrar()
    
    
    
    
        