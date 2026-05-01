from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from frontend.services.state_service import reset_state, state
from frontend.views.accounting_view import AccountingView
from frontend.views.attendance_view import AttendanceView
from frontend.views.employee_detail_view import EmployeeDetailView
from frontend.views.employee_payment_view import EmployeePaymentView
from frontend.views.incident_view import IncidentView
from frontend.views.main_dashboard_view import MainDashboardView
from frontend.views.membership_list_view import MembershipListView
from frontend.views.membership_select_view import MembershipSelectView
from frontend.views.payment_register_view import PaymentRegisterView
from frontend.views.payment_verification_view import PaymentVerificationView
from frontend.views.performance_view import PerformanceView
from frontend.views.reports_view import ReportsView
from frontend.views.schedule_reassign_view import ScheduleReassignView
from frontend.views.security_view import SecurityView
from frontend.views.survey_view import SurveyView
from frontend.views.worker_notifications_view import WorkerNotificationsView
from frontend.views.pages.alerts_page import AlertsPage
from frontend.views.pages.employee_page import EmployeePage
from frontend.views.pages.schedule_page import SchedulePage
from frontend.views.pages.trainer_page import TrainerPage


ACTION_META = {
    "memberships": {
        "label": "Membresías",
        "description": "Consulta planes y revisa el estado de tu membresía.",
    },
    "select_membership": {
        "label": "Seleccionar plan",
        "description": "Asocia un plan real a la cuenta autenticada.",
    },
    "register_payment": {
        "label": "Registrar pago",
        "description": "Envía el pago para que administración lo verifique.",
    },
    "verify_payment": {
        "label": "Verificar pagos",
        "description": "Confirma pagos pendientes y activa membresías.",
    },
    "security": {
        "label": "Bitácora",
        "description": "Revisa accesos, intentos fallidos y eventos sensibles.",
    },
    "alerts": {
        "label": "Alertas",
        "description": "Resumen contextual de pagos, membresías y seguridad.",
    },
    "schedules": {
        "label": "Horarios",
        "description": "Consulta o administra clases y sesiones.",
    },
    "trainers": {
        "label": "Entrenadores",
        "description": "Compara entrenadores o administra su disponibilidad.",
    },
    "employees": {
        "label": "Personal",
        "description": "Registra y consulta personal del gimnasio.",
    },
    "attendance": {
        "label": "Asistencia",
        "description": "Control de asistencia de clientes.",
    },
    "schedule_reassign": {
        "label": "Reasignación",
        "description": "Modifica horarios por eventos y reasigna entrenadores.",
    },
    "accounting": {
        "label": "Contabilidad",
        "description": "Gestiona cobros, saldos e indicadores contables.",
    },
    "employee_detail": {
        "label": "Detalle empleado",
        "description": "Consulta datos laborales completos del empleado.",
    },
    "incidents": {
        "label": "Incidencias",
        "description": "Reporta y resuelve incidencias del personal.",
    },
    "performance": {
        "label": "Evaluaciones",
        "description": "Evaluación de desempeño de usuarios.",
    },
    "worker_notif": {
        "label": "Notif. trabajador",
        "description": "Mensajes y alertas relacionadas con personal.",
    },
    "reports": {
        "label": "Reportes",
        "description": "Reportes gerenciales de membresías, actividad y finanzas.",
    },
    "emp_payments": {
        "label": "Pago empleados",
        "description": "Liquida y confirma nómina del personal.",
    },
    "surveys": {
        "label": "Encuestas",
        "description": "Gestiona encuestas de satisfacción del servicio.",
    },
}


ROLE_MENU = {
    "user": [
        ("Inicio", None),
        ("Dashboard", "dashboard"),
        ("Cliente", None),
        ("Membresías", "memberships"),
        ("Seleccionar plan", "select_membership"),
        ("Registrar pago", "register_payment"),
        ("Horarios", "schedules"),
        ("Entrenadores", "trainers"),
        ("Alertas", "alerts"),
        ("Encuestas", "surveys"),
    ],
    "admin": [
        ("Inicio", None),
        ("Dashboard", "dashboard"),
        ("Clientes", None),
        ("Membresías", "memberships"),
        ("Seleccionar plan", "select_membership"),
        ("Registrar pago", "register_payment"),
        ("Verificar pagos", "verify_payment"),
        ("Seguridad", "security"),
        ("Alertas", "alerts"),
        ("Operación", None),
        ("Horarios", "schedules"),
        ("Entrenadores", "trainers"),
        ("Personal", "employees"),
        ("Asistencia", "attendance"),
        ("Reasignación", "schedule_reassign"),
        ("Contabilidad", "accounting"),
        ("Detalle empleado", "employee_detail"),
        ("Incidencias", "incidents"),
        ("Evaluaciones", "performance"),
        ("Notif. trabajador", "worker_notif"),
        ("Gerencia", None),
        ("Reportes", "reports"),
        ("Pago empleados", "emp_payments"),
        ("Encuestas", "surveys"),
    ],
    "seguridad": [
        ("Seguridad", None),
        ("Dashboard", "dashboard"),
        ("Bitácora", "security"),
        ("Alertas", "alerts"),
    ],
}


DASHBOARD_KEYS = {
    "user": ["memberships", "select_membership", "register_payment", "schedules"],
    "admin": ["verify_payment", "schedules", "employees", "reports"],
    "seguridad": ["security", "alerts"],
}


