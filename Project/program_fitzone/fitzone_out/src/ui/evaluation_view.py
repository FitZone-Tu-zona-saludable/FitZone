from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView, QSpinBox
)
from PySide6.QtCore import Qt
from src.services.evaluation_service import EvaluationService
from src.services.trainer_service import TrainerService
from src.services.auth_service import AuthService


class EvaluationView(QWidget):
    """Vista para que entrenadores evalúen el desempeño de usuarios (Sprint 3 - Andrés)."""

    def __init__(self, eval_service: EvaluationService,
                 trainer_service: TrainerService,
                 auth_service: AuthService):
        super().__init__()
        self.ev_svc = eval_service
        self.tr_svc = trainer_service
        self.auth = auth_service

        self.setWindowTitle("FitZone – Evaluación de Usuarios")
        self.setGeometry(200, 100, 950, 600)
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()

        title = QLabel("⭐ Evaluación de Desempeño de Usuarios")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        layout.addWidget(title)

        # ── FORMULARIO ──────────────────────────────────────────────
        f1 = QHBoxLayout()
        self.cmb_entrenador = QComboBox()
        self.cmb_entrenador.setStyleSheet(self._inp())
        self._cargar_entrenadores()

        self.cmb_cliente = QComboBox()
        self.cmb_cliente.setStyleSheet(self._inp())
        self._cargar_clientes()

        f1.addWidget(QLabel("Entrenador:"))
        f1.addWidget(self.cmb_entrenador)
        f1.addWidget(QLabel("Cliente:"))
        f1.addWidget(self.cmb_cliente)
        layout.addLayout(f1)

        f2 = QHBoxLayout()
        self.spin_puntualidad = QSpinBox()
        self.spin_puntualidad.setRange(0, 10)
        self.spin_rendimiento = QSpinBox()
        self.spin_rendimiento.setRange(0, 10)
        self.spin_actitud = QSpinBox()
        self.spin_actitud.setRange(0, 10)
        self.txt_comentarios = QLineEdit()
        self.txt_comentarios.setPlaceholderText("Comentarios (opcional)")
        self.txt_comentarios.setStyleSheet(self._inp())

        for sp in [self.spin_puntualidad, self.spin_rendimiento, self.spin_actitud]:
            sp.setStyleSheet(self._inp())

        btn_evaluar = QPushButton("⭐ Registrar Evaluación")
        btn_evaluar.setStyleSheet(self._btn("#6c5ce7"))
        btn_evaluar.clicked.connect(self._evaluar)

        f2.addWidget(QLabel("Puntualidad (0-10):"))
        f2.addWidget(self.spin_puntualidad)
        f2.addWidget(QLabel("Rendimiento:"))
        f2.addWidget(self.spin_rendimiento)
        f2.addWidget(QLabel("Actitud:"))
        f2.addWidget(self.spin_actitud)
        f2.addWidget(self.txt_comentarios)
        f2.addWidget(btn_evaluar)
        layout.addLayout(f2)

        # ── BOTONES CONSULTA ─────────────────────────────────────────
        btns = QHBoxLayout()
        btn_todos = QPushButton("📋 Todas las Evaluaciones")
        btn_todos.setStyleSheet(self._btn("#636e72"))
        btn_todos.clicked.connect(self._ver_todas)

        btn_promedio = QPushButton("📊 Promedio del Cliente")
        btn_promedio.setStyleSheet(self._btn("#0984e3"))
        btn_promedio.clicked.connect(self._ver_promedio)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.setStyleSheet(self._btn("#2d3436"))
        btn_volver.clicked.connect(self.close)

        for b in [btn_todos, btn_promedio, btn_volver]:
            btns.addWidget(b)
        layout.addLayout(btns)

        # ── TABLA ───────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Entrenador", "Cliente", "Puntualidad", "Rendimiento", "Actitud", "Promedio", "Fecha"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self._ver_todas()

    def _cargar_entrenadores(self):
        self.cmb_entrenador.clear()
        for t in self.tr_svc.get_trainers():
            self.cmb_entrenador.addItem(f"{t.nombre} ({t.especialidad})", t)

    def _cargar_clientes(self):
        self.cmb_cliente.clear()
        for u in self.auth.get_users():
            if u.get_role() == "user":
                self.cmb_cliente.addItem(f"{u.get_name()} ({u.get_email()})", u)

    def _evaluar(self):
        entrenador = self.cmb_entrenador.currentData()
        cliente = self.cmb_cliente.currentData()
        if not entrenador or not cliente:
            QMessageBox.warning(self, "Error", "Selecciona entrenador y cliente")
            return
        ev, msg = self.ev_svc.evaluar_usuario(
            entrenador.id_trabajador, entrenador.nombre,
            cliente.id_cliente, cliente.get_name(),
            self.spin_puntualidad.value(),
            self.spin_rendimiento.value(),
            self.spin_actitud.value(),
            self.txt_comentarios.text().strip()
        )
        if ev:
            QMessageBox.information(self, "OK",
                                    f"{msg}\nPromedio: {ev.promedio}/10")
        else:
            QMessageBox.warning(self, "Error", msg)
        self.txt_comentarios.clear()
        self._ver_todas()

    def _ver_todas(self):
        self._mostrar(self.ev_svc.get_all())

    def _ver_promedio(self):
        cliente = self.cmb_cliente.currentData()
        if not cliente:
            return
        prom = self.ev_svc.promedio_cliente(cliente.id_cliente)
        if prom is not None:
            QMessageBox.information(self, "Promedio",
                                    f"Promedio de {cliente.get_name()}: {prom}/10")
        else:
            QMessageBox.information(self, "Sin datos",
                                    f"No hay evaluaciones para {cliente.get_name()}")

    def _mostrar(self, lista):
        self.table.setRowCount(len(lista))
        for row, e in enumerate(lista):
            self.table.setItem(row, 0, QTableWidgetItem(str(e.id_evaluacion)))
            self.table.setItem(row, 1, QTableWidgetItem(e.nombre_entrenador))
            self.table.setItem(row, 2, QTableWidgetItem(e.nombre_cliente))
            self.table.setItem(row, 3, QTableWidgetItem(str(e.puntualidad)))
            self.table.setItem(row, 4, QTableWidgetItem(str(e.rendimiento)))
            self.table.setItem(row, 5, QTableWidgetItem(str(e.actitud)))
            self.table.setItem(row, 6, QTableWidgetItem(str(e.promedio)))
            self.table.setItem(row, 7, QTableWidgetItem(e.fecha))

    def _inp(self):
        return "padding: 6px; border: 1px solid #dcdde1; border-radius: 6px;"

    def _btn(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 7px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")
