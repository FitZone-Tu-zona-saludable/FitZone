from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton



class UsuarioView(QWidget):
    def __init__(self, usuario):
        super().__init__()

        self.setWindowTitle("Panel Usuario")

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Bienvenido {usuario.nombre}"))

        if hasattr(usuario, "membresia") and usuario.membresia:
            layout.addWidget(QLabel(f"Membresía: {usuario.membresia}"))
        else:
            layout.addWidget(QLabel("No tienes membresía activa"))

        # 🔥 Botón volver
        self.btn_volver = QPushButton("Volver al Login")
        self.btn_volver.clicked.connect(self.volver_login)

        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

    def volver_login(self):
        from app.ui.login_view import LoginView

        self.login = LoginView()
        self.login.show()
        self.close()
