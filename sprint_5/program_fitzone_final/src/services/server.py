# server.py — Servidor FastAPI de FitZone
# Expone los servicios del backend como API REST.
# El frontend (PySide6) o cualquier cliente HTTP puede consumirlo.
#
# Uso en desarrollo:
#   uvicorn server:app --reload --port 8000
#
# Uso empaquetado (.exe con PyInstaller):
#   El hilo del servidor arranca automáticamente desde app.py
#   llamando a start_server_thread().  No es necesario ejecutar
#   este archivo directamente.

import threading
import uvicorn

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# ── Servicios del backend ────────────────────────────────────────────────────
from src.services.auth_service import AuthService
from src.services.membership_service import MembershipService
from src.services.payment_service import PaymentService
from src.services.schedule_service import ScheduleService
from src.services.trainer_service import TrainerService
from src.services.worker_service import WorkerService
from src.services.attendance_service import AttendanceService
from src.services.incident_service import IncidentService
from src.services.accounting_service import AccountingService
from src.services.report_service import ReportService
from src.services.survey_service import SurveyService
from src.services.notification_service import NotificationService
from src.services.evaluation_service import EvaluationService
from src.services.performance_service import PerformanceService
from src.services.security_service import SecurityService
from src.services.employee_payment_service import EmployeePaymentService

# ── Instancias compartidas ────────────────────────────────────────────────────
_auth         = AuthService()
_memberships  = MembershipService(_auth)
_payments     = PaymentService(_auth, _memberships)
_schedules    = ScheduleService()
_trainers     = TrainerService()
_workers      = WorkerService()
_attendance   = AttendanceService()
_incidents    = IncidentService()
_accounting   = AccountingService(_auth)
_reports      = ReportService(_auth)
_surveys      = SurveyService()
_notifications= NotificationService()
_evaluations  = EvaluationService()
_performance  = PerformanceService()
_security     = SecurityService()
_emp_payments = EmployeePaymentService()

# ── Aplicación FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title="FitZone API",
    description="API REST interna para el sistema de gestión FitZone.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ════════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ════════════════════════════════════════════════════════════════════════════════

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"

class MembershipSelectRequest(BaseModel):
    user_id: int
    membership_id: int

class PaymentRequest(BaseModel):
    user_id: int
    membership_id: int
    amount: float
    method: str
    reference: str = ""

class ScheduleCreate(BaseModel):
    fecha: str
    hora_inicio: str
    hora_fin: str
    tipo: str
    cupos: int
    id_entrenador: Optional[int] = None

class ScheduleUpdate(ScheduleCreate):
    id_horario: int

class TrainerAvailability(BaseModel):
    trainer_id: int
    available: bool

class WorkerCreate(BaseModel):
    nombre: str
    cargo: str
    telefono: str = ""
    correo: str = ""
    experiencia: str = ""
    modalidad: str = "presencial"
    documento: str = ""
    role: str = "trabajador"

class AttendanceRegister(BaseModel):
    user_id: int
    schedule_id: int

class IncidentCreate(BaseModel):
    worker_id: int
    description: str
    tipo: str = "general"

class SurveyCreate(BaseModel):
    user_id: int
    trainer_id: int
    score: int
    comment: str = ""


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — AUTENTICACIÓN
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["estado"])
def root():
    """Verifica que el servidor esté activo."""
    return {"status": "ok", "app": "FitZone API"}


@app.post("/auth/login", tags=["autenticación"])
def login(body: LoginRequest):
    """Autentica un usuario y devuelve sus datos básicos."""
    user = _auth.login(body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )
    return {
        "user_id":  user.id_cliente,
        "name":     user.nombre,
        "email":    user.correo,
        "role":     user.get_role(),
        "membership": user.membership,
    }


@app.post("/auth/register", tags=["autenticación"])
def register(body: RegisterRequest):
    """Crea una cuenta nueva (rol 'user' por defecto)."""
    try:
        user = _auth.create_user(body.name, body.email, body.password, body.role)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {
        "user_id": user.id_cliente,
        "name":    user.nombre,
        "email":   user.correo,
        "role":    user.get_role(),
    }


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — MEMBRESÍAS
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/memberships", tags=["membresías"])
def list_memberships():
    """Lista todos los planes de membresía disponibles."""
    return _memberships.list_memberships()


@app.get("/memberships/user/{user_id}", tags=["membresías"])
def user_memberships(user_id: int):
    """Devuelve la(s) membresía(s) activa(s) de un usuario."""
    return _memberships.list_user_memberships(user_id)


@app.post("/memberships/select", tags=["membresías"])
def select_membership(body: MembershipSelectRequest):
    """Asocia un plan al usuario."""
    result = _memberships.select_membership(body.user_id, body.membership_id)
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("message"))
    return result


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — PAGOS
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/payments", tags=["pagos"])
def list_payments():
    """Lista todos los pagos registrados."""
    return _payments.list_payments()


@app.post("/payments", tags=["pagos"])
def register_payment(body: PaymentRequest):
    """Registra un pago de membresía."""
    result = _payments.register_payment(
        body.user_id,
        body.membership_id,
        body.amount,
        body.method,
        body.reference,
    )
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("message"))
    return result


@app.patch("/payments/{payment_id}/verify", tags=["pagos"])
def verify_payment(payment_id: int):
    """Verifica (aprueba) un pago pendiente."""
    result = _payments.verify_payment(payment_id)
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.get("message"))
    return result


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — HORARIOS
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/schedules", tags=["horarios"])
def list_schedules(fecha: Optional[str] = None, trainer_id: Optional[int] = None):
    """Lista horarios, con filtros opcionales por fecha y entrenador."""
    schedules = _schedules.get_schedules()
    result = []
    for s in schedules:
        if fecha and s.fecha != fecha:
            continue
        if trainer_id and s.id_entrenador != trainer_id:
            continue
        result.append(s.to_dict())
    return result


