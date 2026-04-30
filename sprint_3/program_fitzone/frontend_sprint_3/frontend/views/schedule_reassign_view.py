# schedule_reassign_view.py
# Vista de modificación de horarios y reasignación de entrenadores
# Sprint 3 - Alex (RF17: Modificación de horarios y reasignación de entrenadores)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QFormLayout, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt
from frontend.controllers.schedule_controller import ScheduleController
from frontend.controllers.trainer_controller import TrainerController


class ScheduleReassignView(QWidget):
    """Vista para modificar horarios y reasignar entrenadores (Sprint 3)."""

    def __init__(self):
        super().__init__()
        self.sched_ctrl   = ScheduleController()
        self.trainer_ctrl = TrainerController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("🗓  Modificación de Horarios y Reasignación de Entrenadores")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Modifica horarios existentes y asigna un entrenador diferente ante eventos externos.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Tabla horarios ──────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Hora inicio", "Hora fin", "Tipo", "Entrenador asignado"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # ── Botones ─────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_refresh = QPushButton("🔄  Actualizar lista")
        btn_refresh.clicked.connect(self._load_data)
        btn_edit = QPushButton("✏️  Modificar horario seleccionado")
        btn_edit.setObjectName("Primary")
        btn_edit.clicked.connect(self._edit_selected)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch()
        btn_row.addWidget(btn_edit)
        layout.addLayout(btn_row)

        # ── Reasignar entrenador ─────────────────────────────────────
        reassign_lbl = QLabel("Reasignación rápida de entrenador")
        reassign_lbl.setObjectName("H2")
        layout.addWidget(reassign_lbl)

        reassign_row = QHBoxLayout()
        self.combo_horario  = QComboBox()
        self.combo_trainer  = QComboBox()
        btn_reassign = QPushButton("🔁  Reasignar")
        btn_reassign.setObjectName("Primary")
        btn_reassign.clicked.connect(self._reassign)
        reassign_row.addWidget(QLabel("Horario:"))
        reassign_row.addWidget(self.combo_horario)
        reassign_row.addWidget(QLabel("Nuevo entrenador:"))
        reassign_row.addWidget(self.combo_trainer)
        reassign_row.addWidget(btn_reassign)
        layout.addLayout(reassign_row)

    def _load_data(self):
        schedules = self.sched_ctrl.list_schedules()
        self.table.setRowCount(len(schedules))
        self.combo_horario.clear()
        for i, s in enumerate(schedules):
            self.table.setItem(i, 0, QTableWidgetItem(str(s["id_horario"])))
            self.table.setItem(i, 1, QTableWidgetItem(s["fecha"]))
            self.table.setItem(i, 2, QTableWidgetItem(s["hora_inicio"]))
            self.table.setItem(i, 3, QTableWidgetItem(s["hora_fin"]))
            self.table.setItem(i, 4, QTableWidgetItem(s["tipo"]))
            self.table.setItem(i, 5, QTableWidgetItem(
                str(s["id_entrenador"]) if s["id_entrenador"] else "Sin asignar"))
            self.combo_horario.addItem(
                f"#{s['id_horario']} — {s['fecha']} {s['hora_inicio']} ({s['tipo']})",
                s["id_horario"]
            )

        trainers = self.trainer_ctrl.list_trainers()
        self.combo_trainer.clear()
        for t in trainers:
            self.combo_trainer.addItem(
                f"{t['nombre']} ({t.get('especialidad', '')})",
                t["id_trabajador"]
            )

    def _edit_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un horario primero.")
            return
        id_h = int(self.table.item(row, 0).text())
        dialog = _EditScheduleDialog(id_h, self.sched_ctrl, self)
        if dialog.exec():
            self._load_data()

    def _reassign(self):
        id_horario  = self.combo_horario.currentData()
        id_trainer  = self.combo_trainer.currentData()
        if id_horario is None or id_trainer is None:
            QMessageBox.warning(self, "Datos", "Selecciona horario y entrenador.")
            return
        result = self.sched_ctrl.edit_schedule(id_horario, entrenador=id_trainer)
        if result:
            QMessageBox.information(self, "Reasignado",
                                    "Entrenador reasignado correctamente.")
            self._load_data()
        else:
            QMessageBox.critical(self, "Error", "No se pudo reasignar.")


class _EditScheduleDialog(QDialog):
    """Diálogo para editar los campos de un horario existente."""

    def __init__(self, id_horario, ctrl, parent=None):
        super().__init__(parent)
        self.id_horario = id_horario
        self.ctrl = ctrl
        self.setWindowTitle(f"Editar Horario #{id_horario}")
        self.setMinimumWidth(360)
        form = QFormLayout(self)

        self.inp_fecha  = QLineEdit(); self.inp_fecha.setPlaceholderText("YYYY-MM-DD")
        self.inp_hora   = QLineEdit(); self.inp_hora.setPlaceholderText("HH:MM")
        self.inp_tipo   = QLineEdit(); self.inp_tipo.setPlaceholderText("yoga / cardio …")
        self.inp_cupos  = QLineEdit(); self.inp_cupos.setPlaceholderText("Número de cupos")

        form.addRow("Fecha:",       self.inp_fecha)
        form.addRow("Hora inicio:", self.inp_hora)
        form.addRow("Tipo clase:",  self.inp_tipo)
        form.addRow("Cupos:",       self.inp_cupos)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._apply)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _apply(self):
        kwargs = {}
        if self.inp_fecha.text().strip():
            kwargs["fecha"]  = self.inp_fecha.text().strip()
        if self.inp_hora.text().strip():
            kwargs["hora"]   = self.inp_hora.text().strip()
        if self.inp_tipo.text().strip():
            kwargs["tipo"]   = self.inp_tipo.text().strip()
        if self.inp_cupos.text().strip():
            try:
                kwargs["cupos"] = int(self.inp_cupos.text().strip())
            except ValueError:
                pass
        self.ctrl.edit_schedule(self.id_horario, **kwargs)
        self.accept()
