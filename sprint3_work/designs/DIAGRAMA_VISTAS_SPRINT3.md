# Diagrama de Vistas — Sprint 3 (Alex)

```
Sprint3Page (sprint3_page.py)
├── Sidebar NavItem buttons
│   ├── 📋 Asistencia       → AttendanceView
│   ├── 🗓 Mod. Horarios    → ScheduleReassignView
│   │                             └── _EditScheduleDialog (QDialog)
│   ├── 💰 Contabilidad     → AccountingView
│   ├── 👔 Empleados        → EmployeeDetailView
│   │                             └── _EditEmployeeDialog (QDialog)
│   ├── ⚠️ Incidencias      → IncidentView
│   ├── ⭐ Evaluación       → PerformanceView
│   └── 🔔 Notificaciones   → WorkerNotificationsView
│
└── QStackedWidget (muestra la vista activa)
```

## Flujo de datos (MVC)
```
Vista (PySide6) ──► Controlador ──► Servicio (src/) ──► JSON (data/)
     ▲                                                        │
     └────────────────────────────────────────────────────────┘
                        (to_dict / load)
```

## Nuevos archivos JSON (data/)
- `attendance.json`  — Asistencias
- `performance.json` — Evaluaciones
- `incidents.json`   — Incidencias
- `accounting.json`  — Contabilidad
