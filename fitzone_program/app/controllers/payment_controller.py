from __future__ import annotations

from decimal import Decimal

from app.models.enums import PaymentMethod
from app.services.payment_service import PaymentService


class PaymentController:
    def __init__(self, payment_service: PaymentService) -> None:
        self.payment_service = payment_service

    def register_payment(self, user_id: str, user_membership_id: str, amount: Decimal, method: PaymentMethod, reference: str):
        return self.payment_service.register_payment(user_id, user_membership_id, amount, method, reference)

    def list_payments_by_user(self, user_id: str):
        return self.payment_service.list_payments_by_user(user_id)
