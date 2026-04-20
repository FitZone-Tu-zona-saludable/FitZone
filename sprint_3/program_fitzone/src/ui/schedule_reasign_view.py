from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView
)
from src.services.schedule_service import ScheduleService
from src.services.trainer_service import TrainerService


class ScheduleReasignView(QWidget):
    """Vista para modificar horarios por eventos externos y reasignar entrenadores (Sprint 3 - Andrés)."""

    def __init__(self, schedule_service: ScheduleService, trainer_service: TrainerService):
        super().__init__()
        self.ss = schedule_service
        self.ts = trainer_service
        self._selected_horario = None

        self.setWindowTitle("FitZone – Horarios y Reasignación")
        self.setGeometry(200, 100, 960, 560)
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()

        title = QLabel("📅 Modificación de Horarios y Reasignación de Entrenadores")
        title.setStyleSheet("font-size: 17px; font-weight: bold; padding: 6px;")
        layout.addWidget(title)

        # ── MODIFICAR HORARIO ────────────────────────────────────────
        mod_lbl = QLabel("Modificar horario por evento externo:")
        mod_lbl.setStyleSheet("font-weight: bold; margin-top: 4px;")
        layout.addWidget(mod_lbl)

        mod_form = QHBoxLayout()
        self.txt_nueva_fecha = QLineEdit()
        self.txt_nueva_fecha.setPlaceholderText("Nueva fecha YYYY-MM-DD")
        self.txt_nueva_fecha.setStyleSheet(self._inp())

        self.txt_nueva_hi = QLineEdit()
        self.txt_nueva_hi.setPlaceholderText("Nueva hora inicio HH:MM")
        self.txt_nueva_hi.setStyleSheet(self._inp())

        self.txt_nueva_hf = QLineEdit()
        self.txt_nueva_hf.setPlaceholderText("Nueva hora fin HH:MM")
        self.txt_nueva_hf.setStyleSheet(self._inp())

        self.txt_motivo = QLineEdit()
        self.txt_motivo.setPlaceholderText("Motivo del cambio")
        self.txt_motivo.setStyleSheet(self._inp())

        btn_modificar = QPushButton("📝 Modificar Horario")
        btn_modificar.setStyleSheet(self._btn("#e17055"))
        btn_modificar.clicked.connect(self._modificar_horario)

        for w in [self.txt_nueva_fecha, self.txt_nueva_hi,
                  self.txt_nueva_hf, self.txt_motivo, btn_modificar]:
            mod_form.addWidget(w)
        layout.addLayout(mod_form)

        # ── REASIGNAR ENTRENADOR ─────────────────────────────────────
        rea_lbl = QLabel("Reasignar entrenador al horario seleccionado:")
        rea_lbl.setStyleSheet("font-weight: bold; margin-top: 4px;")
        layout.addWidget(rea_lbl)

        rea_form = QHBoxLayout()
        self.cmb_entrenador = QComboBox()
        self.cmb_entrenador.setStyleSheet(self._inp())
        self._cargar_entrenadores()

        btn_reasignar = QPushButton("🔄 Reasignar Entrenador")
        btn_reasignar.setStyleSheet(self._btn("#0984e3"))
        btn_reasignar.clicked.connect(self._reasignar)

        btn_refresh = QPushButton("🔄 Refrescar")
        btn_refresh.setStyleSheet(self._btn("#636e72"))
        btn_refresh.clicked.connect(self._cargar_tabla)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.setStyleSheet(self._btn("#2d3436"))
        btn_volver.clicked.connect(self.close)

        for w in [QLabel("Entrenador disponible:"), self.cmb_entrenador,
                  btn_reasignar, btn_refresh, btn_volver]:
            rea_form.addWidget(w)
        layout.addLayout(rea_form)

        # ── TABLA HORARIOS ───────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Hora Inicio", "Hora Fin", "Tipo", "Cupos", "ID Entrenador"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self._seleccionar)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self._cargar_tabla()

    def _cargar_entrenadores(self):
        self.cmb_entrenador.clear()
        for t in self.ts.get_disponibles():
            self.cmb_entrenador.addItem(f"{t.nombre} ({t.especialidad})", t)

    def _modificar_horario(self):
        if not self._selected_horario:
            QMessageBox.warning(self, "Aviso", "Selecciona un horario en la tabla")
            return
        motivo = self.txt_motivo.text().strip() or "evento externo"
        s, msg = self.ss.modificar_por_evento_externo(
            self._selected_horario,
            nueva_fecha=self.txt_nueva_fecha.text().strip() or None,
            nueva_hora_inicio=self.txt_nueva_hi.text().strip() or None,
            nueva_hora_fin=self.txt_nueva_hf.text().strip() or None,
            motivo=motivo
        )
        if s:
            QMessageBox.information(self, "OK", msg)
            for f in [self.txt_nueva_fecha, self.txt_nueva_hi,
                      self.txt_nueva_hf, self.txt_motivo]:
                f.clear()
        else:
            QMessageBox.warning(self, "Error", msg)
        self._cargar_tabla()

    def _reasignar(self):
        if not self._selected_horario:
            QMessageBox.warning(self, "Aviso", "Selecciona un horario en la tabla")
            return
        entrenador = self.cmb_entrenador.currentData()
        if not entrenador:
            QMessageBox.warning(self, "Aviso", "No hay entrenadores disponibles")
            return
        ok, msg = self.ss.reasignar_entrenador(
            self._selected_horario, entrenador.id_trabajador, self.ts
        )
        QMessageBox.information(self, "OK" if ok else "Error", msg)
        self._cargar_entrenadores()
        self._cargar_tabla()

    def _seleccionar(self, row, _):
        item = self.table.item(row, 0)
        if item:
            self._selected_horario = int(item.text())

    def _cargar_tabla(self):
        horarios = self.ss.get_schedules()
        self.table.setRowCount(len(horarios))
        for row, s in enumerate(horarios):
            self.table.setItem(row, 0, QTableWidgetItem(str(s.id_horario)))
            self.table.setItem(row, 1, QTableWidgetItem(s.fecha))
            self.table.setItem(row, 2, QTableWidgetItem(s.hora_inicio))
            self.table.setItem(row, 3, QTableWidgetItem(s.hora_fin))
            self.table.setItem(row, 4, QTableWidgetItem(s.tipo))
            self.table.setItem(row, 5, QTableWidgetItem(str(s.cupos)))
            self.table.setItem(row, 6, QTableWidgetItem(
                str(s.id_entrenador) if s.id_entrenador else "Sin asignar"))

    def _inp(self):
        return "padding: 6px; border: 1px solid #dcdde1; border-radius: 6px;"

    def _btn(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 7px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")
