import os
import sqlite3
from pathlib import Path


class BaseCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def lastrowid(self):
        return getattr(self._cursor, 'lastrowid', None)

    def close(self):
        self._cursor.close()

    @property
    def rowcount(self):
        return getattr(self._cursor, 'rowcount', 0)


class SQLiteCursorWrapper(BaseCursorWrapper):
    def execute(self, query, params=()):
        query = query.replace('%s', '?')
        return self._cursor.execute(query, params)

    def executemany(self, query, seq_of_params):
        query = query.replace('%s', '?')
        return self._cursor.executemany(query, seq_of_params)


class SQLiteConnectionWrapper:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return SQLiteCursorWrapper(self._connection.cursor())

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


class PostgresCursorWrapper(BaseCursorWrapper):
    def execute(self, query, params=()):
        self._cursor.execute(query, params)
        return self

    def executemany(self, query, seq_of_params):
        self._cursor.executemany(query, seq_of_params)
        return self


class PostgresConnectionWrapper:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return PostgresCursorWrapper(self._connection.cursor())

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


class DatabaseConnection:
    def __init__(self, host='localhost', user='postgres', password='', database='gym_management'):
        self.provider = os.getenv('FITZONE_DB_PROVIDER', 'sqlite').strip().lower()
        self.host = os.getenv('DB_HOST', host)
        self.user = os.getenv('DB_USER', user)
        self.password = os.getenv('DB_PASSWORD', password)
        self.database = os.getenv('DB_NAME', database)
        self.supabase_db_url = os.getenv('SUPABASE_DB_URL', '').strip()
        self.supabase_url = os.getenv('SUPABASE_URL', '').strip()
        self.supabase_key = os.getenv('SUPABASE_KEY', '').strip()

        base_dir = Path(__file__).resolve().parents[1]
        self.base_dir = base_dir
        self.data_dir = base_dir / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._db_path = self.data_dir / f'{self.database}.sqlite3'

        if self.provider == 'sqlite':
            self._initialize_sqlite_schema()

    def connect(self):
        if self.provider == 'postgres':
            return self._connect_postgres()
        return self._connect_sqlite()

    def _connect_sqlite(self):
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON')
        return SQLiteConnectionWrapper(connection)

    def _connect_postgres(self):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError as exc:
            raise RuntimeError(
                'No se encontró psycopg2. Instala dependencias con: pip install -r requirements.txt'
            ) from exc

        dsn = self.supabase_db_url or os.getenv('DATABASE_URL', '').strip()
        if dsn:
            connection = psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.database,
                cursor_factory=psycopg2.extras.RealDictCursor,
                sslmode=os.getenv('DB_SSLMODE', 'require'),
            )
        return PostgresConnectionWrapper(connection)

    def _initialize_sqlite_schema(self):
        connection = sqlite3.connect(self._db_path)
        connection.execute('PRAGMA foreign_keys = ON')
        cursor = connection.cursor()
        cursor.executescript(
            '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL UNIQUE,
                user_password TEXT NOT NULL,
                user_role TEXT NOT NULL,
                user_status TEXT NOT NULL DEFAULT 'active'
            );

            CREATE TABLE IF NOT EXISTS memberships (
                membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                membership_plan TEXT NOT NULL,
                membership_price REAL NOT NULL,
                membership_duration INTEGER NOT NULL,
                membership_benefits TEXT,
                membership_status TEXT NOT NULL DEFAULT 'active',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                membership_id INTEGER NOT NULL,
                payment_amount REAL NOT NULL,
                payment_date TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                payment_reference TEXT NOT NULL,
                payment_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (membership_id) REFERENCES memberships(membership_id)
            );

            CREATE TABLE IF NOT EXISTS access_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                action TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            '''
        )
        connection.commit()
        connection.close()
