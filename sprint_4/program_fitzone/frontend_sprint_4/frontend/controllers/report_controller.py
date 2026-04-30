# report_controller.py
# Controlador de reportes para gerencia — Sprint 4 (Alex)

from src.services.auth_service import AuthService
from src.services.report_service import ReportService


class ReportController:
    def __init__(self):
        auth = AuthService()
        # Intenta cargar accounting service si existe
        try:
            from src.services.accounting_service import AccountingService
            acc = AccountingService()
        except Exception:
            acc = None
        self.service = ReportService(auth, acc)

    def members_report(self):
        return self.service.report_members()

    def activity_report(self):
        return self.service.report_activity()

    def financial_report(self):
        return self.service.report_financial_summary()
