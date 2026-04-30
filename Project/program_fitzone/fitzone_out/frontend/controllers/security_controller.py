from frontend.services.app_context import security_service


class SecurityController:
    def __init__(self):
        self.service = security_service

    def load_logs(self):
        return self.service.get_access_logs()
