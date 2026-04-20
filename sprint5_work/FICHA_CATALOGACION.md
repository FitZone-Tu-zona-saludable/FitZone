# Ficha de Catalogación del Software — FitZone
**Sprint 5 — Entrega final**

| Campo | Valor |
|-------|-------|
| **Nombre del software** | FitZone — Tu zona saludable |
| **Versión** | 1.0.0 |
| **Fecha de entrega** | Sprint 5 |
| **Lenguaje** | Python 3.10+ |
| **Arquitectura** | MVC (Modelo-Vista-Controlador) + POO |
| **Interfaz gráfica** | PySide6 (Qt6) |
| **Persistencia** | JSON local (data/*.json) |
| **Análisis de calidad** | SonarQube |
| **Pruebas** | pytest + patrón AAA |
| **Repositorio** | GitHub |

## Módulos del sistema
| Módulo | Sprint | Responsable (vista) |
|--------|--------|-------------------|
| Login, registro, membresías, pagos | 1 | Alex |
| Horarios, entrenadores, personal, notificaciones | 2 | Alex |
| Asistencia, contabilidad, incidencias, evaluaciones | 3 | Alex |
| Reportes, nómina de empleados, encuestas | 4 | Alex |
| Dashboard unificado, manual, cierre visual | 5 | Alex |

## Dependencias
```
PySide6>=6.5.0
pytest
coverage
```

## Equipo de desarrollo
- **Andrés** — Backend, modelos y lógica de negocio
- **Romel** — Autenticación, seguridad, pruebas y calidad
- **Alex** — Interfaz visual (PySide6), controladores e integración
