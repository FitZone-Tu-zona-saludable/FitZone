from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QHeaderView, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from src.services.accounting_service import AccountingService
from src.services.auth_service import AuthService
from src.models.account_record import AccountRecord


class AccountingView(QWidget):
    """Interfaz contable: pagos, saldos y cobros pendientes (Sprint 3 - Andrés)."""

    def __init__(self, auth: AuthService, accounting: AccountingService):
        super().__init__()
        self.auth = auth
        self.accounting = accounting

        self.setWindowTitle("FitZone – Contabilidad")
        self.setGeometry(200, 100, 900, 600)
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()

        title = QLabel("💰 Módulo Contable")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        layout.addWidget(title)

        # ── RESUMEN ─────────────────────────────────────────────────
        self.lbl_resumen = QLabel()
        self.lbl_resumen.setStyleSheet(
            "background: white; border-radius: 8px; padding: 8px; "
            "font-size: 13px; border: 1px solid #dcdde1;"
        )
        layout.addWidget(self.lbl_resumen)

        # ── FORMULARIO NUEVO COBRO ───────────────────────────────────
        form = QHBoxLayout()
        self.cmb_cliente = QComboBox()
        self.cmb_cliente.setStyleSheet(self._inp())
        self._cargar_clientes()

        self.txt_concepto = QLineEdit()
        self.txt_concepto.setPlaceholderText("Concepto (mensualidad, clase…)")
        self.txt_concepto.setStyleSheet(self._inp())

        self.txt_monto = QLineEdit()
        self.txt_monto.setPlaceholderText("Monto")
        self.txt_monto.setStyleSheet(self._inp())

        self.txt_vencimiento = QLineEdit()
        self.txt_vencimiento.setPlaceholderText("Vencimiento YYYY-MM-DD")
        self.txt_vencimiento.setStyleSheet(self._inp())

        btn_registrar = QPushButton("➕ Registrar Cobro")
        btn_registrar.setStyleSheet(self._btn("#00b894"))
        btn_registrar.clicked.connect(self._registrar_cobro)

        for w in [self.cmb_cliente, self.txt_concepto, self.txt_monto,
                  self.txt_vencimiento, btn_registrar]:
            form.addWidget(w)
        layout.addLayout(form)

        # ── BOTONES FILTRO ───────────────────────────────────────────
        btns = QHBoxLayout()
        for label, color, fn in [
            ("📋 Todos", "#636e72", self._ver_todos),
            ("⏳ Pendientes", "#e17055", self._ver_pendientes),
            ("✅ Pagados", "#00b894", self._ver_pagados),
            ("⚠️ Vencidos", "#d63031", self._ver_vencidos),
            ("✔️ Confirmar Pago", "#0984e3", self._confirmar_pago),
            ("🔍 Verificar Vencimientos", "#6c5ce7", self._verificar),
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
            ["ID", "Cliente", "Concepto", "Monto", "Estado", "Fecha", "Vencimiento"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self._seleccionar)
        layout.addWidget(self.table)

        self._selected_id = None
        self.setLayout(layout)
        self._ver_todos()

    def _cargar_clientes(self):
        self.cmb_cliente.clear()
        for u in self.auth.get_users():
            self.cmb_cliente.addItem(f"{u.get_name()} ({u.get_email()})", u)

    def _registrar_cobro(self):
        cliente = self.cmb_cliente.currentData()
        concepto = self.txt_concepto.text().strip()
        monto_txt = self.txt_monto.text().strip()
        vencimiento = self.txt_vencimiento.text().strip()
        if not concepto or not monto_txt:
            QMessageBox.warning(self, "Error", "Completa concepto y monto")
            return
        try:
            monto = float(monto_txt)
        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser numérico")
            return
        self.accounting.registrar_cobro(
            cliente.id_cliente, cliente.get_name(), concepto, monto, vencimiento
        )
        QMessageBox.information(self, "OK", f"Cobro de ${monto} registrado para {cliente.get_name()}")
        self.txt_concepto.clear(); self.txt_monto.clear(); self.txt_vencimiento.clear()
        self._ver_todos()

    def _confirmar_pago(self):
        if not self._selected_id:
            QMessageBox.warning(self, "Aviso", "Selecciona un registro en la tabla")
            return
        ok, msg = self.accounting.confirmar_pago(self._selected_id)
        QMessageBox.information(self, "OK" if ok else "Error", msg)
        self._ver_todos()

    def _verificar(self):
        vencidos = self.accounting.verificar_vencimientos()
        if vencidos:
            QMessageBox.information(self, "Vencimientos",
                                    f"{len(vencidos)} cobro(s) marcados como vencidos")
        else:
            QMessageBox.information(self, "Vencimientos", "No hay cobros vencidos nuevos")
        self._ver_todos()

    def _seleccionar(self, row, _):
        item = self.table.item(row, 0)
        if item:
            self._selected_id = int(item.text())

    def _ver_todos(self):      self._mostrar(self.accounting.get_all())
    def _ver_pendientes(self): self._mostrar(self.accounting.get_pendientes())
    def _ver_pagados(self):    self._mostrar(self.accounting.get_pagados())
    def _ver_vencidos(self):   self._mostrar(self.accounting.get_vencidos())

    def _mostrar(self, registros):
        colores = {
            AccountRecord.ESTADO_PAGADO: "#d4efdf",
            AccountRecord.ESTADO_PENDIENTE: "#fef9e7",
            AccountRecord.ESTADO_VENCIDO: "#fadbd8",
        }
        recaudado = self.accounting.total_recaudado()
        pendiente = self.accounting.total_pendiente()
        self.lbl_resumen.setText(
            f"  💵 Total recaudado: ${recaudado:,.2f}     "
            f"⏳ Total pendiente: ${pendiente:,.2f}"
        )
        self.table.setRowCount(len(registros))
        for row, r in enumerate(registros):
            vals = [str(r.id_registro), r.nombre_cliente, r.concepto,
                    f"${r.monto:,.2f}", r.estado, r.fecha,
                    r.fecha_vencimiento or "—"]
            color = QColor(colores.get(r.estado, "#ffffff"))
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
