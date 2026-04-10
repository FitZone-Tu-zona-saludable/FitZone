from __future__ import annotations

from decimal import Decimal

from app.models.entities import Payment
from app.models.enums import MembershipStatus, PaymentMethod, PaymentStatus, UserStatus
from app.repositories.membership_plan_repository import MembershipPlanRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.user_membership_repository import UserMembershipRepository
from app.repositories.user_repository import UserRepository
from app.utils.common import new_id, now


class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        user_repository: UserRepository,
        user_membership_repository: UserMembershipRepository,
        membership_plan_repository: MembershipPlanRepository,
    ) -> None:
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.user_membership_repository = user_membership_repository
        self.membership_plan_repository = membership_plan_repository

    def register_payment(self, user_id: str, user_membership_id: str, amount: Decimal, method: PaymentMethod, reference: str) -> Payment:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('El usuario no existe.')
        if user.status != UserStatus.ACTIVE:
            raise ValueError('El usuario no está activo para registrar pagos.')

        membership = self.user_membership_repository.get_by_id(user_membership_id)
        if not membership:
            raise ValueError('La membresía no existe.')
        if membership.user_id != user_id:
            raise ValueError('La membresía no pertenece al usuario indicado.')
        if membership.status == MembershipStatus.CANCELLED:
            raise ValueError('No se puede registrar un pago para una membresía cancelada.')

        plan = self.membership_plan_repository.get_by_id(membership.membership_plan_id)
        if not plan:
            raise ValueError('No se encontró el plan asociado a la membresía.')

        normalized_amount = Decimal(str(amount))
        if normalized_amount <= 0:
            raise ValueError('El monto debe ser mayor a cero.')
        if normalized_amount != plan.price:
            raise ValueError(f'Monto inválido. Debe ser exactamente {plan.price}.')

        clean_reference = reference.strip()
        if not clean_reference:
            raise ValueError('La referencia del pago es obligatoria.')

        timestamp = now()
        payment = Payment(
            id=new_id(),
            user_id=user_id,
            user_membership_id=user_membership_id,
            amount=normalized_amount,
            payment_date=timestamp,
            method=method,
            reference=clean_reference,
            status=PaymentStatus.REGISTERED,
            created_at=timestamp,
        )
        return self.payment_repository.create(payment)

    def list_payments_by_user(self, user_id: str) -> list[Payment]:
        return self.payment_repository.list_by_user(user_id)
