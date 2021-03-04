import serial
import threading
from sklearn.externals import joblib
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import sys
sys.path.append('C:/Python37/Lib/site-packages')
from IPython.display import clear_output
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import random
from pyopenBCI import OpenBCyton
import time
import numpy as np
from scipy import signal

## funciones comunicación serial con el manipulador.

def iniciar_comunicacion():
    try:
        ser = serial.Serial(
            port="COM3",
            baudrate=4800,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True,
            dsrdtr=True,
        )
        if ser.isOpen():
            ser.flushInput()  # vacia bufer entrada
            ser.flushOutput()  # vacia bufer salida
        return ser
    except serial.SerialException:
            result = messagebox.showerror(
                "Error al establecer conexión:", message="-Compruebe que el robot está correctamente conectado al puerto")
    return 0


def finalizar_comunicacion_simple(ser):
    while True:
        estado = ser.getCTS()
        if estado == True:
            break
    if ser.isOpen():
        ser.close()

#Función para obtener datos online de la tarjeta
def print_raw(sample):
    print(sample.channels_data)


Objeto "board" llamando a la libreria de OpenBCI
board = OpenCyton(port='COM4', daisy=False)

#Start hace un Callback a la función print_raw
def Start():
    try:
        board.start_stream(print_raw)
    except:
        pass

#Creación del primer hilo para ejecutar la función Start en paralelo
y = threading.Thread(target=Start)
y.daemon = True
y.start()

time.sleep(.02)
board.disconnect()

SCALE_FACTOR = (4500000)/24/(2**23-1)  # From the pyOpenBCI repo
colors = 'rgbycmwr'

# Ajuste de la interfaz con la libreria QTGUI
#
#
# Plots:
# Señales EEG (3 CH)
# PSD (Power Spectral Density)
# Resultado del clasificador 
#
#



app = QtGui.QApplication([])
win = pg.GraphicsWindow(title='Python OpenBCI GUI')
win.setBackground('1E1E1E')
ts_plots = [win.addPlot(row=i, col=0, colspan=2, title='Channel %d' % i, labels={
                        'left': 'uV'}) for i in range(1, 4)]
fft_plot = win.addPlot(row=1, col=2, rowspan=4, title='PSD', labels={
                       'left': 'uV', 'bottom': 'Hz'})
fft_plot.setLimits(xMin=3.5, xMax=15, yMin=0, yMax=20000)
waves_plot = win.addPlot(row=6, col=0, colspan=4, title='Clasificador', labels={
                         'left': 'uV', 'bottom': 'EEG Band'})
waves_plot.setLimits(xMin=0.5, xMax=5.5, yMin=0)
waves_xax = waves_plot.getAxis('bottom')
waves_xax.setTicks([list(zip(range(5), ('', '4Hz', '5Hz', '6Hz', '7Hz')))])


Bandera = False

# Define OpenBCI callback function
def save_data():
    global data
    data.append([i*SCALE_FACTOR for i in sample.channels_data])

# Define funcion updater que actualiza los graficos a 250 Hz
def updater():
    global data, colors
    t_data = np.array(data[-1250:]).T #transpose 
    #fs = 250 #Hz

    # Notch 
    def notch_filter(val, data, fs=250):
        notch_freq_Hz = np.array([float(val)])
        for freq_Hz in np.nditer(notch_freq_Hz):
            bp_stop_Hz = freq_Hz + 3.0 * np.array([-1, 1])
            b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0),'bandstop')
            fin = data = signal.lfilter(b, a, data)
        return fin

    # Bandpass 
    def bandpass(start, stop, data, fs = 250):
        bp_Hz = np.array([start, stop])
        b, a = signal.butter(2, bp_Hz / fs, btype='bandpass')
        return signal.lfilter(b, a, data, axis=0)

    # Aplicando los filtros
    nf_data = [[],[],[]]
    bp_nf_data = [[],[],[]]

    for i in range(3):
        nf_data[i] = notch_filter(60, t_data[i])
        #print (nf_data)
        bp_nf_data[i] = bandpass(1, 20, nf_data[i])
        if i == 0:
            vector0 = bp_nf_data[i]
            vector0 = vector0[600:len(vector0)]
        if i == 1:
            vector1 = bp_nf_data[i]
            vector1 = vector1[600:len(vector1)]
      #  if i == 2:
       #     vector2 = bp_nf_data[i]
        #    vector2 = vector2[600:len(vector2)]   
        #if i == 3:
         #   vector3 = bp_nf_data[i]
         #   vector3 = vector3[600:len(vector3)]  
        #if i == 4:
          #  vector4 = bp_nf_data[i]
          #  vector4 = vector4[600:len(vector4)]    

    # Plotear los 3 canales EEG 
    for j in range(3):
        global color_s
        color_s = [[77,147,167],[145,75,211],[1,250,68],[235,222,82],[0,233,195],[194,85,81],[221,104,29],[159,201,121]]
        ts_plots[j].clear()
        if j == 0:
            ts_plots[j].plot(pen=color_s[j]).setData(vector0)
        if j == 1:
            ts_plots[j].plot(pen=color_s[j]).setData(vector1)
        #if j == 2:
            #ts_plots[j].plot(pen=color_s[j]).setData(vector2)
        #if j == 3:
         #   ts_plots[j].plot(pen=color_s[j]).setData(vector3)
        #if j == 4:
         #   ts_plots[j].plot(pen=color_s[j]).setData(vector4)
    

