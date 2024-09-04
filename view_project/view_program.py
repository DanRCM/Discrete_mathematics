import time
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import random as rd
from PIL import ImageTk, Image, ImageSequence
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
GRAY_COLOR = "#999999"
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

def show_rsa_steps():
    steps = [
        "Generando claves públicas y privadas...\n"
        "Generando números primos p y q...",
        "Calculando n = p * q...",
        "Calculando φ(n) = (p-1) * (q-1)...",
        "Seleccionando e tal que 1 < e < φ(n) y gcd(e, φ(n)) = 1...",
        "Calculando d tal que d ≡ e^(-1) (mod φ(n))...",
        "Claves generadas: (e, n) y (d, n)..."
        "\nA continuación su mensaje encriptado:\n"
    ]
    for step in steps:
        terminal_text.config(text=terminal_text.cget("text") + step + "\n")
        terminalFrame.update()
        time.sleep(1)  # Adjust the delay as needed

def show_decryption_steps():
    steps = [
        "Leyendo el mensaje cifrado...",
        "Desencriptando el mensaje con la clave privada...",
        "Mensaje desencriptado con éxito."
    ]
    for step in steps:
        terminal_text.config(text=terminal_text.cget("text") + step + "\n")
        terminalFrame.update()
        time.sleep(1)  # Adjust the delay as needed

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
    show_rsa_steps()
    processed_message = encrypt(message, public_key)
    terminal_text.config(text=terminal_text.cget("text") + "Mensaje encriptado:\n" + str(processed_message) + "\n")
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
        show_decryption_steps()  # Show decryption steps
        processed_message = decrypt(ciphertext, private_key)
        terminal_text.config(text=terminal_text.cget("text") + "Mensaje desencriptado:\n" + processed_message + "\n")
    except ValueError:
        messagebox.showerror("Error", "Mensaje cifrado inválido.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al desencriptar: {str(e)}")

def on_select(*args):
    if default.get() == "Encrypted Message ":
        on_encrypt()
    else:
        on_decrypt()

def button_clicked(*args):
    terminal_text.config(text="")  # Clear terminal text before each operation
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

def select_folder_or_file(*args):
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
    else:
        entry_message.config(state=tk.DISABLED)
        entry_storage.config(state=tk.DISABLED)
        entry_message.delete(0, tk.END)
        entry_storage.delete(0, tk.END)

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

def make_option_menu(parent, value, *values, font, bg_color_1, bg_color_2, fg_color_1):
    global default
    default = tk.StringVar(parent)
    default.set(value)
    option_menu = tk.OptionMenu(parent, default, value, *values, command=update_ui)
    option_menu.config(bg=bg_color_2, fg=fg_color_1, font=font, highlightthickness=0, activebackground=bg_color_1, activeforeground=fg_color_1, cursor="hand2", relief="flat")
    option_menu['menu'].config(bg=bg_color_1, fg=fg_color_1, font=font, activebackground=bg_color_1, activeforeground=fg_color_1, cursor="hand2")
    option_menu.place(x=490 + 10.5, y=295 + 10)  # Moved 5 px up

# GUI Setup
window = tk.Tk()
window.title("Tkinter Designer")
window.geometry("882x539")  # Increased size by 20 pixels in width and height
window.configure(bg=WHITE_COLOR)
canvas = tk.Canvas(window, bg=WHITE_COLOR, height=539, width=882, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(451, 0, 451 + 431, 0 + 539, fill=WHITE_COLOR, outline="")

## Entry Menu Title
title1 = tk.Label(window, text="Enter your Message", bg=WHITE_COLOR, fg=BG_COLOR_2, font="Arial-BoldMT 22 bold")
title1.place(x=490, y=75)

## Entry Fields
def create_rounded_entry(parent, x, y, width, height, text_var, placeholder, font, bg_color, fg_color, border_color, has_option_menu = False, command=None):
    frame = tk.Frame(parent, bg=border_color, bd=0)
    frame.place(x=x, y=y, width=width, height=height)
    entry_frame = RoundedSquare(frame, width, height, 10, 0, WHITE_COLOR_2, WHITE_COLOR)
    entry_frame.place(x=0, y=0)
    entry_label = tk.Label(entry_frame, text=placeholder, bg=WHITE_COLOR_2, fg=BG_COLOR_1, font=font)
    entry_label.place(x=12.5, y=8)
    entry = tk.Entry(frame, textvariable=text_var, bd=0, bg=bg_color, fg=GRAY_COLOR, font="Arial 10", highlightthickness=0)
    entry.place(x=12.5, y=24.5, width=width-25, height=height-25)
    entry.insert(0, placeholder)

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=BG_COLOR_1)

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=GRAY_COLOR)

    if has_option_menu:
        make_option_menu(parent, "Encrypted Message ", "Decrypted Message ", font="Arial-BoldMT 10 bold", bg_color_1=WHITE_COLOR, bg_color_2=WHITE_COLOR_2, fg_color_1=BG_COLOR_1)
        entry.config(fg=BG_COLOR_1)
        entry.place(x=12.5, y=24.5, width=width-25-34, height=height-25)
    else:
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    return entry

