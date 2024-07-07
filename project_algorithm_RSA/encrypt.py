
# Función para cifrar un mensaje
def encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), 'big')
    ciphertext = pow(message_int, e, n)
    return ciphertext