from pathlib import Path

from backend.fit_zone_program.config.database import DatabaseConnection


def main():
    db = DatabaseConnection()
    if db.provider != 'postgres':
        raise RuntimeError('Configura FITZONE_DB_PROVIDER=postgres antes de ejecutar este script.')

    schema_path = Path(__file__).resolve().with_name('supabase_schema.sql')
    sql = schema_path.read_text(encoding='utf-8')

    connection = db.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    print('Esquema creado correctamente en Supabase/Postgres.')


if __name__ == '__main__':
    main()
