import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import messagebox
import threading
import time
import matplotlib.pyplot as plt

s_rate=44100
AMPLITUD=1

NOTASM={
    "DO":261.63,
    "RE":293.66,
    "MI":329.63,
    "FA":349.23,
    "SOL":392.00,
    "LA":440.00,
    "SI":493.88,
    "do" : 523.25
}

NOTASR={
    261.63:"DO",
    293.66:"RE",
    329.63:"MI",
    349.23:"FA",
    392.00:"SOL",
    440.00:"LA",
    493.88:"SI",
    523.25:"do",
}

star=[
    "DO", "DO", "SOL", "SOL", "LA", "LA", "SOL",  # Twinkle, twinkle, little star
    "FA", "FA", "MI", "MI", "RE", "RE", "DO",  # How I wonder what you are
    "SOL", "SOL", "FA", "FA", "MI", "MI", "RE",  # Up above the world so high
    "SOL", "SOL", "FA", "FA", "MI", "MI", "RE",  # Like a diamond in the sky
    "DO", "DO", "SOL", "SOL", "LA", "LA", "SOL",  # Twinkle, twinkle, little star
    "FA", "FA", "MI", "MI", "RE", "RE", "DO"   # How I wonder what you are
]

feliz_cum = [
    "DO", "DO", "RE", "DO", "FA", "MI",    # Feliz cumpleaños a ti
    "DO", "DO", "RE", "DO", "SOL", "FA",    # Feliz cumpleaños a ti
    "DO", "DO", "DO", "LA", "LA", "LA", "FA",  # Feliz cumpleaños querido (nombre)
    "MI", "MI", "RE", "DO", "SI", "DO"       # Feliz cumpleaños a ti
]

jing_bells = [
    "SOL", "SOL", "SOL", "DO", "MI", "RE", "DO", "SI", "DO",    # Jingle bells, jingle bells,
    "SOL", "SOL", "SOL", "DO", "MI", "RE", "DO", "DO", "DO",    # Jingle all the way
    "SOL", "SOL", "SOL", "DO", "MI", "RE", "DO", "SI", "DO",    # Oh! what fun it is to ride
    "SOL", "SOL", "SOL", "DO", "MI", "RE", "DO", "DO", "DO"     # In a one horse open sleigh
]

songs={
    "Estrellita":star,
    "Happy Birthday":feliz_cum,
    "Jingle Bell":jing_bells
}

def generar_seno(freq,t,s_rate=s_rate,foDur=0.7):
    global AMPLITUD
    t=np.linspace(0,t,int(s_rate*t),endpoint=False)
    wave=AMPLITUD*np.sin(2*np.pi*freq*t)
    graphicWave(t,wave,freq)
    #fade_out = np.linspace(1, 0, int(s_rate * foDur))
    #wave[-len(fade_out):] *= fade_out  # Aplicar el fade-out al final de la onda
    return wave

def playNote(f,time):
    global currentNote, currFreq
    currentNote=NOTASR.get(f)
    currFreq=NOTASM.get(currentNote)
    print(currentNote)
    lab_curr_note['text']=currentNote
    label_curr_freq['text']=currFreq
    wave=generar_seno(freq=f,t=time)
    sd.play(wave,s_rate)
    sd.wait()
    print("AMPLITUD: ",AMPLITUD)
    print("S_RATE: ",s_rate)
    

def setAdjValues():
    global currAmp, currSFreq
    
    amplitud = amp_slider.get()
    sample_rate = sample_rate_slider.get()
    print(amplitud)
    print(sample_rate)
    global AMPLITUD,s_rate
    AMPLITUD=amplitud
    s_rate=sample_rate
    messagebox.showinfo("Guardado","Los parametros se han establecido con exito")
    label_curr_AMP['text']=AMPLITUD
    label_curr_s_rate['text']=s_rate

def playSong():
    global stop
    song=lista_canciones.get()
    for i in songs.get(song):
        if(not(stop)):
            playNote(NOTASM.get(i),DURACION)
            time.sleep(0.1)
        else:
            return

def play():
    global stop
    stop = False  # Restablecer el estado de detención
    hilo = threading.Thread(target=playSong)
    hilo.start()
    

def stopSong():
    global stop
    stop=True

def onClose():
    stopSong()
    ventana.destroy()

def graphicWave(dom,wave,freq):
    timeD = dom[:int(s_rate * 0.02)]  # Mostrar solo los primeros 20ms
    waveD = wave[:int(s_rate * 0.02)]  # Mostrar solo los primeros 20ms
    notaF=NOTASR.get(freq)
    plt.plot(timeD, waveD)
    plt.title("Onda Sinusoidal de la nota "+notaF)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.show()
    
    
    
