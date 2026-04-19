# security_view.py
# Vista para mostrar la bitácora de accesos en FitZone
# Ahora conectada al controlador real SecurityController
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from frontend.controllers.security_controller import SecurityController


class SecurityView(QWidget):
    """
    Vista para mostrar la bitácora de accesos.
    Permite consultar los registros de seguridad y actualizarlos desde el backend.
    """

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Seguridad")

        # Controlador real de seguridad
        self.controller = SecurityController()

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bitácora de accesos"))

        # Área de texto para mostrar logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        layout.addWidget(self.logs)

        # Botón para actualizar registros
        btn = QPushButton("Actualizar")
        btn.clicked.connect(self.show_logs)
        layout.addWidget(btn)

        self.setLayout(layout)

        # Cargar registros iniciales
        self.show_logs()

    def show_logs(self):
        """
        Carga y muestra los registros de seguridad desde el controlador.
        """
        lines = []
        logs = self.controller.load_logs() or []
        for log in logs:
            created = log.get("created_at", "")
            user = log.get("user_email", "desconocido")
            action = log.get("action", "")
            result = log.get("result", "")
            lines.append(f"{created} | {user} | {action} | {result}")

        text = "\n".join(lines) if lines else "Sin registros"
        self.logs.setText(text)