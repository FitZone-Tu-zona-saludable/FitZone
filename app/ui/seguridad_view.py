from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton



class SeguridadView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Panel Seguridad")

        self.lista = QListWidget()

        # 🔥 Botón volver
        self.btn_volver = QPushButton("Volver al Login")
        self.btn_volver.clicked.connect(self.volver_login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Logs del sistema"))
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

        self.cargar_logs()

    def cargar_logs(self):
        try:
            with open("logs.txt", "r") as f:
                for linea in f.readlines():
                    self.lista.addItem(linea.strip())
        except:
            self.lista.addItem("No hay logs disponibles")

    def volver_login(self):
        from app.ui.login_view import LoginView

        self.login = LoginView()
        self.login.show()
        self.close()
