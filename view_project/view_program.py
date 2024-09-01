import time
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import random as rd
from PIL import ImageTk, Image
from project_algorithm_RSA.key_generation import public_key, private_key
from project_algorithm_RSA.decrypt import decrypt
from project_algorithm_RSA.encrypt import encrypt

# Constants
ASSETS_PATH = Path(__file__).resolve().parent / "assets"
BG_COLOR_1 = "#0B0B0C"
BG_COLOR_2 = "#0F1014"
BG_COLOR_3 = "#646464"
WHITE_COLOR = "#eeeff1"
WHITE_COLOR_2 = "#FCFDFF"
ORANGE_COLOR = "#f68b00"

# Global Variables
processed_message = ""
index = 0
current_text = ""
our_text = []

# Utility Functions
def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs): return True
        time.sleep(period)
    return False

def start_animation():
    global index, entry_processed
    entry_processed.delete(0, tk.END)
    if not index + 1 > len(our_text):
        if not terminal_text.cget("text") == "" and index == 0:
            terminal_text.config(text="")
        current_text = terminal_text.cget("text")
        terminal_text.config(text=current_text + our_text[index])
        index += 1
        num = rd.randint(500, 2000)
        terminalFrame.after(num, start_animation)
    else:
        entry_processed.insert(0, processed_message)
        index = 0

def on_encrypt(*args):
    global processed_message, our_text
    terminalFrame.after(1000, start_animation)
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Advertencia", "Por favor ingrese un mensaje.")
        return
    processed_message = encrypt(message, public_key)
    our_text = ["A continuación su mensaje encriptado: --------------------\n", "--------------------\n", " _____\n"]

def on_decrypt(*args):
    global processed_message, our_text
    terminalFrame.after(1000, start_animation)
    try:
        ciphertext = int(entry_message.get())
        processed_message = decrypt(ciphertext, private_key)
        our_text = ["A continuación su mensaje desencriptado: --------------------\n", "--------------------\n", " _____\n"]
    except ValueError:
        messagebox.showerror("Error", "Mensaje cifrado inválido.")

def on_select(*args):
    if default.get() == "Encrypted Message ":
        on_encrypt()
    else:
        on_decrypt()

def button_clicked():
    on_select()
    start_animation()

def goto_documentation(*args):
    webbrowser.open('https://docs.google.com/document/d/1GxvPILn68NUJFLwhEI8Qod8sgEZbURSJuQ-JDiqcsSg/edit?usp=sharing', new=0, autoraise=True)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None):
        super().__init__(parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg)
        self.command = command
        if cornerradius > 0.5 * width or cornerradius > 0.5 * height:
            raise ValueError("cornerradius is greater than width or height.")
        rad = 2 * cornerradius
        self.create_polygon((padding, height - cornerradius - padding, padding, cornerradius + padding, padding + cornerradius, padding, width - padding - cornerradius, padding, width - padding, cornerradius + padding, width - padding, height - cornerradius - padding, width - padding - cornerradius, height - padding, padding + cornerradius, height - padding), fill=color, outline=color)
        self.create_arc((padding, padding + rad, padding + rad, padding), start=90, extent=90, fill=color, outline=color)
        self.create_arc((width - padding - rad, padding, width - padding, padding + rad), start=0, extent=90, fill=color, outline=color)
        self.create_arc((width - padding, height - rad - padding, width - padding - rad, height - padding), start=270, extent=90, fill=color, outline=color)
        self.create_arc((padding, height - padding - rad, padding + rad, height - padding), start=180, extent=90, fill=color, outline=color)
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
        super().__init__(parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg)
        if cornerradius > 0.5 * width or cornerradius > 0.5 * height:
            raise ValueError("cornerradius is greater than width or height.")
        rad = 2 * cornerradius
        self.create_polygon((padding, height - cornerradius - padding, padding, cornerradius + padding, padding + cornerradius, padding, width - padding - cornerradius, padding, width - padding, cornerradius + padding, width - padding, height - cornerradius - padding, width - padding - cornerradius, height - padding, padding + cornerradius, height - padding), fill=color, outline=color)
        self.create_arc((padding, padding + rad, padding + rad, padding), start=90, extent=90, fill=color, outline=color)
        self.create_arc((width - padding - rad, padding, width - padding, padding + rad), start=0, extent=90, fill=color, outline=color)
        self.create_arc((width - padding, height - rad - padding, width - padding - rad, height - padding), start=270, extent=90, fill=color, outline=color)
        self.create_arc((padding, height - padding - rad, padding + rad, height - padding), start=180, extent=90, fill=color, outline=color)
        self.configure(width=width, height=height)

def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)
    f.place(x=x, y=y)
    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)
    return label

# GUI Setup
window = tk.Tk()
window.title("Tkinter Designer")
window.geometry("862x519")
window.configure(bg=WHITE_COLOR)
canvas = tk.Canvas(window, bg=BG_COLOR_2, height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill=WHITE_COLOR, outline="")

