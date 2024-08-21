## pip install waiting
## pip install pillow
## pip install tkinter

from tkinter import messagebox

from waiting import wait

import PIL.Image
from PIL import ImageTk, Image
import tkinter.ttk as ttk
import tkinter as tk
import random as rd

import sv_ttk
import customtkinter as ctk

#from flet import *

from project_algorithm_RSA.key_generation import public_key, private_key
from project_algorithm_RSA.decrypt import decrypt
from project_algorithm_RSA.encrypt import encrypt

# view_program.py

import time
import webbrowser
import re
import sys
import os
import tkinter as tk
import tkinter.messagebox as tk1
import tkinter.filedialog
from pathlib import Path

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Funciones para la interfaz gráfica

isFinished = False

import threading
import queue

import threading
import tkinter as tk
from tkinter import messagebox
import random as rd

import threading
import tkinter as tk
from tkinter import messagebox
import random as rd


bg_color_1 = "#0B0B0C"
bg_color_2 = "#0F1014"
white_color = "#F6F7F9"

processed_message = ""


def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs): return True
        time.sleep(period)
    return False

def on_encrypt(*args):
    global processed_message
    terminalFrame.after(1000, start_animation)
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Advertencia", "Por favor ingrese un mensaje.")
        return
    processed_message = encrypt(message, public_key)


def on_decrypt(*args):
    global processed_message
    terminalFrame.after(1000, start_animation)
    try:
        ciphertext = int(entry_message.get())
        processed_message = decrypt(ciphertext, private_key)
    except ValueError:
        messagebox.showerror("Error", "Mensaje cifrado inválido.")

#move method
index = 0
current_text = ""
#entry = None
def start_animation():
    global index
    global entry
    entry.delete(0, tk.END)
    if not index + 1 > len(our_text):
        if not terminal_text.cget("text") == "" and index == 0:
            terminal_text.config(text="")
            print("text in terminal_text is equal to empty")
        current_text = terminal_text.cget("text")
        terminal_text.config(text=current_text + our_text[index])
        index += 1
        num = rd.randint(500, 2000)
        terminalFrame.after(num, start_animation)
    elif index + 1 > len(our_text):
        entry.insert(0, processed_message)
        print(processed_message, ", ")
        print(entry.get())
        print("Button clicked 2")
        index = 0
        return
    # else:
    #     index = 0
    #     return
    # isFinished = True

def on_select(*args):
    if entry_message.get():
        if default.get() == "Encrypted Message ":
            on_encrypt()
        else:
            on_decrypt()

def button_clicked():
    on_select()
    start_animation()
    print("Button clicked1")

# def hex_to_RGB(hex_str):
#     """ #FFFFFF -> [255,255,255]"""
#     #Pass 16 to the integer function for change of base
#     return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

# def get_color_gradient(c1, c2, n):
#     """
#     Given two hex colors, returns a color gradient
#     with n colors.
#     """
#     assert n > 1
#     c1_rgb = np.array(hex_to_RGB(c1))/255
#     c2_rgb = np.array(hex_to_RGB(c2))/255
#     mix_pcts = [x/(n-1) for x in range(n)]
#     rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
#     return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]




def goto_documentation(*args):
    webbrowser.open('https://docs.google.com/document/d/1GxvPILn68NUJFLwhEI8Qod8sgEZbURSJuQ-JDiqcsSg/edit?usp=sharing', new=0, autoraise=True)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, bg=bg)
        self.command = command

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)


        id = shape()
        (x0,y0,x1,y1) = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()


class RoundedSquare(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg):
        tk.Canvas.__init__(self, parent, borderwidth=0,
                           relief="flat", highlightthickness=0, bg=bg)

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)


        id = shape()
        (x0,y0,x1,y1) = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)


ASSETS_PATH = Path(__file__).resolve().parent / "assets"
output_path = ""


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


window = tk.Tk()
logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
#window.call('wm', 'iconphoto', window._w, logo)
window.title("Tkinter Designer")

window.geometry("862x519")
window.configure(bg=bg_color_2)

canvas = tk.Canvas(
    window, bg=bg_color_2, height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill=bg_color_1, outline="")

title = tk.Label(canvas,
    text="Algoritmo de Cifrado RSA", bg=bg_color_2,
    fg="white",justify="left", font="Poppins 22 bold")
#title.place(x=20.0, y=90.0)
title.place(x=20.0, y=45.0)
#canvas.create_rectangle(25, 160, 33 + 60, 160 + 5, fill="#FCFCFC", outline="")
canvas.create_rectangle(25, 115, 33 + 60, 115 + 5, fill="#FCFCFC", outline="")

know_more = tk.Label(
    canvas,
    text="Haz click aquí para ver la documentación.",
    bg="#202220", fg="white",justify="left", cursor="hand2")
#know_more.place(x=20, y=430)
know_more.place(x=20, y=480)
know_more.bind('<Button-1>', goto_documentation)





text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
#token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
#URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
#filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)

token_entry_img = RoundedSquare(canvas, 345, 60, 10, 0, bg_color_2, bg_color_1)
URL_entry_img = RoundedSquare(canvas, 345, 60, 10, 0, bg_color_2, bg_color_1)
filePath_entry_img = RoundedSquare(canvas, 345, 60, 10, 0, bg_color_2, bg_color_1)

