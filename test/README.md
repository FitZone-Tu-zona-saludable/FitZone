# README - Pruebas automáticas del programa FitZone

## Descripción
Este proyecto incluye un conjunto de pruebas automáticas para validar el funcionamiento del sistema **FitZone**. Las pruebas fueron diseñadas para comprobar tanto la lógica del negocio como el comportamiento de la interfaz gráfica.

El esquema de pruebas está organizado con **pytest** y contempla tres tipos principales:

- **Pruebas unitarias**: validan funciones puntuales del servicio de autenticación.
- **Pruebas funcionales**: verifican el comportamiento visible de las ventanas del sistema.
- **Pruebas de integración**: prueban flujos completos, como el inicio de sesión y la apertura de paneles según el rol del usuario.

---

## Estructura general del proyecto

```text
Fitzone-F4/
├── app.py
├── pytest.ini
├── src/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_admin_ui.py
│   ├── test_ui_login.py
│   ├── test_ui_user.py
│   ├── test_ui_security.py
│   └── test_integration.py
└── data/
```

---

## Tecnologías utilizadas en las pruebas

Las pruebas automáticas del proyecto están construidas principalmente con:

- **Python**
- **pytest** para la ejecución de pruebas
- **pytest-qt** para interacción con la interfaz gráfica
- **PySide6** para las vistas del sistema
- **JSON temporal** para aislar datos de prueba sin afectar los archivos reales

---

## Configuración de pytest

El archivo `pytest.ini` define la ruta de pruebas, el patrón de nombres y los marcadores usados en el proyecto.

Se emplean los siguientes marcadores:

- `unit`: pruebas unitarias rápidas, sin interfaz gráfica.
- `functional`: pruebas funcionales sobre la GUI.
- `integration`: pruebas de integración entre vistas, servicios y flujos del sistema.

---

## Qué validan las pruebas

### 1. Pruebas unitarias
Archivo principal: `tests/test_auth.py`

Estas pruebas verifican operaciones clave del servicio de autenticación, por ejemplo:

- creación de usuarios
- validación de datos básicos
- inicio de sesión exitoso
- rechazo de contraseñas incorrectas
- manejo de usuarios inexistentes
- registro de pagos
- eliminación de usuarios

Estas pruebas permiten confirmar que la lógica principal funciona correctamente antes de probar la interfaz.

### 2. Pruebas funcionales
Archivos principales:

- `tests/test_ui_login.py`
- `tests/test_admin_ui.py`
- `tests/test_ui_user.py`
- `tests/test_ui_security.py`

Estas pruebas validan el comportamiento de las ventanas del sistema, incluyendo:

- inicio de sesión desde la interfaz
- navegación hacia registro de usuario
- carga de panel de usuario
- visualización y actualización de logs de seguridad
- carga de tabla de usuarios en panel administrador
- creación, edición y eliminación de usuarios desde la GUI
- cierre de sesión y retorno a la pantalla de acceso

### 3. Pruebas de integración
Archivo principal: `tests/test_integration.py`

Estas pruebas comprueban flujos completos del sistema, como:

- login con rol administrador
- apertura del panel correspondiente
- carga correcta de usuarios en la tabla administrativa
- flujo de acceso del rol de seguridad y visualización de logs

---

## Aislamiento de datos de prueba

Uno de los puntos más importantes del proyecto es que las pruebas no trabajan directamente sobre los datos reales. En `conftest.py` se crea un entorno temporal con archivos como:

- `users.json`
- `logs.json`

Esto permite ejecutar pruebas repetidas sin dañar la información persistida del sistema.

Además, se preparan fixtures para:

- crear una única instancia de `QApplication`
- construir un `AuthService` temporal
- cerrar automáticamente ventanas `QMessageBox`
- simular escritura lenta en los campos de texto

---

## Requisitos para ejecutar las pruebas

Antes de ejecutar las pruebas, se recomienda tener instalado:

```bash
pip install pytest pytest-qt PySide6
```

Si el proyecto usa un entorno virtual, primero debe activarse.

---

## Ejecución de pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar solo pruebas unitarias

```bash
pytest -m unit
```

### Ejecutar solo pruebas funcionales

```bash
pytest -m functional
```

### Ejecutar solo pruebas de integración

```bash
pytest -m integration
```

### Ejecutar un archivo específico

```bash
pytest tests/test_auth.py
```

### Ejecutar una prueba específica con más detalle

```bash
pytest tests/test_auth.py -v
```

---

## Cobertura de pruebas

Si se desea medir cobertura del código, puede utilizarse `pytest-cov`.

Instalación:

```bash
pip install pytest-cov
```

Ejecución con reporte en terminal:

```bash
pytest --cov=src --cov-report=term-missing
```

Ejecución para generar `coverage.xml`:

```bash
pytest --cov=src --cov-report=xml
```

Este archivo puede utilizarse posteriormente en herramientas de análisis como SonarQube.

---

## Buenas prácticas aplicadas

En las pruebas automáticas del proyecto se aplican varias buenas prácticas:

- separación entre lógica del negocio y pruebas de interfaz
- uso de marcadores para clasificar escenarios
- aislamiento de datos con archivos temporales
- automatización de eventos visuales con `qtbot`
- simulación de interacción real del usuario
- pruebas por roles del sistema: administrador, usuario y seguridad

---

## Alcance del sistema probado

Las pruebas cubren principalmente estos módulos:

- autenticación de usuarios
- panel de administrador
- panel de usuario
- panel de seguridad
- flujo de acceso según rol
- persistencia temporal de usuarios y logs para escenarios de prueba

---

## Limitaciones actuales

Aunque el conjunto de pruebas es útil y funcional, todavía puede ampliarse con:

- validaciones más profundas de errores de entrada
- pruebas de persistencia final con archivos reales controlados
- pruebas de rendimiento
- pruebas de regresión más amplias
- integración continua con ejecución automática en cada cambio

---

## Conclusión

El sistema de pruebas automáticas de **FitZone** permite verificar de forma organizada tanto la lógica interna como los flujos principales de la interfaz gráfica. Gracias al uso de `pytest`, `pytest-qt` y datos temporales en JSON, el proyecto cuenta con una base sólida para asegurar calidad, detectar errores y facilitar futuras mejoras.
