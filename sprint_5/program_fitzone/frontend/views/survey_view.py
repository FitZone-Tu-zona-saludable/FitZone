# survey_view.py
# Vista de encuesta de satisfacción para evaluación de entrenadores e instalaciones
# Sprint 4 - Alex (RF27: Evaluación de entrenadores)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QSpinBox, QFrame, QTabWidget, QTextEdit
)
from PySide6.QtCore import Qt
from frontend.controllers.survey_controller import SurveyController
from frontend.resources.theme import COLORS


class SurveyView(QWidget):
    """Vista de encuesta de satisfacción y resultados de evaluación de entrenadores."""

    def __init__(self):
        super().__init__()
        self.controller = SurveyController()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("📝  Encuesta de Satisfacción")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Evalúa entrenadores e instalaciones. Consulta el promedio de satisfacción.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        tabs = QTabWidget()
        tabs.addTab(self._build_form_tab(),    "✍️ Registrar Encuesta")
        tabs.addTab(self._build_results_tab(), "📊 Resultados")
        layout.addWidget(tabs)

    # ── Tab 1: Formulario de encuesta ─────────────────────────────────
    def _build_form_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(20, 16, 20, 16)
        v.setSpacing(14)

        # Datos del cliente
        lbl_cli = QLabel("Datos del cliente")
        lbl_cli.setObjectName("H2")
        v.addWidget(lbl_cli)

        row_cli = QHBoxLayout()
        self.inp_id_cli  = QLineEdit(); self.inp_id_cli.setPlaceholderText("ID Cliente")
        self.inp_nom_cli = QLineEdit(); self.inp_nom_cli.setPlaceholderText("Nombre Cliente")
        row_cli.addWidget(self.inp_id_cli); row_cli.addWidget(self.inp_nom_cli)
        v.addLayout(row_cli)

        # Datos del entrenador
        lbl_ent = QLabel("Entrenador evaluado (opcional)")
        lbl_ent.setObjectName("H2")
        v.addWidget(lbl_ent)

        row_ent = QHBoxLayout()
        self.inp_id_ent  = QLineEdit(); self.inp_id_ent.setPlaceholderText("ID Entrenador")
        self.inp_nom_ent = QLineEdit(); self.inp_nom_ent.setPlaceholderText("Nombre Entrenador")
        row_ent.addWidget(self.inp_id_ent); row_ent.addWidget(self.inp_nom_ent)
        v.addLayout(row_ent)

        # Puntajes
        lbl_scores = QLabel("Calificaciones (1 = Malo · 5 = Excelente)")
        lbl_scores.setObjectName("H2")
        v.addWidget(lbl_scores)

        score_row = QHBoxLayout()
        lbl_pe = QLabel("Entrenador:")
        self.spin_ent  = QSpinBox(); self.spin_ent.setRange(1, 5); self.spin_ent.setValue(5)
        lbl_pi = QLabel("Instalaciones:")
        self.spin_inst = QSpinBox(); self.spin_inst.setRange(1, 5); self.spin_inst.setValue(5)
        for w2 in [lbl_pe, self.spin_ent, lbl_pi, self.spin_inst]:
            score_row.addWidget(w2)
        v.addLayout(score_row)

        # Comentario
        lbl_com = QLabel("Comentario o sugerencia:")
        lbl_com.setObjectName("H2")
        v.addWidget(lbl_com)
        self.inp_comentario = QLineEdit()
        self.inp_comentario.setPlaceholderText("Escribe tu comentario o sugerencia...")
        v.addWidget(self.inp_comentario)

        btn_submit = QPushButton("📨  Enviar encuesta")
        btn_submit.setObjectName("Primary")
        btn_submit.clicked.connect(self._submit_survey)
        v.addWidget(btn_submit, 0, Qt.AlignRight)
        v.addStretch()
        return w

    # ── Tab 2: Resultados ─────────────────────────────────────────────
    def _build_results_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(10)

        btn_load = QPushButton("🔄  Cargar resultados")
        btn_load.setObjectName("Primary")
        btn_load.clicked.connect(self._load_results)
        v.addWidget(btn_load, 0, Qt.AlignRight)

        # Promedio global
        self.lbl_avg_inst = QLabel("Promedio instalaciones: —")
        self.lbl_avg_inst.setObjectName("H2")
        v.addWidget(self.lbl_avg_inst)

        # Tabla de encuestas
        self.tbl = QTableWidget()
        self.tbl.setColumnCount(7)
        self.tbl.setHorizontalHeaderLabels([
            "ID", "Cliente", "Entrenador eval.", "⭐ Entrenador",
            "⭐ Instalaciones", "Comentario", "Fecha"
        ])
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        v.addWidget(self.tbl)

        # Resultados por entrenador
        lbl_per = QLabel("Promedio por entrenador")
        lbl_per.setObjectName("H2")
        v.addWidget(lbl_per)
        self.txt_trainer_scores = QTextEdit()
        self.txt_trainer_scores.setReadOnly(True)
        self.txt_trainer_scores.setMaximumHeight(120)
        v.addWidget(self.txt_trainer_scores)
        return w

    def _submit_survey(self):
        id_cli = self.inp_id_cli.text().strip()
        nom    = self.inp_nom_cli.text().strip()
        if not id_cli or not nom:
            QMessageBox.warning(self, "Validación", "ID y nombre del cliente son obligatorios.")
            return
        try:
            id_cli = int(id_cli)
        except ValueError:
            QMessageBox.warning(self, "Validación", "El ID debe ser un número."); return

        id_ent  = self.inp_id_ent.text().strip() or None
        nom_ent = self.inp_nom_ent.text().strip()
        if id_ent:
            try:
                id_ent = int(id_ent)
            except ValueError:
                id_ent = None

        result = self.controller.submit_survey(
            id_cli, nom,
            self.spin_ent.value(), self.spin_inst.value(),
            self.inp_comentario.text().strip(), id_ent, nom_ent
        )
        if result["success"]:
            QMessageBox.information(self, "Encuesta enviada",
                                    "¡Gracias! Tu encuesta fue registrada correctamente.")
            for inp in [self.inp_id_cli, self.inp_nom_cli,
                        self.inp_id_ent, self.inp_nom_ent, self.inp_comentario]:
                inp.clear()

    def _load_results(self):
        surveys = self.controller.list_surveys()
        self.tbl.setRowCount(len(surveys))
        for i, s in enumerate(surveys):
            self.tbl.setItem(i, 0, QTableWidgetItem(str(s["id_encuesta"])))
            self.tbl.setItem(i, 1, QTableWidgetItem(s["nombre_cliente"]))
            self.tbl.setItem(i, 2, QTableWidgetItem(s.get("nombre_entrenador", "—")))
            self.tbl.setItem(i, 3, QTableWidgetItem(str(s["puntaje_entrenador"])))
            self.tbl.setItem(i, 4, QTableWidgetItem(str(s["puntaje_instalaciones"])))
            self.tbl.setItem(i, 5, QTableWidgetItem(s["comentario"]))
            self.tbl.setItem(i, 6, QTableWidgetItem(s["fecha"]))

        avg_inst = self.controller.avg_facility()
        self.lbl_avg_inst.setText(f"Promedio instalaciones: {avg_inst:.1f} / 5")

        trainer_avgs = self.controller.avg_trainer_scores()
        if trainer_avgs:
            lines = [f"• {k[1]} (ID {k[0]}): {v:.1f}/5"
                     for k, v in trainer_avgs.items()]
            self.txt_trainer_scores.setText("\n".join(lines))
        else:
            self.txt_trainer_scores.setText("No hay evaluaciones de entrenadores aún.")
