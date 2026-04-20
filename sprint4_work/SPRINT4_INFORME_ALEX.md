# Sprint 4 — Reportes, nómina y evaluación del servicio
## Responsable: Alex — Interfaz visual e integración
**Fecha:** Sprint 4 | Proyecto FitZone | Python + PySide6 + MVC

---

## Objetivo del Sprint 4
Cerrar funciones directivas del sistema: reportes, pago de empleados y evaluación del servicio.

## Requisitos cubiertos (Alex — Interfaz)
| RF  | Descripción | Vista creada |
|-----|-------------|-------------|
| RF23 | Generar reportes | `reports_view.py` (3 pestañas: membresías, actividad, financiero) |
| RF26 | Administrar pago de empleado | `employee_payment_view.py` |
| RF27 | Evaluación de entrenadores | `survey_view.py` |

---

## Archivos creados por Alex en Sprint 4

### Modelos (src/models/)
- `employee_payment.py` — Liquidación de empleado (horas × valor_hora − descuentos)
- `satisfaction_survey.py` — Encuesta de satisfacción (entrenador + instalaciones)

### Servicios (src/services/)
- `employee_payment_service.py` — Liquidaciones con persistencia JSON
- `survey_service.py` — Encuestas con cálculo de promedios por entrenador
- `report_service.py` — Consolidación de reportes: membresías, actividad, financiero

### Controladores (frontend/controllers/)
- `employee_payment_controller.py`
- `survey_controller.py`
- `report_controller.py`

### Vistas PySide6 (frontend/views/)
- `reports_view.py` — Generación de reportes con 3 tabs (membresías, pagos, financiero)
- `employee_payment_view.py` — Liquidación de nómina con horas, descuentos y valor neto
- `survey_view.py` — Encuesta de satisfacción + resultados y promedios por entrenador

### Página Sprint 4 (frontend/views/pages/)
- `sprint4_page.py` — Sidebar con acceso a reportes, nómina y encuestas

### Datos (data/)
- `employee_payments.json`, `surveys.json`

---

## Herencia de Sprints anteriores
Sprint 4 incluye **todo lo del Sprint 3** (asistencia, horarios, contabilidad, empleados, incidencias, evaluaciones, notificaciones) más los módulos nuevos.

---

## Cómo ejecutar
```bash
cd sprint4/program_fitzone
pip install PySide6
python app.py
```
Login: `romel@mail.com` / `123` (admin)
