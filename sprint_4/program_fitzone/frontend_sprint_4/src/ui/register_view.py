import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox,
    QFrame
)
from PySide6.QtCore import Qt


class RegisterView(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

        self.setWindowTitle("FitZone - Registro")
        self.setGeometry(300, 150, 500, 450)
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 🟩 CARD
        card = QFrame()
        card.setFixedWidth(320)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()

        # 🟩 TÍTULO
        title = QLabel("Crear cuenta 🆕")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2f3640;
        """)
        layout.addWidget(title)

        subtitle = QLabel("Regístrate para continuar")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        layout.addWidget(subtitle)

        # 🟩 INPUTS
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.name_input.setStyleSheet(self.input_style())
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet(self.input_style())
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.confirm_password_input)

        # 🟩 BOTÓN CREAR
        self.btn_register = QPushButton("Crear Cuenta")
        self.btn_register.setStyleSheet(self.button_style("#00b894"))
        self.btn_register.clicked.connect(self.register)
        layout.addWidget(self.btn_register)

        # 🟩 BOTÓN VOLVER
        self.btn_back = QPushButton("Volver")
        self.btn_back.setStyleSheet(self.button_style("#636e72"))
        self.btn_back.clicked.connect(self.volver)
        layout.addWidget(self.btn_back)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    # 🎨 INPUT STYLE
    def input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                margin-top: 5px;
            }
        """

    # 🎨 BUTTON STYLE
    def button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: #2d3436;
            }}
        """

    # 🟩 VALIDAR EMAIL
    def is_valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    # 🟩 REGISTRO
    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()

        if not name or not email or not password or not confirm:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Error", "Correo inválido")
            return

        if len(password) < 3:
            QMessageBox.warning(self, "Error", "La contraseña debe tener mínimo 3 caracteres")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        for user in self.auth.get_users():
            if user.get_email() == email:
                QMessageBox.warning(self, "Error", "El correo ya está registrado")
                return

        self.auth.create_user(name, email, password, "user")

        QMessageBox.information(self, "Éxito", "Cuenta creada correctamente")

        self.volver()

    # 🟩 VOLVER
    def volver(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()