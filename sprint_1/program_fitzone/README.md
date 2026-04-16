# FitZone corregido y preparado para Supabase

Proyecto organizado en MVC con backend y frontend separados.

## Qué quedó corregido
- Imports normalizados para que no dependan de la carpeta desde donde ejecutes Python.
- Estructura convertida en paquetes para evitar errores entre `controllers`, `services` y `views`.
- Script de arranque desde raíz para el frontend.
- Base de datos local con SQLite por defecto.
- Preparación para Supabase/Postgres por variables de entorno.

## Usuarios de prueba
- admin@gym.com / 1234
- client@gym.com / 1234
- security@gym.com / 1234

## Instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecutar prueba rápida
```bash
python test_program.py
```

## Ejecutar demo por consola
```bash
python run_console_demo.py
```

## Ejecutar frontend
```bash
python start_frontend.py
```

## Usar SQLite local
De forma predeterminada el proyecto usa SQLite y crea la base en:
`backend/fit_zone_program/data/gym_management.sqlite3`

## Preparar Supabase
1. Copia `.env.example` a `.env`
2. Cambia `FITZONE_DB_PROVIDER=postgres`
3. Completa `SUPABASE_DB_URL`
4. Ejecuta:
```bash
python backend/fit_zone_program/database/setup_supabase.py
```

## Nota
`SUPABASE_URL` y `SUPABASE_KEY` quedaron documentados para una futura integración con la API REST/Auth de Supabase, pero la conexión actual del proyecto está preparada por Postgres para mantener compatibilidad con tu MVC actual.