class Sprint5Page(QWidget):
    def __init__(self, role=None):
        super().__init__()
        self.role = role or (state.get("user") or {}).get("role", "user")
        self.views = {}
        self.nav_buttons = {}
        self.setWindowTitle("FitZone — Panel principal")
        self._build_ui()

    def _build_ui(self):
        # ── Layout raíz ──────────────────────────────────────────────────────
        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        # CORRECCIÓN CRÍTICA: usar setFixedWidth + setSizePolicy(Fixed, Expanding)
        # garantiza que el sidebar NUNCA se encoja al agrandar la ventana.
        # No se usan posiciones absolutas ni stretch que compita con el contenido.
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)           # ancho fijo: nunca se reduce
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 16, 0, 16)
        sb.setSpacing(4)

        brand = QLabel("FitZone")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignCenter)
        sb.addWidget(brand)

        role_label = QLabel(f"Rol: {self.role.capitalize()}")
        role_label.setObjectName("Muted")
        role_label.setAlignment(Qt.AlignCenter)
        sb.addWidget(role_label)

        # Mostrar nombre e ID del usuario autenticado
        user_data = state.get("user") or {}
        user_name = user_data.get("name", "")
        user_id   = str(user_data.get("id", user_data.get("user_id", ""))).zfill(2)
        if user_name:
            id_label = QLabel(f"ID: {user_id} · {user_name}")
            id_label.setObjectName("Muted")
            id_label.setAlignment(Qt.AlignCenter)
            sb.addWidget(id_label)

        sb.addSpacing(8)

        # ── Stack de contenido ────────────────────────────────────────────────
        self.stack = QStackedWidget()
        # CORRECCIÓN: QStackedWidget debe expandirse; el sidebar tiene fixed width.
        # main.setStretchFactor garantiza que el stack tome todo el espacio sobrante.
        self._build_views()

        for label, key in ROLE_MENU.get(self.role, ROLE_MENU["user"]):
            if key is None:
                header = QLabel(f"── {label.upper()} ──")
                header.setObjectName("Muted")
                header.setContentsMargins(14, 10, 0, 4)
                sb.addWidget(header)
                continue

            btn = QPushButton(label)
            btn.setObjectName("NavItem")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _=False, target=key: self._navigate(target))
            sb.addWidget(btn)
            self.nav_buttons[key] = btn

        sb.addStretch()

        logout_btn = QPushButton("Cerrar sesión")
        logout_btn.clicked.connect(self._logout)
        sb.addWidget(logout_btn)

        main.addWidget(sidebar, 0)       # stretch=0 → ancho fijo, no cede espacio
        main.addWidget(self.stack, 1)    # stretch=1 → ocupa todo el espacio restante
        self._navigate("dashboard")

    def _dashboard_actions(self):
        actions = []
        for key in DASHBOARD_KEYS.get(self.role, []):
            meta = ACTION_META.get(key)
            if meta:
                actions.append({"key": key, **meta})
        return actions

    def _build_views(self):
        builders = {
            "dashboard": lambda: MainDashboardView(
                self.role,
                self._dashboard_actions(),
                navigate_callback=self._navigate,
            ),
            "memberships": MembershipListView,
            "select_membership": MembershipSelectView,
            "register_payment": PaymentRegisterView,
            "verify_payment": PaymentVerificationView,
            "security": SecurityView,
            "alerts": AlertsPage,
            "schedules": lambda: SchedulePage(self.role),
            "trainers": lambda: TrainerPage(self.role),
            "employees": lambda: EmployeePage(self.role),
            "attendance": AttendanceView,
            "schedule_reassign": ScheduleReassignView,
            "accounting": AccountingView,
            "employee_detail": EmployeeDetailView,
            "incidents": IncidentView,
            "performance": PerformanceView,
            "worker_notif": WorkerNotificationsView,
            "reports": ReportsView,
            "emp_payments": EmployeePaymentView,
            "surveys": SurveyView,
        }

        allowed_keys = [key for _, key in ROLE_MENU.get(self.role, []) if key]
        for key in allowed_keys:
            builder = builders.get(key)
            if not builder:
                continue
            view = builder() if callable(builder) else builder
            self.views[key] = view
            self.stack.addWidget(view)

        list_view = self.views.get("memberships")
        select_view = self.views.get("select_membership")
        if list_view and select_view:
            list_view.open_selection = self._open_membership_selection
            select_view.btn_back.clicked.connect(lambda: self._navigate("memberships"))
            select_view.selection_completed = self._after_membership_selection

    def _open_membership_selection(self, membership):
        select_view = self.views.get("select_membership")
        if not select_view:
            return
        select_view.set_membership(membership)
        self._navigate("select_membership")

    def _after_membership_selection(self, membership):
        payment_view = self.views.get("register_payment")
        if payment_view and hasattr(payment_view, "on_activate"):
            payment_view.on_activate()
        self._navigate("register_payment")

    def _navigate(self, key):
        for button_key, button in self.nav_buttons.items():
            button.setChecked(button_key == key)

        view = self.views.get(key)
        if view is None:
            return

        self.stack.setCurrentWidget(view)
        if hasattr(view, "on_activate"):
            view.on_activate()

    def _logout(self):
        reset_state()
        from frontend.views.login_view import LoginView

        self.login = LoginView()
        self.login.resize(420, 500)
        self.login.show()
        self.close()
