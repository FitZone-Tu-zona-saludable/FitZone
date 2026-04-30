# employee_detail_view.py
# Vista de consulta y actualización de datos de empleados
# Sprint 3 - Alex (RF22: Actualizar datos de empleados / RF24: Consultar información de empleado)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt
from frontend.controllers.employee_controller import EmployeeController


class EmployeeDetailView(QWidget):
    """Vista para consultar y actualizar datos laborales y personales del empleado."""

    def __init__(self):
        super().__init__()
        self.controller = EmployeeController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("👔  Gestión de Empleados")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Consulta información laboral, descuentos, modalidad y actualiza datos del empleado.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Tabla de empleados ───────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Cargo", "Teléfono", "Correo",
            "Modalidad", "Contrato", "Rev. Médica"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # ── Botones ──────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_data)
        btn_edit = QPushButton("✏️  Editar seleccionado")
        btn_edit.setObjectName("Primary")
        btn_edit.clicked.connect(self._edit_selected)
        btn_detail = QPushButton("🔍  Ver detalle")
        btn_detail.clicked.connect(self._view_detail)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch()
        btn_row.addWidget(btn_detail)
        btn_row.addWidget(btn_edit)
        layout.addLayout(btn_row)

    def _load_data(self):
        employees = self.controller.list_employees()
        self.table.setRowCount(len(employees))
        for i, e in enumerate(employees):
            self.table.setItem(i, 0, QTableWidgetItem(str(e.get("id_trabajador", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(e.get("nombre", "")))
            self.table.setItem(i, 2, QTableWidgetItem(e.get("cargo", "")))
            self.table.setItem(i, 3, QTableWidgetItem(e.get("telefono", "")))
            self.table.setItem(i, 4, QTableWidgetItem(e.get("correo", "")))
            self.table.setItem(i, 5, QTableWidgetItem(e.get("modalidad", "")))
            self.table.setItem(i, 6, QTableWidgetItem(e.get("tipo_contrato", "N/A")))
            rev = "✅" if e.get("revision_medica") else "❌"
            self.table.setItem(i, 7, QTableWidgetItem(rev))

    def _edit_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un empleado primero.")
            return
        worker_id = int(self.table.item(row, 0).text())
        dialog = _EditEmployeeDialog(worker_id, self.controller, self)
        if dialog.exec():
            self._load_data()
            QMessageBox.information(self, "Actualizado",
                                    "Datos del empleado actualizados correctamente.")

    def _view_detail(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un empleado primero.")
            return
        employees = self.controller.list_employees()
        e = employees[row]
        info = "\n".join(f"{k}: {v}" for k, v in e.items())
        msg = QMessageBox(self)
        msg.setWindowTitle("Detalle del Empleado")
        msg.setText(info)
        msg.exec()


class _EditEmployeeDialog(QDialog):
    def __init__(self, worker_id, ctrl, parent=None):
        super().__init__(parent)
        self.worker_id = worker_id
        self.ctrl = ctrl
        self.setWindowTitle(f"Editar Empleado #{worker_id}")
        self.setMinimumWidth(400)
        form = QFormLayout(self)

        self.inp_nombre   = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre completo")
        self.inp_cargo    = QLineEdit(); self.inp_cargo.setPlaceholderText("Cargo")
        self.inp_telefono = QLineEdit(); self.inp_telefono.setPlaceholderText("Teléfono")
        self.inp_correo   = QLineEdit(); self.inp_correo.setPlaceholderText("Correo")
        self.combo_modal  = QComboBox()
        self.combo_modal.addItems(["presencial", "remoto", "mixto"])
        self.combo_rev    = QComboBox()
        self.combo_rev.addItems(["Sí", "No"])

        form.addRow("Nombre:",          self.inp_nombre)
        form.addRow("Cargo:",           self.inp_cargo)
        form.addRow("Teléfono:",        self.inp_telefono)
        form.addRow("Correo:",          self.inp_correo)
        form.addRow("Modalidad:",       self.combo_modal)
        form.addRow("Rev. médica:",     self.combo_rev)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._apply)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def _apply(self):
        kwargs = {}
        if self.inp_nombre.text().strip():   kwargs["nombre"]   = self.inp_nombre.text().strip()
        if self.inp_cargo.text().strip():    kwargs["cargo"]    = self.inp_cargo.text().strip()
        if self.inp_telefono.text().strip(): kwargs["telefono"] = self.inp_telefono.text().strip()
        if self.inp_correo.text().strip():   kwargs["correo"]   = self.inp_correo.text().strip()
        kwargs["modalidad"]       = self.combo_modal.currentText()
        kwargs["revision_medica"] = self.combo_rev.currentText() == "Sí"
        self.ctrl.edit_employee(self.worker_id, **kwargs)
        self.accept()
