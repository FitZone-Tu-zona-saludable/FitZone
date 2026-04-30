"""
schedule_admin_view.py
======================
Sprint 2 - Pantalla de **administración de horarios**.

Permite al administrador crear, modificar y eliminar clases o sesiones.
Conecta con `api_service_ext.save_schedule / delete_schedule`, validando
respuestas de éxito y error con feedback visual.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QTimeEdit, QSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox,
)

from frontend.services.api_service_ext import (
    fetch_schedules, save_schedule, delete_schedule, fetch_trainers,
)
from frontend.views.components.widgets import PageHeader, Card
from frontend.views.components.alerts import AlertBanner


class ScheduleAdminView(QWidget):
    """CRUD visual de horarios para administradores."""

    def __init__(self):
        super().__init__()
        self._editing_id: int | None = None
        self._build_ui()
        self.reload()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        root.addWidget(PageHeader(
            "Administración de horarios",
            "Crea, modifica o elimina las clases y sesiones del gimnasio.",
        ))

        # contenedor para banners de feedback
        self.feedback_slot = QVBoxLayout()
        root.addLayout(self.feedback_slot)

        # ---------- Formulario --------------------------------------------------
        form_card = Card()
        form = QHBoxLayout()

        self.in_class = QLineEdit(); self.in_class.setPlaceholderText("Nombre de la clase")
        self.in_date = QDateEdit(QDate.currentDate()); self.in_date.setCalendarPopup(True)
        self.in_date.setDisplayFormat("yyyy-MM-dd")
        self.in_time = QTimeEdit(QTime(7, 0)); self.in_time.setDisplayFormat("HH:mm")
        self.in_trainer = QComboBox()
        for t in fetch_trainers():
            self.in_trainer.addItem(t["name"], t["id"])
        self.in_capacity = QSpinBox(); self.in_capacity.setRange(1, 200); self.in_capacity.setValue(15)

        for w, lbl in [(self.in_class, "Clase"),
                       (self.in_date, "Fecha"),
                       (self.in_time, "Hora"),
                       (self.in_trainer, "Entrenador"),
                       (self.in_capacity, "Cupos")]:
            col = QVBoxLayout()
            l = QLabel(lbl); l.setObjectName("Muted")
            col.addWidget(l); col.addWidget(w)
            form.addLayout(col)

        form_card.layout.addLayout(form)

        actions = QHBoxLayout()
        self.btn_save = QPushButton("Guardar horario"); self.btn_save.setObjectName("Primary")
        self.btn_save.clicked.connect(self._save)
        self.btn_cancel = QPushButton("Cancelar edición"); self.btn_cancel.clicked.connect(self._reset_form)
        self.btn_cancel.setVisible(False)
        actions.addStretch(); actions.addWidget(self.btn_cancel); actions.addWidget(self.btn_save)
        form_card.layout.addLayout(actions)
        root.addWidget(form_card)

        # ---------- Tabla -------------------------------------------------------
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Hora", "Clase", "Entrenador", "Cupos", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

    # ------------------------------------------------------------------ helpers
    def _show_feedback(self, msg: str, kind: str):
        # limpiar banners viejos
        while self.feedback_slot.count():
            item = self.feedback_slot.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.feedback_slot.addWidget(AlertBanner(msg, kind=kind, autohide_ms=4000))

    def _reset_form(self):
        self._editing_id = None
        self.in_class.clear()
        self.in_date.setDate(QDate.currentDate())
        self.in_time.setTime(QTime(7, 0))
        self.in_trainer.setCurrentIndex(0)
        self.in_capacity.setValue(15)
        self.btn_save.setText("Guardar horario")
        self.btn_cancel.setVisible(False)

    # ------------------------------------------------------------------ actions
    def _save(self):
        data = {
            "class_name": self.in_class.text().strip(),
            "date": self.in_date.date().toString("yyyy-MM-dd"),
            "time": self.in_time.time().toString("HH:mm"),
            "trainer_id": self.in_trainer.currentData(),
            "capacity": self.in_capacity.value(),
        }
        if self._editing_id:
            data["id"] = self._editing_id
        result = save_schedule(data)
        if result.get("success"):
            self._show_feedback(result["message"], "success")
            self._reset_form()
            self.reload()
        else:
            self._show_feedback(result.get("message", "Error"), "danger")

    def _edit(self, row: dict):
        self._editing_id = row["id"]
        self.in_class.setText(row["class_name"])
        self.in_date.setDate(QDate.fromString(row["date"], "yyyy-MM-dd"))
        self.in_time.setTime(QTime.fromString(row["time"], "HH:mm"))
        idx = self.in_trainer.findData(row["trainer_id"])
        if idx >= 0:
            self.in_trainer.setCurrentIndex(idx)
        self.in_capacity.setValue(row["capacity"])
        self.btn_save.setText("Actualizar horario")
        self.btn_cancel.setVisible(True)

    def _delete(self, schedule_id: int):
        confirm = QMessageBox.question(
            self, "Confirmar", "¿Eliminar este horario?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        r = delete_schedule(schedule_id)
        self._show_feedback(r.get("message", ""), "success" if r.get("success") else "danger")
        self.reload()

    def reload(self):
        rows = fetch_schedules()
        trainers = {t["id"]: t["name"] for t in fetch_trainers()}
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            cells = [r["id"], r["date"], r["time"], r["class_name"],
                     trainers.get(r["trainer_id"], "—"),
                     f"{r['enrolled']}/{r['capacity']}"]
            for c, val in enumerate(cells):
                it = QTableWidgetItem(str(val))
                it.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, it)

            box = QWidget(); h = QHBoxLayout(box); h.setContentsMargins(4, 2, 4, 2)
            b_edit = QPushButton("Editar")
            b_del = QPushButton("Eliminar"); b_del.setObjectName("Danger")
            b_edit.clicked.connect(lambda _=False, row=r: self._edit(row))
            b_del.clicked.connect(lambda _=False, sid=r["id"]: self._delete(sid))
            h.addWidget(b_edit); h.addWidget(b_del)
            self.table.setCellWidget(i, 6, box)
