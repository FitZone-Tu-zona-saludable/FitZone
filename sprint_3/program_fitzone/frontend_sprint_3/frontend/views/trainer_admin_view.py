"""
trainer_admin_view.py
=====================
Sprint 2 - **Administración básica de entrenadores y su disponibilidad**.

Lista los entrenadores y permite alternar su disponibilidad mediante un
botón. Muestra retroalimentación visual sobre cada cambio.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView,
)

from frontend.services.api_service_ext import fetch_trainers, set_trainer_availability
from frontend.views.components.widgets import PageHeader, StatusChip
from frontend.views.components.alerts import AlertBanner


class TrainerAdminView(QWidget):
    """Panel administrativo de entrenadores."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self.reload()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        root.addWidget(PageHeader(
            "Administración de entrenadores",
            "Gestiona la disponibilidad de cada entrenador del gimnasio.",
        ))

        self.feedback_slot = QVBoxLayout()
        root.addLayout(self.feedback_slot)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Especialidad", "Experiencia", "Disponibilidad", "Acción"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

    def _show_feedback(self, msg, kind):
        while self.feedback_slot.count():
            it = self.feedback_slot.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        self.feedback_slot.addWidget(AlertBanner(msg, kind=kind, autohide_ms=3500))

    def reload(self):
        trainers = fetch_trainers()
        self.table.setRowCount(len(trainers))
        for i, t in enumerate(trainers):
            cells = [t["id"], t["name"], t["specialty"],
                     f"{t['experience_years']} años"]
            for c, val in enumerate(cells):
                it = QTableWidgetItem(str(val)); it.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, it)
            self.table.setCellWidget(
                i, 4, StatusChip("Disponible" if t["available"] else "No disponible")
            )

            box = QWidget(); h = QHBoxLayout(box); h.setContentsMargins(4, 2, 4, 2)
            btn = QPushButton("Marcar no disponible" if t["available"] else "Marcar disponible")
            if not t["available"]:
                btn.setObjectName("Primary")
            btn.clicked.connect(lambda _=False, tr=t: self._toggle(tr))
            h.addWidget(btn)
            self.table.setCellWidget(i, 5, box)

    def _toggle(self, trainer: dict):
        r = set_trainer_availability(trainer["id"], not trainer["available"])
        self._show_feedback(r.get("message", ""), "success" if r.get("success") else "danger")
        self.reload()
