import random

# Función de prueba de primalidad (método de Miller-Rabin)
def is_prime(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    # Realizar el test de Miller-Rabin
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Función para generar números primos grandes (p y q) usando el test de Miller-Rabin
def generate_large_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if is_prime(prime_candidate):
            return prime_candidate