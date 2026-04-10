from __future__ import annotations

from datetime import date, datetime

from app.config.database import get_connection
from app.models.entities import UserMembership
from app.models.enums import MembershipStatus


class UserMembershipRepository:
    def create(self, membership: UserMembership) -> UserMembership:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO user_memberships (id, user_id, membership_plan_id, start_date, end_date, status, assigned_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    membership.id,
                    membership.user_id,
                    membership.membership_plan_id,
                    membership.start_date.isoformat(),
                    membership.end_date.isoformat(),
                    membership.status.value,
                    membership.assigned_at.isoformat(),
                ),
            )
        return membership

    def get_by_id(self, membership_id: str) -> UserMembership | None:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM user_memberships WHERE id = ?", (membership_id,)).fetchone()
        return self._to_entity(row) if row else None

    def list_by_user(self, user_id: str) -> list[UserMembership]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM user_memberships WHERE user_id = ? ORDER BY assigned_at DESC", (user_id,)
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row) -> UserMembership:
        return UserMembership(
            id=row["id"],
            user_id=row["user_id"],
            membership_plan_id=row["membership_plan_id"],
            start_date=date.fromisoformat(row["start_date"]),
            end_date=date.fromisoformat(row["end_date"]),
            status=MembershipStatus(row["status"]),
            assigned_at=datetime.fromisoformat(row["assigned_at"]),
        )