# Función Analisis() que se ejecuta cada 15 o 30 seg
def Analisis():
    t_data2 = np.array(data[-3750:]).T #transpose
    fs = 250

        # Notch Filter
    def notch_filter(val, data, fs=250):
        notch_freq_Hz = np.array([float(val)])
        for freq_Hz in np.nditer(notch_freq_Hz):
            bp_stop_Hz = freq_Hz + 3.0 * np.array([-1, 1])
            b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0),'bandstop')
            fin = data = signal.lfilter(b, a, data)
        return fin

    # Bandpass filter
    def bandpass(start, stop, data, fs = 250):
        nyq = 0.5 * fs
        low = start / nyq
        high = stop / nyq
        b, a = signal.butter(2, [low, high], btype='bandpass')
        return signal.lfilter(b, a, data)
    
	
  #Metodo que corta las señales obtenidas del PSD
    def Argumentos(freqs, psd, rangoLow, rangoHigh):
        Low = ((rangoLow*100)/max(freqs))/100
        Rango = int(np.ceil(Low*len(freqs)))

        rangoHigh = ((rangoHigh*100)/max(freqs))/100
        Rango2 = int(np.ceil(rangoHigh*len(freqs)))

        freqs = freqs[Rango:Rango2]
        psd = psd[Rango:Rango2]

        max_psd = max(psd)
        a = 0
        for i in psd:
            if (i == max_psd):
                ejeX = freqs[a]
            a += 1

        return max_psd, ejeX

    # Aplicando Filtros
    nf_data = [[],[],[]]
    bp_nf_data = [[],[],[]]
    data_final = [[],[],[]]

    for i in range(3):
        nf_data[i] = notch_filter(60, t_data2[i])
        bp_nf_data[i] = bandpass(1, 20, nf_data[i])
        if i == 0:
            vector0 = bp_nf_data[i]
            vector0 = vector0[600:len(vector0)]
        if i == 1:
            vector1 = bp_nf_data[i]
            vector1 = vector1[800:len(vector1)]
        #if i == 2:
            #vector2 = bp_nf_data[i]
            #vector2 = vector2[800:len(vector2)]   
        #if i == 3:
         #   vector3 = bp_nf_data[i]
         #   vector3 = vector3[800:len(vector3)]  
        #if i == 4:
         #   vector4 = bp_nf_data[i]
         #   vector4 = vector4[800:len(vector4)]

    for kk in range(3):
        if kk == 0:
            data_final[kk] = vector0
        if kk == 1:
            data_final[kk] = vector1
        #if kk == 2:
            #data_final[kk] = vector2
        #if kk == 3:
         #   data_final[kk] = vector3
        #if kk == 4:
         #   data_final[kk] = vector4            
    
    # Obtener la densidad espectral de potencia y graficarla
    sp = [[], [], []]
    freq = [[], [], []]
    win = 512 * fs

    fft_plot.clear()
    for k in range(3):
        freq[k], sp[k] = signal.welch(data_final[k], fs, nperseg=win)
        #sp[k] = np.absolute(np.fft.fft(bp_nf_data[k]))
        #freq[k] = np.fft.fftfreq(bp_nf_data[k].shape[-1], 1.0/fs)
        fft_plot.plot(pen=color_s[k]).setData(freq[k], sp[k])
    
 #Obtener los rangos a analizar del PSD

    max4, freq4 = Argumentos(freq[0], sp[0], 3.85, 4.15)
    max5, freq5 = Argumentos(freq[0], sp[0], 4.85, 5.15)
    max6, freq6 = Argumentos(freq[0], sp[0], 5.85, 6.15)
    max7, freq7 = Argumentos(freq[0], sp[0], 6.85, 7.15)

    Maximos = [max4, max5, max6, max7]
    Max_Freqs = [freq4, freq5, freq6, freq7]

    MaximoF = max(Maximos)

    a = 0
    for i in Maximos:
        if(i == MaximoF):
            Freq_final = Max_Freqs[a]
        a += 1

    ValorY = MaximoF
    ValorX = Freq_final




