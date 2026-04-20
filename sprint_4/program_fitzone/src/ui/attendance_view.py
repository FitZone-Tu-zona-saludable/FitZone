from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from src.services.attendance_service import AttendanceService
from src.services.auth_service import AuthService


class AttendanceView(QWidget):
    """Vista del afiche de asistencia de clientes (Sprint 3 - Andrés)."""

    def __init__(self, auth: AuthService, attendance: AttendanceService):
        super().__init__()
        self.auth = auth
        self.attendance = attendance

        self.setWindowTitle("FitZone – Registro de Asistencia")
        self.setGeometry(200, 100, 820, 560)
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()

        # ── TÍTULO ──────────────────────────────────────────────────
        title = QLabel("📋 Registro de Asistencia de Clientes")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        layout.addWidget(title)

        # ── FORMULARIO ──────────────────────────────────────────────
        form = QHBoxLayout()

        self.cmb_cliente = QComboBox()
        self.cmb_cliente.setStyleSheet(self._input_style())
        self._cargar_clientes()

        self.txt_clase = QLineEdit()
        self.txt_clase.setPlaceholderText("Clase / Servicio (yoga, cardio…)")
        self.txt_clase.setStyleSheet(self._input_style())

        self.txt_obs = QLineEdit()
        self.txt_obs.setPlaceholderText("Observaciones (opcional)")
        self.txt_obs.setStyleSheet(self._input_style())

        form.addWidget(QLabel("Cliente:"))
        form.addWidget(self.cmb_cliente)
        form.addWidget(self.txt_clase)
        form.addWidget(self.txt_obs)
        layout.addLayout(form)

        # ── BOTONES ─────────────────────────────────────────────────
        btns = QHBoxLayout()
        btn_registrar = QPushButton("✅ Registrar Entrada")
        btn_registrar.setStyleSheet(self._btn_style("#00b894"))
        btn_registrar.clicked.connect(self._registrar)

        btn_hoy = QPushButton("📅 Ver Hoy")
        btn_hoy.setStyleSheet(self._btn_style("#0984e3"))
        btn_hoy.clicked.connect(self._ver_hoy)

        btn_todos = QPushButton("🔄 Ver Todos")
        btn_todos.setStyleSheet(self._btn_style("#636e72"))
        btn_todos.clicked.connect(self._ver_todos)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.setStyleSheet(self._btn_style("#2d3436"))
        btn_volver.clicked.connect(self.close)

        for b in [btn_registrar, btn_hoy, btn_todos, btn_volver]:
            btns.addWidget(b)
        layout.addLayout(btns)

        # ── TABLA ───────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Cliente", "Fecha", "Hora", "Clase/Servicio"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self._ver_hoy()

    def _cargar_clientes(self):
        self.cmb_cliente.clear()
        for u in self.auth.get_users():
            self.cmb_cliente.addItem(f"{u.get_name()} ({u.get_email()})", u)

    def _registrar(self):
        cliente = self.cmb_cliente.currentData()
        if not cliente:
            QMessageBox.warning(self, "Error", "Selecciona un cliente")
            return
        clase = self.txt_clase.text().strip()
        obs = self.txt_obs.text().strip()
        a = self.attendance.registrar_entrada(
            cliente.id_cliente, cliente.get_name(), clase, obs
        )
        QMessageBox.information(self, "OK",
                                f"Entrada registrada para {a.nombre_cliente} a las {a.hora}")
        self.txt_clase.clear()
        self.txt_obs.clear()
        self._ver_hoy()

    def _ver_hoy(self):
        self._mostrar(self.attendance.get_today())

    def _ver_todos(self):
        self._mostrar(self.attendance.get_all())

    def _mostrar(self, registros):
        self.table.setRowCount(len(registros))
        for row, r in enumerate(registros):
            self.table.setItem(row, 0, QTableWidgetItem(str(r.id_asistencia)))
            self.table.setItem(row, 1, QTableWidgetItem(r.nombre_cliente))
            self.table.setItem(row, 2, QTableWidgetItem(r.fecha))
            self.table.setItem(row, 3, QTableWidgetItem(r.hora))
            self.table.setItem(row, 4, QTableWidgetItem(r.clase_servicio or "—"))

    def _input_style(self):
        return "padding: 6px; border: 1px solid #dcdde1; border-radius: 6px;"

    def _btn_style(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 8px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")
