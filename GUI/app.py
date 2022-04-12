import tkinter as tk
from tkinter import HORIZONTAL, Scale, filedialog, Text
import os
from os import listdir
import numpy
import pickle
import pygame
import random as r
from tkinter import font
from tkinter import PhotoImage

#like html this is the body
root = tk.Tk()

root.title('M-LADMS - COMP4905 Honours Project')

#make bakgrounds transparent
root.wm_attributes('-transparentcolor', 'grey')


#project variables
primary_color = '#222831'
secondary_color = '#393E46'
slider_color = '#f0f4f9'
highlight_color = '#FFD369'
main_font = ("Century Gothic", 15, 'bold')

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

#slider array so we can reset their values
slider_arr = []

#function should toggle the disabled state of a given button if it is in btn_arr
def toggle_button(button):    
        if (button["state"] == "disabled"):
            button["state"] = "normal"
        else:
            button["state"] = "disabled"

#function is called when play button is pressed - play button should be disabled
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

#function silences the music and should re-enable the play button
def silence():
    pygame.quit()
    if(len(btn_arr) > 0):
        toggle_button(btn_arr[0])

#function calculates the values which are sent to the model
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
    return att

#function clears genre name, play/stop button, and slider selections
def clear():
    #stop music
    silence()
    
    #set sliders back to 0
    for i in range(len(slider_arr)):
        slider_arr[i].set(0)
        
    #remove play and stop buttons
    for i in range(len(btn_arr)):
        btn_arr[i].grid_forget()
    
    #remove genre title
    genre_name.grid_forget()
    
#function randomizes value for sliders
def random_selection():
    for i in range(len(slider_arr)):
        new_val = r.randint(0, 100)
        slider_arr[i].set(new_val)
    process()
    
#function grabs data from sliders and gets their relative values
#function then sends data to model for prediction
def process():
    #stop music if it is currently playing
    silence()
    
    #toggle play button
    if(len(btn_arr) > 0):
        toggle_button(btn_arr[0])
    
    #load model
    pickle_model = pickle.load(open("../models/kmeans.pkl", 'rb'))
    
    #grab slider values and apply to scale
    acousticness = acoust.get()/100
    valence = val.get()/100
    instrumentalness = inst.get()/100
    speechiness = speech.get()/100
    liveness = live.get()/100
    
    #get relative values for slider input
    speech_factor = factor(speechiness, 0)
    val_factor = factor(valence, 1)
    inst_factor = factor(instrumentalness, 2)
    acoust_factor = factor(acousticness, 3)
    live_factor = factor(liveness, 4)
    x = [[acoust_factor, val_factor, inst_factor,  speech_factor, live_factor]]
    
    #model predictions
    y_pred = pickle_model.predict(x)
    genre = genre_dict[y_pred[0]][0]
    
    #change genre label
    genre_name.config(text=genre)
    genre_name.grid(column=2, row=3)
    
    
    drum = r.randint(0,2)
    melody=r.randint(3,5)
    rhythm=r.randint(6,8)
    
    #add play button
    playBtn = tk.Button(root, image=play_btn_img, padx=2, pady=5, bd=0,bg=primary_color,activeforeground=secondary_color,
                        command= lambda: play(drum, melody, rhythm, genre_dict[y_pred[0]][1])) #we can pass the genre too
    playBtn.grid(column=2, row=4, padx=30, sticky='W')
    
    #add stop button
    stopBtn = tk.Button(root, image=stop_btn_img, padx=2, pady=5,bd=0,bg=primary_color,
                        command=silence)
    stopBtn.grid(column=2, row=4, padx=30, sticky='E')
    
    #add buttons to button array
    btn_arr.append(playBtn)
    btn_arr.append(stopBtn)
    

canvas = tk.Canvas(root, height=400, width=700, bg=primary_color, highlightthickness=0, bd=0)
canvas.grid(columnspan=3, rowspan=5)

#create images for stop and play buttons
play_btn_img = PhotoImage(file='./images/play.png')
stop_btn_img = PhotoImage(file='./images/stop.png')

#slider labels
#acoust_img = PhotoImage(file='./images/acoust_label.png')
acoust_label = tk.Label(root, text="Acousticness", font=main_font,fg="white", bg=primary_color).grid(column=0, row=0, padx=4, pady=4)
val_label = tk.Label(root, text="Valence", font=main_font, fg="white", bg=primary_color).grid(column=0, row=1, padx=4, pady=4)
inst_label = tk.Label(root, text="Instrumentalness", font=main_font,fg="white", bg=primary_color).grid(column=0, row=2, padx=4, pady=4)
speech_label = tk.Label(root, text="Speechiness", font=main_font,fg="white", bg=primary_color).grid(column=0, row=3, padx=4, pady=4)
live_label = tk.Label(root, text="Liveness", font=main_font, fg="white", bg=primary_color).grid(column=0, row=4, padx=4, pady=4)

#sliders
acoust = tk.Scale(root, from_=0, to=100, length = 250,orient=HORIZONTAL,font=main_font,fg="white", bg=primary_color, highlightthickness=0, sliderrelief='flat', bd=1, troughcolor=slider_color, activebackground=highlight_color)
acoust.grid(column=1, row=0)
val = tk.Scale(root, from_=0, to=100, length = 250, orient=HORIZONTAL, font=main_font,fg="white", bg=primary_color, highlightthickness=0, sliderrelief='flat', bd=1, troughcolor=slider_color, activebackground=highlight_color)
val.grid(column=1, row=1)
inst = tk.Scale(root, from_=0, to=100, length = 250,orient=HORIZONTAL, font=main_font,fg="white", bg=primary_color, highlightthickness=0, sliderrelief='flat', bd=1, troughcolor=slider_color, activebackground=highlight_color)
inst.grid(column=1, row=2)
speech = tk.Scale(root, from_=0, to=100, length = 250,orient=HORIZONTAL, font=main_font,fg="white", bg=primary_color, highlightthickness=0, sliderrelief='flat', bd=1, troughcolor=slider_color, activebackground=highlight_color)
speech.grid(column=1, row=3)
live = tk.Scale(root, from_=0, to=100, length = 250, orient=HORIZONTAL, font=main_font,fg="white", bg=primary_color, highlightthickness=0, sliderrelief='flat', bd=1, troughcolor=slider_color, activebackground=highlight_color)
live.grid(column=1, row=4)

slider_arr.append(acoust)
slider_arr.append(val)
slider_arr.append(inst)
slider_arr.append(speech)
slider_arr.append(live)


#process button
processBtn = tk.Button(root, text="Process", padx=10, pady=5, fg="white", bg=secondary_color, command=process, font=main_font, bd=0)
processBtn.grid(column=2, row=0)

#clear button
clearBtn = tk.Button(root, text="Clear", padx=10, pady=5, fg="white", bg=secondary_color, font=main_font, bd=0, command=clear)
clearBtn.grid(column=2, row=1)

#random button
randomBtn = tk.Button(root, text="Random", padx=10, pady=5, fg='white', bg=highlight_color, font=main_font, bd=0, command=random_selection)
randomBtn.grid(column=2, row=2)

#genre textbox
genre_name = tk.Label(root, text = "Default", bg=primary_color, fg='white',font=("Century Gothic", 20, 'bold'))

#stop music if the window closes
def on_close():
    silence()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)

root.resizable(False, False)
root.mainloop()
