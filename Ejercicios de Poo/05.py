#Ejercicio 5
#Realizar una clase que administre una agenda. Se debe almacenar para cada contacto el nombre, el teléfono y
#el email. Además deberá mostrar un menú con las siguientes opciones
#● Añadir contacto
#● Lista de contactos
#● Buscar contacto
#● Editar contacto
#● Cerrar agenda

class Agenda:

    def __init__(self):
        self.contactos = []

    def menu(self):
        print("1_#● Añadir contacto   ")
        print("2_#● Lista  contacto   ")
        print("3_#● Buscar contacto   ")
        print("4_#● Editar contacto   ")
        print("5_#● Cerrar agenda     ")
        return int(input(""))
    
    def contacto(self):
        nombre = input("Nombre :")
        telefono = int(input("Ingresar Telefono : "))
        email = input("Email :")

        listA = [nombre,telefono,email]

        self.contactos.append(listA)

    def mostrar(self):
        for i in self.contactos:
            print("Nombre: ", i[0],"Telefono : ",i[1],"Email : ",i[2])

    def busqueda(self):
        nombes = input("¿Quien quiere buscar?")

        for i in self.contactos:
            if i[0] == nombes:
                print("Nombre: ", i[0],"Telefono : ",i[1],"Email : ",i[2])
                return
        

    def editar(self):
        nombes = input("¿Quien quiere buscar?")

        for i in self.contactos:
            if i[0] == nombes:
                i[1] = int(input("Ingresar nuevo telefono : "))
                i[2] = input("Ingresar nuevo email : ") 
                print("Nombre: ", i[0],"Telefono : ",i[1],"Email : ",i[2])
                return
        
agendas = Agenda()

opcion = 0

while opcion != 5:

    opcion = agendas.menu()

    if opcion == 1:
        agendas.contacto()

    if opcion == 2:
        agendas.mostrar()

    if opcion == 3:
        agendas.busqueda()

    if opcion == 4:
        agendas.editar()








    