message_var = tk.StringVar()
storage_var = tk.StringVar()
processed_var = tk.StringVar()

entry_message = create_rounded_entry(window, 490, 137.5, 321, 60, message_var, "Message", "Arial-BoldMT 10 bold", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)
entry_storage = create_rounded_entry(window, 490, 137.5 + 81, 321, 60, storage_var, "File name", "Arial-BoldMT 10 bold", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR)
entry_processed = create_rounded_entry(window, 490, 137.5 + 81*2, 321, 60, processed_var, "", "Arial-BoldMT 10 bold", WHITE_COLOR_2, BG_COLOR_1, ORANGE_COLOR, True, select_folder_or_file)

entry_message.focus()

# Folder/File Selection
folder_label = tk.Label(window, text="No folder selected", bg=WHITE_COLOR, fg=BG_COLOR_1, font="Arial 10")
folder_label.place(x=490, y=299 + 70)

original_image = Image.open(ASSETS_PATH / "path_picker_2.png")
resized_image = original_image.resize((30, 30), Image.LANCZOS)
path_picker_img = ImageTk.PhotoImage(resized_image)
path_picker_button = tk.Button(image=path_picker_img, text = '', compound = 'center', bg = WHITE_COLOR_2, borderwidth = 0)
path_picker_button.config(highlightthickness = 0, command = select_folder_or_file, relief = 'flat', cursor = 'hand2')
path_picker_button.place(x=765, y=238 + 75)

# Encrypt/Decrypt Button
encrypt_button_frame = tk.Frame(window, height=50, width=120)
encrypt_button_frame.place(x=451 + 215.5 - 60 - 20, y=410)  # Align with Documentation button
encrypt_button = RoundedButton(encrypt_button_frame, 120, 50, 20, 2, ORANGE_COLOR, WHITE_COLOR, command=button_clicked)
encrypt_button.place(x=0, y=0)
encrypt_button_label = tk.Label(encrypt_button_frame, text='D/E', bg=ORANGE_COLOR, fg='white', font='Arial 10 bold')
encrypt_button_label.place(x=40, y=15)
encrypt_button_label.bind("<Button-1>", button_clicked)

# Terminal Frame
terminalFrame = RoundedSquare(canvas, 431 + 50, 539, 50, 0, BG_COLOR_2, WHITE_COLOR)
terminalFrame.place(x=-50, y=0)
terminal_text = tk.Label(canvas, text="", bg=BG_COLOR_2, fg=WHITE_COLOR, font=("DejaVu Sans Mono", int(8.0)), justify=tk.LEFT, anchor="nw")
terminal_text.place(x=50, y=170, width=451 - 100, height=539 - 200)

# Titles
title1 = tk.Label(canvas, text="RSA", bg=BG_COLOR_2, fg=WHITE_COLOR, font="Arial-BoldMT 30 bold")
title1.place(x=50, y=60)
title2 = tk.Label(canvas, text="Encryption/Decryption", bg=BG_COLOR_2, fg=WHITE_COLOR, font="Arial-BoldMT 20 bold")
title2.place(x=50, y=100)

## Documentation Button
know_more = tk.Label(
    canvas,
    text="Click here to go to the documentation",
    bg=BG_COLOR_2, fg=BG_COLOR_3,justify="left",
    cursor="hand2"
)
know_more.place(x=20, y=500)
know_more.bind('<Button-1>', goto_documentation)

# Start the Tkinter main loop
window.mainloop()