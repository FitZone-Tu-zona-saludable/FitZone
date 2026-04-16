from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from frontend.frontend.controllers.membership_controller import load_memberships


class MembershipListView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.open_selection = None
        self.load_data()

    def load_data(self):
        self.clear_layout()
        data = load_memberships()
        if not data:
            self.layout.addWidget(QLabel('No hay membresias disponibles'))
            return
        for m in data:
            card = QFrame()
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(f"Plan: {m['name']}"))
            card_layout.addWidget(QLabel(f"Precio: ${m['price']}"))
            card_layout.addWidget(QLabel(f"Duracion: {m.get('duration', 30)} dias"))
            card_layout.addWidget(QLabel(f"Beneficios: {m.get('benefits', '')}"))
            btn = QPushButton('Seleccionar')
            btn.clicked.connect(partial(self.on_select, m))
            card_layout.addWidget(btn)
            self.layout.addWidget(card)

    def on_select(self, membership):
        if callable(self.open_selection):
            self.open_selection(membership)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
