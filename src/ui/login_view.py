from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox,
    QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from src.services.auth_service import AuthService


class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.auth = AuthService()

        self.setWindowTitle("FitZone")
        self.setGeometry(300, 150, 500, 450)
        self.setStyleSheet("background-color: #f5f6fa;")

        # 🟩 LAYOUT PRINCIPAL
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

        # 🔥 CREAR CARD_LAYOUT (CLAVE)
        card_layout = QVBoxLayout()

        # 🟩 LOGO
        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")

        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(180, 210))
        else:
            logo.setText("FitZone 💪")

        logo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo)

        # 🟩 TÍTULO
        title = QLabel("FitZone")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2f3640;
        """)
        card_layout.addWidget(title)

        subtitle = QLabel("Iniciar sesión")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        card_layout.addWidget(subtitle)

        # 🟩 EMAIL
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet(self.input_style())
        card_layout.addWidget(self.email_input)

        # 🟩 PASSWORD
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        card_layout.addWidget(self.password_input)

        # 🟩 BOTÓN LOGIN
        self.btn_login = QPushButton("Ingresar")
        self.btn_login.setStyleSheet(self.button_style("#0984e3"))
        self.btn_login.clicked.connect(self.login)
        card_layout.addWidget(self.btn_login)

        # 🟩 BOTÓN REGISTRO
        self.btn_register = QPushButton("Crear cuenta ")
        self.btn_register.setStyleSheet(self.button_style("#00b894"))
        self.btn_register.clicked.connect(self.go_register)
        card_layout.addWidget(self.btn_register)

        # 🟩 ASIGNAR LAYOUT A CARD
        card.setLayout(card_layout)

        # 🟩 AGREGAR CARD AL MAIN
        main_layout.addWidget(card)

        # 🟩 SET LAYOUT FINAL
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

    # 🟩 LOGIN
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        user = self.auth.login(email, password)

        if user:
            role = user.get_role()

            if role == "admin":
                from src.ui.admin_view import AdminView
                self.admin = AdminView(self.auth)
                self.admin.show()
                self.close()

            elif role == "user":
                if user.membership is None:
                    from src.ui.plans_view import PlansView
                    self.plans = PlansView(self.auth, user)
                    self.plans.show()
                else:
                    from src.ui.user_view import UserView
                    self.user_view = UserView(user)
                    self.user_view.show()
                self.close()

            elif role == "seguridad":
                from src.ui.security_view import SecurityView
                self.security = SecurityView(self.auth)
                self.security.show()
                self.close()

        else:
            QMessageBox.warning(self, "Error", "Correo o contraseña incorrectos")

    # 🟩 IR A REGISTRO
    def go_register(self):
        from src.ui.register_view import RegisterView
        self.register = RegisterView(self.auth)
        self.register.show()
        self.close()
