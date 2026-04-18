# FitZone

Sistema de gestión de gimnasio desarrollado en **Python** con arquitectura **MVC**, backend y frontend separados, persistencia local con **SQLite** por defecto y compatibilidad con **PostgreSQL/Supabase** por variables de entorno.

## Descripción general

FitZone permite gestionar el flujo base de un gimnasio durante el Sprint 1 del proyecto:

- registro de usuarios
- autenticación de acceso
- selección de membresías
- registro y verificación de pagos
- consulta de bitácora de accesos

El proyecto está organizado para que la lógica del negocio quede separada de la interfaz, facilitando mantenimiento, pruebas y futuras ampliaciones.

## Características principales

- Arquitectura **MVC**
- Backend en Python
- Frontend de escritorio con **PySide6**
- Base de datos local con **SQLite**
- Preparación para **PostgreSQL / Supabase**
- Validaciones básicas en registro, membresías y pagos
- Prueba rápida del flujo principal
- Estructura modular para continuar con siguientes sprints

## Tecnologías utilizadas

- **Python 3**
- **PySide6**
- **SQLite**
- **psycopg2-binary**
- **PostgreSQL / Supabase** (opcional)
- **SonarQube** para análisis estático de código

## Estructura del proyecto

```text
program_fitzone/
├── backend/
│   └── fit_zone_program/
│       ├── config/
│       ├── controllers/
│       ├── database/
│       ├── data/
│       ├── models/
│       ├── main.py
│       └── sprint_1_summary.md
├── frontend/
│   └── frontend/
│       ├── assets/
│       ├── controllers/
│       ├── models/
│       ├── services/
│       ├── views/
│       └── main.py
├── requirements.txt
├── run_console_demo.py
├── start_frontend.py
├── test_program.py
└── sonar-project.properties
```

## Módulos funcionales

### Backend
Incluye la lógica principal del sistema:

- **UserController**: registro, validación de correo y autenticación
- **MembershipController**: catálogo y asignación de membresías
- **PaymentController**: registro, consulta y verificación de pagos
- **AccessController**: registro de accesos y consulta de bitácora

### Frontend
Incluye vistas y controladores para la interacción del usuario:

- inicio de sesión
- creación de cuenta
- dashboard principal
- gestión de membresías
- registro y verificación de pagos
- horarios y vistas auxiliares

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Python 3.10 o superior**
- **pip**
- entorno virtual recomendado

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd TU-REPOSITORIO
```

### 2. Crear entorno virtual

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución del proyecto

### Ejecutar prueba rápida del flujo principal

```bash
python test_program.py
```

Esta prueba valida de forma básica:

- registro de usuario
- inicio de sesión
- selección de membresía
- registro de pago
- verificación de pago
- consulta de logs

### Ejecutar demo por consola

```bash
python run_console_demo.py
```

### Ejecutar el frontend

```bash
python start_frontend.py
```

## Base de datos

### Opción 1: SQLite local (predeterminada)

El proyecto usa SQLite por defecto y crea la base de datos automáticamente en:

```text
backend/fit_zone_program/data/gym_management.sqlite3
```

También puede generar bases auxiliares para pruebas y demo, por ejemplo:

- `test_gym_management.sqlite3`
- `gym_management_demo.sqlite3`

### Opción 2: PostgreSQL / Supabase

El sistema puede conectarse a PostgreSQL o Supabase usando variables de entorno.

Configura un archivo `.env` con valores como estos:

```env
FITZONE_DB_PROVIDER=postgres
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=tu_clave
DB_NAME=gym_management
DB_SSLMODE=require
SUPABASE_DB_URL=
SUPABASE_URL=
SUPABASE_KEY=
```

Si vas a trabajar con Supabase/PostgreSQL, revisa además:

```text
backend/fit_zone_program/database/setup_supabase.py
backend/fit_zone_program/database/supabase_schema.sql
```

## Usuarios de prueba

Puedes usar estos accesos de ejemplo si están cargados en tu entorno:

- `admin@gym.com / 1234`
- `client@gym.com / 1234`
- `security@gym.com / 1234`

## Flujo básico del sistema

1. Registrar usuario
2. Autenticar usuario
3. Seleccionar membresía
4. Registrar pago
5. Verificar pago
6. Consultar historial o bitácora de accesos

## Pruebas y calidad

El proyecto incluye:

- script de prueba rápida: `test_program.py`
- demo funcional: `run_console_demo.py`
- configuración de análisis estático: `sonar-project.properties`

De acuerdo con el análisis mostrado en SonarQube del Sprint 1:

- **Quality Gate:** Passed
- **Reliability:** A
- **Maintainability:** A
- **Security:** presenta observaciones que deben revisarse en siguientes iteraciones

## Estado del proyecto

Este repositorio corresponde al desarrollo base del **Sprint 1**.  
La estructura quedó preparada para continuar con nuevos módulos y mejoras en sprints posteriores.

## Posibles mejoras futuras

- cifrado más robusto de contraseñas con `bcrypt`
- integración completa con Supabase Auth
- pruebas unitarias más amplias
- manejo de roles más detallado
- mejoras visuales y navegación del frontend
- reportes administrativos

## Autor

**Andres Valdes**

## Licencia

Proyecto académico desarrollado para la asignatura de Ingeniería de Software.
