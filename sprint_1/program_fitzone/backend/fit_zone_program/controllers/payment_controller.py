from datetime import date
from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.models.payment import Payment


class PaymentController:
    def __init__(self, database_connection: DatabaseConnection):
        self.__database_connection = database_connection

    def user_exists(self, user_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def membership_exists(self, membership_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT membership_id FROM memberships WHERE membership_id = %s', (membership_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def get_membership_price(self, membership_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT membership_price FROM memberships WHERE membership_id = %s', (membership_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return float(row['membership_price']) if row else None

    def membership_belongs_to_user(self, user_id, membership_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT membership_id FROM memberships WHERE membership_id = %s AND user_id = %s', (membership_id, user_id))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row is not None

    def register_payment(self, user_id, membership_id, payment_amount, payment_method,
                         payment_reference, payment_status='pending'):
        if not self.user_exists(user_id):
            return {'success': False, 'message': 'The user does not exist.'}
        if not self.membership_exists(membership_id):
            return {'success': False, 'message': 'The membership does not exist.'}
        if not self.membership_belongs_to_user(user_id, membership_id):
            return {'success': False, 'message': 'The membership does not belong to the user.'}

        expected_amount = self.get_membership_price(membership_id)
        if expected_amount is None:
            return {'success': False, 'message': 'Membership price could not be validated.'}
        if float(payment_amount) != float(expected_amount):
            return {'success': False, 'message': f'Invalid amount. Expected: {expected_amount}'}

        payment = Payment(None, user_id, membership_id, payment_amount, date.today().isoformat(), payment_method, payment_reference, payment_status)
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO payments (
                user_id, membership_id, payment_amount, payment_date,
                payment_method, payment_reference, payment_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                payment.get_user_id(),
                payment.get_membership_id(),
                payment.get_payment_amount(),
                payment.get_payment_date(),
                payment.get_payment_method(),
                payment.get_payment_reference(),
                payment.get_payment_status(),
            ),
        )
        connection.commit()
        payment_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {'success': True, 'message': 'Payment registered successfully.', 'payment_id': payment_id}

    def list_payments(self):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT p.payment_id AS id, u.user_name AS user, p.payment_amount AS amount,
                   p.payment_method AS method, p.payment_reference AS reference,
                   p.payment_status AS status, p.membership_id AS membership_id, p.user_id AS user_id
            FROM payments p
            INNER JOIN users u ON u.user_id = p.user_id
            ORDER BY p.payment_id DESC
            '''
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return {'success': True, 'data': [dict(row) for row in rows]}

    def verify_payment(self, payment_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE payments SET payment_status = %s WHERE payment_id = %s', ('paid', payment_id))
        updated = cursor._cursor.rowcount > 0
        connection.commit()
        cursor.close()
        connection.close()
        return {'success': updated, 'message': 'Payment verified.' if updated else 'Payment not found.'}
