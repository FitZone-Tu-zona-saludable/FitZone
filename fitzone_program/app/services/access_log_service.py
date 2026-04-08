from __future__ import annotations

from app.models.entities import AccessLog
from app.models.enums import AccessAction, AccessResult
from app.repositories.access_log_repository import AccessLogRepository
from app.utils.common import new_id, now


class AccessLogService:
    def __init__(self, access_log_repository: AccessLogRepository) -> None:
        self.access_log_repository = access_log_repository

    def record(self, user_id: str | None, email_attempted: str, action: AccessAction, result: AccessResult, ip_address: str) -> AccessLog:
        log = AccessLog(
            id=new_id(),
            user_id=user_id,
            email_attempted=email_attempted,
            action=action,
            result=result,
            ip_address=ip_address,
            created_at=now(),
        )
        return self.access_log_repository.create(log)

    def list_logs(self) -> list[AccessLog]:
        return self.access_log_repository.list_all()

    def list_by_user(self, user_id: str) -> list[AccessLog]:
        return self.access_log_repository.list_by_user(user_id)
