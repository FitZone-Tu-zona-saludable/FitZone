class Usuario:
    def __init__(self, nombre, correo, password, rol="usuario"):
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol