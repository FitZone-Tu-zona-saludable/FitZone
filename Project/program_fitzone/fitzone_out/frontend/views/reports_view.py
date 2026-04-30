# reports_view.py
# Vista de generación y consulta de reportes para gerencia
# Sprint 4 - Alex (RF23: Generar reportes)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTabWidget, QHeaderView,
    QFrame, QTextEdit
)
from PySide6.QtCore import Qt
from frontend.controllers.report_controller import ReportController
from frontend.resources.theme import COLORS


class ReportsView(QWidget):
    """Vista de reportes gerenciales: membresías, actividad y resumen financiero."""

    def __init__(self):
        super().__init__()
        self.controller = ReportController()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("📊  Generación de Reportes — Gerencia")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Consulta y exporta reportes de membresías, actividad y contabilidad.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Tabs ─────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_members_tab(),  "👥 Membresías")
        self.tabs.addTab(self._build_activity_tab(), "💳 Actividad de Pagos")
        self.tabs.addTab(self._build_financial_tab(),"💰 Resumen Financiero")
        layout.addWidget(self.tabs)

    # ── Tab 1: Membresías ─────────────────────────────────────────────
    def _build_members_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(12, 12, 12, 12)

        btn_row = QHBoxLayout()
        btn_gen = QPushButton("📈  Generar reporte de membresías")
        btn_gen.setObjectName("Primary")
        btn_gen.clicked.connect(self._gen_members)
        btn_row.addStretch()
        btn_row.addWidget(btn_gen)
        v.addLayout(btn_row)

        # Tarjetas resumen
        self.summary_row = QHBoxLayout()
        self.card_activas    = self._make_card("Activas",      "0", COLORS["success"])
        self.card_por_vencer = self._make_card("Por vencer",   "0", COLORS["warning"])
        self.card_vencidas   = self._make_card("Vencidas",     "0", COLORS["danger"])
        self.card_sin        = self._make_card("Sin membresía","0", COLORS["text_muted"])
        for c in [self.card_activas, self.card_por_vencer,
                  self.card_vencidas, self.card_sin]:
            self.summary_row.addWidget(c[0])
        v.addLayout(self.summary_row)

        self.tbl_members = QTableWidget()
        self.tbl_members.setColumnCount(5)
        self.tbl_members.setHorizontalHeaderLabels(
            ["Nombre", "Correo", "Rol", "Plan", "Estado"])
        self.tbl_members.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_members.setEditTriggers(QTableWidget.NoEditTriggers)
        v.addWidget(self.tbl_members)
        return w

    def _gen_members(self):
        data = self.controller.members_report()
        self.card_activas[1].setText(str(data["activas"]))
        self.card_por_vencer[1].setText(str(data["por_vencer"]))
        self.card_vencidas[1].setText(str(data["vencidas"]))
        self.card_sin[1].setText(str(data["sin_membresia"]))
        rows = data["detalle"]
        self.tbl_members.setRowCount(len(rows))
        for i, r in enumerate(rows):
            self.tbl_members.setItem(i, 0, QTableWidgetItem(r["nombre"]))
            self.tbl_members.setItem(i, 1, QTableWidgetItem(r["correo"]))
            self.tbl_members.setItem(i, 2, QTableWidgetItem(r["rol"]))
            self.tbl_members.setItem(i, 3, QTableWidgetItem(r["plan"]))
            self.tbl_members.setItem(i, 4, QTableWidgetItem(r["estado"]))

    # ── Tab 2: Actividad de pagos ─────────────────────────────────────
    def _build_activity_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(12, 12, 12, 12)
        btn_gen = QPushButton("📋  Generar reporte de actividad")
        btn_gen.setObjectName("Primary")
        btn_gen.clicked.connect(self._gen_activity)
        v.addWidget(btn_gen, 0, Qt.AlignRight)
        self.lbl_total_pagos = QLabel("Total pagos: —")
        self.lbl_total_pagos.setObjectName("H2")
        v.addWidget(self.lbl_total_pagos)
        self.tbl_activity = QTableWidget()
        self.tbl_activity.setColumnCount(4)
        self.tbl_activity.setHorizontalHeaderLabels(
            ["Usuario", "Correo", "Valor ($)", "Método"])
        self.tbl_activity.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_activity.setEditTriggers(QTableWidget.NoEditTriggers)
        v.addWidget(self.tbl_activity)
        return w

    def _gen_activity(self):
        data = self.controller.activity_report()
        self.lbl_total_pagos.setText(f"Total pagos registrados: {data['total_pagos']}")
        rows = data["detalle"]
        self.tbl_activity.setRowCount(len(rows))
        for i, r in enumerate(rows):
            self.tbl_activity.setItem(i, 0, QTableWidgetItem(r["usuario"]))
            self.tbl_activity.setItem(i, 1, QTableWidgetItem(r["correo"]))
            self.tbl_activity.setItem(i, 2, QTableWidgetItem(f"${r['valor']:,.0f}"))
            self.tbl_activity.setItem(i, 3, QTableWidgetItem(r["metodo"]))

    # ── Tab 3: Resumen financiero ─────────────────────────────────────
    def _build_financial_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(12, 12, 12, 12)
        btn_gen = QPushButton("💰  Generar resumen financiero")
        btn_gen.setObjectName("Primary")
        btn_gen.clicked.connect(self._gen_financial)
        v.addWidget(btn_gen, 0, Qt.AlignRight)
        self.txt_financial = QTextEdit()
        self.txt_financial.setReadOnly(True)
        self.txt_financial.setPlaceholderText(
            "Presiona el botón para generar el resumen financiero...")
        v.addWidget(self.txt_financial)
        return w

    def _gen_financial(self):
        data = self.controller.financial_report()
        if "error" in data:
            self.txt_financial.setText(data["error"])
            return
        text = (
            f"📅 Fecha de generación: {data['fecha_generacion']}\n\n"
            f"✅ Total ingresos pagados:  ${data['total_ingresos']:,.0f}\n"
            f"⏳ Total pendiente por cobrar: ${data['total_pendiente']:,.0f}\n"
            f"📄 Total entradas contables: {data['total_entradas']}\n"
        )
        self.txt_financial.setText(text)

    def _make_card(self, label, value, color):
        frame = QFrame(); frame.setObjectName("Card")
        v = QVBoxLayout(frame)
        lbl = QLabel(label); lbl.setObjectName("Muted"); lbl.setAlignment(Qt.AlignCenter)
        val = QLabel(value)
        val.setAlignment(Qt.AlignCenter)
        val.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        v.addWidget(lbl); v.addWidget(val)
        return frame, val
