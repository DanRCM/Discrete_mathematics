import time
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import random as rd
from PIL import ImageTk, Image
from project_algorithm_RSA.key_generation import generate_and_save_keys, load_keys
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
selected_folder = ""
selected_file = ""
animation_index = 0

# Generate keys if not exist
if not Path('public_key.pem').exists() or not Path('private_key.pem').exists():
    public_key, private_key = generate_and_save_keys(bits=512)
else:
    public_key, private_key = load_keys()

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
        num = rd.randint(100, 300)  # Adjusted delay for smoother animation
        terminalFrame.after(num, start_animation)
    else:
        entry_processed.insert(0, processed_message)
        index = 0

def animate_dots():
    global animation_index
    dots = ["", ".", "..", "..."]
    terminal_text.config(text="Procesando su mensaje" + dots[animation_index])
    animation_index = (animation_index + 1) % len(dots)
    terminalFrame.after(500, animate_dots)  # Adjust the speed of the animation here

def on_encrypt(*args):
    global processed_message, our_text
    terminal_text.config(text="Iniciando proceso de encriptación...\n")
    terminalFrame.after(1000, start_animation)
    message = entry_message.get()
    filename = entry_storage.get()
    if not message:
        messagebox.showwarning("Advertencia", "Por favor ingrese un mensaje.")
        return
    if not filename:
        messagebox.showwarning("Advertencia", "Por favor ingrese un nombre de archivo.")
        return
    if not selected_folder:
        messagebox.showwarning("Advertencia", "Por favor seleccione una carpeta.")
        return
    terminal_text.config(text="Generando claves públicas y privadas...\n")
    processed_message = encrypt(message, public_key)
    terminal_text.config(text=terminal_text.cget("text") + "Mensaje encriptado:\n" + str(processed_message) + "\n")
    our_text = ["A continuación su mensaje encriptado:\n", "--------------------\n", " _____     \n", "\n", "\n", "\n"]
    save_to_file(processed_message, filename)
    terminal_text.config(text=terminal_text.cget("text") + "Mensaje guardado en archivo.\n")

def on_decrypt(*args):
    global processed_message, our_text
    terminal_text.config(text="Iniciando proceso de desencriptación...\n")
    terminalFrame.after(1000, start_animation)
    try:
        if not selected_file:
            messagebox.showwarning("Advertencia", "Por favor seleccione un archivo.")
            return
        with open(selected_file, 'r') as file:
            ciphertext = int(file.read())
        terminal_text.config(text=terminal_text.cget("text") + "Leyendo archivo encriptado...\n")
        processed_message = decrypt(ciphertext, private_key)
        terminal_text.config(text=terminal_text.cget("text") + "Mensaje desencriptado:\n" + processed_message + "\n")
        our_text = ["A continuación su mensaje desencriptado:\n", "--------------------\n", " _____     \n", "\n", "\n", "\n"]
        animate_dots()  # Start the dots animation
    except ValueError:
        messagebox.showerror("Error", "Mensaje cifrado inválido.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al desencriptar: {str(e)}")

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

def save_to_file(message, filename):
    file_path = Path(selected_folder) / f"{filename}.txt"
    with open(file_path, 'w') as file:
        file.write(str(message))

def load_from_file(filepath):
    with open(filepath, 'r') as file:
        return int(file.read())

def select_folder_or_file():
    global selected_folder, selected_file
    if default.get() == "Encrypted Message ":
        selected_folder = filedialog.askdirectory(title="Seleccionar carpeta")
        if selected_folder:
            folder_label.config(text=selected_folder)
    else:
        selected_file = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if selected_file:
            folder_label.config(text=selected_file)

