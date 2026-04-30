# Sprint 3 — Operación interna y control administrativo
## Responsable: Alex — Interfaz visual e integración
**Fecha:** Sprint 3 | Proyecto FitZone | Python + PySide6 + MVC

---

## Objetivo del Sprint 3
Cubrir la administración interna del gimnasio: asistencia, incidencias, contabilidad y seguimiento del personal.

## Requisitos cubiertos (Alex — Interfaz)
| RF | Descripción | Vista creada |
|----|-------------|-------------|
| RF5  | Notificar pago a trabajador | `worker_notifications_view.py` |
| RF6  | Evaluar desempeño de usuarios | `performance_view.py` |
| RF8  | Notificar vencimiento de membresía a trabajador | `worker_notifications_view.py` |
| RF15 | Actualización del afiche de asistencia del cliente | `attendance_view.py` |
| RF17 | Modificación de horarios y reasignación de entrenadores | `schedule_reassign_view.py` |
| RF21 | Administrar cuenta (contabilidad) | `accounting_view.py` |
| RF22 | Actualizar datos de empleados | `employee_detail_view.py` |
| RF24 | Consultar información de empleado | `employee_detail_view.py` |
| RF28 | Gestión del personal (incidencias) | `incident_view.py` |

---

## Archivos creados por Alex en Sprint 3

### Modelos (src/models/)
- `attendance.py` — Modelo de registro de asistencia del cliente
- `performance.py` — Modelo de evaluación de desempeño
- `incident.py` — Modelo de incidencias del personal
- `account_entry.py` — Modelo de entrada contable

### Servicios (src/services/)
- `attendance_service.py` — CRUD de asistencia con persistencia JSON
- `performance_service.py` — Gestión de evaluaciones
- `incident_service.py` — Gestión de incidencias del personal
- `accounting_service.py` — Módulo contable (ingresos, cobros, saldos)

### Controladores (frontend/controllers/)
- `attendance_controller.py`
- `performance_controller.py`
- `incident_controller.py`
- `accounting_controller.py`

### Vistas PySide6 (frontend/views/)
- `attendance_view.py` — Afiche de asistencia con tabla y formulario
- `schedule_reassign_view.py` — Modificación de horarios y reasignación de entrenadores
- `accounting_view.py` — Panel contable con tarjetas de resumen
- `employee_detail_view.py` — Consulta y edición de datos del empleado
- `incident_view.py` — Registro de incidencias del personal
- `performance_view.py` — Evaluación de desempeño por entrenador
- `worker_notifications_view.py` — Notificaciones de pago y vencimiento al trabajador

### Página Sprint 3 (frontend/views/pages/)
- `sprint3_page.py` — Sidebar de navegación que integra todas las vistas anteriores

### Datos (data/)
- `attendance.json`, `performance.json`, `incidents.json`, `accounting.json`

---

## Estándar de integración respetado
- Toda vista importa sus controladores desde `frontend/controllers/`
- Todo controlador instancia el servicio real de `src/services/`
- Todos los modelos implementan `to_dict()` para persistencia JSON
- Se usa el sistema de tema `theme.py` con COLORS y ObjectNames
- No se eliminó ningún archivo ni funcionalidad de sprints anteriores

---

## Cómo ejecutar
```bash
cd sprint3/program_fitzone
pip install PySide6
python app.py
```
Login: `romel@mail.com` / `123` (admin) o `user@mail.com` / `123` (usuario)
