"""
MEMBERSHIPS PAGE

ES:
Página que muestra las membresías usando tarjetas.

Responsabilidades:
- Construir la vista completa
- Usar el controller para obtener datos
- Renderizar tarjetas

EN:
Displays memberships page.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from frontend.frontend.controllers.membership_controller import load_memberships, select_membership
from frontend.frontend.views.components.card_widget import CardWidget
from functools import partial


class MembershipsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        self.clear_layout()

        data = load_memberships()

        for m in data:
            card = CardWidget()

            label = QLabel(f"{m['name']} - ${m['price']}")
            btn = QPushButton("Seleccionar")

            btn.clicked.connect(partial(self.handle_select, m))

            card.add_widget(label)
            card.add_widget(btn)

            self.layout.addWidget(card)

    def handle_select(self, membership):
        select_membership(membership)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()