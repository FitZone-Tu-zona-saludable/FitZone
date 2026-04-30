from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from frontend.services.state_service import refresh_current_user, state
from frontend.views.components.widgets import Card, PageHeader, StatusChip


ROLE_COPY = {
    "admin": (
        "Panel administrativo",
        "Acceso operativo y gerencial sobre pagos, personal, horarios, incidencias y reportes.",
    ),
    "user": (
        "Portal del cliente",
        "Consulta planes, registra pagos, revisa horarios y gestiona tu experiencia como usuario.",
    ),
    "seguridad": (
        "Centro de seguridad",
        "Monitorea la bitácora, detecta eventos sensibles y revisa alertas operativas.",
    ),
}


class MainDashboardView(QWidget):
    def __init__(self, role, quick_actions, navigate_callback=None):
        super().__init__()
        self.role = role
        self.quick_actions = quick_actions
        self.navigate = navigate_callback
        self._build_ui()
        self.reload()

    def _build_ui(self):
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(16)

        title, subtitle = ROLE_COPY.get(
            self.role,
            ("Panel FitZone", "Resumen general del sistema."),
        )
        self.root.addWidget(PageHeader(title, subtitle))

        self.summary_card = Card()
        self.summary_name = QLabel()
        self.summary_name.setObjectName("H2")
        self.summary_role = QLabel()
        self.summary_role.setObjectName("Muted")
        self.summary_status = StatusChip("pendiente")
        self.summary_text = QLabel()
        self.summary_text.setWordWrap(True)
        self.summary_card.layout.addWidget(self.summary_name)
        self.summary_card.layout.addWidget(self.summary_role)
        self.summary_card.layout.addWidget(self.summary_status, 0, Qt.AlignLeft)
        self.summary_card.layout.addWidget(self.summary_text)
        self.root.addWidget(self.summary_card)

        self.grid = QGridLayout()
        self.grid.setSpacing(16)
        self.root.addLayout(self.grid)
        self.root.addStretch()

    def _clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _summary_message(self, user):
        membership = user.get("membership") or {}
        payments = user.get("payments", [])
        if self.role == "user":
            if not membership:
                return "Aún no tienes una membresía activa. Empieza consultando los planes disponibles."
            return (
                f"Plan: {membership.get('name', 'Sin plan')} · "
                f"Estado: {membership.get('estado', 'pendiente')} · "
                f"Pagos registrados: {len(payments)}"
            )

        if self.role == "seguridad":
            return "Tu acceso está enfocado en bitácora, control de accesos y alertas."

        return (
            f"Usuario administrativo con acceso a {len(self.quick_actions)} módulos visibles "
            f"en esta sesión."
        )

    def _build_action_card(self, action):
        card = Card()
        title = QLabel(action["label"])
        title.setObjectName("H2")
        description = QLabel(action["description"])
        description.setWordWrap(True)
        description.setObjectName("Muted")

        btn = QPushButton("Abrir módulo")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda _=False, key=action["key"]: self.navigate(key))

        card.layout.addWidget(title)
        card.layout.addWidget(description)
        card.layout.addStretch()
        card.layout.addWidget(btn, 0, Qt.AlignRight)
        return card

    def reload(self):
        refresh_current_user()
        user = state.get("user") or {}
        self.summary_name.setText(f"Bienvenido, {user.get('name', 'Usuario')}")
        self.summary_role.setText(f"Rol activo: {user.get('role', '').capitalize()}")

        membership = user.get("membership") or {}
        if self.role == "user" and membership:
            self.summary_status.set_status(membership.get("estado", "pendiente"))
        elif self.role == "seguridad":
            self.summary_status.set_status("pendiente")
            self.summary_status.setText("Seguridad")
        else:
            self.summary_status.set_status("activo")
            self.summary_status.setText("Administración")

        self.summary_text.setText(self._summary_message(user))

        self._clear_grid()
        for index, action in enumerate(self.quick_actions):
            self.grid.addWidget(self._build_action_card(action), index // 2, index % 2)

    def on_activate(self):
        self.reload()
