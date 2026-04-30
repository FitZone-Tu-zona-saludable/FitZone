# payment_verification_view.py
# Vista para verificar pagos en FitZone
# Ahora conectada al controlador real PaymentController y al servicio de alertas
# Documentado línea por línea en español

from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from frontend.controllers.payment_controller import PaymentController
from frontend.services.alert_service import AlertService


class PaymentVerificationView(QWidget):
    """
    Vista para verificar pagos registrados.
    Permite listar pagos y marcar como verificados en el backend.
    """

    def __init__(self):
        super().__init__()

        # Controlador real de pagos
        self.controller = PaymentController()

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Cargar datos iniciales
        self.load_data()

    def load_data(self):
        """
        Carga los pagos desde el controlador y los muestra en la interfaz.
        """
        self.clear_layout()
        data = self.controller.load_payments()

        if not data:
            self.layout.addWidget(QLabel('No hay pagos disponibles'))
            return

        self.layout.addWidget(QLabel('Pagos registrados'))
        for p in data:
            label = QLabel(f"{p['user']} - {p['membership']} - ${p['amount']} - {p['status']}")
            btn = QPushButton('Verificar')
            btn.clicked.connect(partial(self.handle_verify, p['id']))

            # Si ya está verificado, deshabilitar botón
            if str(p['status']).lower() == 'verificado':
                btn.setEnabled(False)

            self.layout.addWidget(label)
            self.layout.addWidget(btn)

    def handle_verify(self, payment_id):
        """
        Acción para verificar un pago usando el controlador real.
        """
        result = self.controller.verify_payment(payment_id)

        if result and result.get('success'):
            AlertService.info(self, 'Éxito', result.get('message', 'Pago verificado correctamente.'))
            self.load_data()
        else:
            AlertService.error(self, 'Error', result.get('message', 'No se pudo verificar el pago.'))

    def clear_layout(self):
        """
        Limpia el layout eliminando widgets previos.
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()