# attendance_view.py
# Vista del afiche/registro de asistencia del cliente
# Sprint 3 - Alex (RF15: Actualización del afiche de asistencia del cliente)
# Usa el tema visual FitZone de Sprint 2

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from frontend.controllers.attendance_controller import AttendanceController
from frontend.resources.theme import COLORS


class AttendanceView(QWidget):
    """Vista para registrar y consultar la asistencia de clientes."""

    def __init__(self):
        super().__init__()
        self.controller = AttendanceController()
        self.setWindowTitle("Asistencia - FitZone")
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # ── Título ─────────────────────────────────────────────────
        title = QLabel("📋  Registro de Asistencia")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Registra y actualiza el afiche de asistencia de cada cliente.")
        subtitle.setObjectName("Muted")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # ── Formulario de registro ──────────────────────────────────
        form_row = QHBoxLayout()
        self.inp_id      = QLineEdit(); self.inp_id.setPlaceholderText("ID Cliente")
        self.inp_nombre  = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Cliente")
        self.inp_clase   = QLineEdit(); self.inp_clase.setPlaceholderText("Clase / Sesión")
        self.inp_servicio= QLineEdit(); self.inp_servicio.setPlaceholderText("Servicio adicional")
        btn_reg = QPushButton("✅  Registrar Asistencia")
        btn_reg.setObjectName("Primary")
        btn_reg.clicked.connect(self._register)

        for w in [self.inp_id, self.inp_nombre, self.inp_clase, self.inp_servicio, btn_reg]:
            form_row.addWidget(w)
        layout.addLayout(form_row)

        # ── Tabla de asistencias ────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "ID Cliente", "Nombre", "Clase", "Servicio", "Fecha"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # ── Botones de acción ───────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_data)
        btn_delete = QPushButton("🗑  Eliminar seleccionado")
        btn_delete.setObjectName("Danger")
        btn_delete.clicked.connect(self._delete_selected)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch()
        btn_row.addWidget(btn_delete)
        layout.addLayout(btn_row)

    def _load_data(self):
        records = self.controller.list_attendance()
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id_asistencia"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r["id_cliente"])))
            self.table.setItem(i, 2, QTableWidgetItem(r["nombre_cliente"]))
            self.table.setItem(i, 3, QTableWidgetItem(r["clase"]))
            self.table.setItem(i, 4, QTableWidgetItem(r["servicio"]))
            self.table.setItem(i, 5, QTableWidgetItem(r["fecha"]))

    def _register(self):
        id_cli = self.inp_id.text().strip()
        nombre = self.inp_nombre.text().strip()
        clase  = self.inp_clase.text().strip()
        serv   = self.inp_servicio.text().strip()

        if not id_cli or not nombre:
            QMessageBox.warning(self, "Validación",
                                "ID y nombre del cliente son obligatorios.")
            return

        try:
            id_cli = int(id_cli)
        except ValueError:
            QMessageBox.warning(self, "Validación", "El ID debe ser un número.")
            return

        result = self.controller.register(id_cli, nombre, clase, serv)
        if result["success"]:
            QMessageBox.information(self, "Éxito", "Asistencia registrada correctamente.")
            self.inp_id.clear(); self.inp_nombre.clear()
            self.inp_clase.clear(); self.inp_servicio.clear()
            self._load_data()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la asistencia.")

    def _delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un registro primero.")
            return
        id_a = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirmar", f"¿Eliminar registro de asistencia #{id_a}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.controller.delete(id_a)
            self._load_data()
