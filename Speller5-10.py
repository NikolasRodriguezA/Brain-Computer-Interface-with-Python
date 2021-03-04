# Librerias.
import os
import datetime
import time
import random
from tkinter import *
import subprocess
import math
# Variables.
global color
global color1
bandera=0
t=10
# Función para centrar la Interfaz.
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

# Asignación del nombre de la ventana--Instancia.
ventana= Tk()
ww, hh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
ventana.configure(bg='black')
#Dimensiones de la ventana
ventana.overrideredirect(1)
ventana.geometry("%dx%d+0+0" % (ww, hh))
center(ventana) 

# Configuración Inicial del Rectángulo de la esquina superior izquierda, Dimensiones(Tamaño y Posición) y Color.
l1= Label(ventana,bg='#ffffff')
l1.place(x=40, y=20)
txt=' ▢ '
color  ="white"
# Configuracion del label para el rectágulo de la esquina superior izquierda.
l11= Label(ventana,bg='black')
l11.place(x=80, y=165)
l11.config(text="4Hz",fg="WHITE",font=("gothic",25))

# Configuración Inicial del Rectángulo de la esquina superior derecha, Dimensiones(Tamaño y Posición) y Color.
l2= Label(ventana,bg='#ffffff')
l2.place(x=1280, y=20)
txt1=' ▢ '
color1  = "white"
# Configuracion del label para el rectágulo de la esquina superior derecha.
l21= Label(ventana,bg='black')
l21.place(x=1320, y=165)
l21.config(text="5Hz",fg="WHITE",font=("gothic",25))

# Configuración Inicial del Rectángulo de la esquina inferior izquierda, Dimensiones(Tamaño y Posición) y Color.
l3= Label(ventana,bg='#ffffff')
l3.place(x=40, y=700)
txt2=' ▢ '
color2  = "white"
# Configuracion del label para el rectágulo de la esquina inferior izquierda.
l31= Label(ventana,bg='black')
l31.place(x=75, y=850)
l31.config(text="6Hz",fg="WHITE",font=("gothic",25))

# Configuración Inicial del Rectángulo de la esquina inferior derecha, Dimensiones(Tamaño y Posición) y Color.
l4= Label(ventana,bg='#ffffff')
l4.place(x=1280, y=700)
txt3=' ▢ '
color3  = "yellow"
# Configuracion del label para el rectágulo de la esquina inferior derecha.
l41= Label(ventana,bg='black')
l41.place(x=1320, y=850)
l41.config(text="7Hz",fg="WHITE",font=("gothic",25))


#Tiempo en milisegundo, 100=10hz 83.3333333=12hz 66.666666=15
#7hz=142ms 5.88hz=170ms
#8Hz    = 125ms --> 125/2
#7hz    = 142ms --> 142/2   
#6hz    = 166ms --> 166/2
#5Hz    = 200ms --> 200/2
#4Hz    = 250ms --> 250/2
# Asignacion de Tiempos.
Cuatro  = 250/2
Cinco   = 200/2
Seis    = 166/2
Siete   = 142/2
Ocho    = 125/2
Nueve   = 111/2
Tiempo  = 10000
def labelconfig():  # Función Para cambiar el color del Rectángulo de negro a blanco a una frecuencia de 4 Hz.
    global color    
    z=txt
    if color=="black": # Condición para cononcer el color actual del rectángulo y poderlo cambiar.
        color="white"
    else:
        color="black"
    l1.config(text=z,fg='white',bg=str(color),font=("Helvetica",90))# Datos para actualizar la ventana.
    ventana.after(math.ceil(Cuatro), labelconfig)   # Función para Actualizar la ventana.

def labelconfig1(): # Función Para cambiar el color del Rectángulo de negro a blanco a una frecuencia de 5 Hz.
    global color1
    z=txt1
    if color1=="black": # Condición para cononcer el color actual del rectángulo y poderlo cambiar.
        color1="white"
    else:
        color1="black"
    l2.config(text=z,fg='white',bg=str(color1),font=("Helvetica",90))# Datos para actualizar la ventana.
    ventana.after(math.ceil(Cinco), labelconfig1)   # Función para Actualizar la ventana.

def labelconfig2(): # Función Para cambiar el color del Rectángulo de negro a blanco a una frecuencia de 6 Hz.
    global color2
    z=txt2
    if color2=="black": # Condición para cononcer el color actual del rectángulo y poderlo cambiar.
        color2="white"
    else:
        color2="black"
    l3.config(text=z,fg='white',bg=str(color2),font=("Helvetica",90))# Datos para actualizar la ventana.
    ventana.after(math.ceil(Seis), labelconfig2)    # Función para Actualizar la ventana.

def labelconfig3(): # Función Para cambiar el color del Rectángulo de negro a blanco a una frecuencia de 7 Hz.
    global color3
    z=txt3
    if color3=="black": # Condición para cononcer el color actual del rectángulo y poderlo cambiar.
        color3="white"
    else:
        color3="black"
    l4.config(text=z,fg='white',bg=str(color3),font=("Helvetica",90))# Datos para actualizar la ventana.
    ventana.after(math.ceil(Siete), labelconfig3)   # Función para Actualizar la ventana. 

def root(): # Función encargada de Pausar el parpadero de los rectángulos por 5 Segundos.
    global Tiempo # El tiempo es de 10 Segundos, De los cuales los rectángulos estaran parpadeando.
    global bandera # Bandera para intercambiar de 5s a 10s.
    global t
    bandera=1
    time.sleep(t) # Al inicio se tiene t=10s de pausa con la finalidad de sincronizar esta interfaz SSVEP-SP con la interfaz que procesa la señal.
    bandera=0
    t=5
    ventana.after(Tiempo, root) # Función para Actualizar la ventana.
    
# Llamado de Funciones.
labelconfig()
labelconfig1()
labelconfig2()
labelconfig3()
root()
i= TRUE
while i == TRUE: # Ciclo infinito
    print("Tiempo= %d"%(t)) 
    if bandera==0:
        ventana.update() # Función para Actualizar la interfaz.
    else:
        print("Wait")
 

