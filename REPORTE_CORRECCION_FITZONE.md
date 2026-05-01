# Reporte de corrección técnica - FitZone

## Validación realizada

- Pruebas automáticas: `121 passed, 23 skipped`.
- Cobertura final: `95.49%` sobre `src/models` y `src/services`.
- Archivo de cobertura generado: `coverage.xml`.
- Arquitectura MVC mantenida.
- Persistencia en JSON mantenida.
- Interfaz visual y flujo visible no modificados.

## Correcciones aplicadas

1. Se agregó encapsulamiento compatible en entidades con properties y métodos `get_<campo>()` / `set_<campo>(valor)`.
2. Se mantuvo compatibilidad con el código existente que accede a atributos públicos.
3. Se corrigió `AttendanceService.registrar_entrada()`: el parámetro `observaciones` ahora se usa, se guarda y se carga desde JSON.
4. Se agregó `json_storage.py` para cargar listas JSON de forma segura cuando los archivos no existen, están vacíos o contienen JSON inválido.
5. Se reforzaron pruebas unitarias reales para modelos, servicios, persistencia JSON, ramas negativas, reportes y accessors.
6. Se actualizó `sonar-project.properties` para SonarQube y cobertura.

## Archivos agregados

- `src/models/model_accessors.py`
- `src/services/json_storage.py`
- `tests/test_quality_coverage_and_accessors.py`
- `coverage.xml`

## Archivos modificados principales

- Entidades en `src/models/*.py`.
- Servicios con persistencia JSON en `src/services/*.py`.
- `src/services/attendance_service.py`.
- `sonar-project.properties`.

## Comandos para ejecutar pruebas y cobertura

```bash
python -m pytest
coverage run --source=src/models,src/services -m pytest
coverage report -m
coverage xml
```

Alternativa con pytest-cov:

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-report=xml
```

## Comando para SonarQube Scanner

```bash
sonar-scanner
```

Con token:

```bash
sonar-scanner -Dsonar.login=TU_TOKEN
```

O en versiones nuevas:

```bash
sonar-scanner -Dsonar.token=TU_TOKEN
```

## Recomendación final de sonar-project.properties

```properties
sonar.projectKey=program_fitzone
sonar.projectName=program_fitzone
sonar.host.url=http://localhost:9000

sonar.sources=src/models,src/services
sonar.tests=tests
sonar.test.inclusions=tests/**/*.py
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.version=3.13

sonar.exclusions=**/__pycache__/**,data/**,z/**,.pytest_cache/**,**/main.py,frontend/**,src/ui/**
sonar.coverage.exclusions=**/__init__.py
```

## Nota

El código completo corregido está dentro del proyecto entregado en el archivo `.zip`.
