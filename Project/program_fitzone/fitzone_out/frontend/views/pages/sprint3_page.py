# sprint3_page.py
# Página principal del Sprint 3 — integra todas las vistas de Alex
# Sprint 3 - Alex

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt

# Vistas Sprint 3
from frontend.views.attendance_view import AttendanceView
from frontend.views.schedule_reassign_view import ScheduleReassignView
from frontend.views.accounting_view import AccountingView
from frontend.views.employee_detail_view import EmployeeDetailView
from frontend.views.incident_view import IncidentView
from frontend.views.performance_view import PerformanceView
from frontend.views.worker_notifications_view import WorkerNotificationsView


class Sprint3Page(QWidget):
    """
    Página central del Sprint 3.
    Contiene menú lateral con acceso a todas las funcionalidades
    asignadas a Alex en el Sprint 3.
    """

    MENU_ITEMS = [
        ("📋  Asistencia",          "attendance"),
        ("🗓  Modificar Horarios",  "schedule"),
        ("💰  Contabilidad",        "accounting"),
        ("👔  Empleados",           "employees"),
        ("⚠️  Incidencias",         "incidents"),
        ("⭐  Evaluación",          "performance"),
        ("🔔  Notificaciones",      "notifications"),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone — Sprint 3")
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

        sprint_lbl = QLabel("Sprint 3")
        sprint_lbl.setObjectName("Muted")
        sprint_lbl.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(sprint_lbl)
        sb_layout.addSpacing(12)

        self.stack = QStackedWidget()

        self.views = {
            "attendance":    AttendanceView(),
            "schedule":      ScheduleReassignView(),
            "accounting":    AccountingView(),
            "employees":     EmployeeDetailView(),
            "incidents":     IncidentView(),
            "performance":   PerformanceView(),
            "notifications": WorkerNotificationsView(),
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

        # Selección inicial
        self._navigate("attendance")

    def _navigate(self, key):
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == key)
        self.stack.setCurrentWidget(self.views[key])
