# performance_view.py
# Vista para que entrenadores evalúen el desempeño de los usuarios
# Sprint 3 - Alex (RF6: Evaluar desempeño de usuarios)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QSpinBox
)
from PySide6.QtCore import Qt
from frontend.controllers.performance_controller import PerformanceController


class PerformanceView(QWidget):
    """Vista para que entrenadores evalúen el desempeño de los clientes."""

    def __init__(self):
        super().__init__()
        self.controller = PerformanceController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("⭐  Evaluación de Desempeño")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Los entrenadores registran la evaluación de progreso de cada cliente.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Formulario ───────────────────────────────────────────────
        form_lbl = QLabel("Nueva evaluación")
        form_lbl.setObjectName("H2")
        layout.addWidget(form_lbl)

        row1 = QHBoxLayout()
        self.inp_id_cli  = QLineEdit(); self.inp_id_cli.setPlaceholderText("ID Cliente")
        self.inp_nom_cli = QLineEdit(); self.inp_nom_cli.setPlaceholderText("Nombre Cliente")
        self.inp_id_ent  = QLineEdit(); self.inp_id_ent.setPlaceholderText("ID Entrenador")
        self.inp_nom_ent = QLineEdit(); self.inp_nom_ent.setPlaceholderText("Nombre Entrenador")
        for w in [self.inp_id_cli, self.inp_nom_cli, self.inp_id_ent, self.inp_nom_ent]:
            row1.addWidget(w)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.spin_puntaje = QSpinBox()
        self.spin_puntaje.setRange(1, 10)
        self.spin_puntaje.setValue(7)
        self.inp_obs = QLineEdit()
        self.inp_obs.setPlaceholderText("Observaciones del entrenador")
        btn_eval = QPushButton("✅  Registrar evaluación")
        btn_eval.setObjectName("Primary")
        btn_eval.clicked.connect(self._create_eval)
        row2.addWidget(QLabel("Puntaje (1-10):"))
        row2.addWidget(self.spin_puntaje)
        row2.addWidget(self.inp_obs)
        row2.addWidget(btn_eval)
        layout.addLayout(row2)

        # ── Tabla de evaluaciones ────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Nombre Cliente",
            "Entrenador", "Nombre Entrenador", "Puntaje", "Fecha"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_data)
        layout.addWidget(btn_refresh, 0, Qt.AlignLeft)

    def _load_data(self):
        evals = self.controller.list_evaluations()
        self.table.setRowCount(len(evals))
        for i, e in enumerate(evals):
            self.table.setItem(i, 0, QTableWidgetItem(str(e["id_eval"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(e["id_cliente"])))
            self.table.setItem(i, 2, QTableWidgetItem(e["nombre_cliente"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(e["id_entrenador"])))
            self.table.setItem(i, 4, QTableWidgetItem(e["nombre_entrenador"]))
            self.table.setItem(i, 5, QTableWidgetItem(str(e["puntaje"])))
            self.table.setItem(i, 6, QTableWidgetItem(e["fecha"]))

    def _create_eval(self):
        id_cli = self.inp_id_cli.text().strip()
        nom_cli = self.inp_nom_cli.text().strip()
        id_ent = self.inp_id_ent.text().strip()
        nom_ent = self.inp_nom_ent.text().strip()
        if not all([id_cli, nom_cli, id_ent, nom_ent]):
            QMessageBox.warning(self, "Validación", "Todos los campos son obligatorios.")
            return
        try:
            id_cli = int(id_cli); id_ent = int(id_ent)
        except ValueError:
            QMessageBox.warning(self, "Validación", "Los IDs deben ser números.")
            return
        puntaje = self.spin_puntaje.value()
        obs     = self.inp_obs.text().strip()
        self.controller.create_evaluation(id_cli, nom_cli, id_ent, nom_ent, puntaje, obs)
        QMessageBox.information(self, "Registrado", "Evaluación guardada correctamente.")
        for inp in [self.inp_id_cli, self.inp_nom_cli, self.inp_id_ent, self.inp_nom_ent, self.inp_obs]:
            inp.clear()
        self._load_data()
