from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget
)

def volver_login(self):
    from app.ui.login_view import LoginView  # 👈 IMPORT LOCAL

    self.login = LoginView()
    self.login.show()
    self.close()


class AdminView(QWidget):
    def __init__(self, auth_service):
        super().__init__()

        self.auth = auth_service

        self.setWindowTitle("Panel Administrador")

        # Inputs
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")

        # Botón registrar
        self.boton = QPushButton("Registrar Usuario")
        self.boton.clicked.connect(self.registrar_usuario)

        # 🔥 Botón volver
        self.btn_volver = QPushButton("Volver al Login")
        self.btn_volver.clicked.connect(self.volver_login)

        # Lista usuarios
        self.lista = QListWidget()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("ADMIN"))
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.input_correo)
        layout.addWidget(self.input_password)
        layout.addWidget(self.boton)
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

    def registrar_usuario(self):
        nombre = self.input_nombre.text()
        correo = self.input_correo.text()
        password = self.input_password.text()

        self.auth.registrar_usuario(nombre, correo, password)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.clear()
        for usuario in self.auth.listar_usuarios():
            self.lista.addItem(f"{usuario.nombre} - {usuario.correo}")

    def volver_login(self):
        from app.ui.login_view import LoginView  # 👈 IMPORT LOCAL

        self.login = LoginView()
        self.login.show()
        self.close()
