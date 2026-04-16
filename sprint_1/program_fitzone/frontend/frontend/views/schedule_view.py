# =========================
# views/schedule_view.py
# =========================

"""
===========================================================
VISTA: SCHEDULE VIEW (HORARIOS)
===========================================================

ES:
Muestra los horarios disponibles del gimnasio.

Responsabilidades:
- Consultar horarios desde el controlador
- Mostrar la información al usuario

EN:
Schedules view

Responsibilities:
- Load schedules
- Display schedules
===========================================================
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from frontend.frontend.controllers import schedule_controller as controller


class ScheduleView(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Horarios")

        layout = QVBoxLayout()

        # =========================
        # TÍTULO
        # =========================
        title = QLabel("Horarios disponibles")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # =========================
        # CARGA DE DATOS
        # =========================
        schedules = controller.load_schedules()

        for s in schedules:
            label = QLabel(f"{s['day']} - {s['time']}")
            layout.addWidget(label)

        self.setLayout(layout)