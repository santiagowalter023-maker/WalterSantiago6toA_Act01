# ACA VA ESTAR EL CODIGO PICHON
import pygame

pygame.init()

ancho = 1020
alto = 720

ventana = pygame.display.set_mode((ancho, alto))

corriendo = True 
while corriendo == True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

pygame.quit()

print("Bienvenido")
