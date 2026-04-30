from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from frontend.controllers.membership_controller import MembershipController
from frontend.controllers.payment_controller import PaymentController
from frontend.services.state_service import refresh_current_user, state
from frontend.views.components.widgets import Card, PageHeader


class PaymentRegisterView(QWidget):
    def __init__(self):
        super().__init__()
        self.membership_controller = MembershipController()
        self.payment_controller = PaymentController()
        self.memberships = []
        self._build_ui()
        self.reload_memberships()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        root.addWidget(PageHeader(
            "Registrar pago",
            "El pago queda pendiente hasta que un administrador lo verifique.",
        ))

        form_card = Card()
        form = QFormLayout()

        self.membership_combo = QComboBox()
        self.membership_combo.currentIndexChanged.connect(self._sync_amount_with_plan)
        self.amount_input = QLineEdit()
        self.method_input = QLineEdit()
        self.method_input.setText("Transferencia")
        self.reference_input = QLineEdit()

        form.addRow("Membresía", self.membership_combo)
        form.addRow("Monto", self.amount_input)
        form.addRow("Método", self.method_input)
        form.addRow("Referencia", self.reference_input)
        form_card.layout.addLayout(form)

        self.status_label = QLabel()
        self.status_label.setObjectName("Muted")
        form_card.layout.addWidget(self.status_label)

        btn = QPushButton("Guardar pago")
        btn.setObjectName("Primary")
        btn.clicked.connect(self.save_payment)
        form_card.layout.addWidget(btn, 0, Qt.AlignRight)

        root.addWidget(form_card)

        history_card = Card()
        history_title = QLabel("Historial del usuario actual")
        history_title.setObjectName("H2")
        history_card.layout.addWidget(history_title)

        self.payments_table = QTableWidget(0, 5)
        self.payments_table.setHorizontalHeaderLabels([
            "ID", "Plan", "Monto", "Método", "Estado"
        ])
        history_card.layout.addWidget(self.payments_table)
        root.addWidget(history_card)

    def _sync_amount_with_plan(self):
        membership = self.membership_combo.currentData()
        if membership:
            self.amount_input.setText(str(membership.get("price", 0)))
            self.status_label.setText(
                f"Estado actual del plan: {membership.get('estado', 'pendiente')}"
            )
        else:
            self.status_label.setText("No hay membresías disponibles para pagar.")

    def _current_user_id(self):
        user = state.get("user") or {}
        return user.get("user_id")

    def reload_memberships(self):
        self.membership_combo.clear()
        self.memberships = []
        user_id = self._current_user_id()
        if not user_id:
            self.status_label.setText("Debes iniciar sesión para registrar un pago.")
            return

        self.memberships = self.membership_controller.load_user_memberships(user_id)
        for membership in self.memberships:
            label = (
                f"{membership['name']} · ${membership['price']:,.0f} · "
                f"{membership.get('estado', 'pendiente')}"
            )
            self.membership_combo.addItem(label, membership)

        self._sync_amount_with_plan()
        self._reload_payment_history()

    def _reload_payment_history(self):
        user = state.get("user") or {}
        payments = user.get("payments", [])
        self.payments_table.setRowCount(len(payments))
        for row, payment in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(str(payment.get("id", ""))))
            self.payments_table.setItem(row, 1, QTableWidgetItem(payment.get("membership_name", "Sin plan")))
            self.payments_table.setItem(row, 2, QTableWidgetItem(f"${float(payment.get('amount', payment.get('value', 0))):,.0f}"))
            self.payments_table.setItem(row, 3, QTableWidgetItem(payment.get("method", "")))
            self.payments_table.setItem(row, 4, QTableWidgetItem(payment.get("estado", "")))

    def save_payment(self):
        membership = self.membership_combo.currentData()
        if membership is None:
            QMessageBox.warning(self, "Aviso", "Primero debes seleccionar una membresía.")
            return

        try:
            amount = float(self.amount_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Error", "Ingresa un monto válido.")
            return

        payment_data = {
            "user_id": self._current_user_id(),
            "membership_id": membership.get("id"),
            "amount": amount,
            "method": self.method_input.text().strip() or "Transferencia",
            "reference": self.reference_input.text().strip(),
        }
        result = self.payment_controller.register_payment(payment_data)

        if result.get("success"):
            refresh_current_user()
            QMessageBox.information(
                self,
                "Pago registrado",
                result.get("message", "Pago registrado correctamente."),
            )
            self.reference_input.clear()
            self.reload_memberships()
        else:
            QMessageBox.critical(
                self,
                "Error",
                result.get("message", "No se pudo registrar el pago."),
            )

    def on_activate(self):
        refresh_current_user()
        self.reload_memberships()
