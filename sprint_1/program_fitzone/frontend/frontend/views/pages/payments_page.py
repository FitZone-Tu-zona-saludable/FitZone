"""
PAYMENTS PAGE

ES:
Página de verificación de pagos.

Responsabilidades:
- Mostrar pagos
- Permitir verificación
- Refrescar UI

EN:
Displays payments and allows verification.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from frontend.frontend.controllers.payment_controller import load_payments, verify_payment
from frontend.frontend.views.components.card_widget import CardWidget
from functools import partial


class PaymentsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        self.clear_layout()

        data = load_payments()

        for p in data:
            card = CardWidget()

            label = QLabel(f"{p['user']} - ${p['amount']} - {p['status']}")
            btn = QPushButton("Verificar")

            btn.clicked.connect(partial(self.handle_verify, p["id"]))

            card.add_widget(label)
            card.add_widget(btn)

            self.layout.addWidget(card)

    def handle_verify(self, payment_id):
        verify_payment(payment_id)
        self.load_data()

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()