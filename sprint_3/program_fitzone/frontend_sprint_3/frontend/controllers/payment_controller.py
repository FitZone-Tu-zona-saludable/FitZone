# payment_controller.py
# Controlador para manejar la lógica de pagos en FitZone
# Ahora conectado al servicio real del backend (payment_service)
# Documentado línea por línea en español

from src.services.payment_service import PaymentService

class PaymentController:
    """
    Controlador para gestionar pagos.
    Contiene métodos para listar, registrar y verificar pagos.
    """

    def __init__(self):
        # Inicializa el servicio de pagos del backend
        self.service = PaymentService()

    def load_payments(self):
        """
        Devuelve la lista completa de pagos desde el servicio real.
        """
        return self.service.list_payments()

    def register_payment(self, payment_data):
        """
        Registra un nuevo pago usando el servicio real.
        """
        return self.service.register_payment(payment_data)

    def verify_payment(self, payment_id):
        """
        Verifica un pago existente según su ID en el servicio real.
        """
        result = self.service.verify_payment(payment_id)
        return result
