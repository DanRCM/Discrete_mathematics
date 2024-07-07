from tkinter import messagebox
import tkinter as tk
from project_algorithm_RSA.key_generation import public_key, private_key
from project_algorithm_RSA.decrypt import decrypt
from project_algorithm_RSA.encrypt import encrypt

# view_program.py

# Funciones para la interfaz gráfica
def on_encrypt():
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Advertencia", "Por favor ingrese un mensaje.")
        return
    ciphertext = encrypt(message, public_key)
    entry_encrypted.delete(0, tk.END)
    entry_encrypted.insert(0, str(ciphertext))

def on_decrypt():
    try:
        ciphertext = int(entry_encrypted.get())
        decrypted_message = decrypt(ciphertext, private_key)
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decrypted_message)
    except ValueError:
        messagebox.showerror("Error", "Mensaje cifrado inválido.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cifrado RSA")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_message = tk.Label(frame, text="Mensaje:")
label_message.grid(row=0, column=0, sticky="e")
entry_message = tk.Entry(frame, width=50)
entry_message.grid(row=0, column=1, padx=5, pady=5)

button_encrypt = tk.Button(frame, text="Cifrar", command=on_encrypt)
button_encrypt.grid(row=0, column=2, padx=5, pady=5)

label_encrypted = tk.Label(frame, text="Mensaje cifrado:")
label_encrypted.grid(row=1, column=0, sticky="e")
entry_encrypted = tk.Entry(frame, width=50)
entry_encrypted.grid(row=1, column=1, padx=5, pady=5)

button_decrypt = tk.Button(frame, text="Desencriptar", command=on_decrypt)
button_decrypt.grid(row=1, column=2, padx=5, pady=5)

label_decrypted = tk.Label(frame, text="Mensaje desencriptado:")
label_decrypted.grid(row=2, column=0, sticky="e")
entry_decrypted = tk.Entry(frame, width=50)
entry_decrypted.grid(row=2, column=1, padx=5, pady=5)