def update_ui(*args):
    if default.get() == "Encrypted Message ":
        entry_message.config(state=tk.NORMAL)
        entry_storage.config(state=tk.NORMAL)
        entry_message.delete(0, tk.END)
        entry_storage.delete(0, tk.END)
        folder_button_label.config(text='Folder/File')
    else:
        entry_message.config(state=tk.DISABLED)
        entry_storage.config(state=tk.DISABLED)
        entry_message.delete(0, tk.END)
        entry_storage.delete(0, tk.END)
        folder_button_label.config(text='Folder/File')

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
window.geometry("882x539")  # Increased size by 20 pixels in width and height
window.configure(bg=WHITE_COLOR)
canvas = tk.Canvas(window, bg=BG_COLOR_2, height=539, width=882, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(451, 0, 451 + 431, 0 + 539, fill=WHITE_COLOR, outline="")

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
entry_storage = create_rounded_entry(window, 490, 218 + 25, 321, 35, storage_var, "File name", "Arial 10", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)
entry_processed = create_rounded_entry(window, 490, 299 + 30, 321, 35, processed_var, "", "Arial 10", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)

entry_message.focus()

# Labels
message_text_id = tk.Label(window, text="Message", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial-BoldMT 10 bold")
storage_text_id = tk.Label(window, text="File name", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial-BoldMT 10 bold")
message_text_id.place(x=490, y=137)
storage_text_id.place(x=490, y=218)

# Folder/File Selection
folder_label = tk.Label(window, text="No folder selected", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial 10")
folder_label.place(x=490, y=299 + 70)

folder_button_frame = tk.Frame(window, height=50, width=120)
folder_button_frame.place(x=490, y=299 + 100)  # Moved 20 px to the right
folder_button = RoundedButton(folder_button_frame, 120, 50, 20, 2, ORANGE_COLOR, WHITE_COLOR, command=select_folder_or_file)
folder_button.place(x=0, y=0)
folder_button_label = tk.Label(folder_button_frame, text='Folder/File', bg=ORANGE_COLOR, fg='white', font='Arial 10 bold')
folder_button_label.place(x=15, y=15)

# Dropdown Menu
default = tk.StringVar(window)
default.set("Encrypted Message ")
option_menu = tk.OptionMenu(window, default, "Encrypted Message ", "Decrypted Message ", command=update_ui)
option_menu.config(bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial 10", highlightthickness=2, highlightbackground=ORANGE_COLOR, activebackground=WHITE_COLOR, activeforeground=BG_COLOR_1)
option_menu['menu'].config(bg=WHITE_COLOR, fg=BG_COLOR_1)
option_menu.place(x=490, y=295)  # Moved 5 px up

# Encrypt/Decrypt Button
encrypt_button_frame = tk.Frame(window, height=50, width=120)
encrypt_button_frame.place(x=451 + 315.5 - 60 - 20, y=400)  # Align with Documentation button
encrypt_button = RoundedButton(encrypt_button_frame, 120, 50, 20, 2, ORANGE_COLOR, WHITE_COLOR, command=button_clicked)
encrypt_button.place(x=0, y=0)
encrypt_button_label = tk.Label(encrypt_button_frame, text='D/E', bg=ORANGE_COLOR, fg='white', font='Arial 10 bold')
encrypt_button_label.place(x=40, y=15)

# Terminal Frame
terminalFrame = tk.Frame(window, bg=BG_COLOR_2, height=539 - 200, width=451 - 100)
terminalFrame.place(x=50, y=100)
terminal_text = tk.Label(terminalFrame, text="", bg=BG_COLOR_2, fg=WHITE_COLOR, font="Arial 10 bold", justify=tk.LEFT, anchor="nw")
terminal_text.place(x=0, y=0, width=451 - 100, height=539 - 200)

# Titles
title1 = tk.Label(canvas, text="RSA", bg=BG_COLOR_2, fg=WHITE_COLOR, font="Arial-BoldMT 30 bold")
title1.place(x=50, y=20)
title2 = tk.Label(canvas, text="Encryption/Decryption", bg=BG_COLOR_2, fg=WHITE_COLOR, font="Arial-BoldMT 20 bold")
title2.place(x=50, y=60)

# Documentation Button
doc_button_frame = tk.Frame(window, height=50, width=120)
doc_button_frame.place(x=451 + 315.5 - 60 - 20, y=470)  # Moved 10 px down
doc_btn = RoundedButton(doc_button_frame, 120, 50, 20, 2, ORANGE_COLOR, WHITE_COLOR, command=goto_documentation)
doc_btn.place(x=0, y=0)
doc_button_label = tk.Label(doc_button_frame, text='Documentation', bg=ORANGE_COLOR, fg='white', font='Arial 10 bold')
doc_button_label.place(x=15, y=15)

# Main Loop
window.mainloop()