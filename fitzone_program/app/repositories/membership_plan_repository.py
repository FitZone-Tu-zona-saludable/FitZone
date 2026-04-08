from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.config.database import get_connection
from app.models.entities import MembershipPlan
from app.models.enums import MembershipPlanStatus


class MembershipPlanRepository:
    def create(self, plan: MembershipPlan) -> MembershipPlan:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO membership_plans (id, name, price, duration_days, benefits, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    plan.id,
                    plan.name,
                    str(plan.price),
                    plan.duration_days,
                    plan.benefits,
                    plan.status.value,
                    plan.created_at.isoformat(),
                    plan.updated_at.isoformat(),
                ),
            )
        return plan

    def get_by_id(self, plan_id: str) -> MembershipPlan | None:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM membership_plans WHERE id = ?", (plan_id,)).fetchone()
        return self._to_entity(row) if row else None

    def list_all(self, only_active: bool = False) -> list[MembershipPlan]:
        query = "SELECT * FROM membership_plans"
        params: tuple = ()
        if only_active:
            query += " WHERE status = ?"
            params = (MembershipPlanStatus.ACTIVE.value,)
        query += " ORDER BY price ASC"
        with get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row) -> MembershipPlan:
        return MembershipPlan(
            id=row["id"],
            name=row["name"],
            price=Decimal(row["price"]),
            duration_days=row["duration_days"],
            benefits=row["benefits"],
            status=MembershipPlanStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