@app.post("/schedules", tags=["horarios"])
def create_schedule(body: ScheduleCreate):
    """Crea un nuevo horario."""
    _schedules.create_schedule(
        body.fecha, body.hora_inicio, body.hora_fin,
        body.tipo, body.cupos, body.id_entrenador,
    )
    return {"success": True, "message": "Horario creado correctamente."}


@app.put("/schedules/{schedule_id}", tags=["horarios"])
def update_schedule(schedule_id: int, body: ScheduleCreate):
    """Actualiza un horario existente."""
    updated = _schedules.update_schedule(
        schedule_id,
        fecha=body.fecha,
        hora_inicio=body.hora_inicio,
        hora_fin=body.hora_fin,
        tipo=body.tipo,
        cupos=body.cupos,
        id_entrenador=body.id_entrenador,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado.")
    return {"success": True, "message": "Horario actualizado correctamente."}


@app.delete("/schedules/{schedule_id}", tags=["horarios"])
def delete_schedule(schedule_id: int):
    """Elimina un horario."""
    deleted = _schedules.delete_schedule(schedule_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado.")
    return {"success": True, "message": "Horario eliminado correctamente."}


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — ENTRENADORES
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/trainers", tags=["entrenadores"])
def list_trainers():
    """Lista todos los entrenadores."""
    return [t.__dict__ for t in _trainers.get_trainers()]


@app.patch("/trainers/availability", tags=["entrenadores"])
def set_trainer_availability(body: TrainerAvailability):
    """Actualiza la disponibilidad de un entrenador."""
    updated = _trainers.set_availability(body.trainer_id, body.available)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado.")
    return {"success": True, "message": "Disponibilidad actualizada."}


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — PERSONAL / TRABAJADORES
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/workers", tags=["personal"])
def list_workers():
    """Lista todo el personal registrado."""
    return [w.__dict__ for w in _workers.get_workers()]


@app.post("/workers", tags=["personal"])
def create_worker(body: WorkerCreate):
    """Registra un nuevo trabajador o empleado."""
    if body.role == "empleado":
        _workers.register_employee(
            body.nombre, body.cargo, body.telefono, body.correo,
            experiencia=body.experiencia, modalidad=body.modalidad,
            documento=body.documento,
        )
    else:
        _workers.create_worker(
            body.nombre, body.cargo, body.telefono, body.correo,
            experiencia=body.experiencia, modalidad=body.modalidad,
            documento=body.documento,
        )
    return {"success": True, "message": "Personal registrado correctamente."}


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — ASISTENCIA
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/attendance", tags=["asistencia"])
def list_attendance():
    """Lista todos los registros de asistencia."""
    return _attendance.get_all_attendance()


@app.post("/attendance", tags=["asistencia"])
def register_attendance(body: AttendanceRegister):
    """Registra asistencia de un usuario a un horario."""
    result = _attendance.register_attendance(body.user_id, body.schedule_id)
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("message"))
    return result


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — INCIDENCIAS
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/incidents", tags=["incidencias"])
def list_incidents():
    """Lista todas las incidencias reportadas."""
    return _incidents.get_incidents()


@app.post("/incidents", tags=["incidencias"])
def create_incident(body: IncidentCreate):
    """Crea una nueva incidencia."""
    result = _incidents.create_incident(body.worker_id, body.description, body.tipo)
    return {"success": True, "data": result}


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — CONTABILIDAD
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/accounting/summary", tags=["contabilidad"])
def accounting_summary():
    """Devuelve el resumen contable (ingresos, saldos, indicadores)."""
    return _accounting.get_summary()


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — ENCUESTAS
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/surveys", tags=["encuestas"])
def list_surveys():
    """Lista todas las encuestas de satisfacción."""
    return _surveys.get_surveys()


@app.post("/surveys", tags=["encuestas"])
def create_survey(body: SurveyCreate):
    """Registra una nueva encuesta de satisfacción."""
    result = _surveys.create_survey(
        body.user_id, body.trainer_id, body.score, body.comment
    )
    return {"success": True, "data": result}


# ════════════════════════════════════════════════════════════════════════════════
# RUTAS — REPORTES
# ════════════════════════════════════════════════════════════════════════════════

@app.get("/reports/memberships", tags=["reportes"])
def report_memberships():
    """Reporte de membresías activas, vencidas y pendientes."""
    return _reports.membership_report()


@app.get("/reports/revenue", tags=["reportes"])
def report_revenue():
    """Reporte de ingresos por membresías."""
    return _reports.revenue_report()


@app.get("/reports/activity", tags=["reportes"])
def report_activity():
    """Reporte de actividad general del gimnasio."""
    return _reports.activity_report()


# ════════════════════════════════════════════════════════════════════════════════
# LANZADOR EN HILO (para integración con PyInstaller / app.py)
# ════════════════════════════════════════════════════════════════════════════════

def start_server_thread(host: str = "127.0.0.1", port: int = 8000) -> threading.Thread:
    """
    Arranca uvicorn en un hilo daemon.

    Llamar desde app.py antes de iniciar el QApplication:

        from server import start_server_thread
        start_server_thread()

    El hilo se detiene automáticamente al cerrar la aplicación.
    """
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="warning",   # silencioso en producción
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True, name="fitzone-api")
    thread.start()
    return thread
