from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.controllers.user_controller import UserController
from backend.fit_zone_program.controllers.membership_controller import MembershipController
from backend.fit_zone_program.controllers.payment_controller import PaymentController


def main():
    database_connection = DatabaseConnection(
        host='localhost',
        user='root',
        password='Av2005609@',
        database='gym_management'
    )

    user_controller = UserController(database_connection)
    membership_controller = MembershipController(database_connection)
    payment_controller = PaymentController(database_connection)

    user_result = user_controller.register_user(
        user_name='Andres Diaz',
        user_email='andres@example.com',
        user_password='123456',
        user_role='client'
    )
    print(user_result)

    if user_result['success']:
        membership_result = membership_controller.select_membership(
            user_id=user_result['user_id'],
            membership_plan='Premium',
            membership_price=120.00,
            membership_duration=30,
            membership_benefits='Gym access, trainer support, nutrition guide'
        )
        print(membership_result)

        if membership_result['success']:
            payment_result = payment_controller.register_payment(
                user_id=user_result['user_id'],
                membership_id=membership_result['membership_id'],
                payment_amount=120.00,
                payment_method='card',
                payment_reference='PAY-1001'
            )
            print(payment_result)


if __name__ == '__main__':
    main()
