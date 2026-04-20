# incident_view.py
# Vista de incidencias del personal (inasistencias, permisos, etc.)
# Sprint 3 - Alex (RF28: Gestión del personal)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QTextEdit
)
from PySide6.QtCore import Qt
from frontend.controllers.incident_controller import IncidentController


class IncidentView(QWidget):
    """Vista para registrar y consultar incidencias del personal."""

    def __init__(self):
        super().__init__()
        self.controller = IncidentController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("⚠️  Gestión de Incidencias del Personal")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Reporta inasistencias, permisos e incapacidades del personal con causa y fecha.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Formulario ───────────────────────────────────────────────
        form_lbl = QLabel("Registrar nueva incidencia")
        form_lbl.setObjectName("H2")
        layout.addWidget(form_lbl)

        row1 = QHBoxLayout()
        self.inp_id_trab  = QLineEdit(); self.inp_id_trab.setPlaceholderText("ID Trabajador")
        self.inp_nombre   = QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Trabajador")
        self.combo_tipo   = QComboBox()
        self.combo_tipo.addItems(["inasistencia", "llegada_tarde", "permiso", "incapacidad", "otro"])
        row1.addWidget(self.inp_id_trab)
        row1.addWidget(self.inp_nombre)
        row1.addWidget(QLabel("Tipo:"))
        row1.addWidget(self.combo_tipo)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.inp_causa = QLineEdit()
        self.inp_causa.setPlaceholderText("Descripción de la causa")
        btn_reg = QPushButton("📝  Registrar incidencia")
        btn_reg.setObjectName("Primary")
        btn_reg.clicked.connect(self._register)
        row2.addWidget(QLabel("Causa:"))
        row2.addWidget(self.inp_causa)
        row2.addWidget(btn_reg)
        layout.addLayout(row2)

        # ── Tabla ────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "ID Trabajador", "Nombre", "Tipo", "Causa", "Fecha"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_data)
        layout.addWidget(btn_refresh, 0, Qt.AlignLeft)

    def _load_data(self):
        records = self.controller.list_incidents()
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id_incidencia"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r["id_trabajador"])))
            self.table.setItem(i, 2, QTableWidgetItem(r["nombre_trabajador"]))
            self.table.setItem(i, 3, QTableWidgetItem(r["tipo"]))
            self.table.setItem(i, 4, QTableWidgetItem(r["causa"]))
            self.table.setItem(i, 5, QTableWidgetItem(r["fecha"]))

    def _register(self):
        id_t   = self.inp_id_trab.text().strip()
        nombre = self.inp_nombre.text().strip()
        tipo   = self.combo_tipo.currentText()
        causa  = self.inp_causa.text().strip()
        if not id_t or not nombre:
            QMessageBox.warning(self, "Validación", "ID y nombre del trabajador son obligatorios.")
            return
        try:
            id_t = int(id_t)
        except ValueError:
            QMessageBox.warning(self, "Validación", "El ID debe ser un número.")
            return
        self.controller.create_incident(id_t, nombre, tipo, causa)
        QMessageBox.information(self, "Registrado", "Incidencia registrada correctamente.")
        self.inp_id_trab.clear(); self.inp_nombre.clear(); self.inp_causa.clear()
        self._load_data()
