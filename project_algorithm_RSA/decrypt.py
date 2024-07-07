
# Función para descifrar un mensaje
def decrypt(ciphertext, private_key):
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    message = message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode('utf-8', errors='replace')
    return message