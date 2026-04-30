# 💪 FitZone — Sistema de Gestión de Gimnasio (Sprint 5 — Versión Final)

## 📌 Descripción
FitZone es una aplicación de escritorio completa para la gestión integral de un gimnasio.
Desarrollada en Python siguiendo **POO + MVC**, con interfaz gráfica en **PySide6** y
persistencia en **JSON** (preparada para migración a MySQL).

Integra los módulos de los **Sprints 1 al 5**: acceso, membresías, pagos, horarios,
entrenadores, personal, asistencia, contabilidad, incidencias, evaluaciones,
notificaciones, nómina, reportes y encuestas de satisfacción.

---

## 🎯 Módulos del sistema

| Módulo | Sprint | Descripción |
|---|---|---|
| Autenticación / Registro | S1 | Login por rol, registro de cuentas |
| Membresías | S1 | Planes, selección, estado |
| Pagos de clientes | S1 | Registro y verificación |
| Seguridad / Bitácora | S1 | Logs de acceso |
| Horarios | S2 | CRUD + consulta |
| Entrenadores | S2 | CRUD + asignación |
| Personal (empleados) | S2 | Registro y gestión |
| Asistencia | S3 | Registro de entrada de clientes |
| Modificación de horarios | S3 | Reasignación por eventos externos |
| Contabilidad | S3 | Cobros, pagos, saldos |
| Empleados (detalle) | S3 | Estado laboral, salario neto |
| Incidencias | S3 | Registro y resolución |
| Evaluación de usuarios | S3 | Desempeño por entrenador |
| Notificaciones trabajador | S3 | Pagos y vencimientos |
| Reportes gerenciales | S4 | Membresías, actividad, contabilidad |
| Pago de empleados (nómina) | S4 | Liquidación y confirmación |
| Encuestas satisfacción | S4 | Calificación entrenadores/instalaciones |

---

## 🧱 Arquitectura

```
fitzone/
├── app.py                  ← Punto de entrada principal
├── src/
│   ├── models/             ← Entidades del dominio
│   ├── services/           ← Lógica de negocio (backend)
│   └── ui/                 ← Vistas admin/seguridad (PySide6)
├── frontend/
│   ├── controllers/        ← Intermediarios MVC del frontend
│   ├── services/           ← Contexto, estado, navegación
│   ├── resources/          ← Tema visual centralizado
│   └── views/              ← Todas las vistas del frontend
│       └── pages/          ← Páginas compuestas (Sprint5Page)
├── tests/                  ← Pruebas automatizadas (pytest)
└── data/                   ← Persistencia JSON
```

---

## 🛠 Tecnologías

- **Python 3.10+**
- **PySide6** — Interfaz gráfica
- **pytest** — Pruebas automatizadas
- **SonarQube** — Calidad de código
- **JSON** — Persistencia (preparado para MySQL)

---

## ▶️ Instalación y ejecución

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (Windows)
venv\Scripts\activate
# Activar (Mac/Linux)
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

### Credenciales de prueba
| Correo | Contraseña | Rol |
|---|---|---|
| romel@mail.com | 123 | admin |
| user@mail.com | 123 | user |
| seg@mail.com | 123 | seguridad |

---

## 🧪 Pruebas

```bash
pytest tests/ -v
```

## 📊 Análisis SonarQube

```bash
sonar-scanner
```

---

## 📁 Estructura de datos persistidos

Los archivos JSON en `data/` se crean automáticamente al iniciar el sistema.

---

*FitZone — Proyecto integrador Python POO + MVC | Sprint 5 - Versión Final*
