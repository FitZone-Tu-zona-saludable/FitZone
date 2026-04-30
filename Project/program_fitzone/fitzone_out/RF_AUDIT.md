# Auditoría RF1–RF29

Esta matriz se reconstruye desde `README.md`, `MANUAL_USUARIO_SPRINT5.md`,
comentarios `RFxx` en vistas/controladores y pruebas en `tests/`.

No aparece en el `zip` una tabla formal única con la definición exacta de
RF1–RF29, así que los rótulos marcados como "inferencia" son una
reconstrucción técnica de la numeración.

| RF | Funcionalidad | Estado | Evidencia |
|---|---|---|---|
| RF1 | Login por rol | completo | `frontend/views/login_view.py`, `tests/test_frontend_smoke.py` |
| RF2 | Registro de usuarios | completo | `frontend/views/login_view.py`, `tests/test_auth.py` |
| RF3 | Consultar planes y tarifas | completo | `frontend/views/membership_list_view.py` |
| RF4 | Seleccionar membresía | completo | `frontend/views/membership_select_view.py`, `tests/test_membership_payment_flow.py` |
| RF5 | Notificar pago a trabajador | completo | `frontend/views/worker_notifications_view.py`, `src/services/notification_service.py` |
| RF6 | Evaluar desempeño de usuarios | completo | `frontend/views/performance_view.py`, `tests/test_sprint3_andres.py` |
| RF7 | Registrar pago de cliente | completo | `frontend/views/payment_register_view.py`, `tests/test_membership_payment_flow.py` |
| RF8 | Notificar vencimiento de membresía a trabajador | completo | `frontend/views/worker_notifications_view.py`, `tests/test_sprint3_andres.py` |
| RF9 | Verificar pago de cliente (inferencia) | completo | `frontend/views/payment_verification_view.py`, `src/services/payment_service.py` |
| RF10 | Consultar horarios disponibles (inferencia) | completo | `frontend/views/schedule_consult_view.py` |
| RF11 | Administrar horarios (inferencia) | completo | `frontend/views/schedule_admin_view.py`, `src/services/schedule_service.py` |
| RF12 | Seleccionar entrenador (inferencia) | completo | `frontend/views/trainer_select_view.py`, `frontend/services/api_service_ext.py` |
| RF13 | Administrar entrenadores (inferencia) | completo | `frontend/views/trainer_admin_view.py`, `src/services/trainer_service.py` |
| RF14 | Registrar trabajador y empleado (inferencia) | completo | `frontend/views/staff_register_view.py`, `src/services/worker_service.py` |
| RF15 | Actualización del afiche de asistencia del cliente | completo | `frontend/views/attendance_view.py`, `tests/test_sprint3_andres.py` |
| RF16 | Bitácora y control de accesos (inferencia) | completo | `frontend/views/security_view.py`, `src/services/security_service.py` |
| RF17 | Modificación de horarios y reasignación de entrenadores | completo | `frontend/views/schedule_reassign_view.py`, `tests/test_sprint3_andres.py` |
| RF18 | Alertas del sistema (inferencia) | completo | `frontend/views/pages/alerts_page.py` |
| RF19 | Consulta de datos/membresía del usuario (inferencia) | completo | `frontend/views/main_dashboard_view.py`, `frontend/views/membership_list_view.py` |
| RF20 | Gestión operativa de pagos y membresías desde administración (inferencia) | completo | `frontend/views/payment_verification_view.py`, `frontend/views/reports_view.py` |
| RF21 | Administrar cuenta / contabilidad | completo | `frontend/views/accounting_view.py`, `tests/test_sprint3_andres.py` |
| RF22 | Actualizar datos de empleados | completo | `frontend/views/employee_detail_view.py`, `tests/test_sprint3_andres.py` |
| RF23 | Generar reportes | completo | `frontend/views/reports_view.py`, `tests/test_sprint4_andres.py` |
| RF24 | Consultar información de empleado | completo | `frontend/views/employee_detail_view.py`, `tests/test_sprint3_andres.py` |
| RF25 | Liquidación de nómina (inferencia) | completo | `src/services/payroll_service.py`, `tests/test_sprint4_andres.py` |
| RF26 | Administrar pago de empleado | completo | `frontend/views/employee_payment_view.py`, `tests/test_sprint4_andres.py` |
| RF27 | Encuestas / evaluación de entrenadores | completo | `frontend/views/survey_view.py`, `tests/test_sprint4_andres.py` |
| RF28 | Gestión del personal / incidencias | completo | `frontend/views/incident_view.py`, `tests/test_sprint3_andres.py` |
| RF29 | Integración del sistema Sprint 5 por rol (inferencia) | completo | `frontend/views/pages/sprint5_page.py`, `tests/test_frontend_smoke.py` |

## Observaciones

- La ausencia de una matriz RF formal en el repositorio obligó a reconstruir
  varios rótulos a partir de los artefactos disponibles.
- El estado marcado como `completo` significa que existe flujo funcional
  backend + integración visible o prueba automatizada asociada.
