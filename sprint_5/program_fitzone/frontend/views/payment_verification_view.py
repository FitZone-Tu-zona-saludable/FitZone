from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from frontend.controllers.payment_controller import PaymentController
from frontend.views.components.widgets import Card, PageHeader, StatusChip


class PaymentVerificationView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PaymentController()
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        root.addWidget(PageHeader(
            "Verificación de pagos",
            "Solo administración debe confirmar pagos pendientes para activar membresías.",
        ))

        summary = Card()
        self.summary_text = QLabel()
        self.summary_text.setObjectName("Muted")
        summary.layout.addWidget(self.summary_text)
        root.addWidget(summary)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Usuario", "Plan", "Monto", "Método", "Estado", "Acción"
        ])
        root.addWidget(self.table)

    def load_data(self):
        payments = self.controller.load_payments()
        self.table.setRowCount(len(payments))

        pending = 0
        verified = 0
        for row, payment in enumerate(payments):
            estado = payment.get("estado", "")
            if estado == "verificado":
                verified += 1
            else:
                pending += 1

            self.table.setItem(row, 0, QTableWidgetItem(str(payment.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(payment.get("user_name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(payment.get("membership_name", "")))
            self.table.setItem(row, 3, QTableWidgetItem(f"${payment.get('amount', 0):,.0f}"))
            self.table.setItem(row, 4, QTableWidgetItem(payment.get("method", "")))
            self.table.setCellWidget(row, 5, StatusChip(estado or "pendiente"))

            box = QWidget()
            layout = QHBoxLayout(box)
            layout.setContentsMargins(4, 2, 4, 2)
            btn = QPushButton("Verificar")
            btn.setObjectName("Primary")
            btn.setEnabled(estado != "verificado")
            btn.clicked.connect(
                lambda _=False, payment_id=payment.get("id"): self.handle_verify(payment_id)
            )
            layout.addWidget(btn)
            self.table.setCellWidget(row, 6, box)

        self.summary_text.setText(
            f"Pagos pendientes: {pending} · Pagos verificados: {verified}"
        )

    def handle_verify(self, payment_id):
        result = self.controller.verify_payment(payment_id)
        title = "Pago verificado" if result.get("success") else "No verificado"
        body = result.get("message", "No se pudo verificar el pago.")
        if result.get("success"):
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, title, body)
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, title, body)
        self.load_data()

    def on_activate(self):
        self.load_data()
