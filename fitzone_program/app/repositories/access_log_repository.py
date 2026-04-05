from __future__ import annotations

from datetime import datetime

from app.config.database import get_connection
from app.models.entities import AccessLog
from app.models.enums import AccessAction, AccessResult


class AccessLogRepository:
    def create(self, log: AccessLog) -> AccessLog:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO access_logs (id, user_id, email_attempted, action, result, ip_address, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    log.id,
                    log.user_id,
                    log.email_attempted,
                    log.action.value,
                    log.result.value,
                    log.ip_address,
                    log.created_at.isoformat(),
                ),
            )
        return log

    def list_all(self) -> list[AccessLog]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM access_logs ORDER BY created_at DESC").fetchall()
        return [self._to_entity(row) for row in rows]

    def list_by_user(self, user_id: str) -> list[AccessLog]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM access_logs WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row) -> AccessLog:
        return AccessLog(
            id=row["id"],
            user_id=row["user_id"],
            email_attempted=row["email_attempted"],
            action=AccessAction(row["action"]),
            result=AccessResult(row["result"]),
            ip_address=row["ip_address"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
