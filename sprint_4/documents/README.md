# FitZone - Tu zona saludable

Aplicacion de escritorio desarrollada en **Python** con enfoque **POO + MVC** para la gestion operativa y administrativa de un gimnasio. El proyecto usa **PySide6** para la interfaz grafica, **JSON** para persistencia local y **pytest + SonarQube** para pruebas y control de calidad.

## Alcance funcional

### Sprint 1
- Registro de usuarios.
- Inicio de sesion por roles.
- Consulta de tarifas y seleccion de membresia.
- Registro y verificacion de pagos.
- Control de acceso basico.

### Sprint 2
- Eliminacion de cuentas.
- Consulta y administracion de horarios.
- Gestion de entrenadores.
- Registro de trabajadores y empleados.
- Notificaciones por pago y vencimiento.
- Actualizacion del estado de membresias.

### Sprint 3
- Registro de asistencia.
- Modificacion de horarios y reasignacion de entrenadores.
- Contabilidad interna.
- Consulta y actualizacion de empleados.
- Gestion de incidencias.
- Evaluacion de usuarios.

### Sprint 4
- Generacion de reportes administrativos.
- Administracion de pago de empleados (nomina).
- Registro de encuestas de satisfaccion y evaluacion del servicio.
- Exportacion de reportes en formato JSON.

## Tecnologias
- Python 3
- PySide6
- JSON para persistencia local
- pytest
- coverage / pytest-cov
- SonarQube

## Estructura del proyecto

```text
program_fitzone/
├── app.py
├── assert_tests.py
├── sonar-project.properties
├── pytest.ini
├── data/
│   ├── users.json
│   ├── payroll.json
│   ├── surveys.json
│   └── ...
├── src/
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── assets/
├── tests/
│   ├── test_auth.py
│   ├── test_sprint2_andres.py
│   ├── test_sprint3_andres.py
│   └── test_sprint4_andres.py
└── z/
    ├── requirements.txt
    ├── README.md
    ├── Manual de usuario.txt
    └── MANUAL DE INSTALACION.txt
```

## Modulos relevantes de Sprint 4
- `src/services/payroll_service.py`: liquidacion, confirmacion y consulta de pagos de empleados.
- `src/services/survey_service.py`: registro de encuestas, promedios y sugerencias.
- `src/services/report_service.py`: reportes consolidados de clientes, membresias, contabilidad, actividad, nomina y satisfaccion.
- `tests/test_sprint4_andres.py`: suite automatizada del alcance funcional del sprint.

## Requisitos previos
- Python 3.11 o superior.
- pip.
- Entorno virtual recomendado.
- SonarQube Community (opcional, para analisis de calidad).

## Instalacion

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r z/requirements.txt
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r z/requirements.txt
```

## Ejecucion del sistema
```bash
python app.py
```

## Usuarios base
Si el archivo `data/users.json` no existe, el sistema crea usuarios iniciales:
- **Admin:** `romel@mail.com` / `123`
- **Usuario:** `user@mail.com` / `123`
- **Seguridad:** `seg@mail.com` / `123`

## Ejecucion de pruebas

### Suite completa
```bash
pytest -q
```

### Solo Sprint 4
```bash
pytest -q tests/test_sprint4_andres.py
```

### Generar coverage.xml
```bash
pytest --cov=. --cov-report=xml:coverage.xml
```

## Analisis con SonarQube
Asegurate de tener el servidor en `http://localhost:9000` y un token valido.

```bash
sonar-scanner.bat -Dsonar.host.url=http://localhost:9000 -Dsonar.token=TU_TOKEN
```

Propiedades usadas por el proyecto (`sonar-project.properties`):
- `sonar.projectKey=program_fitzone`
- `sonar.sources=src/models,src/services`
- `sonar.tests=tests`
- `sonar.python.coverage.reportPaths=coverage.xml`

## Persistencia de datos
El sistema guarda la informacion en archivos JSON dentro de la carpeta `data/`.
Esto facilita la portabilidad del proyecto, las pruebas locales y la demostracion academica sin depender de MySQL.

## Observaciones tecnicas
- El proyecto mantiene una separacion clara entre modelos, servicios e interfaz.
- El Sprint 4 esta mejor evidenciado en la capa de servicios y pruebas que en la capa de interfaz.
- El test `test_auth.py` puede fallar si se ejecuta sobre `data/users.json` con informacion previa; se recomienda aislar la persistencia en pruebas con fixtures temporales.
- Tambien se recomienda validar correos unicos al crear usuarios para evitar duplicados.

## Estado del proyecto
El incremento de Sprint 4 deja operativas las funciones de reportes, nomina y encuestas, y prepara al proyecto para el cierre tecnico del Sprint 5 con enfoque en documentacion, pruebas finales y presentacion.
