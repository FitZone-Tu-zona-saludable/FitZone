from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from frontend.controllers.security_controller import SecurityController
from frontend.views.components.widgets import Card, PageHeader


class SecurityView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = SecurityController()
        self._build_ui()
        self.show_logs()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(PageHeader(
            "Bitácora de seguridad",
            "Consulta accesos exitosos, fallidos y eventos sensibles del sistema.",
        ))

        summary = Card()
        self.summary = QLabel()
        self.summary.setObjectName("Muted")
        summary.layout.addWidget(self.summary)
        layout.addWidget(summary)

        logs_card = Card()
        title = QLabel("Registros recientes")
        title.setObjectName("H2")
        logs_card.layout.addWidget(title)
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        logs_card.layout.addWidget(self.logs)

        btn = QPushButton("Actualizar bitácora")
        btn.setObjectName("Primary")
        btn.clicked.connect(self.show_logs)
        logs_card.layout.addWidget(btn)

        layout.addWidget(logs_card)

    def show_logs(self):
        logs = self.controller.load_logs() or []
        ordered_logs = list(reversed(logs[-50:]))
        lines = [
            f"{log.get('date', '')} | {log.get('message', '')}"
            for log in ordered_logs
        ]
        self.summary.setText(f"Total de eventos registrados: {len(logs)}")
        self.logs.setText("\n".join(lines) if lines else "Sin registros")

    def on_activate(self):
        self.show_logs()
