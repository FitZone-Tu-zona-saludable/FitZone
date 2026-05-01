from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from frontend.services.app_context import auth_service
from frontend.services.state_service import reset_state, set_current_user


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear cuenta")
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["user"])

        layout.addRow("Nombre", self.name_input)
        layout.addRow("Correo", self.email_input)
        layout.addRow("Contraseña", self.password_input)
        layout.addRow("Rol", self.role_input)

        btn = QPushButton("Registrar")
        btn.setObjectName("Primary")
        btn.clicked.connect(self._register)
        layout.addRow(btn)

    def _register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip().lower()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not name or not email or not password:
            QMessageBox.warning(self, "Aviso", "Completa todos los campos.")
            return

        if len(password) < 3:
            QMessageBox.warning(self, "Aviso", "La contraseña debe tener al menos 3 caracteres.")
            return

        try:
            user = auth_service.create_user(name, email, password, role)
        except ValueError as exc:
            QMessageBox.warning(self, "Error", str(exc))
            return

        uid = str(user.id_cliente).zfill(2)
        QMessageBox.information(
            self, "Cuenta creada",
            f"Cuenta creada correctamente.\n\nNombre: {name}\nID asignado: {uid}"
        )
        self.accept()


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone - Login")
        self.resize(420, 500)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(360)
        card.setStyleSheet(
            "QFrame { background-color: #1C312B; border-radius: 10px; padding: 20px; }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(120, 140, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo.setText("FitZone")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(logo)

        title = QLabel("FITZONE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #21C07A;")
        card_layout.addWidget(title)

        subtitle = QLabel("Iniciar sesión")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #9DB3AB;")
        card_layout.addWidget(subtitle)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        card_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.password_input)

        btn_login = QPushButton("Iniciar sesión")
        btn_login.setObjectName("Primary")
        btn_login.clicked.connect(self._login)
        card_layout.addWidget(btn_login)

        btn_register = QPushButton("Crear cuenta")
        btn_register.clicked.connect(self._register)
        card_layout.addWidget(btn_register)



        main_layout.addWidget(card)

    def _login(self):
        email = self.email_input.text().strip().lower()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Campos vacíos", "Ingresa tu correo y contraseña.")
            return

        user = auth_service.login(email, password)
        if not user:
            QMessageBox.critical(self, "Error", "Correo o contraseña incorrectos.")
            self.password_input.clear()
            return

        reset_state()
        set_current_user(user)

        from frontend.views.pages.sprint5_page import Sprint5Page

        self.next_win = Sprint5Page(role=user.get_role())
        self.next_win.setWindowTitle("FitZone — Panel principal")
        self.next_win.resize(1280, 760)
        self.next_win.show()
        self.close()

    def _register(self):
        dialog = RegisterDialog(self)
        dialog.exec()
