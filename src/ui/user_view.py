from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
)


class UserView(QWidget):
    def load_info(self):
        plan = self.user.membership if self.user else "Sin plan"
    
        self.info.setText(
            f"Usuario activo\n"
            f"Plan: {plan}\n"
            "Pagos:\n- $50\n- $30"
        )
        layout = QVBoxLayout()

        self.label = QLabel("Bienvenido Usuario")
        layout.addWidget(self.label)

        self.info = QTextEdit()
        self.info.setReadOnly(True)
        layout.addWidget(self.info)

        self.btn_load = QPushButton("Ver información")
        self.btn_load.clicked.connect(self.load_info)
        layout.addWidget(self.btn_load)

        self.btn_back = QPushButton("Volver")
        self.btn_back.clicked.connect(self.volver)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_info(self):
        self.info.setText(
            "Usuario activo\n"
            "Plan: Activo\n"
            "Pagos:\n- $50\n- $30"
        )

    def volver(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()