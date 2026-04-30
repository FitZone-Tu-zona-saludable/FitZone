# sprint4_page.py
# Página central del Sprint 4 — Reportes, nómina y evaluación del servicio
# Sprint 4 - Alex

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt

from frontend.views.reports_view import ReportsView
from frontend.views.employee_payment_view import EmployeePaymentView
from frontend.views.survey_view import SurveyView


class Sprint4Page(QWidget):
    """
    Página central del Sprint 4.
    Acceso a reportes gerenciales, pago de empleados y encuestas de satisfacción.
    """

    MENU_ITEMS = [
        ("📊  Reportes Gerenciales",   "reports"),
        ("💼  Pago de Empleados",      "payments"),
        ("📝  Encuesta Satisfacción",  "survey"),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone — Sprint 4")
        self._build_ui()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(210)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 16, 0, 16)
        sb_layout.setSpacing(4)

        brand = QLabel("FitZone")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(brand)

        sprint_lbl = QLabel("Sprint 4")
        sprint_lbl.setObjectName("Muted")
        sprint_lbl.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(sprint_lbl)
        sb_layout.addSpacing(12)

        self.stack = QStackedWidget()
        self.views = {
            "reports":  ReportsView(),
            "payments": EmployeePaymentView(),
            "survey":   SurveyView(),
        }
        for v in self.views.values():
            self.stack.addWidget(v)

        self.nav_buttons = {}
        for label, key in self.MENU_ITEMS:
            btn = QPushButton(label)
            btn.setObjectName("NavItem")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, k=key: self._navigate(k))
            sb_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        sb_layout.addStretch()
        main.addWidget(sidebar)
        main.addWidget(self.stack)

        self._navigate("reports")

    def _navigate(self, key):
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == key)
        self.stack.setCurrentWidget(self.views[key])