DURACION=1
stop=False
ventana=tk.Tk()
ventana.title("Piano en python")
ventana.protocol("WM_DELETE_WINDOW",onClose)
ventana.resizable(False,False)
ventana.configure(background="PeachPuff2")
currentNote=""
currAmp=""
currFreq=""
currSFreq=""

teclas=dict()
#Se agregan los botones
for i,(nota, freq) in enumerate(NOTASM.items()):
    boton=tk.Button(ventana,text=nota,command=lambda f=freq: playNote(f,DURACION),
                    width=5,height=15,bg="khaki",anchor="s")
    boton.grid(row=0,column=i,padx=5)
    teclas[nota]=boton
    
frame_editBut=tk.Frame(ventana,bg="PeachPuff3")
frame_editBut.grid(row=0,column=len(NOTASM),padx=10)
    
label_amplitud=tk.Label(frame_editBut,text="Establezca los parametros")
label_amplitud.grid(row=0,column=0,columnspan=2,padx=5,pady=10)

label_amplitud=tk.Label(frame_editBut,text="Amplitud")
label_amplitud.grid(row=1,column=0,padx=5,pady=10)
amp_slider=tk.Scale(frame_editBut,from_=0,to=5,orient="horizontal",resolution=0.01)
amp_slider.set(1)
amp_slider.grid(row=2,column=0)

label_sample_rate = tk.Label(frame_editBut, text="Frecuencia de Muestreo (Hz):")
label_sample_rate.grid(row=1, column=1, padx=5, pady=10)

# Crear un control deslizante para la frecuencia de muestreo
sample_rate_slider = tk.Scale(frame_editBut, from_=22050, to=96000, orient="horizontal", resolution=1000)
sample_rate_slider.set(44100)  # Valor inicial
sample_rate_slider.grid(row=2, column=1, padx=5, pady=10)

btn_aplicar = tk.Button(frame_editBut, text="Aplicar Ajustes", command=setAdjValues)
btn_aplicar.grid(row=3, column=0,columnspan=2, padx=5, pady=10)


player_frame=tk.Frame(ventana,bg="PeachPuff3")
player_frame.grid(row=1,column=0,columnspan=8,pady=10)
label_player=tk.Label(player_frame,text="Reproductor de canciones")
label_player.grid(row=0,column=0,padx=5,pady=10,columnspan=8)

lista_canciones = tk.StringVar()
lista_canciones.set("Estrellita")
menu_canciones = tk.OptionMenu(player_frame, lista_canciones,"Estrellita", "Happy Birthday", "Jingle Bell")
menu_canciones.grid(row=1,column=0,padx=5)

# Botón para reproducir la canción
btn_reproducir = tk.Button(player_frame, text="Reproducir Canción", command=play)
btn_reproducir.grid(row=1,column=1,padx=5)

btn_stop=tk.Button(player_frame,text="Parar Cancion",command=stopSong)
btn_stop.grid(row=1,column=2,padx=5)

info_frame=tk.Frame(ventana,bg="PeachPuff3")
info_frame.grid(row=1,column=8)
info_frame.grid_anchor("n")

label_nota=tk.Label(info_frame,text="Nota escuchada")
label_nota.grid(row=0,column=0,padx=5,pady=5)

label_amp=tk.Label(info_frame,text="Amplitud")
label_amp.grid(row=0,column=1,padx=5,pady=5)

label_freq=tk.Label(info_frame,text="Frecuencia de nota")
label_freq.grid(row=0,column=2,padx=5,pady=5)

label_s_rate=tk.Label(info_frame,text="Frecuencia de muestreo")
label_s_rate.grid(row=0,column=3,padx=5,pady=5)


lab_curr_note=tk.Label(info_frame,text=str(currentNote))
lab_curr_note.grid(row=1,column=0,padx=5,pady=5)

label_curr_AMP=tk.Label(info_frame,text=str(currAmp))
label_curr_AMP.grid(row=1,column=1,padx=5,pady=5)
label_curr_AMP["text"]=str(AMPLITUD)

label_curr_freq=tk.Label(info_frame,text=str(currFreq))
label_curr_freq.grid(row=1,column=2,padx=5,pady=5)


label_curr_s_rate=tk.Label(info_frame,text=str(currSFreq))
label_curr_s_rate.grid(row=1,column=3,padx=5,pady=5)
label_curr_s_rate['text']=str(s_rate)


ventana.mainloop()


