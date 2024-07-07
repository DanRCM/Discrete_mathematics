from project_algorithm_RSA.math_logic import generate_large_prime
from sympy import mod_inverse

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

# Definir claves
public_key, private_key = generate_rsa_keys(bits=512)
