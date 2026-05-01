from frontend.services.app_context import payment_service


class PaymentController:
    def __init__(self):
        self.service = payment_service

    def load_payments(self):
        return self.service.list_payments()

    def register_payment(self, payment_data):
        return self.service.register_payment(payment_data)

    def verify_payment(self, payment_id):
        return self.service.verify_payment(payment_id)
