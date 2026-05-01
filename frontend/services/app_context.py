from src.services.accounting_service import AccountingService
from src.services.attendance_service import AttendanceService
from src.services.auth_service import AuthService
from src.services.employee_payment_service import EmployeePaymentService
from src.services.evaluation_service import EvaluationService
from src.services.incident_service import IncidentService
from src.services.membership_service import MembershipService
from src.services.notification_service import NotificationService
from src.services.payment_service import PaymentService
from src.services.payroll_service import PayrollService
from src.services.performance_service import PerformanceService
from src.services.report_service import ReportService
from src.services.schedule_service import ScheduleService
from src.services.security_service import SecurityService
from src.services.survey_service import SurveyService
from src.services.trainer_service import TrainerService
from src.services.worker_service import WorkerService

from frontend.services.state_service import set_current_user


auth_service = AuthService()
membership_service = MembershipService(auth_service=auth_service)
payment_service = PaymentService(
    auth_service=auth_service,
    membership_service=membership_service,
)
security_service = SecurityService(auth_service=auth_service)
schedule_service = ScheduleService()
trainer_service = TrainerService()
worker_service = WorkerService()
accounting_service = AccountingService()
survey_service = SurveyService()
employee_payment_service = EmployeePaymentService()
notification_service = NotificationService()
report_service = ReportService(auth_service, accounting_service)
attendance_service = AttendanceService()
incident_service = IncidentService()
performance_service = PerformanceService()
evaluation_service = EvaluationService()
payroll_service = PayrollService()


class _UserControllerAdapter:
    def login_user(self, email, password):
        user = auth_service.login(email, password)
        if user:
            return {"success": True, "data": set_current_user(user)}
        return {"success": False, "message": "Credenciales incorrectas."}

    def register_user(self, name, email, password, role="user"):
        try:
            user = auth_service.create_user(name, email, password, role)
        except ValueError as exc:
            return {"success": False, "message": str(exc)}
        return {"success": True, "data": set_current_user(user)}

    def list_users(self):
        return auth_service.get_users()


class _MembershipControllerAdapter:
    def list_membership_plans(self):
        return {"success": True, "data": membership_service.list_memberships()}

    def select_membership(self, user_id, plan_id):
        return membership_service.select_membership(user_id, plan_id)

    def list_user_memberships(self, user_id):
        return membership_service.get_user_memberships(user_id)


class _PaymentControllerAdapter:
    def register_payment(self, user_id, membership_id, amount, method, reference):
        return payment_service.register_payment({
            "user_id": user_id,
            "membership_id": membership_id,
            "amount": amount,
            "method": method,
            "reference": reference,
        })

    def list_payments(self):
        return payment_service.list_payments()

    def verify_payment(self, payment_id):
        return payment_service.verify_payment(payment_id)


user_controller = _UserControllerAdapter()
membership_controller = _MembershipControllerAdapter()
payment_controller = _PaymentControllerAdapter()