# Entry Fields
def create_rounded_entry(parent, x, y, width, height, text_var, placeholder, font, bg_color, fg_color, border_color):
    frame = tk.Frame(parent, bg=border_color, bd=0)
    frame.place(x=x, y=y, width=width, height=height)
    entry = tk.Entry(frame, textvariable=text_var, bd=0, bg=bg_color, fg=fg_color, font=font, highlightthickness=0)
    entry.place(x=2, y=2, width=width-4, height=height-4)
    entry.insert(0, placeholder)
    return entry

message_var = tk.StringVar()
storage_var = tk.StringVar()
processed_var = tk.StringVar()

entry_message = create_rounded_entry(window, 490, 137 + 25, 321, 35, message_var, "Message", "Arial 10", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)
entry_storage = create_rounded_entry(window, 490, 218 + 25, 321, 35, storage_var, "Storage document", "Arial 10", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)
entry_processed = create_rounded_entry(window, 490, 299 + 25, 321, 35, processed_var, "", "Arial 10", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)

entry_message.focus()

# Labels
message_text_id = tk.Label(window, text="Message", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial-BoldMT 10 bold")
storage_text_id = tk.Label(window, text="Storage document", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial-BoldMT 10 bold")
message_text_id.place(x=490, y=137)
storage_text_id.place(x=490, y=218)

# Button with Image
storage_button_img = Image.open(ASSETS_PATH / "path_picker.png")
storage_button_img = storage_button_img.resize((30, 30), Image.LANCZOS)
storage_button_img = ImageTk.PhotoImage(storage_button_img)

storage_button = tk.Button(window, image=storage_button_img, bd=0, bg=WHITE_COLOR, activebackground=WHITE_COLOR, command=lambda: print("Storage button clicked"))
storage_button.place(x=820, y=218 + 25)

# Dropdown Menu
listOptions = ["Encrypted Message ", "Decrypted Message"]
default = tk.StringVar()
default.set(listOptions[0])
caret_down_img = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "arrow_down.png"))

typeSelector = tk.OptionMenu(window, default, *listOptions)
typeSelector.place(x=490, y=300.5)
typeSelector.config(bg=WHITE_COLOR_2, fg=BG_COLOR_3, font="Arial-BoldMT 10 bold", highlightthickness=0, activeforeground=BG_COLOR_1, activebackground=WHITE_COLOR_2, cursor="hand2", relief="flat", indicatoron=False)
typeSelector["menu"].config(bg=WHITE_COLOR_2, fg=BG_COLOR_3, font="Arial-BoldMT 10", activeforeground=BG_COLOR_1, activebackground=WHITE_COLOR, cursor="hand2", relief="flat", borderwidth=0, border=0)
caret_down_label = tk.Label(typeSelector, bg="#F6F7F9", fg="#515486", font="Arial-BoldMT 10 bold", image=caret_down_img)
caret_down_label.place(relx=1.87, rely=0.35)

# Title
canvas.create_text(623.5, 88.0, text="Enter your message.", fill=BG_COLOR_2, font="Arial-BoldMT 22 bold")

# Process Button
first_button_frame = tk.Frame(window, height=50, width=120)
first_button_frame.place(x=431 + 215.5 - 60, y=401)
process_btn = RoundedButton(first_button_frame, 120, 50, 20, 2, ORANGE_COLOR, WHITE_COLOR, command=button_clicked)
process_btn.place(x=0, y=0)
encrypt_button_label = tk.Label(first_button_frame, text='Process', bg=ORANGE_COLOR, fg='white', font='Arial 10 bold')
encrypt_button_label.place(x=35, y=15)
encrypt_button_label.bind('<Button-1>', on_encrypt)

# Terminal Frame
terminalFrame = RoundedSquare(canvas, 431 + 50, 519, 50, 0, BG_COLOR_2, WHITE_COLOR)
terminalFrame.place(x=-50, y=0)
title1 = tk.Label(canvas, text="RSA", bg=BG_COLOR_2, fg="white", justify="left", font="Poppins 50 bold")
title1.place(x=40.0 + 16, y=45.0)
title2 = tk.Label(canvas, text="ALGORITHM", bg=BG_COLOR_2, fg="white", justify="left", font="Poppins 20 bold")
title2.place(x=185.0 + 16, y=82.0)

terminal_text = tk.Label(window, text='', bg=BG_COLOR_2, fg="white", font=("DejaVu Sans Mono", int(8.0)), justify="left", wraplength=380, anchor=tk.NW, width=50, height=23)
terminal_text.place(x=33, y=160)

# Documentation Link
know_more = tk.Label(canvas, text="Haz click aquí para ver la documentación.", bg=BG_COLOR_2, fg=BG_COLOR_3, justify="left", cursor="hand2")
know_more.place(x=20, y=480)
know_more.bind('<Button-1>', goto_documentation)

window.resizable(False, False)
window.mainloop()