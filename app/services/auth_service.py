from app.models.usuario import Usuario
from app.utils.security import encriptar_password
from datetime import datetime


class AuthService:
    def __init__(self):
        self.usuarios = []

    def registrar_usuario(self, nombre, correo, password, rol="usuario"):
        password_hash = encriptar_password(password)
        usuario = Usuario(nombre, correo, password_hash, rol)
        self.usuarios.append(usuario)

    # 🔥 AQUÍ VA TU MÉTODO
    def listar_usuarios(self):
        return self.usuarios

    def registrar_log(self, correo, resultado):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.now()} - {correo} - {resultado}\n")

    def login(self, correo, password):
        password_hash = encriptar_password(password)

        for usuario in self.usuarios:
            if usuario.correo == correo and usuario.password == password_hash:
                self.registrar_log(correo, "ACCESO EXITOSO")
                return usuario

        self.registrar_log(correo, "ACCESO FALLIDO")
        return None
