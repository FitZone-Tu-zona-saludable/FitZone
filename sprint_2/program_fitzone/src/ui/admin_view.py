from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class AdminView(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

        self.setWindowTitle("Panel Administrador")
        self.setGeometry(200, 100, 850, 550)
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()

        # 🟩 HEADER CON LOGO
        header_layout = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")

        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(40, 60))
        else:
            logo.setText("💪")

        title = QLabel("Panel Administrador")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # 🟩 FORMULARIO
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        self.name_input.setStyleSheet(self.input_style())

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet(self.input_style())

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setStyleSheet(self.input_style())

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)

        main_layout.addLayout(form_layout)

        # 🟩 BOTONES
        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Crear")
        self.btn_add.setStyleSheet(self.button_style("#00b894"))
        self.btn_add.clicked.connect(self.create_user)

        self.btn_update = QPushButton("✏️ Editar")
        self.btn_update.setStyleSheet(self.button_style("#0984e3"))
        self.btn_update.clicked.connect(self.update_user)

        self.btn_delete = QPushButton("🗑 Eliminar")
        self.btn_delete.setStyleSheet(self.button_style("#d63031"))
        self.btn_delete.clicked.connect(self.delete_user)

        self.btn_refresh = QPushButton("🔄 Refrescar")
        self.btn_refresh.setStyleSheet(self.button_style("#636e72"))
        self.btn_refresh.clicked.connect(self.load_users)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(btn_layout)

        # 🟩 TABLA
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "Correo", "Rol"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # 🔥 seleccionar fila y llenar inputs
        self.table.cellClicked.connect(self.select_user)

        main_layout.addWidget(self.table)

        # 🟩 BOTÓN VOLVER
        self.btn_back = QPushButton("⬅ Volver")
        self.btn_back.setStyleSheet(self.button_style("#2d3436"))
        self.btn_back.clicked.connect(self.volver)

        main_layout.addWidget(self.btn_back)

        self.setLayout(main_layout)

        self.load_users()

    # 🟩 ESTILOS
    def input_style(self):
        return """
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 6px;
            }
        """

    def button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2d3436;
            }}
        """

    # 🟩 CARGAR USUARIOS
    def load_users(self):
        users = self.auth.get_users()
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.get_name()))
            self.table.setItem(row, 1, QTableWidgetItem(user.get_email()))
            self.table.setItem(row, 2, QTableWidgetItem(user.get_role()))

    # 🟩 SELECCIONAR FILA
    def select_user(self, row, column):
        self.name_input.setText(self.table.item(row, 0).text())
        self.email_input.setText(self.table.item(row, 1).text())

    # 🟩 CREAR
    def create_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if name and email and password:
            self.auth.create_user(name, email, password, "user")
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario creado")
        else:
            QMessageBox.warning(self, "Error", "Completa todos los campos")

    # 🟩 EDITAR
    def update_user(self):
        email = self.email_input.text()
        name = self.name_input.text()

        if self.auth.update_user(email, name):
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario actualizado")
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

    # 🟩 ELIMINAR
    def delete_user(self):
        email = self.email_input.text()

        if self.auth.delete_user(email):
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario eliminado")
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

    # 🟩 VOLVER
    def volver(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()