from frontend.services.app_context import report_service


class ReportController:
    def __init__(self):
        self.service = report_service

    def members_report(self):
        return self.service.report_members()

    def activity_report(self):
        return self.service.report_activity()

    def financial_report(self):
        return self.service.report_financial_summary()
