import tkinter as tk
from tkinter import HORIZONTAL, Scale, filedialog, Text
import os
from os import listdir
import numpy
import pickle
import pygame
import random as r
from tkinter import font

#like html this is the body
root = tk.Tk()

genre = 'NA'
genre_dict = {
    0: ["Psytrance","psytrance"],
    1: ["Hip Hop", "hiphop"],
    2: ["Trap", "trap"],
    3: ["Hardstyle", "hardstyle"],
    4: ["RnB", "rnb"],
    5: ["Synthwave", "synth"],
    6: ["Pop", "pop"]
}

#button array so we can turn them on and off
btn_arr = []

#https://www.online-convert.com/result#j=c591cb40-c5ff-4df3-8b38-e585cab2ff0f
def play(drum, melody, rhythm, genre):
    #disable button
    toggle_button(btn_arr[0])
    
    genre_dir = '../sounds/'+genre+'/'
    all_sounds = listdir(genre_dir) #replace synth with the selected genre
    
    pygame.mixer.init()
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    channel3 = pygame.mixer.Channel(2)
    
    sound1 = pygame.mixer.Sound(genre_dir + all_sounds[melody])
    sound2 = pygame.mixer.Sound(genre_dir + all_sounds[rhythm])
    sound3 = pygame.mixer.Sound(genre_dir + all_sounds[drum])
    
    channel1.play(sound1, -1)
    channel2.play(sound2, -1)
    channel3.play(sound3, -1)
    
def silence():
    pygame.quit()
    if(len(btn_arr) > 0):
        toggle_button(btn_arr[0])

def factor(val, pos):
    mins = {
        0: -2.353,
        1: -3.280,
        2: -2.774,
        3: -3.833,
        4: -1.410
        }
    maxs = {
        0: 5.488,
        1: 5.210,
        2: 4.528,
        3: 4.819,
        4: 4.251
        }
    
    min_val = mins[pos]/1.5
    max_val = maxs[pos]/1.5
    diff = max_val - min_val
    att = min_val + (diff * val)
    print(att)
    return att

def toggle_button(button):    
        if (button["state"] == "disabled"):
            button["state"] = "normal"
        else:
            button["state"] = "disabled"

def process():
    #stop music if it is currently playing
    silence()
    
    #toggle play button
    if(len(btn_arr) > 0):
        toggle_button(btn_arr[0])
    
    pickle_model = pickle.load(open("../models/kmeans.pkl", 'rb'))
    
    #grab slider values and apply to scale
    acousticness = acoust.get()/100
    valence = val.get()/100
    instrumentalness = inst.get()/100
    speechiness = speech.get()/100
    liveness = live.get()/100
    
    acoust_factor = factor(acousticness, 3)
    val_factor = factor(valence, 1)
    inst_factor = factor(instrumentalness, 2)
    speech_factor = factor(speechiness, 0)
    live_factor = factor(liveness, 4)
    x = [[acoust_factor, val_factor, inst_factor,  speech_factor, live_factor]]
    
    #model predictions
    y_pred = pickle_model.predict(x)
    genre = genre_dict[y_pred[0]][0]
    
    #change genre label
    genre_name.config(text=genre)
    genre_name.grid(column=2, row=2)
    
    
    drum = r.randint(0,2)
    melody=r.randint(3,5)
    rhythm=r.randint(6,8)
    
    #add play button
    playBtn = tk.Button(root, text="Play", padx=10, pady=5, bg='#263A51', fg='white', font='Raleway', 
                        command= lambda: play(drum, melody, rhythm, genre_dict[y_pred[0]][1])) #we can pass the genre too
    playBtn.grid(column=2, row=3, padx = 8, sticky='W')
    
    #add stop button
    stopBtn = tk.Button(root, text="Stop", padx=10, pady=5, bg='#8F1522', fg='white', font='Raleway', 
                        command=silence)
    stopBtn.grid(column=2, row=3, padx = 8, sticky='E')
    
    #add buttons to button array
    btn_arr.append(playBtn)
    btn_arr.append(stopBtn)
    

canvas = tk.Canvas(root, height=400, width=700)
canvas.grid(columnspan=3, rowspan=5)

#slider labels
acoust_label = tk.Label(root, text="Acousticness", font='Raleway').grid(column=0, row=0, padx=4, pady=4)
val_label = tk.Label(root, text="Valence", font='Raleway').grid(column=0, row=1, padx=4, pady=4)
inst_label = tk.Label(root, text="Instrumentalness", font='Raleway').grid(column=0, row=2, padx=4, pady=4)
speech_label = tk.Label(root, text="Speechiness", font='Raleway').grid(column=0, row=3, padx=4, pady=4)
live_label = tk.Label(root, text="Liveness", font='Raleway').grid(column=0, row=4, padx=4, pady=4)

#sliders
acoust = tk.Scale(root, from_=0, to=100, length = 300,orient=HORIZONTAL, font="Raleway")
acoust.grid(column=1, row=0)
val = tk.Scale(root, from_=0, to=100, length = 300, orient=HORIZONTAL, font="Raleway")
val.grid(column=1, row=1)
inst = tk.Scale(root, from_=0, to=100, length = 300,orient=HORIZONTAL, font="Raleway")
inst.grid(column=1, row=2)
speech = tk.Scale(root, from_=0, to=100, length = 300,orient=HORIZONTAL, font="Raleway")
speech.grid(column=1, row=3)
live = tk.Scale(root, from_=0, to=100, length = 300, orient=HORIZONTAL, font="Raleway")
live.grid(column=1, row=4)

#process button
processBtn = tk.Button(root, text="Process", padx=10, pady=5, fg="white", bg="#263A51", command=process, font="Raleway")
processBtn.grid(column=2, row=0)

#clear button
clearBtn = tk.Button(root, text="Clear", padx=10, pady=5, fg="white", bg="#263A51", font="Raleway")
clearBtn.grid(column=2, row=1)

#genre textbox
genre_name = tk.Label(root, text = "Default", fg="Black", font=("Raleway", 20))

#stop music if the window closes
def on_close():
    silence()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
