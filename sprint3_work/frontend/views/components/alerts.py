"""
components/alerts.py
====================
Componentes de alerta visual reutilizables para FitZone.

Cubren los requerimientos del Sprint 2 de Alex:
    * "Crear mensajes y alertas visuales para pago confirmado"
    * "Mensajes y alertas visuales de vencimiento de membresía"

Estos widgets son agnósticos del backend: reciben texto y un tipo (success,
warning, danger, info) y se renderizan con el tema FitZone.

Uso típico:
    banner = AlertBanner("Pago confirmado correctamente", "success")
    layout.addWidget(banner)

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


_ICONS = {"success": "✔", "warning": "⚠", "danger": "✖", "info": "ℹ"}
_OBJECT = {
    "success": "AlertSuccess",
    "warning": "AlertWarning",
    "danger":  "AlertDanger",
    "info":    "AlertSuccess",
}


class AlertBanner(QFrame):
    """Banner inline de notificación. Soporta cierre manual y autohide."""

    def __init__(self, message: str, kind: str = "success",
                 dismissible: bool = True, autohide_ms: int = 0, parent=None):
        super().__init__(parent)
        self.setObjectName(_OBJECT.get(kind, "AlertSuccess"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 10, 10)

        icon = QLabel(_ICONS.get(kind, "ℹ"))
        icon.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(icon)

        text = QLabel(message)
        text.setWordWrap(True)
        layout.addWidget(text, 1)

        if dismissible:
            close_btn = QPushButton("×")
            close_btn.setFixedSize(26, 26)
            close_btn.setStyleSheet(
                "background: transparent; border: none; font-size: 18px;"
            )
            close_btn.clicked.connect(self.hide)
            layout.addWidget(close_btn, 0, Qt.AlignRight)

        if autohide_ms > 0:
            QTimer.singleShot(autohide_ms, self.hide)


# ---------------------------------------------------------------------------
# Helpers de dominio: encapsulan los mensajes oficiales del Sprint 2
# ---------------------------------------------------------------------------
def payment_confirmed_alert(reference: str = "") -> AlertBanner:
    """Alerta verde estandarizada para pago confirmado."""
    msg = "Pago confirmado correctamente."
    if reference:
        msg += f" Referencia: {reference}"
    return AlertBanner(msg, kind="success", autohide_ms=6000)


def membership_expiring_alert(days_left: int) -> AlertBanner:
    """Alerta preventiva de vencimiento próximo de membresía."""
    if days_left <= 0:
        return AlertBanner(
            "Tu membresía ha vencido. Renueva para continuar entrenando.",
            kind="danger",
        )
    return AlertBanner(
        f"Tu membresía vence en {days_left} día(s). Te recomendamos renovar.",
        kind="warning",
    )
