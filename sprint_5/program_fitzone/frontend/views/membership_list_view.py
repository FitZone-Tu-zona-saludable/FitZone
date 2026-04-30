from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from frontend.controllers.membership_controller import MembershipController
from frontend.services.state_service import state
from frontend.views.components.widgets import Card, PageHeader, StatusChip


class MembershipListView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = MembershipController()
        self.open_selection = None
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(16)

        self.root.addWidget(PageHeader(
            "Planes disponibles",
            "Consulta tarifas, duración y estado actual de tu membresía.",
        ))

        self.summary_card = Card()
        self.summary_title = QLabel("Tu estado actual")
        self.summary_title.setObjectName("H2")
        self.summary_status_row = QVBoxLayout()
        self.summary_text = QLabel()
        self.summary_text.setWordWrap(True)
        self.summary_text.setObjectName("Muted")
        self.summary_card.layout.addWidget(self.summary_title)
        self.summary_card.layout.addLayout(self.summary_status_row)
        self.summary_card.layout.addWidget(self.summary_text)
        self.root.addWidget(self.summary_card)

        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(12)
        self.root.addLayout(self.list_layout)

    def _clear_plan_cards(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        while self.summary_status_row.count():
            item = self.summary_status_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _current_membership(self):
        user = state.get("user") or {}
        user_id = user.get("user_id")
        if not user_id:
            return None
        memberships = self.controller.load_user_memberships(user_id)
        return memberships[0] if memberships else None

    def _build_plan_card(self, plan, current_membership):
        card = Card()

        title = QLabel(f"{plan['name']} · ${plan['price']:,.0f}")
        title.setObjectName("H2")
        card.layout.addWidget(title)

        duration = QLabel(f"Duración: {plan['duration_days']} días")
        duration.setObjectName("Muted")
        card.layout.addWidget(duration)

        description = QLabel(plan["description"])
        description.setWordWrap(True)
        card.layout.addWidget(description)

        if current_membership and current_membership.get("id") == plan["id"]:
            card.layout.addWidget(
                StatusChip(current_membership.get("estado", "pendiente"))
            )

        btn = QPushButton("Seleccionar este plan")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda _=False, selected=plan: self.on_select(selected))
        card.layout.addWidget(btn, 0, Qt.AlignRight)
        return card

    def load_data(self):
        self._clear_plan_cards()
        plans = self.controller.load_memberships()
        current_membership = self._current_membership()

        if current_membership:
            self.summary_status_row.addWidget(
                StatusChip(current_membership.get("estado", "pendiente"))
            )
            self.summary_text.setText(
                f"Plan actual: {current_membership.get('name', 'Sin plan')} · "
                f"${current_membership.get('price', 0):,.0f}\n"
                f"Duración: {current_membership.get('duration_days', 0)} días\n"
                f"Descripción: {current_membership.get('description', 'Sin descripción')}"
            )
        else:
            self.summary_text.setText(
                "Aún no tienes una membresía seleccionada. Revisa las opciones y elige el plan que más te convenga."
            )

        if not plans:
            self.list_layout.addWidget(QLabel("No hay planes disponibles en este momento."))
            return

        for plan in plans:
            self.list_layout.addWidget(self._build_plan_card(plan, current_membership))

    def on_select(self, membership):
        if callable(self.open_selection):
            self.open_selection(membership)

    def on_activate(self):
        self.load_data()
