# Diagrama del Sistema Completo — Sprint 5 (Alex)

```
app.py
  └── LoginView
        └── (login exitoso) → MainPage / Sprint5Page
              └── Sidebar (todos los módulos)
                    ├── 🏠 Dashboard        → MainDashboardView
                    ├── 💳 Membresías       → MembershipListView
                    ├── ➕ Selec. Plan      → MembershipSelectView
                    ├── 💸 Reg. Pago        → PaymentRegisterView
                    ├── ✅ Verif. Pago      → PaymentVerificationView
                    ├── 🔒 Seguridad        → SecurityView
                    ├── 🔔 Alertas          → AlertsPage
                    ├── 📅 Horarios         → SchedulePage
                    ├── 🏋️ Entrenadores     → TrainerPage
                    ├── 👥 Personal         → EmployeePage
                    ├── 📋 Asistencia       → AttendanceView        [S3]
                    ├── 🗓 Mod. Horarios    → ScheduleReassignView  [S3]
                    ├── 💰 Contabilidad     → AccountingView        [S3]
                    ├── 👔 Empleados (det.) → EmployeeDetailView    [S3]
                    ├── ⚠️ Incidencias      → IncidentView          [S3]
                    ├── ⭐ Evaluaciones     → PerformanceView       [S3]
                    ├── 🔔 Notif. Trab.    → WorkerNotificationsView[S3]
                    ├── 📊 Reportes        → ReportsView            [S4]
                    ├── 💼 Pago Empleados  → EmployeePaymentView    [S4]
                    └── 📝 Encuestas       → SurveyView             [S4]
```

## Tema visual centralizado (theme.py)
```
COLORS = { bg, surface, primary (#21C07A), danger, warning, ... }
apply_theme(app)  →  QSS global aplicado a toda la app
ObjectNames: H1, H2, Muted, Brand, Card, Sidebar, NavItem, Primary, Danger
```
