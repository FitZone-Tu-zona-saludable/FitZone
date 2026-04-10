from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from app.models import usuario
from app.services.auth_service import AuthService


# Importar vistas según rol
from app.ui.admin_view import AdminView
from app.ui.usuario_view import UsuarioView
from app.ui.seguridad_view import SeguridadView


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.auth = AuthService()

        # 🔥 Usuarios de prueba
        self.auth.registrar_usuario("Romel", "romel@mail.com", "1234", "admin")
        self.auth.registrar_usuario("Cliente", "user@mail.com", "1234", "usuario")
        self.auth.registrar_usuario("Seguridad", "seg@mail.com", "1234", "seguridad")

        self.setWindowTitle("Login FitZone")

        # 📝 Inputs
        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)

        # 🔘 Botón
        self.boton = QPushButton("Iniciar sesión")
        self.boton.clicked.connect(self.login)

        # 📢 Mensaje
        self.label = QLabel("")

        # 📦 Layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_correo)
        layout.addWidget(self.input_password)
        layout.addWidget(self.boton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def login(self):
        correo = self.input_correo.text()
        password = self.input_password.text()

        usuario = self.auth.login(correo, password)

        if usuario:
            self.label.setText(f"Bienvenido {usuario.nombre}")

            # 🔥 Redirección según rol

            if usuario.rol == "admin":
                self.ventana = AdminView(self.auth)

            elif usuario.rol == "usuario":
                self.ventana = UsuarioView(usuario)

            elif usuario.rol == "seguridad":
                self.ventana = SeguridadView()

            else:
                self.label.setText("Rol no reconocido")
                return

            # Mostrar nueva ventana y cerrar login
            self.ventana.show()
            self.close()

        else:
            self.label.setText("Error en login")
