# FITZONE
## README técnico y funcional - Sprint 3

**Autor:** Andres Valdes  
**Fecha del documento:** 19 de abril de 2026

---

## 1. Resumen

| Campo | Detalle |
|---|---|
| **Proyecto** | FitZone - Sistema de gestión de gimnasio |
| **Versión documentada** | Estado acumulado hasta Sprint 3 |
| **Arquitectura** | Python + POO + MVC + PySide6 |
| **Persistencia** | Archivos JSON locales en carpeta `data`; **no se usa base de datos en esta versión** |
| **Estado de calidad** | Quality Gate **Passed** en SonarQube con **85.3%** de cobertura del nuevo código |

---

## 2. Revisión histórica

| Fecha | Versión | Descripción | Autor |
|---|---:|---|---|
| 19/04/2026 | 1.0 | Creación del README técnico y funcional consolidado del proyecto FitZone hasta Sprint 3. | Andres Valdes |

---

## 3. Introducción

Este documento README resume la estructura, propósito, tecnologías, forma de ejecución y estado funcional del proyecto **FitZone** hasta el **Sprint 3**. Se elaboró con base en el programa entregado, la organización del proyecto y la evidencia de calidad observada en SonarQube.

La versión actual del sistema está orientada a la gestión de usuarios y a la operación administrativa del gimnasio. Como decisión técnica actual, la persistencia **ya no se realiza con base de datos**, sino mediante **archivos JSON locales por módulo**.

---

## 4. Descripción general del sistema

FitZone es una aplicación de escritorio desarrollada en **Python** para apoyar la gestión de un gimnasio. El sistema separa la lógica del negocio, los modelos y la interfaz gráfica, organizando las responsabilidades en capas claramente diferenciadas.

A nivel funcional, el proyecto integra:

- autenticación por roles,
- administración de usuarios,
- gestión de horarios,
- gestión de entrenadores y personal,
- módulos administrativos del Sprint 3.

Entre los módulos consolidados en este sprint se encuentran:

- asistencia,
- contabilidad,
- incidencias,
- notificaciones al trabajador,
- evaluaciones de usuarios,
- reasignaciones de horarios.

---

## 5. Arquitectura y organización del proyecto

| Componente | Descripción |
|---|---|
| `app.py` | Punto de entrada de la aplicación. Inicia la interfaz y carga la vista de login. |
| `src/models` | Entidades del sistema: cliente, empleado, entrenador, asistencia, contabilidad, incidencia, notificación, evaluación y horario. |
| `src/services` | Lógica de negocio y persistencia de cada módulo. Aquí se concentran reglas, validaciones y acceso a los archivos JSON. |
| `src/ui` | Vistas del sistema en PySide6 para login, administración, asistencia, contabilidad, empleados, incidencias, evaluaciones y reasignación. |
| `tests` | Pruebas automatizadas por módulo. Incluye pruebas de autenticación, Sprint 2 y Sprint 3. |
| `data` | Archivos JSON persistentes que almacenan la información operativa del sistema. |
| `sonar-project.properties` | Configuración del análisis estático y de la cobertura reportada a SonarQube. |

---

## 6. Persistencia actual por archivos JSON

En esta versión del proyecto, **se elimina el uso de base de datos** como mecanismo de persistencia. Toda la información del sistema se almacena en **archivos JSON** ubicados en la carpeta `data`.

### Archivos principales de persistencia

| Archivo | Uso principal |
|---|---|
| `users.json` | Usuarios, roles, pagos y estado de membresía. |
| `workers.json` | Trabajadores y empleados con información laboral. |
| `trainers.json` | Entrenadores, disponibilidad y horarios asociados. |
| `schedules.json` | Horarios del gimnasio y reasignaciones. |
| `attendance.json` | Registros de asistencia por cliente. |
| `accounting.json` | Cobros, pagos, saldos pendientes y vencidos. |
| `incidents.json` | Incidencias del personal y su resolución. |
| `notifications.json` | Notificaciones a clientes y trabajadores. |
| `evaluations.json` | Evaluaciones de desempeño de usuarios. |
| `logs.json` | Registro de actividad y trazabilidad básica del sistema. |

