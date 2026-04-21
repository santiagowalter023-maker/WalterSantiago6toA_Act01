#EJERCICIO 8 
#En una arena de combate se enfrentan 2 personajes uno controlado por el usuario y uno controlado por el sistema 
#Cada personaje posee ciertas caracteristicas que determinan su capacidad de resistir ataques y de causar daño
#durante el combate . el combate ,el usuario puede decidir que accion realizar en su turno , mientras que el oponenrte responde
#automaticamente
#el combate finaliza cuando uno de los personajes no puede continuar

import random

class Personajecontrolado:
    
    def atributo(self,nom,h):
        nom = input("¿Como se llama ? ")
        h   = int(input("¿Que altura tiene? : "))
        
        self.nombre1 = nom
        self.altura1 = h
        
    def __init__(self):
        self.fuerza1      = int(input("Ingrese su fuerza : "))
        self.resistencia1 = int(input("Ingrese su resistencia : ")) 
        
    def daño(self):
        return (self.fuerza1 * 100) - self.resistencia1
    
    def mostar(self):
        print("Estas Listo para Combatir")
        print("Usted se llama : ",self.nombre1)
        print("Su altura es   : ",self.altura1)
        print("Su fuerza es   : ",self.fuerza1)
        print("Su resistencia : ",self.resistencia1)
        print("Su daño es     : ",self.daño())   # ← corregido


class PersonajeAutomatico:

    def Atributo(self):
        self.nombre2 = "Bot"
        self.altura2 = random.randint(150,200)
        
    def __init__(self):
        self.fuerza2 = random.randint(1,10)
        self.resistencia2 = random.randint(50,100)
        
    def Daño(self):
        return (self.fuerza2 * 100) - self.resistencia2
    
    def Mostar(self):
        print("Su  Rival      es    : ",self.nombre2)
        print("Su  Altura     es    : ",self.altura2)
        print("Su Fuerza      es    : ",self.fuerza2)
        print("Su Resistencia es    : ",self.resistencia2)
        print("Su daño        es    : ",self.Daño())


class Combate(Personajecontrolado,PersonajeAutomatico):
    
    def __init__(self):
        Personajecontrolado.__init__(self)
        PersonajeAutomatico.__init__(self)
        
        self.atributo("",0)
        self.Atributo()
        
    def Menu(self):
        op = 0
        
        while op != 4:
            print("01 Ataque ")
            print("02 Recupero Vida")
            print("03 ATAQUEEE")
            print("04 cerrar")
            
            op = int(input("Opcion: "))
            
            if op == 1:
                print("Ataque 1")
                
                ataque1 = self.resistencia2 - self.daño()
                self.resistencia2 = ataque1
                
                print("El rival quedo con vida:", self.resistencia2)
                
            if op == 2: 
                recuper = self.resistencia1 + (self.resistencia1 / 10)
                self.resistencia1 = recuper
                
                print("Recupero Vida:", self.resistencia1)
                
            if op == 3:
                ataque2 = self.resistencia1 - self.Daño()
                self.resistencia1 = ataque2
                
                print("El enemigo contraataca, te queda:", self.resistencia1)


# PROGRAMA PRINCIPAL
control = Combate()

control.mostar()
control.Mostar()

control.Menu()
    
    
    
    
    
        
    
       

