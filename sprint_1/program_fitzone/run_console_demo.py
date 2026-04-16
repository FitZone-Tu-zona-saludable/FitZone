import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'backend' / 'fit_zone_program'))
from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.controllers.user_controller import UserController
from backend.fit_zone_program.controllers.membership_controller import MembershipController
from backend.fit_zone_program.controllers.payment_controller import PaymentController
from backend.fit_zone_program.controllers.access_controller import AccessController


def main():
    db = DatabaseConnection(database='gym_management_demo')
    users = UserController(db)
    memberships = MembershipController(db)
    payments = PaymentController(db)
    access = AccessController(db)

    if not users.email_exists('demo@fitzone.com'):
        print(users.register_user('Demo', 'demo@fitzone.com', '1234', 'client'))
    login = users.authenticate_user('demo@fitzone.com', '1234')
    access.log_access('demo@fitzone.com', 'login', 'success' if login['success'] else 'failed')
    print(login)
    selected = memberships.select_membership(login['user']['user_id'], 'Premium', 80000, 30, 'Clases grupales')
    print(selected)
    payment = payments.register_payment(login['user']['user_id'], selected['membership_id'], 80000, 'efectivo', 'REF-001')
    print(payment)
    print(payments.list_payments())
    print(payments.verify_payment(payment['payment_id']))
    print(access.list_logs())


if __name__ == '__main__':
    main()
