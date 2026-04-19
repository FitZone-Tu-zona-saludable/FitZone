# alerts_page.py
# Vista de alertas en FitZone
# Ahora conectada al servicio real de alertas (AlertService)
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from frontend.services.alert_service import AlertService


class AlertsPage(QWidget):
    """
    Vista para mostrar alertas importantes al usuario.
    Incluye mensajes de pago confirmado y vencimiento de membresía.
    """

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Alertas - FitZone")
        self.resize(600, 400)

        # Construcción de la interfaz
        self.init_ui()

    def init_ui(self):
        """
        Construye la interfaz gráfica de la página de alertas.
        """
        layout = QVBoxLayout()

        # Título principal
        title = QLabel("Alertas del sistema")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b; margin: 10px;")
        layout.addWidget(title)

        # Botón para mostrar alerta de pago confirmado
        btn_payment = QPushButton("Pago confirmado")
        btn_payment.setStyleSheet("background-color: #27ae60; color: white; padding: 6px; border-radius: 5px;")
        btn_payment.clicked.connect(self.show_payment_alert)
        layout.addWidget(btn_payment)

        # Botón para mostrar alerta de vencimiento de membresía
        btn_expiration = QPushButton("Membresía vencida")
        btn_expiration.setStyleSheet("background-color: #e67e22; color: white; padding: 6px; border-radius: 5px;")
        btn_expiration.clicked.connect(self.show_expiration_alert)
        layout.addWidget(btn_expiration)

        # Asignar layout principal
        self.setLayout(layout)

    def show_payment_alert(self):
        """
        Muestra un mensaje de pago confirmado usando el servicio de alertas.
        """
        AlertService.info(self, "Pago confirmado", "Tu pago ha sido registrado exitosamente.")

    def show_expiration_alert(self):
        """
        Muestra un mensaje de vencimiento de membresía usando el servicio de alertas.
        """
        AlertService.warning(self, "Membresía vencida", "Tu membresía ha vencido. Por favor, renueva para continuar disfrutando de FitZone.")