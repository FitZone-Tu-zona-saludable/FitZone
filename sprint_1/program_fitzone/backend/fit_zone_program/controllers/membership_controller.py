from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.models.membership import Membership


CATALOG = [
    {
        'id': 1,
        'name': 'Basica',
        'price': 50000,
        'duration': 30,
        'benefits': 'Acceso a maquinas y zona cardio',
    },
    {
        'id': 2,
        'name': 'Premium',
        'price': 80000,
        'duration': 30,
        'benefits': 'Maquinas, cardio y clases grupales',
    },
    {
        'id': 3,
        'name': 'VIP',
        'price': 120000,
        'duration': 30,
        'benefits': 'Todos los beneficios + entrenador base',
    },
]


class MembershipController:
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

    def list_catalog(self):
        return {'success': True, 'data': CATALOG}

    def get_user_membership(self, user_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT membership_id, user_id, membership_plan, membership_price,
                   membership_duration, membership_benefits, membership_status
            FROM memberships WHERE user_id = %s
            ORDER BY membership_id DESC LIMIT 1
            ''',
            (user_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return {'success': True, 'data': dict(row) if row else None}

    def select_membership(self, user_id, membership_plan, membership_price, membership_duration,
                          membership_benefits, membership_status='active'):
        if not self.user_exists(user_id):
            return {'success': False, 'message': 'The user does not exist.'}
        if membership_price <= 0 or membership_duration <= 0:
            return {'success': False, 'message': 'Price and duration must be greater than zero.'}

        membership = Membership(
            membership_id=None,
            user_id=user_id,
            membership_plan=membership_plan,
            membership_price=membership_price,
            membership_duration=membership_duration,
            membership_benefits=membership_benefits,
            membership_status=membership_status,
        )
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO memberships (
                user_id, membership_plan, membership_price, membership_duration,
                membership_benefits, membership_status
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                membership.get_user_id(),
                membership.get_membership_plan(),
                membership.get_membership_price(),
                membership.get_membership_duration(),
                membership.get_membership_benefits(),
                membership.get_membership_status(),
            ),
        )
        connection.commit()
        membership_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {'success': True, 'message': 'Membership assigned successfully.', 'membership_id': membership_id}
