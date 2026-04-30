"""
trainer_select_view.py
======================
Sprint 2 - Vista de **selección de entrenador** con información comparativa
suficiente para que el usuario decida.

Muestra tarjetas con: nombre, especialidad, años de experiencia, rating y
disponibilidad. Permite seleccionar uno y dispara `assign_trainer`.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QScrollArea, QFrame,
)

from frontend.services.api_service_ext import fetch_trainers, assign_trainer
from frontend.services.state_service import state
from frontend.views.components.widgets import PageHeader, Card, StatusChip
from frontend.views.components.alerts import AlertBanner


class TrainerSelectView(QWidget):
    """Catálogo visual de entrenadores comparables."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self.reload()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        root.addWidget(PageHeader(
            "Selecciona tu entrenador",
            "Compara especialidades, experiencia y disponibilidad.",
        ))

        self.feedback_slot = QVBoxLayout()
        root.addLayout(self.feedback_slot)

        # Grid scrollable para responsividad
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        container = QWidget(); self.grid = QGridLayout(container)
        self.grid.setSpacing(16)
        scroll.setWidget(container)
        root.addWidget(scroll, 1)

    # ------------------------------------------------------------------ data
    def reload(self):
        # vaciar grid
        while self.grid.count():
            it = self.grid.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        trainers = fetch_trainers()
        cols = 3
        for idx, t in enumerate(trainers):
            self.grid.addWidget(self._trainer_card(t), idx // cols, idx % cols)

    def on_activate(self):
        self.reload()

    def _trainer_card(self, t: dict) -> Card:
        card = Card()

        # Encabezado con nombre + chip de disponibilidad
        head = QHBoxLayout()
        name = QLabel(t["name"]); name.setObjectName("H2")
        head.addWidget(name); head.addStretch()
        head.addWidget(StatusChip("Disponible" if t["available"] else "No disponible"))
        card.layout.addLayout(head)

        spec = QLabel(f"Especialidad: {t['specialty']}")
        exp  = QLabel(f"Experiencia: {t['experience_years']} años")
        rate = QLabel(f"Calificación: ★ {t['rating']:.1f}")
        for lbl in (spec, exp, rate):
            lbl.setObjectName("Muted")
            card.layout.addWidget(lbl)

        card.layout.addStretch()

        btn = QPushButton("Seleccionar entrenador")
        btn.setObjectName("Primary")
        btn.setEnabled(t["available"])
        btn.clicked.connect(lambda _=False, tr=t: self._select(tr))
        card.layout.addWidget(btn)

        return card

    # ------------------------------------------------------------------ action
    def _select(self, trainer: dict):
        user = state.get("user") or {"user_id": 0}
        result = assign_trainer(user["user_id"], trainer["id"])
        kind = "success" if result.get("success") else "danger"

        # limpiar banners
        while self.feedback_slot.count():
            it = self.feedback_slot.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        self.feedback_slot.addWidget(
            AlertBanner(result.get("message", ""), kind=kind, autohide_ms=4000)
        )
