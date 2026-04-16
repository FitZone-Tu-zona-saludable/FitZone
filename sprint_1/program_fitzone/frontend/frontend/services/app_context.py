from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.controllers.user_controller import UserController
from backend.fit_zone_program.controllers.membership_controller import MembershipController
from backend.fit_zone_program.controllers.payment_controller import PaymentController
from backend.fit_zone_program.controllers.access_controller import AccessController


database_connection = DatabaseConnection(database='gym_management')
user_controller = UserController(database_connection)
membership_controller = MembershipController(database_connection)
payment_controller = PaymentController(database_connection)
access_controller = AccessController(database_connection)


def seed_defaults():
    defaults = [
        ('Administrador', 'admin@gym.com', '1234', 'admin'),
        ('Cliente', 'client@gym.com', '1234', 'client'),
        ('Seguridad', 'security@gym.com', '1234', 'seguridad'),
    ]
    for name, email, password, role in defaults:
        if not user_controller.email_exists(email):
            user_controller.register_user(name, email, password, role)


seed_defaults()
