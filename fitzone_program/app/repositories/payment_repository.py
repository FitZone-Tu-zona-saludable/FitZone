from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.config.database import get_connection
from app.models.entities import Payment
from app.models.enums import PaymentMethod, PaymentStatus


class PaymentRepository:
    def create(self, payment: Payment) -> Payment:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO payments (id, user_id, user_membership_id, amount, payment_date, method, reference, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payment.id,
                    payment.user_id,
                    payment.user_membership_id,
                    str(payment.amount),
                    payment.payment_date.isoformat(),
                    payment.method.value,
                    payment.reference,
                    payment.status.value,
                    payment.created_at.isoformat(),
                ),
            )
        return payment

    def list_by_user(self, user_id: str) -> list[Payment]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row) -> Payment:
        return Payment(
            id=row["id"],
            user_id=row["user_id"],
            user_membership_id=row["user_membership_id"],
            amount=Decimal(row["amount"]),
            payment_date=datetime.fromisoformat(row["payment_date"]),
            method=PaymentMethod(row["method"]),
            reference=row["reference"],
            status=PaymentStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )
