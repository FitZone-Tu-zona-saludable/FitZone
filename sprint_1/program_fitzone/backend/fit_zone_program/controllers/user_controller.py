import hashlib
from backend.fit_zone_program.config.database import DatabaseConnection
from backend.fit_zone_program.models.user import User


class UserController:
    def __init__(self, database_connection: DatabaseConnection):
        self.__database_connection = database_connection

    def encrypt_password(self, user_password):
        return hashlib.sha256(user_password.encode()).hexdigest()

    def email_exists(self, user_email):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT user_id FROM users WHERE user_email = %s', (user_email.lower(),))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def register_user(self, user_name, user_email, user_password, user_role='client', user_status='active'):
        user_name = (user_name or '').strip()
        user_email = (user_email or '').strip().lower()
        user_password = (user_password or '').strip()
        user_role = (user_role or 'client').strip().lower()

        if not user_name or not user_email or not user_password:
            return {'success': False, 'message': 'Name, email and password are required.'}

        if self.email_exists(user_email):
            return {'success': False, 'message': 'The email is already registered.'}

        encrypted_password = self.encrypt_password(user_password)
        user = User(None, user_name, user_email, encrypted_password, user_role, user_status)

        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO users (user_name, user_email, user_password, user_role, user_status)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (
                user.get_user_name(),
                user.get_user_email(),
                user.get_user_password(),
                user.get_user_role(),
                user.get_user_status(),
            ),
        )
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {'success': True, 'message': 'User registered successfully.', 'user_id': user_id}

    def authenticate_user(self, user_email, user_password):
        user_email = (user_email or '').strip().lower()
        user_password = (user_password or '').strip()

        if not user_email or not user_password:
            return {'success': False, 'message': 'Email and password are required.'}

        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            'SELECT user_id, user_name, user_email, user_password, user_role, user_status FROM users WHERE user_email = %s',
            (user_email,),
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row is None:
            return {'success': False, 'message': 'User not found.'}

        encrypted_password = self.encrypt_password(user_password)
        if row['user_password'] != encrypted_password:
            return {'success': False, 'message': 'Invalid password.'}

        if row['user_status'] != 'active':
            return {'success': False, 'message': 'Inactive user.'}

        return {
            'success': True,
            'message': 'Login successful.',
            'user': {
                'user_id': row['user_id'],
                'user_name': row['user_name'],
                'user_email': row['user_email'],
                'user_role': row['user_role'],
                'user_status': row['user_status'],
            },
        }

    def delete_user(self, user_id):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        deleted = cursor._cursor.rowcount > 0
        connection.commit()
        cursor.close()
        connection.close()
        return {'success': deleted, 'message': 'User deleted.' if deleted else 'User not found.'}

    def list_users(self):
        connection = self.__database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT user_id, user_name, user_email, user_role, user_status FROM users ORDER BY user_id')
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        users = [dict(row) for row in rows]
        return {'success': True, 'data': users}
