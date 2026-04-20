# accounting_view.py
# Interfaz contable para visualizar pagos, saldos y cobros
# Sprint 3 - Alex (RF21: Administrar cuenta / contabilidad)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QMessageBox, QHeaderView, QFrame
)
from PySide6.QtCore import Qt
from frontend.controllers.accounting_controller import AccountingController
from frontend.resources.theme import COLORS


class AccountingView(QWidget):
    """Vista contable: ingresos, cobros pendientes y saldos por pagar."""

    def __init__(self):
        super().__init__()
        self.controller = AccountingController()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # ── Título ──────────────────────────────────────────────────
        title = QLabel("💰  Administración Contable")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ── Tarjetas de resumen ──────────────────────────────────────
        summary = QHBoxLayout()
        self.lbl_ingresos  = self._summary_card("Total ingresos", "$ 0", COLORS["success"])
        self.lbl_pendiente = self._summary_card("Total pendiente", "$ 0", COLORS["warning"])
        summary.addWidget(self.lbl_ingresos[0])
        summary.addWidget(self.lbl_pendiente[0])
        layout.addLayout(summary)

        # ── Formulario nueva entrada ─────────────────────────────────
        form_lbl = QLabel("Nueva entrada contable")
        form_lbl.setObjectName("H2")
        layout.addWidget(form_lbl)

        form_row = QHBoxLayout()
        self.inp_concepto  = QLineEdit(); self.inp_concepto.setPlaceholderText("Concepto")
        self.inp_monto     = QLineEdit(); self.inp_monto.setPlaceholderText("Monto ($)")
        self.inp_referencia= QLineEdit(); self.inp_referencia.setPlaceholderText("Referencia")
        self.combo_tipo    = QComboBox()
        self.combo_tipo.addItems(["ingreso", "cobro_pendiente", "saldo_por_pagar", "descuento"])
        btn_add = QPushButton("➕  Agregar")
        btn_add.setObjectName("Primary")
        btn_add.clicked.connect(self._add_entry)
        for w in [self.inp_concepto, self.inp_monto, self.combo_tipo,
                  self.inp_referencia, btn_add]:
            form_row.addWidget(w)
        layout.addLayout(form_row)

        # ── Tabla ────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Concepto", "Tipo", "Monto ($)", "Estado", "Referencia", "Fecha"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # ── Botones de acción ────────────────────────────────────────
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

    def _summary_card(self, label, value, color):
        frame = QFrame()
        frame.setObjectName("Card")
        v = QVBoxLayout(frame)
        lbl = QLabel(label)
        lbl.setObjectName("Muted")
        lbl.setAlignment(Qt.AlignCenter)
        val_lbl = QLabel(value)
        val_lbl.setAlignment(Qt.AlignCenter)
        val_lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
        v.addWidget(lbl)
        v.addWidget(val_lbl)
        return frame, val_lbl

    def _load_data(self):
        records = self.controller.list_entries()
        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id_entrada"])))
            self.table.setItem(i, 1, QTableWidgetItem(r["concepto"]))
            self.table.setItem(i, 2, QTableWidgetItem(r["tipo"]))
            self.table.setItem(i, 3, QTableWidgetItem(f"${r['monto']:,.0f}"))
            self.table.setItem(i, 4, QTableWidgetItem(r["estado"]))
            self.table.setItem(i, 5, QTableWidgetItem(r["referencia"]))
            self.table.setItem(i, 6, QTableWidgetItem(r["fecha"]))
        # Actualizar resumen
        self.lbl_ingresos[1].setText(f"${self.controller.total_ingresos():,.0f}")
        self.lbl_pendiente[1].setText(f"${self.controller.total_pendiente():,.0f}")

    def _add_entry(self):
        concepto = self.inp_concepto.text().strip()
        tipo     = self.combo_tipo.currentText()
        ref      = self.inp_referencia.text().strip()
        try:
            monto = float(self.inp_monto.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validación", "El monto debe ser un número.")
            return
        if not concepto:
            QMessageBox.warning(self, "Validación", "El concepto es obligatorio.")
            return
        self.controller.add_entry(concepto, tipo, monto, ref)
        self.inp_concepto.clear(); self.inp_monto.clear(); self.inp_referencia.clear()
        self._load_data()

    def _mark_paid(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección", "Selecciona una entrada primero.")
            return
        id_e = int(self.table.item(row, 0).text())
        result = self.controller.mark_paid(id_e)
        if result["success"]:
            QMessageBox.information(self, "Actualizado", "Entrada marcada como pagada.")
            self._load_data()
