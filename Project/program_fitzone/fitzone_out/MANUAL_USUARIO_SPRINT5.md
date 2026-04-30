# Manual de Usuario — FitZone
**Versión:** 1.0 | **Sprint:** 5 | **Autor:** Alex

---

## ¿Qué es FitZone?
FitZone es un sistema de gestión para gimnasios que permite administrar usuarios, membresías, pagos, horarios, entrenadores, personal y reportes desde un panel unificado.

---

## Requisitos de instalación
- Python 3.10 o superior
- PySide6: `pip install PySide6`
- No requiere internet ni base de datos externa (usa archivos JSON locales)

---

## Inicio del sistema
```bash
python app.py
```

---

## Pantalla de Login
Ingresa tu correo y contraseña. El sistema redirige según tu rol:
- **Admin:** acceso completo a todos los módulos
- **Usuario:** acceso a membresías y pagos
- **Seguridad:** acceso a bitácora de accesos

---

## Módulos disponibles

### 🏠 Dashboard
Vista de bienvenida con accesos rápidos a todos los módulos del sistema.

### 💳 Membresías
- **Membresías:** lista los planes disponibles (Básico, Estándar, Premium, Trimestral, Anual)
- **Seleccionar plan:** elige el plan de membresía para el usuario activo
- **Registrar pago:** registra un pago indicando monto y método
- **Verificar pago:** consulta y confirma pagos pendientes

### 🔒 Seguridad
- **Seguridad:** muestra la bitácora de accesos exitosos y fallidos
- **Alertas:** notificaciones de pago confirmado y vencimiento de membresía

### 📅 Operación
- **Horarios:** consulta y administra clases y sesiones disponibles
- **Entrenadores:** gestión de entrenadores y su disponibilidad
- **Personal:** registro de trabajadores y empleados

### 📋 Administración interna (Sprint 3)
- **Asistencia:** registra la entrada de clientes a clases/servicios
- **Mod. Horarios:** modifica horarios existentes y reasigna entrenadores
- **Contabilidad:** registra ingresos, cobros pendientes y saldos
- **Empleados (det.):** consulta y actualiza datos laborales del empleado
- **Incidencias:** reporta inasistencias y permisos del personal con causa
- **Evaluaciones:** entrenadores evalúan el desempeño de los clientes (puntaje 1-10)
- **Notif. Trabajador:** centro de notificaciones de pagos y vencimientos para trabajadores

### 📊 Gerencia (Sprint 4)
- **Reportes:** genera reportes de membresías, actividad de pagos y resumen financiero
- **Pago Empleados:** liquida salarios con horas, valor/hora y descuentos
- **Encuestas:** clientes evalúan entrenadores e instalaciones (1-5); visualiza promedios

---

## Datos de prueba
| Rol | Correo | Contraseña |
|-----|--------|-----------|
| Admin | romel@mail.com | 123 |
| Usuario | user@mail.com | 123 |
| Seguridad | seg@mail.com | 123 |

---

## Solución de problemas
- **Error al iniciar:** verifica que PySide6 esté instalado con `pip install PySide6`
- **Datos no aparecen:** revisa que la carpeta `data/` esté en el mismo directorio que `app.py`
- **Pantalla en blanco:** ejecuta desde la carpeta raíz del proyecto
