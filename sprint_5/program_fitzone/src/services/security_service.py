from src.services.auth_service import AuthService


class SecurityService:
    """Servicio de bitácora de seguridad (Sprint 2)."""

    def __init__(self, auth_service=None):
        self.auth = auth_service or AuthService()

    def get_access_logs(self):
        return [
            {
                "date": log.get("date", ""),
                "message": log.get("message", ""),
            }
            for log in self.auth.logs
        ]
