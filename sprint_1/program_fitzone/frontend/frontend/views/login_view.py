from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from frontend.frontend.controllers.auth_controller import authenticate
from frontend.frontend.views.pages.main_page import MainPage
from frontend.frontend.views.dialogs.register_dialog import RegisterDialog


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FitZone - Login')
        self.resize(420, 420)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        card = QFrame()
        card_layout = QVBoxLayout()
        card_layout.setSpacing(12)

        title = QLabel('FITZONE')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 22px; font-weight: bold;')
        card_layout.addWidget(title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Correo electronico')
        card_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Contrasena')
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)

        btn_login = QPushButton('Iniciar sesion')
        btn_login.clicked.connect(self.login)
        card_layout.addWidget(btn_login)

        btn_register = QPushButton('Crear cuenta')
        btn_register.clicked.connect(self.register)
        card_layout.addWidget(btn_register)

        card.setLayout(card_layout)
        card.setFixedWidth(300)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def login(self):
        result = authenticate(self.email_input.text().strip(), self.password_input.text().strip())
        if result.get('success'):
            self.menu = MainPage(result.get('role'))
            self.menu.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result.get('message', 'Credenciales invalidas'))

    def register(self):
        dialog = RegisterDialog(self)
        dialog.exec()
