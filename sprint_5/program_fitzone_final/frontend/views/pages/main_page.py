# main_page.py
# Página heredada del Sprint 1/2 — actualmente reemplazada por Sprint5Page.
# Se conserva completa para evitar ImportError desde user_view.py (legado).

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

from frontend.views.membership_list_view import MembershipListView
from frontend.views.membership_select_view import MembershipSelectView
from frontend.views.payment_verification_view import PaymentVerificationView
from frontend.views.payment_register_view import PaymentRegisterView
from frontend.views.security_view import SecurityView
from frontend.views.pages.schedule_page import SchedulePage
from frontend.views.pages.trainer_page import TrainerPage
from frontend.views.pages.employee_page import EmployeePage
from frontend.views.pages.alerts_page import AlertsPage


class MainPage(QWidget):
    """Página heredada con menú lateral básico (Sprint 1/2)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone")
        self.resize(1100, 680)
        self._build_ui()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)

        # ── Menú lateral ──────────────────────────────────────────────
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(6)

        title_label = QLabel("Panel de Control FitZone")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        menu_layout.addWidget(title_label)

        self.stack = QStackedWidget()

        # Instancia las vistas
        self.membership_list_view   = MembershipListView()
        self.membership_select_view = MembershipSelectView()
        self.payment_register_view  = PaymentRegisterView()
        self.payment_verification_view = PaymentVerificationView()
        self.security_view   = SecurityView()
        self.schedule_page   = SchedulePage()
        self.trainer_page    = TrainerPage()
        self.employee_page   = EmployeePage()
        self.alerts_page     = AlertsPage()

        views = [
            ("Membresías",           self.membership_list_view),
            ("Seleccionar Membresía",self.membership_select_view),
            ("Registrar Pago",       self.payment_register_view),
            ("Verificar Pago",       self.payment_verification_view),
            ("Seguridad",            self.security_view),
            ("Horarios",             self.schedule_page),
            ("Entrenadores",         self.trainer_page),
            ("Empleados",            self.employee_page),
            ("Alertas",              self.alerts_page),
        ]

        for label, view in views:
            self.stack.addWidget(view)
            btn = QPushButton(label)
            btn.setStyleSheet("color: black; font-size: 14px;")
            btn.clicked.connect(lambda _, v=view: self.stack.setCurrentWidget(v))
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.stack, 1)
