"""
staff_register_view.py
======================
Sprint 2 - **Formulario de registro de trabajador y empleado**.

Un mismo formulario maneja ambos roles (trabajador / empleado) cambiando
las opciones del combo "Tipo". Realiza validaciones básicas en cliente y
muestra alertas visuales según la respuesta del backend.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpinBox,
)

from frontend.services.api_service_ext import register_staff, fetch_staff
from frontend.views.components.widgets import PageHeader, Card
from frontend.views.components.alerts import AlertBanner


class StaffRegisterView(QWidget):
    """Alta de trabajadores y empleados con tabla de consulta."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._reload_table()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        root.addWidget(PageHeader(
            "Registro de trabajadores y empleados",
            "Da de alta personal del gimnasio con su rol y datos básicos.",
        ))

        self.feedback_slot = QVBoxLayout()
        root.addLayout(self.feedback_slot)

        # ---- Formulario en dos columnas dentro de una Card ----------------
        card = Card()
        form_row = QHBoxLayout()

        col_a = QFormLayout(); col_b = QFormLayout()

        self.in_name = QLineEdit(); self.in_name.setPlaceholderText("Nombre completo")
        self.in_doc  = QLineEdit(); self.in_doc.setPlaceholderText("Documento de identidad")
        self.in_phone = QLineEdit(); self.in_phone.setPlaceholderText("Teléfono")
        self.in_email = QLineEdit(); self.in_email.setPlaceholderText("Correo electrónico")

        self.in_role = QComboBox(); self.in_role.addItems(["trabajador", "empleado"])
        self.in_position = QLineEdit(); self.in_position.setPlaceholderText("Cargo (ej. Recepción)")
        self.in_modality = QComboBox(); self.in_modality.addItems(["tiempo completo", "medio tiempo", "por horas"])
        self.in_experience = QSpinBox(); self.in_experience.setRange(0, 60); self.in_experience.setSuffix(" años")

        col_a.addRow("Nombre completo", self.in_name)
        col_a.addRow("Documento", self.in_doc)
        col_a.addRow("Teléfono", self.in_phone)
        col_a.addRow("Correo", self.in_email)

        col_b.addRow("Tipo", self.in_role)
        col_b.addRow("Cargo", self.in_position)
        col_b.addRow("Modalidad", self.in_modality)
        col_b.addRow("Experiencia", self.in_experience)

        form_row.addLayout(col_a, 1); form_row.addLayout(col_b, 1)
        card.layout.addLayout(form_row)

        actions = QHBoxLayout()
        btn_clear = QPushButton("Limpiar"); btn_clear.clicked.connect(self._clear_form)
        btn_save  = QPushButton("Registrar"); btn_save.setObjectName("Primary")
        btn_save.clicked.connect(self._save)
        actions.addStretch(); actions.addWidget(btn_clear); actions.addWidget(btn_save)
        card.layout.addLayout(actions)
        root.addWidget(card)

        # ---- Tabla de personal registrado --------------------------------
        label = QLabel("Personal registrado")
        label.setObjectName("H2")
        root.addWidget(label)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Documento", "Tipo", "Cargo", "Modalidad"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

    # ------------------------------------------------------------------ helpers
    def _clear_form(self):
        for w in (self.in_name, self.in_doc, self.in_phone,
                  self.in_email, self.in_position):
            w.clear()
        self.in_role.setCurrentIndex(0)
        self.in_modality.setCurrentIndex(0)
        self.in_experience.setValue(0)

    def _show_feedback(self, msg: str, kind: str):
        while self.feedback_slot.count():
            it = self.feedback_slot.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        self.feedback_slot.addWidget(AlertBanner(msg, kind=kind, autohide_ms=4000))

    # ------------------------------------------------------------------ action
    def _save(self):
        data = {
            "full_name":   self.in_name.text().strip(),
            "document_id": self.in_doc.text().strip(),
            "phone":       self.in_phone.text().strip(),
            "email":       self.in_email.text().strip(),
            "role":        self.in_role.currentText(),
            "position":    self.in_position.text().strip(),
            "modality":    self.in_modality.currentText(),
            "experience":  self.in_experience.value(),
        }
        if data["email"] and "@" not in data["email"]:
            self._show_feedback("Correo electrónico inválido.", "warning")
            return
        result = register_staff(data)
        if result.get("success"):
            self._show_feedback(result["message"], "success")
            self._clear_form()
            self._reload_table()
        else:
            self._show_feedback(result.get("message", "Error"), "danger")

    def _reload_table(self):
        rows = fetch_staff()
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            cells = [r["id"], r["full_name"], r["document_id"],
                     r["role"], r["position"], r["modality"]]
            for c, val in enumerate(cells):
                it = QTableWidgetItem(str(val))
                it.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, c, it)

    def on_activate(self):
        self._reload_table()