### Implicación técnica

> **Importante:** a partir de Sprint 3, el sistema **ya no usa base de datos**. La persistencia oficial del proyecto se realiza con **archivos JSON**.

---

## 7. Módulos funcionales disponibles

### 7.1 Módulos base y acumulados de sprints previos

- Autenticación por roles y control básico de permisos.
- Gestión de usuarios: creación, consulta, actualización y eliminación.
- Control de membresías, pagos y notificaciones para clientes.
- Gestión de horarios, asignación y selección de entrenadores.
- Registro y administración de trabajadores y personal del gimnasio.

### 7.2 Módulos incorporados o consolidados en el Sprint 3

- Registro de asistencia del cliente con fecha, hora, servicio y observaciones.
- Módulo contable para registrar cobros, confirmar pagos y calcular totales recaudados o pendientes.
- Consulta ampliada y actualización de empleados, incluyendo estado laboral, contrato, salario y descuento.
- Registro y seguimiento de incidencias del personal con causa y fecha automática.
- Generación de notificaciones dirigidas a trabajadores por pagos y vencimientos.
- Evaluación del desempeño de usuarios por entrenadores con promedio y filtros de consulta.
- Modificación de horarios por eventos externos y reasignación de entrenadores disponibles.

---

## 8. Tecnologías empleadas

- **Python** como lenguaje principal del proyecto.
- **PySide6** para la construcción de la interfaz gráfica de escritorio.
- **pytest** para pruebas automatizadas.
- **SonarQube Community** para análisis estático de calidad.
- **Archivos JSON** para persistencia local.

---

## 9. Instalación y ejecución

### 9.1 Crear entorno virtual

```bash
python -m venv venv
```

### 9.2 Activar el entorno virtual

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 9.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 9.4 Ejecutar la aplicación

```bash
python app.py
```

### 9.5 Ejecutar pruebas

```bash
pytest
```

---

## 10. Pruebas y calidad

| Elemento | Detalle |
|---|---|
| **Pruebas automatizadas** | El repositorio contiene pruebas para autenticación, funcionalidades del Sprint 2 y 41 pruebas específicas del Sprint 3. |
| **Cobertura** | El análisis visible en SonarQube reporta **85.3%** de cobertura para el nuevo código del sprint. |
| **Issues nuevos** | **0** issues nuevos en la ejecución que cerró el Sprint 3. |
| **Duplicación** | **0.0%** en el análisis mostrado. |
| **Seguridad** | **0 security hotspots** pendientes de revisión manual, con nota **A**. |
| **Quality Gate** | Estado **Passed** al cierre del análisis presentado. |

---

## 11. Consideraciones de uso y mantenimiento

- Como la persistencia se realiza con archivos JSON reales en la carpeta `data`, el estado del sistema puede acumular información de ejecuciones previas.
- Para pruebas limpias conviene respaldar o reiniciar esos archivos antes de correr nuevos escenarios.
- La decisión de abandonar la base de datos simplifica la ejecución local y la entrega académica.
- Esta decisión también implica limitaciones de escalabilidad, concurrencia y control centralizado de integridad.
- Para una versión futura más robusta podría retomarse una capa de persistencia basada en base de datos.
- Las vistas del sistema ya están separadas de los servicios, por lo que el proyecto mantiene una base razonable para ampliar funcionalidades en sprints posteriores sin mezclar interfaz y lógica de negocio.

---

## 12. Cierre

El estado actual del proyecto **FitZone** refleja un incremento funcional más maduro que el de los sprints previos. El **Sprint 3** consolida la operación administrativa interna del gimnasio y mejora la calidad técnica observable en SonarQube.

Este README deja explícito que la persistencia vigente del sistema es mediante **archivos JSON locales**, decisión que debe mantenerse documentada en cualquier entrega, demo o sustentación del proyecto.
