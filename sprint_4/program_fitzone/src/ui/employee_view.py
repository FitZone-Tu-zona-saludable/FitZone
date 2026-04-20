from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView, QTextEdit
)
from PySide6.QtCore import Qt
from src.services.worker_service import WorkerService
from src.models.employee import Employee


class EmployeeView(QWidget):
    """Consulta y actualización de empleados con datos laborales (Sprint 3 - Andrés)."""

    ESTADOS = [Employee.ESTADO_ACTIVO, Employee.ESTADO_INACTIVO, Employee.ESTADO_INCAPACITADO]

    def __init__(self, worker_service: WorkerService):
        super().__init__()
        self.ws = worker_service
        self._selected_id = None

        self.setWindowTitle("FitZone – Gestión de Empleados")
        self.setGeometry(200, 100, 980, 620)
        self.setStyleSheet("background-color: #f5f6fa;")

        main = QVBoxLayout()

        title = QLabel("👤 Gestión de Empleados")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        main.addWidget(title)

        # ── FORMULARIO ALTA ──────────────────────────────────────────
        alta_lbl = QLabel("Registrar nuevo empleado:")
        alta_lbl.setStyleSheet("font-weight: bold; margin-top: 6px;")
        main.addWidget(alta_lbl)

        f1 = QHBoxLayout()
        self.f_nombre = QLineEdit(); self.f_nombre.setPlaceholderText("Nombre")
        self.f_cargo = QLineEdit(); self.f_cargo.setPlaceholderText("Cargo")
        self.f_tel = QLineEdit(); self.f_tel.setPlaceholderText("Teléfono")
        self.f_correo = QLineEdit(); self.f_correo.setPlaceholderText("Correo")
        self.f_ingreso = QLineEdit(); self.f_ingreso.setPlaceholderText("Fecha ingreso YYYY-MM-DD")
        for w in [self.f_nombre, self.f_cargo, self.f_tel, self.f_correo, self.f_ingreso]:
            w.setStyleSheet(self._inp()); f1.addWidget(w)
        main.addLayout(f1)

        f2 = QHBoxLayout()
        self.f_salario = QLineEdit(); self.f_salario.setPlaceholderText("Salario")
        self.f_descuento = QLineEdit(); self.f_descuento.setPlaceholderText("Descuento %")
        self.f_contrato = QComboBox()
        self.f_contrato.addItems(["indefinido", "fijo", "obra_labor", "aprendizaje"])
        self.f_contrato.setStyleSheet(self._inp())
        self.f_modalidad = QComboBox()
        self.f_modalidad.addItems(["presencial", "remoto", "hibrido"])
        self.f_modalidad.setStyleSheet(self._inp())
        btn_alta = QPushButton("➕ Registrar Empleado")
        btn_alta.setStyleSheet(self._btn("#00b894"))
        btn_alta.clicked.connect(self._registrar)
        for w in [self.f_salario, self.f_descuento, self.f_contrato, self.f_modalidad, btn_alta]:
            f2.addWidget(w)
        main.addLayout(f2)

        # ── ACCIONES SOBRE SELECCIÓN ─────────────────────────────────
        act = QHBoxLayout()
        self.cmb_estado = QComboBox()
        self.cmb_estado.addItems(self.ESTADOS)
        self.cmb_estado.setStyleSheet(self._inp())

        btn_estado = QPushButton("🔄 Actualizar Estado")
        btn_estado.setStyleSheet(self._btn("#e17055"))
        btn_estado.clicked.connect(self._actualizar_estado)

        btn_info = QPushButton("🔍 Ver Info Completa")
        btn_info.setStyleSheet(self._btn("#6c5ce7"))
        btn_info.clicked.connect(self._ver_info)

        btn_refresh = QPushButton("🔄 Refrescar")
        btn_refresh.setStyleSheet(self._btn("#636e72"))
        btn_refresh.clicked.connect(self._cargar_tabla)

        btn_volver = QPushButton("⬅ Volver")
        btn_volver.setStyleSheet(self._btn("#2d3436"))
        btn_volver.clicked.connect(self.close)

        for w in [QLabel("Nuevo estado:"), self.cmb_estado, btn_estado,
                  btn_info, btn_refresh, btn_volver]:
            act.addWidget(w)
        main.addLayout(act)

        # ── TABLA ───────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Cargo", "Correo", "Estado", "Salario", "Descuento%", "Neto"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self._seleccionar)
        main.addWidget(self.table)

        # ── PANEL INFO ───────────────────────────────────────────────
        self.txt_info = QTextEdit()
        self.txt_info.setReadOnly(True)
        self.txt_info.setMaximumHeight(130)
        self.txt_info.setStyleSheet(
            "background: white; border: 1px solid #dcdde1; border-radius: 8px; padding: 6px;"
        )
        main.addWidget(self.txt_info)

        self.setLayout(main)
        self._cargar_tabla()

    def _registrar(self):
        try:
            salario = float(self.f_salario.text() or 0)
            descuento = float(self.f_descuento.text() or 0)
        except ValueError:
            QMessageBox.warning(self, "Error", "Salario y descuento deben ser numéricos")
            return
        if not self.f_nombre.text() or not self.f_cargo.text():
            QMessageBox.warning(self, "Error", "Nombre y cargo son obligatorios")
            return
        self.ws.register_employee(
            self.f_nombre.text(), self.f_cargo.text(),
            self.f_tel.text(), self.f_correo.text(),
            fecha_ingreso=self.f_ingreso.text(),
            tipo_contrato=self.f_contrato.currentText(),
            modalidad=self.f_modalidad.currentText(),
            salario=salario, descuento=descuento
        )
        QMessageBox.information(self, "OK", f"Empleado {self.f_nombre.text()} registrado")
        for f in [self.f_nombre, self.f_cargo, self.f_tel, self.f_correo,
                  self.f_ingreso, self.f_salario, self.f_descuento]:
            f.clear()
        self._cargar_tabla()

    def _actualizar_estado(self):
        if not self._selected_id:
            QMessageBox.warning(self, "Aviso", "Selecciona un empleado en la tabla")
            return
        nuevo = self.cmb_estado.currentText()
        ok, msg = self.ws.actualizar_estado_laboral(self._selected_id, nuevo)
        QMessageBox.information(self, "OK" if ok else "Error", msg)
        self._cargar_tabla()

    def _ver_info(self):
        if not self._selected_id:
            QMessageBox.warning(self, "Aviso", "Selecciona un empleado")
            return
        info = self.ws.get_info_completa_empleado(self._selected_id)
        if not info:
            self.txt_info.setText("No se encontró información completa (¿es empleado formal?)")
            return
        self.txt_info.setText(
            f"ID: {info['id_trabajador']}  |  Nombre: {info['nombre']}  |  Cargo: {info['cargo']}\n"
            f"Correo: {info['correo']}  |  Teléfono: {info['telefono']}\n"
            f"Ingreso: {info.get('fecha_ingreso','—')}  |  Contrato: {info.get('tipo_contrato','—')}  "
            f"|  Modalidad: {info.get('modalidad','—')}\n"
            f"Estado laboral: {info.get('estado_laboral','—').upper()}\n"
            f"Salario bruto: ${info.get('salario',0):,.2f}  |  "
            f"Descuento: {info.get('descuento',0)}%  |  "
            f"Salario NETO: ${info.get('salario_neto',0):,.2f}"
        )

    def _seleccionar(self, row, _):
        item = self.table.item(row, 0)
        if item:
            self._selected_id = int(item.text())

    def _cargar_tabla(self):
        empleados = self.ws.get_employees()
        self.table.setRowCount(len(empleados))
        for row, e in enumerate(empleados):
            self.table.setItem(row, 0, QTableWidgetItem(str(e.id_trabajador)))
            self.table.setItem(row, 1, QTableWidgetItem(e.nombre))
            self.table.setItem(row, 2, QTableWidgetItem(e.cargo))
            self.table.setItem(row, 3, QTableWidgetItem(e.correo))
            self.table.setItem(row, 4, QTableWidgetItem(e.estado_laboral))
            self.table.setItem(row, 5, QTableWidgetItem(f"${e.salario:,.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{e.descuento}%"))
            self.table.setItem(row, 7, QTableWidgetItem(f"${e.salario_neto:,.2f}"))

    def _inp(self):
        return "padding: 6px; border: 1px solid #dcdde1; border-radius: 6px;"

    def _btn(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 7px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")
