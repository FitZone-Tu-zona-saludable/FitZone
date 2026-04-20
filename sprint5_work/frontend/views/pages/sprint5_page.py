# sprint5_page.py
# Página central del Sprint 5 — Sistema completo pulido y unificado
# Sprint 5 - Alex: Pulir pantallas, consistencia visual, demo en vivo

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

# Vistas Sprint 1 & 2 (heredadas)
from frontend.views.membership_list_view   import MembershipListView
from frontend.views.membership_select_view import MembershipSelectView
from frontend.views.payment_register_view  import PaymentRegisterView
from frontend.views.payment_verification_view import PaymentVerificationView
from frontend.views.security_view          import SecurityView

# Vistas Sprint 2
from frontend.views.pages.schedule_page import SchedulePage
from frontend.views.pages.trainer_page  import TrainerPage
from frontend.views.pages.employee_page import EmployeePage
from frontend.views.pages.alerts_page   import AlertsPage
from frontend.services.alert_service    import AlertService

# Vistas Sprint 3
from frontend.views.attendance_view            import AttendanceView
from frontend.views.schedule_reassign_view     import ScheduleReassignView
from frontend.views.accounting_view            import AccountingView
from frontend.views.employee_detail_view       import EmployeeDetailView
from frontend.views.incident_view              import IncidentView
from frontend.views.performance_view           import PerformanceView
from frontend.views.worker_notifications_view  import WorkerNotificationsView

# Vistas Sprint 4
from frontend.views.reports_view          import ReportsView
from frontend.views.employee_payment_view import EmployeePaymentView
from frontend.views.survey_view           import SurveyView

# Dashboard Sprint 5
from frontend.views.main_dashboard_view import MainDashboardView


class Sprint5Page(QWidget):
    """
    Sistema completo FitZone — Sprint 5.
    Integra todos los módulos en un único panel coherente y pulido.
    """

    MENU_GROUPS = [
        ("── INICIO ──", []),
        ("🏠  Dashboard",        "dashboard"),
        ("── MEMBRESÍAS ──", []),
        ("💳  Membresías",       "memberships"),
        ("➕  Seleccionar plan", "select_membership"),
        ("💸  Registrar pago",   "register_payment"),
        ("✅  Verificar pago",   "verify_payment"),
        ("── SEGURIDAD ──", []),
        ("🔒  Seguridad",        "security"),
        ("🔔  Alertas",          "alerts"),
        ("── OPERACIÓN ──", []),
        ("📅  Horarios",         "schedules"),
        ("🏋️  Entrenadores",     "trainers"),
        ("👥  Personal",         "employees"),
        ("── ADMIN (S3) ──", []),
        ("📋  Asistencia",       "attendance"),
        ("🗓  Mod. Horarios",    "schedule_reassign"),
        ("💰  Contabilidad",     "accounting"),
        ("👔  Empleados (det.)", "employee_detail"),
        ("⚠️  Incidencias",      "incidents"),
        ("⭐  Evaluaciones",     "performance"),
        ("🔔  Notif. Trabajador","worker_notif"),
        ("── GERENCIA (S4) ──", []),
        ("📊  Reportes",         "reports"),
        ("💼  Pago Empleados",   "emp_payments"),
        ("📝  Encuestas",        "surveys"),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone — Sistema Completo (Sprint 5)")
        self._build_ui()

    def _build_ui(self):
        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(215)
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 12, 0, 12)
        sb.setSpacing(2)

        brand = QLabel("FitZone")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignCenter)
        sb.addWidget(brand)
        v_lbl = QLabel("v1.0 — Sprint 5")
        v_lbl.setObjectName("Muted")
        v_lbl.setAlignment(Qt.AlignCenter)
        sb.addWidget(v_lbl)
        sb.addSpacing(8)

        self.stack = QStackedWidget()
        self.views = {}
        self.nav_buttons = {}

        # Instanciar vistas
        dashboard = MainDashboardView(navigate_callback=self._navigate)
        self.views["dashboard"] = dashboard
        self.stack.addWidget(dashboard)

        view_map = {
            "memberships":      MembershipListView,
            "select_membership":MembershipSelectView,
            "register_payment": PaymentRegisterView,
            "verify_payment":   PaymentVerificationView,
            "security":         SecurityView,
            "schedules":        SchedulePage,
            "trainers":         TrainerPage,
            "employees":        EmployeePage,
            "attendance":       AttendanceView,
            "schedule_reassign":ScheduleReassignView,
            "accounting":       AccountingView,
            "employee_detail":  EmployeeDetailView,
            "incidents":        IncidentView,
            "performance":      PerformanceView,
            "worker_notif":     WorkerNotificationsView,
            "reports":          ReportsView,
            "emp_payments":     EmployeePaymentView,
            "surveys":          SurveyView,
        }
        for key, cls in view_map.items():
            if key == "alerts":
                v = AlertsPage(AlertService())
            else:
                v = cls()
            self.views[key] = v
            self.stack.addWidget(v)

        self.views["alerts"] = AlertsPage(AlertService())
        self.stack.addWidget(self.views["alerts"])

        # Construir menú
        for item in self.MENU_GROUPS:
            label, key = item if len(item) == 2 else (item, None)
            if not key:            # es cabecera de grupo
                lbl = QLabel(label)
                lbl.setObjectName("Muted")
                lbl.setContentsMargins(14, 8, 0, 2)
                sb.addWidget(lbl)
            else:
                btn = QPushButton(label)
                btn.setObjectName("NavItem")
                btn.setCheckable(True)
                btn.clicked.connect(lambda _, k=key: self._navigate(k))
                sb.addWidget(btn)
                self.nav_buttons[key] = btn

        sb.addStretch()
        main.addWidget(sidebar)
        main.addWidget(self.stack)

        self._navigate("dashboard")

    def _navigate(self, key):
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == key)
        if key in self.views:
            self.stack.setCurrentWidget(self.views[key])