##########################################################
# CARGA DEL MODELO YA ENTRENADO
##########################################################


    Tree = joblib.load("ModelDecisionTree")
    valor = Tree.predict([[ValorX, ValorY]])
    print(valor)
    Alturas = [0,0,0,0]


##########################################################
# ECALUACIÓN DEL MODELO Y COMANDOS MELFA BASIC IV
##########################################################

    if (valor == ['4hz ']):
        Alturas = [10, 0, 0, 0]
        # Escribir comando serial para el Robot
        ser = iniciar_comunicacion()
        ser.write(b'\rsp 7\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rOG\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(4)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ 98,0,-10,-70,-140\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(1)
        ser = iniciar_comunicacion()
        ser.write(b'\rsp 1\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(1)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ 2,0,0,0,0\r')
        finalizar_comunicacion_simple(ser)

    elif (valor == ['5hz ']):
        Alturas = [0, 10, 0, 0]
        # Escribir comando serial para el Robot
        ser = iniciar_comunicacion()
        ser.write(b'\rSP 8\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rOG\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(3)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ 0,-24,0,79,120\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(2)
        ser = iniciar_comunicacion()
        ser.write(b'\rSP 4\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ 0,0,-60,0,0\r')
        finalizar_comunicacion_simple(ser)


    elif (valor == ['6hz ']):
        Alturas = [0, 0, 10, 0]
        # Escribir comando serial para el Robot
        ser = iniciar_comunicacion()
        ser.write(b'\rsp 8\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rOG\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(3)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ -115,93,-90,0,30\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(2)
        ser = iniciar_comunicacion()
        ser.write(b'\rsp 1\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ -3,0,0,0,0\r')
        finalizar_comunicacion_simple(ser)
    
    elif (valor == ['7hz ']):
        Alturas = [0, 0, 0, 10]
        # Escribir comando serial para el Robot
        ser = iniciar_comunicacion()
        ser.write(b'\rSP 8\r')
        finalizar_comunicacion_simple(ser)
        ser = iniciar_comunicacion()
        ser.write(b'\rOG\r')
        finalizar_comunicacion_simple(ser)
        time.sleep(3)
        ser = iniciar_comunicacion()
        ser.write(b'\rMJ -84,0,0,0,27\r')
        finalizar_comunicacion_simple(ser)

    else:
        Alturas = [0,0,0,0]

 # Grafica el resultado del clasificador

    bg1 = pg.BarGraphItem(x=[1,2,3,4], height=Alturas, width=0.6, brush=[1,250,68])
    waves_plot.clear()
    waves_plot.addItem(bg1)

# 
def start_board():
    board.start_stream(save_data)




###################################################################
# "Main"
# Crea un primer hilo que obtiene datos en paralelo al programa
# Con el metodo timer se ejecutan las funciones updater y Analisis
# segun el tiempo especificato por el metodo timer.start(0)
###################################################################

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        x = threading.Thread(target=start_board)
        x.daemon = True
        x.start()
        timer = QtCore.QTimer()
        timer.timeout.connect(updater)
        timer.start(0)
        timer2 = QtCore.QTimer()
        timer2.timeout.connect(Analisis)
        timer2.start(15000)
        QtGui.QApplication.instance().exec_()
