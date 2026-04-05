from decimal import Decimal

from app.config.database import init_db
from app.controllers.access_log_controller import AccessLogController
from app.controllers.auth_controller import AuthController
from app.controllers.membership_controller import MembershipController
from app.controllers.payment_controller import PaymentController
from app.controllers.user_controller import UserController
from app.models.enums import PaymentMethod, Role, UserStatus
from app.repositories.access_log_repository import AccessLogRepository
from app.repositories.membership_plan_repository import MembershipPlanRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.user_membership_repository import UserMembershipRepository
from app.repositories.user_repository import UserRepository
from app.services.access_log_service import AccessLogService
from app.services.auth_service import AuthService
from app.services.membership_service import MembershipService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService


def bootstrap(reset_db: bool = False):
    init_db(reset=reset_db)

    user_repository = UserRepository()
    membership_plan_repository = MembershipPlanRepository()
    user_membership_repository = UserMembershipRepository()
    payment_repository = PaymentRepository()
    access_log_repository = AccessLogRepository()

    access_log_service = AccessLogService(access_log_repository)
    user_service = UserService(user_repository)
    auth_service = AuthService(user_repository, user_service, access_log_service)
    membership_service = MembershipService(membership_plan_repository, user_membership_repository, user_repository)
    payment_service = PaymentService(payment_repository, user_repository, user_membership_repository, membership_plan_repository)

    membership_service.seed_default_plans()

    return {
        'auth': AuthController(auth_service),
        'users': UserController(user_service),
        'memberships': MembershipController(membership_service),
        'payments': PaymentController(payment_service),
        'access_logs': AccessLogController(access_log_service),
    }


def run_demo() -> None:
    controllers = bootstrap(reset_db=True)

    print('\n=== REGISTRO ===')
    user = controllers['auth'].register(
        name='Andres',
        email='andres@fitzone.com',
        password='ClaveSegura123',
        role=Role.USER,
        phone='3001234567',
    )
    print(user)

    print('\n=== LOGIN ===')
    authenticated_user = controllers['auth'].login('andres@fitzone.com', 'ClaveSegura123')
    print(authenticated_user)

    print('\n=== PLANES DISPONIBLES ===')
    plans = controllers['memberships'].list_plans()
    for plan in plans:
        print(plan)

    print('\n=== ASIGNAR MEMBRESIA ===')
    membership = controllers['memberships'].assign_membership(user.id, plans[0].id)
    print(membership)

    print('\n=== REGISTRAR PAGO ===')
    payment = controllers['payments'].register_payment(
        user_id=user.id,
        user_membership_id=membership.id,
        amount=plans[0].price,
        method=PaymentMethod.TRANSFER,
        reference='TRX-0001',
    )
    print(payment)

    print('\n=== CONSULTAR USUARIOS ===')
    for item in controllers['users'].list_users():
        print(item)

    print('\n=== CAMBIAR ESTADO DEL USUARIO ===')
    updated_user = controllers['users'].change_user_status(user.id, UserStatus.ACTIVE)
    print(updated_user)

    print('\n=== BITACORA DE ACCESO ===')
    for log in controllers['access_logs'].list_access_logs():
        print(log)


if __name__ == '__main__':
    run_demo()
