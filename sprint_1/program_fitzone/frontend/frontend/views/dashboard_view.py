"""
DASHBOARD PAGE

ES:
Panel principal del sistema.

Responsabilidades:
- Mostrar resumen general
- Servir como página inicial después del login

EN:
Main dashboard view.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from frontend.frontend.services.state_service import state


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        user = state.get("user")

        welcome = QLabel(f"Bienvenido {user['username']}" if user else "Bienvenido")

        layout.addWidget(welcome)

        self.setLayout(layout)