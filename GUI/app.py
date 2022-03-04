import tkinter as tk
from tkinter import HORIZONTAL, Scale, filedialog, Text
import os
import numpy
import pickle
import pygame
from tkinter import font

#like html this is the body
root = tk.Tk()

genre_dict = {
    0: "Trap",
    1: "Hip Hop",
    2: "Hardstyle",
    3: "Metal",
    4: "RnB",
    5: "Psytrance",
    6: "Pop"
}

#https://www.online-convert.com/result#j=c591cb40-c5ff-4df3-8b38-e585cab2ff0f
def play():
    pygame.mixer.init()
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)
    channel3 = pygame.mixer.Channel(2)
    
    sound1 = pygame.mixer.Sound('../sounds/ussr1.ogg')
    sound2 = pygame.mixer.Sound('../sounds/mud.ogg')
    sound3 = pygame.mixer.Sound('../sounds/deez.ogg')
    
    channel1.play(sound1, -1)
    channel2.play(sound2, -1)
    channel3.play(sound3, -1)
    
def silence():
    pygame.quit()

def process():
    pickle_model = pickle.load(open("../models/kmeans.pkl", 'rb'))
    print("model loaded...")
    tester = [[1.64223768, -0.09122065, -0.32480933,  1.79689,     0.64424335]]
    print("predicting...")
    y_pred = pickle_model.predict(tester)
    print("done: ", y_pred[0])
    
    genre = genre_dict[y_pred[0]]
    print("genre: ", genre)
    
    #add text box
    genre_name = tk.Label(root, text = genre, fg="Black", font=("Raleway", 20))
    genre_name.grid(column=1, row=2)
    
    #add play button
    playBtn = tk.Button(root, text="Play", padx=10, pady=5, bg='#263A51', fg='white', font='Raleway', command=play)
    playBtn.grid(column=1, row=3)
    
    #add stop button
    stopBtn = tk.Button(root, text="Stop", padx=10, pady=5, bg='#263A51', fg='white', font='Raleway', command=silence)
    stopBtn.grid(column=1, row=4)
    
    


canvas = tk.Canvas(root, height=400, width=700)
canvas.grid(columnspan=3, rowspan=5)

#sliders
acoust = tk.Scale(root, from_=0, to=100, length = 200,orient=HORIZONTAL, font="Raleway")
acoust.grid(column=0, row=0)
val = tk.Scale(root, from_=0, to=100, length = 200, orient=HORIZONTAL, font="Raleway")
val.grid(column=0, row=1)
inst = tk.Scale(root, from_=0, to=100, length = 200,orient=HORIZONTAL, font="Raleway")
inst.grid(column=0, row=2)
speech = tk.Scale(root, from_=0, to=100, length = 200,orient=HORIZONTAL, font="Raleway")
speech.grid(column=0, row=3)
live = tk.Scale(root, from_=0, to=100, length = 200, orient=HORIZONTAL, font="Raleway")
live.grid(column=0, row=4)

processBtn = tk.Button(root, text="Process", padx=10, pady=5, fg="white", bg="#263A51", command=process, font="Raleway")
processBtn.grid(column=1, row=0)
clearBtn = tk.Button(root, text="Clear", padx=10, pady=5, fg="white", bg="#8F1522", font="Raleway")
clearBtn.grid(column=1, row=1)

root.mainloop()