token_entry_img.place(x=477.5, y=137.5)
URL_entry_img.place(x=477.5, y=137.5+81)
filePath_entry_img.place(x=477.5, y=137.5+81*2)

entry_message = tk.Entry(bd=0, bg=bg_color_2,fg=white_color,  highlightthickness=0)
entry_message.place(x=490.0, y=137+25, width=321.0, height=35)
entry_message.focus()

entry_label = tk.Entry(bd=0, bg=bg_color_2, fg=white_color,  highlightthickness=0)
entry_label.place(x=490.0, y=218+25, width=321.0, height=35)


path_picker_img = tk.PhotoImage(file=ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    image = path_picker_img,
    text = '',
    compound = 'center',
    fg = 'white',
    borderwidth = 0,
    highlightthickness = 0,
    #command = select_path,
    relief = 'flat')

path_picker_button.place(
    #x = 783, y = 319,
    x = 783, y = 238,
    width = 24,
    height = 22
)

#message_text_id = canvas.create_text(
#    500.0, 156.0, text="Message ", fill="white",
#    font="Arial-BoldMT 10 bold", anchor="w")
#label_text_id = canvas.create_text(
#    500.0, 234.5, text="Label", fill="#515486",
#    font="Arial-BoldMT 10 bold", anchor="w")

message_text_id = tk.Label(window, text="Message", bg=bg_color_2, fg="white", font="Arial-BoldMT 10 bold")
label_text_id = tk.Label(window, text="Label", bg=bg_color_2, fg="white", font="Arial-BoldMT 10 bold")

message_text_id.place(x=490.0, y=145.0)
label_text_id.place(x=490.0, y=145.0 + 81)


listOptions = ["Encrypted Message ", "Decrypted Message"]
default = tk.StringVar()
default.set(listOptions[0])
caret_down_img = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "arrow_down.png"), size=(0, 0))

typeSelector = tk.OptionMenu(
    window, default, *listOptions)
typeSelector.place(x=490, y=300.5)
typeSelector.config(
    bg=bg_color_2,
    fg="#515486",
    font="Arial-BoldMT 10 bold",
    highlightthickness=0,
    activeforeground="#686bab",
    activebackground=bg_color_2,
    cursor="hand2",
    relief="flat",
    indicatoron=False,
#    image=caret_down_img,
#    compound=tk.RIGHT
)
typeSelector["menu"].config(
    bg="#F6F7F9",
    fg="#515486",
    font="Arial-BoldMT 10",
    activeforeground="#686bab",
    activebackground="#eeeff1",
    cursor="hand2",
    relief="flat",
    borderwidth=0,
    border=0
)
caret_down_label = tk.Label(
    typeSelector,
    bg="#F6F7F9",
    fg="#515486",
    font="Arial-BoldMT 10 bold",
    image=caret_down_img
)
caret_down_label.place(relx=0.87, rely=0.35)

#default.trace("r", on_select)
entry = tk.Entry(bd=0, bg=bg_color_2, fg=white_color,  highlightthickness=0)
entry.place(x=490.0, y=299 + 25, width=321.0, height=35)
#x=490.0, y=145.0 + 162

canvas.create_text(
    623.5, 88.0, text="Enter your message.",
    fill="#515486", font="Arial-BoldMT 22 bold")



#ENCRYPT BUTTON
first_button_frame = tk.Frame(window, height=50, width=120)
first_button_frame.place(x=507, y=401)

process_btn = RoundedButton(first_button_frame, 120, 50, 20, 2, "#f68b00", bg_color_1, command=button_clicked)
process_btn.place(x=0, y=0)
#create_gradient(process_btn, "#f68b00", "#bc48f6", 50)

encrypt_button_label = tk.Label(
    first_button_frame,
    text='Encrypt',
    bg='#3A7FF6', fg='white',
    font='Arial 10 bold')
encrypt_button_label.place(x=35, y=15)
encrypt_button_label.bind('<Button-1>', on_encrypt)



#DECRYPT BUTTON
#second_button_frame = tk.Frame(window, bg='red', height=50, width=120)
#second_button_frame.place(x=667, y=401)

#decrypt_btn = RoundedButton(second_button_frame, 120, 50, 20, 2, '#3A7FF6', 'white', command=on_decrypt)
#decrypt_btn.place(x=0, y=0)

#decrypt_button_label = tk.Label(
#    second_button_frame,
#    text='Decrypt',
#    bg='#3A7FF6', fg='white',
#    font='Arial 10 bold')
#decrypt_button_label.place(x=35, y=15)
#decrypt_button_label.bind('<Button-1>', on_decrypt)

terminalFrame = tk.Frame(window, height=340, width=400, bg=bg_color_2)#bg="#0c1c35")
terminalFrame.place(x=15, y=149)
our_text = [
    "Bienvenido a la encriptadora RSA.\n",
    "A continuación se muestra su texto encriptado:\n",
    entry.get(),
    "A continuación se muestra su texto desencriptado:\n",
    entry.get()
]
terminal_text = tk.Label(terminalFrame, text='', bg=bg_color_2, fg="white", font=("DejaVu Sans Mono", int(10.0)), justify="left", wraplength=380, anchor=tk.NW, width=50, height=20)
terminal_text.place(x=5, y=30)



window.resizable(False, False)