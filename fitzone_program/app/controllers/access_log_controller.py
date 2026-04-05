from __future__ import annotations

from app.services.access_log_service import AccessLogService


class AccessLogController:
    def __init__(self, access_log_service: AccessLogService) -> None:
        self.access_log_service = access_log_service

    def list_access_logs(self):
        return self.access_log_service.list_logs()

    def get_access_logs_by_user(self, user_id: str):
        return self.access_log_service.list_by_user(user_id)
