import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'backend' / 'fit_zone_program'))
from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.controllers.user_controller import UserController
from backend.fit_zone_program.controllers.membership_controller import MembershipController
from backend.fit_zone_program.controllers.payment_controller import PaymentController
from backend.fit_zone_program.controllers.access_controller import AccessController


def test_flow():
    db = DatabaseConnection(database='test_gym_management')
    users = UserController(db)
    memberships = MembershipController(db)
    payments = PaymentController(db)
    access = AccessController(db)

    email = 'qa@fitzone.com'
    if not users.email_exists(email):
        result = users.register_user('QA', email, '1234', 'client')
        assert result['success']

    login = users.authenticate_user(email, '1234')
    assert login['success']
    access.log_access(email, 'login', 'success')

    selection = memberships.select_membership(login['user']['user_id'], 'Basica', 50000, 30, 'Acceso')
    assert selection['success']

    payment = payments.register_payment(login['user']['user_id'], selection['membership_id'], 50000, 'efectivo', 'QA-001')
    assert payment['success']

    listed = payments.list_payments()
    assert listed['success'] and len(listed['data']) >= 1

    verified = payments.verify_payment(payment['payment_id'])
    assert verified['success']

    logs = access.list_logs()
    assert logs['success'] and len(logs['data']) >= 1


if __name__ == '__main__':
    test_flow()
    print('OK')
