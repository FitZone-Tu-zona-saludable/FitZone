"""
schedule_consult_view.py
========================
Sprint 2 - Vista de **consulta de horarios** por fecha, hora y entrenador.

Permite a usuarios y administradores filtrar las clases/sesiones disponibles.
Muestra resultados en una tabla con cupos disponibles y entrenador asignado.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView,
)

from frontend.services.api_service_ext import fetch_schedules, fetch_trainers
from frontend.views.components.widgets import PageHeader, Card, StatusChip


class ScheduleConsultView(QWidget):
    """Vista pública de consulta de horarios."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self.reload()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(PageHeader(
            "Consulta de horarios",
            "Filtra clases y sesiones por fecha, hora o entrenador.",
        ))

        # ----- Filtros dentro de una tarjeta ----------------------------
        filters = Card()
        row = QHBoxLayout()

        self.date_filter = QDateEdit(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDisplayFormat("yyyy-MM-dd")

        self.trainer_filter = QComboBox()
        self.trainer_filter.addItem("Todos los entrenadores", 0)
        for t in fetch_trainers():
            self.trainer_filter.addItem(t["name"], t["id"])

        self.hour_filter = QComboBox()
        self.hour_filter.addItem("Cualquier hora", "")
        for h in ["06:00", "07:00", "08:00", "17:00", "18:00", "19:00", "20:00"]:
            self.hour_filter.addItem(h, h)

        btn_search = QPushButton("Buscar"); btn_search.setObjectName("Primary")
        btn_search.clicked.connect(self.reload)

        btn_clear = QPushButton("Limpiar")
        btn_clear.clicked.connect(self._clear_filters)

        for w, lbl in [(self.date_filter, "Fecha"),
                       (self.hour_filter, "Hora"),
                       (self.trainer_filter, "Entrenador")]:
            col = QVBoxLayout()
            label = QLabel(lbl); label.setObjectName("Muted")
            col.addWidget(label); col.addWidget(w)
            row.addLayout(col)
        row.addWidget(btn_search, 0, Qt.AlignBottom)
        row.addWidget(btn_clear, 0, Qt.AlignBottom)

        filters.layout.addLayout(row)
        layout.addWidget(filters)

        # ----- Tabla ----------------------------------------------------
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Fecha", "Hora", "Clase", "Entrenador", "Cupos", "Estado"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table, 1)

    # ------------------------------------------------------------------ logic
    def _clear_filters(self):
        self.date_filter.setDate(QDate.currentDate())
        self.trainer_filter.setCurrentIndex(0)
        self.hour_filter.setCurrentIndex(0)
        self.reload()

    def reload(self):
        """Recarga la tabla aplicando los filtros activos."""
        date_str = self.date_filter.date().toString("yyyy-MM-dd")
        trainer_id = self.trainer_filter.currentData() or 0
        hour = self.hour_filter.currentData() or ""

        rows = fetch_schedules(filter_date=date_str, trainer_id=trainer_id)
        if hour:
            rows = [r for r in rows if r["time"] == hour]

        trainers = {t["id"]: t["name"] for t in fetch_trainers()}
        self.table.setRowCount(len(rows))

        for i, r in enumerate(rows):
            free = r["capacity"] - r["enrolled"]
            status = "vencido" if free <= 0 else "activo"
            cells = [
                r["date"], r["time"], r["class_name"],
                trainers.get(r["trainer_id"], "—"),
                f"{r['enrolled']}/{r['capacity']}",
            ]
            for c, val in enumerate(cells):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, item)
            self.table.setCellWidget(i, 5, StatusChip("Lleno" if free <= 0 else "Disponible"))
