# employee_payment_view.py
# Vista de pago de empleados con detalle de horas, descuentos y valor final
# Sprint 4 - Alex (RF26: Administrar pago de empleado)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QFrame, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt
from frontend.controllers.employee_payment_controller import EmployeePaymentController
from frontend.resources.theme import COLORS


class EmployeePaymentView(QWidget):
    """Vista de liquidación y pago de empleados."""

    def __init__(self):
        super().__init__()
        self.controller = EmployeePaymentController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("💼  Administración de Pago de Empleados")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Liquida el salario considerando horas trabajadas, tipo de contrato y descuentos.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Formulario de liquidación ────────────────────────────────
        form_lbl = QLabel("Nueva liquidación")
        form_lbl.setObjectName("H2")
        layout.addWidget(form_lbl)

        row1 = QHBoxLayout()
        self.inp_id    = QLineEdit(); self.inp_id.setPlaceholderText("ID Trabajador")
        self.inp_nombre= QLineEdit(); self.inp_nombre.setPlaceholderText("Nombre Trabajador")
        self.combo_con = QComboBox()
        self.combo_con.addItems(["indefinido", "termino_fijo", "prestacion_servicios"])
        for w in [self.inp_id, self.inp_nombre]:
            row1.addWidget(w)
        row1.addWidget(QLabel("Contrato:")); row1.addWidget(self.combo_con)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        lbl_h = QLabel("Horas:")
        self.spin_horas = QSpinBox(); self.spin_horas.setRange(0, 300)
        lbl_vh = QLabel("Valor/hora ($):")
        self.spin_valor = QDoubleSpinBox()
        self.spin_valor.setRange(0, 500000); self.spin_valor.setSingleStep(1000)
        lbl_desc = QLabel("Descuentos ($):")
        self.spin_desc = QDoubleSpinBox()
        self.spin_desc.setRange(0, 200000); self.spin_desc.setSingleStep(1000)
        btn_calc = QPushButton("📄  Liquidar")
        btn_calc.setObjectName("Primary")
        btn_calc.clicked.connect(self._create_liquidation)
        for w in [lbl_h, self.spin_horas, lbl_vh, self.spin_valor,
                  lbl_desc, self.spin_desc, btn_calc]:
            row2.addWidget(w)
        layout.addLayout(row2)

        # ── Tabla ────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Trabajador", "Horas", "Valor/h", "Bruto ($)",
            "Descuentos ($)", "Neto ($)", "Estado", "Fecha"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_data)
        btn_pay = QPushButton("✅  Marcar como pagado")
        btn_pay.setObjectName("Primary")
        btn_pay.clicked.connect(self._mark_paid)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch()
        btn_row.addWidget(btn_pay)
        layout.addLayout(btn_row)

    def _load_data(self):
        records = self.controller.list_payments()
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id_pago"])))
            self.table.setItem(i, 1, QTableWidgetItem(r["nombre_trabajador"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(r["horas_trabajadas"])))
            self.table.setItem(i, 3, QTableWidgetItem(f"${r['valor_hora']:,.0f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"${r['bruto']:,.0f}"))
            self.table.setItem(i, 5, QTableWidgetItem(f"${r['descuentos']:,.0f}"))
            self.table.setItem(i, 6, QTableWidgetItem(f"${r['neto']:,.0f}"))
            self.table.setItem(i, 7, QTableWidgetItem(r["estado"]))
            self.table.setItem(i, 8, QTableWidgetItem(r["fecha"]))

    def _create_liquidation(self):
        id_t   = self.inp_id.text().strip()
        nombre = self.inp_nombre.text().strip()
        if not id_t or not nombre:
            QMessageBox.warning(self, "Validación", "ID y nombre son obligatorios.")
            return
        try:
            id_t = int(id_t)
        except ValueError:
            QMessageBox.warning(self, "Validación", "El ID debe ser un número."); return
        result = self.controller.create_liquidation(
            id_t, nombre,
            self.spin_horas.value(), self.spin_valor.value(),
            self.spin_desc.value(), self.combo_con.currentText()
        )
        if result["success"]:
            neto = result["data"]["neto"]
            QMessageBox.information(
                self, "Liquidación creada",
                f"Liquidación registrada.\nValor neto a pagar: ${neto:,.0f}"
            )
            self.inp_id.clear(); self.inp_nombre.clear()
            self._load_data()

    def _mark_paid(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona una liquidación primero."); return
        id_p = int(self.table.item(row, 0).text())
        result = self.controller.mark_paid(id_p)
        if result["success"]:
            QMessageBox.information(self, "Pagado", "Liquidación marcada como pagada."); self._load_data()
