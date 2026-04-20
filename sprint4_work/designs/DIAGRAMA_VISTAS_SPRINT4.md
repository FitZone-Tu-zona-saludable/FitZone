# Diagrama de Vistas — Sprint 4 (Alex)

```
Sprint4Page (sprint4_page.py)
├── Sidebar NavItem buttons
│   ├── 📊 Reportes Gerenciales  → ReportsView
│   │                                  ├── Tab: Membresías (tbl_members)
│   │                                  ├── Tab: Actividad de Pagos (tbl_activity)
│   │                                  └── Tab: Resumen Financiero (txt_financial)
│   ├── 💼 Pago de Empleados     → EmployeePaymentView
│   └── 📝 Encuesta Satisfacción → SurveyView
│                                       ├── Tab: Registrar Encuesta
│                                       └── Tab: Resultados y Promedios
│
└── QStackedWidget
```

## Servicios nuevos Sprint 4
- `ReportService` — consolida datos de AuthService + AccountingService
- `EmployeePaymentService` — liquidaciones (bruto = horas × valor_hora)
- `SurveyService` — encuestas + cálculo de promedios por entrenador
