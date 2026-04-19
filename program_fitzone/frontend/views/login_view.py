# login_view.py — integración completa de los tres compañeros
# Alex (frontend) + Romel (JSON/data) + tercer compañero (src/services)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame, QDialog, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from frontend.services.app_context import auth_service
from frontend.services.state_service import state


class RegisterDialog(QDialog):
    """Diálogo para crear nueva cuenta — usa AuthService real."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear cuenta")
        layout = QFormLayout()

        self.name_input     = QLineEdit(); self.name_input.setStyleSheet(self._iStyle())
        self.email_input    = QLineEdit(); self.email_input.setStyleSheet(self._iStyle())
        self.password_input = QLineEdit(); self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self._iStyle())
        self.role_input = QComboBox(); self.role_input.addItems(["user"])

        layout.addRow("Nombre",     self.name_input)
        layout.addRow("Correo",     self.email_input)
        layout.addRow("Contraseña", self.password_input)
        layout.addRow("Rol",        self.role_input)

        btn = QPushButton("Registrar")
        btn.clicked.connect(self._register)
        layout.addRow(btn)
        self.setLayout(layout)

    def _iStyle(self):
        return "color:black; background-color:white; padding:6px; border:1px solid #ccc; border-radius:5px; font-size:14px;"

    def _register(self):
        name     = self.name_input.text().strip()
        email    = self.email_input.text().strip()
        password = self.password_input.text().strip()
        role     = self.role_input.currentText()
        if not name or not email or not password:
            QMessageBox.warning(self, "Aviso", "Completa todos los campos.")
            return
        for u in auth_service.get_users():
            if u.get_email() == email:
                QMessageBox.warning(self, "Error", "El correo ya está registrado.")
                return
        auth_service.create_user(name, email, password, role)
        QMessageBox.information(self, "Éxito", "Cuenta creada correctamente.")
        self.accept()


class LoginView(QWidget):
    """Vista de login — navega por rol usando src.services.AuthService."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone - Login")
        self.resize(420, 500)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(360)
        card.setStyleSheet("QFrame { background-color: #f9f9f9; border-radius: 10px; padding: 20px; }")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(12)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(120, 140, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo.setText("FitZone 💪")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(logo)

        title = QLabel("FITZONE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #27ae60;")
        card_layout.addWidget(title)

        subtitle = QLabel("Iniciar sesión")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        card_layout.addWidget(subtitle)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        self.email_input.setStyleSheet(self._iStyle())
        card_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self._iStyle())
        card_layout.addWidget(self.password_input)

        btn_login = QPushButton("Iniciar sesión")
        btn_login.setStyleSheet(self._bStyle("#27ae60"))
        btn_login.clicked.connect(self._login)
        card_layout.addWidget(btn_login)

        btn_register = QPushButton("Crear cuenta")
        btn_register.setStyleSheet(self._bStyle("#2980b9"))
        btn_register.clicked.connect(self._register)
        card_layout.addWidget(btn_register)

        hint = QLabel("romel@mail.com / 123 (admin) | user@mail.com / 123 | seg@mail.com / 123")
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("font-size: 10px; color: #7f8c8d;")
        card_layout.addWidget(hint)

        card.setLayout(card_layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def _iStyle(self):
        return "color:black; background-color:white; padding:8px; border:1px solid #ccc; border-radius:5px; font-size:14px;"

    def _bStyle(self, color):
        return f"QPushButton {{ background-color:{color}; color:white; padding:8px; border-radius:5px; font-weight:bold; }} QPushButton:hover {{ background-color:#2d3436; }}"

    def _login(self):
        email    = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Aviso", "Completa todos los campos.")
            return

        # Usa el AuthService real del tercer compañero
        user = auth_service.login(email, password)

        if user:
            role = user.get_role()
            # Guardar en estado global del frontend (Alex)
            state["user"] = {
                "id": user.id_cliente, "name": user.nombre,
                "email": user.correo,  "role": role,
                "membership": user.membership, "payments": user.payments,
            }

            if role == "admin":
                from src.ui.admin_view import AdminView
                self.next_win = AdminView(auth_service)
                self.next_win.show()
                self.close()

            elif role == "user":
                if user.membership is None:
                    from src.ui.plans_view import PlansView
                    self.next_win = PlansView(auth_service, user)
                    self.next_win.show()
                else:
                    from src.ui.user_view import UserView
                    self.next_win = UserView(user, auth_service)
                    self.next_win.show()
                self.close()

            elif role == "seguridad":
                from src.ui.security_view import SecurityView
                self.next_win = SecurityView(auth_service)
                self.next_win.show()
                self.close()

            else:
                # Cualquier otro rol va al MainPage del frontend (Alex)
                from frontend.views.pages.main_page import MainPage
                self.next_win = MainPage()
                self.next_win.show()
                self.close()
        else:
            QMessageBox.critical(self, "Error", "Correo o contraseña incorrectos.")
            self.password_input.clear()

    def _register(self):
        dialog = RegisterDialog(self)
        dialog.exec()
