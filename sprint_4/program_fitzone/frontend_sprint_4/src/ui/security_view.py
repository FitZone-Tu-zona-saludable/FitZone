from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame
)
from PySide6.QtCore import Qt


class SecurityView(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

        self.setWindowTitle("Panel de Seguridad")
        self.setGeometry(300, 150, 600, 400)
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 🟩 CARD
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("🛡 Panel de Seguridad")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 🟩 LOGS
        self.logs_area = QTextEdit()
        self.logs_area.setReadOnly(True)
        layout.addWidget(self.logs_area)

        # 🟩 BOTÓN ACTUALIZAR
        self.btn_refresh = QPushButton("Actualizar historial")
        self.btn_refresh.clicked.connect(self.load_logs)
        layout.addWidget(self.btn_refresh)

        # 🟩 BOTÓN CONTROL
        self.btn_check = QPushButton("Verificar accesos")
        self.btn_check.clicked.connect(self.check_access)
        layout.addWidget(self.btn_check)

        # 🟩 BOTÓN VOLVER
        self.btn_back = QPushButton("Volver")
        self.btn_back.clicked.connect(self.volver)
        layout.addWidget(self.btn_back)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        # cargar logs al iniciar
        self.load_logs()

    # 🟩 CARGAR HISTORIAL REAL
    def load_logs(self):
        self.logs_area.clear()
        for log in self.auth.logs:
            self.logs_area.append(f"{log['date']} - {log['message']}")

    # 🟩 SIMULACIÓN CONTROL
    def check_access(self):
        self.logs_area.append("\n✔ Sistema verificado correctamente")

    def volver(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()