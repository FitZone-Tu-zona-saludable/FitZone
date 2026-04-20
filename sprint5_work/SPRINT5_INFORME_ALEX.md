# Sprint 5 — Cierre técnico, manual de usuario y material visual
## Responsable: Alex — Interfaz visual e integración
**Fecha:** Sprint 5 | Proyecto FitZone | Python + PySide6 + MVC

---

## Objetivo del Sprint 5
Preparar la versión final del sistema para entrega, sustentación y publicación de evidencias.

## Tareas de Alex — Sprint 5
| Tarea | Estado | Entregable |
|-------|--------|-----------|
| Pulir pantallas finales | ✅ | `main_dashboard_view.py` + tema unificado |
| Dashboard principal nuevo | ✅ | `main_dashboard_view.py` |
| Sistema completo integrado | ✅ | `sprint5_page.py` (todos los módulos) |
| app.py actualizado con tema global | ✅ | `app.py` → `apply_theme()` |
| Manual de usuario | ✅ | `MANUAL_USUARIO_SPRINT5.md` |
| Ficha de catalogación | ✅ | `FICHA_CATALOGACION.md` |
| Flujos documentados para sustentación | ✅ | Sección en este documento |

---

## Archivos creados/modificados por Alex en Sprint 5

### Vistas (frontend/views/)
- `main_dashboard_view.py` — Dashboard de bienvenida con accesos rápidos a todos los módulos

### Páginas (frontend/views/pages/)
- `sprint5_page.py` — Integración TOTAL del sistema (todos los sprints en un solo panel)

### App principal
- `app.py` — Actualizado para usar `apply_theme()` del tema centralizado

---

## Flujos principales para la demo (sustentación)

### Flujo 1 — Acceso y membresía
1. Login: `romel@mail.com` / `123`
2. Ver dashboard → Membresías → Seleccionar plan
3. Registrar pago → Verificar pago

### Flujo 2 — Operación del gimnasio
1. Horarios → ver y agregar sesión
2. Entrenadores → ver disponibilidad
3. Personal → registrar empleado

### Flujo 3 — Administración interna (Sprint 3)
1. Asistencia → registrar entrada de cliente
2. Contabilidad → agregar ingreso y marcarlo como pagado
3. Incidencias → reportar inasistencia de trabajador
4. Evaluación → crear evaluación de cliente

### Flujo 4 — Gerencia (Sprint 4)
1. Reportes → generar reporte de membresías
2. Pago Empleados → crear liquidación y marcar como pagado
3. Encuestas → registrar encuesta y ver promedios

---

## Sistema de tema visual (Alex - Sprint 2 / consolidado Sprint 5)
El archivo `frontend/resources/theme.py` centraliza:
- Paleta de colores COLORS (verde fitness oscuro)
- Hoja de estilos QSS global
- Función `apply_theme(app)` usada en `app.py`
- ObjectNames estándar: H1, H2, Muted, Brand, Card, Sidebar, NavItem, Primary, Danger

---

## Cómo ejecutar el sistema completo
```bash
cd sprint5/program_fitzone
pip install PySide6
python app.py
```
Credenciales de prueba:
- Admin: `romel@mail.com` / `123`
- Usuario: `user@mail.com` / `123`
- Seguridad: `seg@mail.com` / `123`
