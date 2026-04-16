"""
CARD WIDGET

ES:
Componente visual reutilizable tipo tarjeta.

Responsabilidades:
- Contener información agrupada
- Mejorar la presentación visual
- Ser reutilizado en múltiples vistas

EN:
Reusable card component.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout


class CardWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QFrame {
            background-color: #2c2c3e;
            border-radius: 10px;
            padding: 10px;
        }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def add_widget(self, widget):
        self.layout.addWidget(widget)