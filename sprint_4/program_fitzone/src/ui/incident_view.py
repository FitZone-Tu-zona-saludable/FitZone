from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from src.services.incident_service import IncidentService
from src.services.worker_service import WorkerService
from src.models.incident import Incident


class IncidentView(QWidget):
    """Vista para registrar y gestionar incidencias del personal (Sprint 3 - Andrés)."""

    def __init__(self, incident_service: IncidentService, worker_service: WorkerService):
        super().__init__()
        self.inc_svc = incident_service
        self.ws = worker_service
        self._selected_id = None

        self.setWindowTitle("FitZone – Incidencias del Personal")
        self.setGeometry(200, 100, 900, 560)
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()

        title = QLabel("⚠️ Registro de Incidencias del Personal")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        layout.addWidget(title)

        # ── FORMULARIO ──────────────────────────────────────────────
        form = QHBoxLayout()

        self.cmb_trabajador = QComboBox()
        self.cmb_trabajador.setStyleSheet(self._inp())
        self._cargar_trabajadores()

        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems([
            Incident.TIPO_INASISTENCIA, Incident.TIPO_PERMISO,
            Incident.TIPO_INCAPACIDAD, Incident.TIPO_OTRO
        ])
        self.cmb_tipo.setStyleSheet(self._inp())

        self.txt_causa = QLineEdit()
        self.txt_causa.setPlaceholderText("Causa / Descripción")
        self.txt_causa.setStyleSheet(self._inp())

        self.txt_obs = QLineEdit()
        self.txt_obs.setPlaceholderText("Observaciones (opcional)")
        self.txt_obs.setStyleSheet(self._inp())

        btn_registrar = QPushButton("📝 Registrar")
        btn_registrar.setStyleSheet(self._btn("#e17055"))
        btn_registrar.clicked.connect(self._registrar)

        for w in [QLabel("Trabajador:"), self.cmb_trabajador,
                  QLabel("Tipo:"), self.cmb_tipo,
                  self.txt_causa, self.txt_obs, btn_registrar]:
            form.addWidget(w)
        layout.addLayout(form)

        # ── BOTONES ACCIONES ─────────────────────────────────────────
        btns = QHBoxLayout()
        for label, color, fn in [
            ("📋 Todas", "#636e72", self._ver_todas),
            ("⏳ Pendientes", "#e17055", self._ver_pendientes),
            ("✅ Resolver Seleccionada", "#00b894", self._resolver),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(self._btn(color))
            b.clicked.connect(fn)
            btns.addWidget(b)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.setStyleSheet(self._btn("#2d3436"))
        btn_volver.clicked.connect(self.close)
        btns.addWidget(btn_volver)
        layout.addLayout(btns)

        # ── TABLA ───────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Trabajador", "Tipo", "Causa", "Fecha", "Resuelta", "Observaciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self._seleccionar)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self._ver_todas()

    def _cargar_trabajadores(self):
        self.cmb_trabajador.clear()
        for w in self.ws.get_workers():
            self.cmb_trabajador.addItem(f"{w.nombre} – {w.cargo}", w)

    def _registrar(self):
        trabajador = self.cmb_trabajador.currentData()
        causa = self.txt_causa.text().strip()
        if not causa:
            QMessageBox.warning(self, "Error", "La causa es obligatoria")
            return
        self.inc_svc.registrar_incidencia(
            trabajador.id_trabajador, trabajador.nombre,
            self.cmb_tipo.currentText(), causa,
            self.txt_obs.text().strip()
        )
        QMessageBox.information(self, "OK", f"Incidencia registrada para {trabajador.nombre}")
        self.txt_causa.clear(); self.txt_obs.clear()
        self._ver_todas()

    def _resolver(self):
        if not self._selected_id:
            QMessageBox.warning(self, "Aviso", "Selecciona una incidencia")
            return
        ok, msg = self.inc_svc.resolver_incidencia(self._selected_id)
        QMessageBox.information(self, "OK" if ok else "Error", msg)
        self._ver_todas()

    def _seleccionar(self, row, _):
        item = self.table.item(row, 0)
        if item:
            self._selected_id = int(item.text())

    def _ver_todas(self):    self._mostrar(self.inc_svc.get_all())
    def _ver_pendientes(self): self._mostrar(self.inc_svc.get_pendientes())

    def _mostrar(self, lista):
        self.table.setRowCount(len(lista))
        for row, i in enumerate(lista):
            resuelta_txt = "✅ Sí" if i.resuelta else "⏳ No"
            color = QColor("#d4efdf") if i.resuelta else QColor("#fef9e7")
            vals = [str(i.id_incidencia), i.nombre_trabajador, i.tipo,
                    i.causa, i.fecha, resuelta_txt, i.observaciones or "—"]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setBackground(color)
                self.table.setItem(row, col, item)

    def _inp(self):
        return "padding: 6px; border: 1px solid #dcdde1; border-radius: 6px;"

    def _btn(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 7px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")
