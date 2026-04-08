import hashlib

def encriptar_password(password):
    return hashlib.sha256(password.encode()).hexdigest()