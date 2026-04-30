"""
notifications_view.py
=====================
Sprint 2 - Centro visual de notificaciones del usuario.

Demuestra el uso de los componentes `payment_confirmed_alert` y
`membership_expiring_alert` que cubren los entregables:
    * "Mensajes y alertas visuales para pago confirmado"
    * "Mensajes y alertas visuales para vencimiento de membresía"

El backend (Romel/Andrés) será quien decida CUÁNDO emitir cada
notificación; esta vista solo se encarga del render visual coherente.

Autor: Alex - Sprint 2.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from frontend.views.components.widgets import PageHeader, Card
from frontend.views.components.alerts import (
    AlertBanner, payment_confirmed_alert, membership_expiring_alert,
)


class NotificationsView(QWidget):
    """Buzón visual de notificaciones del usuario."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self.populate_demo()

    def _build_ui(self):
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(14)
        self.root.addWidget(PageHeader(
            "Notificaciones",
            "Estado de tus pagos y de tu membresía.",
        ))

        # Card contenedora
        self.card = Card()
        self.root.addWidget(self.card)

        # Botón de demo (útil para QA en pruebas funcionales)
        btn = QPushButton("Generar notificaciones de prueba")
        btn.clicked.connect(self.populate_demo)
        self.root.addWidget(btn, 0, Qt.AlignRight)
        self.root.addStretch()

    def populate_demo(self):
        """Limpia y agrega ejemplos representativos de cada tipo."""
        while self.card.layout.count():
            it = self.card.layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        self.card.layout.addWidget(payment_confirmed_alert("PAY-00231"))
        self.card.layout.addWidget(membership_expiring_alert(5))
        self.card.layout.addWidget(membership_expiring_alert(0))
        self.card.layout.addWidget(
            AlertBanner("Tienes una nueva clase asignada para mañana 07:00.", kind="info")
        )
