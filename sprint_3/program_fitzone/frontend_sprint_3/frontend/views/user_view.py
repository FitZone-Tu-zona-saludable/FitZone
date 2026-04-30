# user_view.py — vista de cuenta de usuario (del tercer compañero, integrada)
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class UserView(QWidget):
    def __init__(self, user, auth=None):
        super().__init__()
        self.user = user
        self.auth = auth
        self.setWindowTitle("FitZone - Mi Cuenta")
        self.setGeometry(250, 120, 600, 420)
        self.setStyleSheet("background-color: #f5f6fa;")
        layout = QVBoxLayout()

        header = QHBoxLayout()
        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(40, 60))
        else:
            logo.setText("💪")
        title = QLabel(f"Bienvenido, {user.get_name()}")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(logo); header.addWidget(title); header.addStretch()
        layout.addLayout(header)

        self.info = QTextEdit()
        self.info.setReadOnly(True)
        self.info.setStyleSheet("QTextEdit { background-color:white; border:1px solid #dcdde1; border-radius:8px; padding:10px; font-size:14px; }")
        layout.addWidget(self.info)

        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Actualizar info")
        btn_refresh.setStyleSheet(self._bStyle("#0984e3"))
        btn_refresh.clicked.connect(self.load_info)

        btn_menu = QPushButton("📋 Menú principal")
        btn_menu.setStyleSheet(self._bStyle("#27ae60"))
        btn_menu.clicked.connect(self._open_menu)

        btn_back = QPushButton("⬅ Cerrar sesión")
        btn_back.setStyleSheet(self._bStyle("#2d3436"))
        btn_back.clicked.connect(self._logout)

        btn_layout.addWidget(btn_refresh); btn_layout.addWidget(btn_menu); btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.load_info()

    def _bStyle(self, color):
        return f"QPushButton {{ background-color:{color}; color:white; padding:8px 16px; border-radius:6px; font-weight:bold; }} QPushButton:hover {{ background-color:#636e72; }}"

    def load_info(self):
        u = self.user
        if u.membership and isinstance(u.membership, dict):
            mem_text = f"  Tipo: {u.membership.get('name', u.membership.get('tipo','—'))}\n  Estado: activa"
        elif u.membership:
            mem_text = f"  Plan: {u.membership}"
        else:
            mem_text = "  Sin membresía activa"
        pagos = "\n".join(f"  • ${p.get('value', p.get('amount','?'))} — {p.get('method','?')}" for p in u.payments) or "  Sin pagos registrados"
        self.info.setText(f"👤 DATOS\n  Nombre: {u.get_name()}\n  Correo: {u.get_email()}\n  Rol: {u.get_role()}\n\n🏋️ MEMBRESÍA\n{mem_text}\n\n💳 PAGOS\n{pagos}")

    def _open_menu(self):
        from frontend.views.pages.main_page import MainPage
        self.menu = MainPage()
        self.menu.show()

    def _logout(self):
        from frontend.views.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
