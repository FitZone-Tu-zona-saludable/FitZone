"""
components/widgets.py
=====================
Pequeños bloques visuales reutilizados por varias vistas (tarjeta con
título, encabezado de página, etiqueta tipo "chip" para estados, etc.).

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class Card(QFrame):
    """Tarjeta contenedora con borde redondeado del tema."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(10)


class PageHeader(QFrame):
    """Encabezado: título grande + subtítulo opcional."""

    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)

        h1 = QLabel(title); h1.setObjectName("H1")
        layout.addWidget(h1)

        if subtitle:
            sub = QLabel(subtitle); sub.setObjectName("Muted")
            layout.addWidget(sub)


class StatusChip(QLabel):
    """Etiqueta coloreada para estados (activo, vencido, pendiente...)."""

    _MAP = {
        "activo":     ("#0E6B45", "#21C07A"),
        "activa":     ("#0E6B45", "#21C07A"),
        "vigente":    ("#0E6B45", "#21C07A"),
        "vencida":    ("#7A1F22", "#E5484D"),
        "vencido":    ("#7A1F22", "#E5484D"),
        "pendiente":  ("#7A5A0E", "#F5A524"),
        "confirmado": ("#0E6B45", "#21C07A"),
    }

    def __init__(self, text: str, parent=None):
        super().__init__(text.capitalize(), parent)
        bg, fg = self._MAP.get(text.lower(), ("#244039", "#9DB3AB"))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f"background-color: {bg}; color: {fg}; "
            f"border-radius: 10px; padding: 3px 10px; font-weight: 600;"
        )
