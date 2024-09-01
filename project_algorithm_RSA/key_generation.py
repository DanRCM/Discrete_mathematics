from project_algorithm_RSA.math_logic import generate_large_prime
from sympy import mod_inverse
from pathlib import Path


# Generación de claves RSA
def generate_rsa_keys(bits=1024):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Elegir e
    e = 65537  # Valor comúnmente utilizado para e

    # Calcular d
    d = mod_inverse(e, phi)

    return (e, n), (d, n)


# Guardar claves en archivos
def save_keys(public_key, private_key):
    with open('public_key.pem', 'w') as pub_file:
        pub_file.write(str(public_key))
    with open('private_key.pem', 'w') as priv_file:
        priv_file.write(str(private_key))


# Cargar claves desde archivos
def load_keys():
    with open('public_key.pem', 'r') as pub_file:
        public_key = eval(pub_file.read())
    with open('private_key.pem', 'r') as priv_file:
        private_key = eval(priv_file.read())
    return public_key, private_key


# Generar y guardar claves si no existen
def generate_and_save_keys(bits=512):
    public_key, private_key = generate_rsa_keys(bits)
    save_keys(public_key, private_key)
    return public_key, private_key


# Verificar si las claves existen y cargarlas o generarlas
if not Path('public_key.pem').exists() or not Path('private_key.pem').exists():
    public_key, private_key = generate_and_save_keys(bits=512)
else:
    public_key, private_key = load_keys()