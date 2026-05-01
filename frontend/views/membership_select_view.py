from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from frontend.controllers.membership_controller import MembershipController
from frontend.services.state_service import (
    refresh_current_user,
    set_selected_membership,
    state,
)
from frontend.views.components.widgets import Card, PageHeader, StatusChip


class MembershipSelectView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = MembershipController()
        self.membership = None
        self.selection_completed = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        root.addWidget(PageHeader(
            "Confirmar selección de plan",
            "Revisa el detalle del plan antes de asociarlo a tu cuenta.",
        ))

        card = Card()
        self.label_name = QLabel("Sin selección")
        self.label_name.setObjectName("H2")
        self.label_status = StatusChip("pendiente")
        self.label_price = QLabel()
        self.label_price.setObjectName("Muted")
        self.label_duration = QLabel()
        self.label_duration.setObjectName("Muted")
        self.label_description = QLabel()
        self.label_description.setWordWrap(True)

        card.layout.addWidget(self.label_name)
        card.layout.addWidget(self.label_status, 0, Qt.AlignLeft)
        card.layout.addWidget(self.label_price)
        card.layout.addWidget(self.label_duration)
        card.layout.addWidget(self.label_description)

        self.btn_confirm = QPushButton("Confirmar plan")
        self.btn_confirm.setObjectName("Primary")
        self.btn_confirm.clicked.connect(self.confirm_selection)
        card.layout.addWidget(self.btn_confirm, 0, Qt.AlignRight)

        self.btn_back = QPushButton("Volver a planes")
        card.layout.addWidget(self.btn_back, 0, Qt.AlignRight)

        root.addWidget(card)

    def set_membership(self, membership):
        self.membership = membership
        if not membership:
            self.label_name.setText("Sin selección")
            self.label_price.setText("")
            self.label_duration.setText("")
            self.label_description.setText("")
            return

        self.label_name.setText(membership.get("name", "Sin nombre"))
        self.label_status.set_status(membership.get("estado", "pendiente"))
        self.label_price.setText(f"Precio: ${membership.get('price', 0):,.0f}")
        self.label_duration.setText(
            f"Duración: {membership.get('duration_days', 0)} días"
        )
        self.label_description.setText(
            membership.get("description", "Sin descripción.")
        )

    def _load_current_membership(self):
        user = state.get("user") or {}
        user_id = user.get("user_id")
        if not user_id:
            return
        memberships = self.controller.load_user_memberships(user_id)
        if memberships:
            self.set_membership(memberships[0])

    def confirm_selection(self):
        if not self.membership:
            QMessageBox.warning(self, "Aviso", "Primero selecciona un plan.")
            return

        user = state.get("user") or {}
        user_id = user.get("user_id")
        if not user_id:
            QMessageBox.critical(self, "Error", "No hay un usuario autenticado.")
            return

        result = self.controller.select_membership(
            user_id=user_id,
            membership_id=self.membership.get("id"),
        )

        if result.get("success"):
            refresh_current_user()
            set_selected_membership(result.get("data"))
            QMessageBox.information(
                self,
                "Plan asociado",
                result.get("message", "Membresía seleccionada correctamente."),
            )
            if callable(self.selection_completed):
                self.selection_completed(result.get("data"))
        else:
            QMessageBox.critical(
                self,
                "Error",
                result.get("message", "No se pudo seleccionar la membresía."),
            )

    def on_activate(self):
        if self.membership:
            self.set_membership(self.membership)
        else:
            self._load_current_membership()
