# =========================
# views/pages/dashboard_page.py
# =========================

"""
Página de inicio (Dashboard)

Muestra información general del sistema.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Bienvenido al sistema del gimnasio")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        description = QLabel("Selecciona una opción del menú lateral")
        description.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(description)

        self.setLayout(layout)