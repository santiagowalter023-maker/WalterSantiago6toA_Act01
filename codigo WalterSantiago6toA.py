import tkinter as tk
from tkinter import messagebox

#CONFIGURACION DE VENTANA

ventana = tk.Tk()
ventana.title("Menú Heladería")
ventana.geometry("400x400")
ventana.configure(bg="green")

#Archivo Definicion


##1.SECCIÓN TAMAÑO
opcion_t = tk.IntVar()


#FUNCION
def mostrar_sabores():
    sabores.pack(pady=10)
    boton_final.pack(pady=20)
    boton_siguiente.pack_forget()


#FUNCION PARA CALCULAR PRECIO
def calcularprecio(bochas):

    if bochas == 1:
        precios = 700
        return precios

    if bochas == 2:
        precios = 1200
        return precios

    if bochas == 3:
        precios = 1600
        return precios


#FUNCION FINAL
def terminar():

    saboras = []

    if limonA.get() == 1:
        saboras.append("Limon")

    if frutillA.get() == 1:
        saboras.append("Frutilla")

    if ananaA.get() == 1:
        saboras.append("Anana")

    if nranjaA.get() == 1:
        saboras.append("Naranja")

    if vainillA.get() == 1:
        saboras.append("Vainilla")

    if ddelecheA.get() == 1:
        saboras.append("DulceDeLeche")

    if tramntanA.get() == 1:
        saboras.append("Tramontana")
        
    if granizadA.get() == 1:
        saboras.append("MentaGranizada")


    bochas = opcion_t.get()

    precio = calcularprecio(bochas)

    #Deficion archivo
    RUTA  = "ticked.txt"
    ABRIR = open(RUTA, "a")


    ABRIR.write(    "Resumen del pedido \n")
    ABRIR.write(    "Bochas: " + str(bochas)+ "\n") 
    ABRIR.write(    "Sabores: " + str(saboras)+ "\n") 
    ABRIR.write(    "Precio: $" + str(precio)+ "\n")
    ABRIR.write("_____________________ \n")

    ABRIR.close()


    if bochas == 0:
        messagebox.showerror(
        "",
        ""    
        "Numero incorrecto de bochas"                   
        )
        return

    if len(saboras) > bochas:
        messagebox.showinfo(
        "",
        ""
        "Elejiste mas sabores que bochas"
        )
        return
    
    precio = calcularprecio(bochas)


    #Destruye ventana y cierra
    ventana.destroy()

    




lbl_paso1 = tk.Label(ventana, text="1. ELIGE EL TAMAÑO",bg= "yellow")
lbl_paso1.pack(pady=50)


bocha1 = tk.Radiobutton(ventana, text="1 Bocha", variable=opcion_t, value=1)
bocha1.pack()

bocha2 = tk.Radiobutton(ventana, text="2 Bochas", variable=opcion_t, value=2)
bocha2.pack()

bocha14 = tk.Radiobutton(ventana, text="1/4 Kilo", variable=opcion_t, value=3)
bocha14.pack()


boton_siguiente = tk.Button(ventana,text="Elegir sabores ",command=mostrar_sabores,bg="red")
boton_siguiente.pack(pady=50)


# SABORES
sabores = tk.Frame(ventana)

limonA    = tk.IntVar()
frutillA  = tk.IntVar()
ananaA    = tk.IntVar()
nranjaA   = tk.IntVar()
vainillA  = tk.IntVar()
ddelecheA = tk.IntVar()
tramntanA = tk.IntVar()
granizadA = tk.IntVar()

#Botones de sabores
#Sabores 

etiqueta01= tk.Label(sabores, text= "Sabores al Agua")
etiqueta01.grid(row= 0,column=0)

limon2       = tk.Checkbutton(sabores, text="Limon", variable=limonA)
limon2.grid(row= 1, column= 0)

frutilla2    = tk.Checkbutton(sabores, text="Frutilla", variable=frutillA)
frutilla2.grid(row= 2, column= 0)

#

anana2       = tk.Checkbutton(sabores, text="Anana", variable=ananaA)
anana2.grid(row= 3, column=0)

naraja2      = tk.Checkbutton(sabores, text="Naranja", variable=nranjaA)
naraja2.grid(row= 4, column=0)

#Sabores a la crema
etiqueta02 = tk.Label(sabores, text= "Sabores a la Crema")
etiqueta02.grid(row=0, column= 1)

vainilla2    = tk.Checkbutton(sabores, text="Vainilla", variable=vainillA)
vainilla2.grid(row= 1, column =1)

dulcelech2   = tk.Checkbutton(sabores, text="Dulce de leche", variable=ddelecheA)
dulcelech2.grid(row= 2,column =1)

#

tramontana2  = tk.Checkbutton(sabores, text="Tramontana", variable=tramntanA)
tramontana2.grid(row= 3,column = 1)

granizada2   = tk.Checkbutton(sabores, text="Menta Granizada", variable=granizadA)
granizada2.grid(row= 4,column = 1)

#BOTÓN FINAL
boton_final = tk.Button(ventana, text="CONFIRMAR PEDIDO", command=terminar)
boton_final.pack(pady= 50)


ventana.mainloop()