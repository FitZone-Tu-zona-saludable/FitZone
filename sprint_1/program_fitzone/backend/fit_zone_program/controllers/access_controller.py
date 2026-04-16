from backend.fit_zone_program.config.database import DatabaseConnection


class AccessController:
    def __init__(self, database_connection: DatabaseConnection):
        self._database_connection = database_connection

    def log_access(self, user_email, action, result):
        connection = self._database_connection.connect()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO access_logs (user_email, action, result) VALUES (%s, %s, %s)',
            ((user_email or '').strip().lower() or 'unknown', action, result),
        )
        connection.commit()
        cursor.close()
        connection.close()

    def list_logs(self):
        connection = self._database_connection.connect()
        cursor = connection.cursor()
        cursor.execute('SELECT user_email, action, result, created_at FROM access_logs ORDER BY log_id DESC')
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return {'success': True, 'data': [dict(row) for row in rows]}
