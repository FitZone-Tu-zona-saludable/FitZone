"""
Sprint 2 – Pruebas de las actividades de Andrés Valdés
Cubre: eliminación de cuenta, estados de membresía, horarios,
       entrenadores, trabajadores/empleados y notificaciones.
"""

import sys
import os
import json
import pytest

# Asegurar que el path apunte a la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.auth_service import AuthService
from src.services.schedule_service import ScheduleService
from src.services.trainer_service import TrainerService
from src.services.worker_service import WorkerService
from src.services.notification_service import NotificationService
from src.models.client import Client


# ─── FIXTURES ────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def archivos_temporales(tmp_path, monkeypatch):
    """Redirige todos los JSON a un directorio temporal para no tocar data/."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    yield


# ─── 1. ELIMINACIÓN DE CUENTA ────────────────────────────────────────────────

class TestEliminarCuenta:

    def test_admin_puede_eliminar_usuario(self):
        auth = AuthService()
        admin = auth.login("romel@mail.com", "123")
        auth.create_user("Victima", "victima@mail.com", "abc", "user")

        ok, msg = auth.delete_user("victima@mail.com", actor=admin)

        assert ok is True
        emails = [u.get_email() for u in auth.get_users()]
        assert "victima@mail.com" not in emails

    def test_usuario_sin_permiso_no_puede_eliminar(self):
        auth = AuthService()
        auth.create_user("Usuario", "usuario@mail.com", "abc", "user")
        actor_sin_permiso = auth.login("user@mail.com", "123")

        ok, msg = auth.delete_user("usuario@mail.com", actor=actor_sin_permiso)

        assert ok is False

    def test_eliminar_deja_log(self):
        auth = AuthService()
        admin = auth.login("romel@mail.com", "123")
        auth.create_user("Traza", "traza@mail.com", "abc", "user")
        auth.delete_user("traza@mail.com", actor=admin)

        logs_texto = " ".join(log["message"] for log in auth.logs)
        assert "traza@mail.com" in logs_texto

    def test_eliminar_usuario_inexistente(self):
        auth = AuthService()
        admin = auth.login("romel@mail.com", "123")
        ok, msg = auth.delete_user("noexiste@mail.com", actor=admin)
        assert ok is False


# ─── 2. ESTADO DE MEMBRESÍA ──────────────────────────────────────────────────

class TestEstadoMembresia:

    def test_membresia_activa(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = {
            "fechaInicio": "2020-01-01",
            "fechaFin": "2099-12-31",
            "estado": "desconocido"
        }
        auth.update_membership_status()
        assert u.membership["estado"] == "activa"

    def test_membresia_vencida(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = {
            "fechaInicio": "2000-01-01",
            "fechaFin": "2000-12-31",
            "estado": "desconocido"
        }
        auth.update_membership_status()
        assert u.membership["estado"] == "vencida"

    def test_membresia_pendiente(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = {
            "fechaInicio": "2099-01-01",
            "fechaFin": "2099-12-31",
            "estado": "desconocido"
        }
        auth.update_membership_status()
        assert u.membership["estado"] == "pendiente"

    def test_membresia_por_vencer(self):
        from datetime import datetime, timedelta
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        hoy = datetime.now()
        u.membership = {
            "fechaInicio": (hoy - timedelta(days=25)).strftime("%Y-%m-%d"),
            "fechaFin": (hoy + timedelta(days=3)).strftime("%Y-%m-%d"),
            "estado": "desconocido"
        }
        auth.update_membership_status()
        assert u.membership["estado"] == "por_vencer"


# ─── 3. HORARIOS ─────────────────────────────────────────────────────────────

class TestHorarios:

    def test_crear_horario(self):
        svc = ScheduleService()
        h = svc.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 15)
        assert h.id_horario == 1
        assert h.tipo == "yoga"
        assert h.cupos == 15

    def test_consultar_horarios(self):
        svc = ScheduleService()
        svc.create_schedule("2025-06-01", "08:00", "09:00", "cardio", 10)
        svc.create_schedule("2025-06-02", "10:00", "11:00", "fuerza", 8)
        assert len(svc.get_schedules()) == 2

    def test_modificar_horario(self):
        svc = ScheduleService()
        h = svc.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 15)
        svc.update_schedule(h.id_horario, tipo="pilates", cupos=12)
        actualizado = svc.get_by_id(h.id_horario)
        assert actualizado.tipo == "pilates"
        assert actualizado.cupos == 12

    def test_filtrar_por_fecha(self):
        svc = ScheduleService()
        svc.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 10)
        svc.create_schedule("2025-06-01", "10:00", "11:00", "cardio", 8)
        svc.create_schedule("2025-06-02", "08:00", "09:00", "fuerza", 5)
        resultado = svc.filter_by_fecha("2025-06-01")
        assert len(resultado) == 2

    def test_persistencia_horario(self):
        svc = ScheduleService()
        svc.create_schedule("2025-07-01", "07:00", "08:00", "spinning", 20)
        svc2 = ScheduleService()
        assert len(svc2.get_schedules()) == 1


# ─── 4. ENTRENADORES ─────────────────────────────────────────────────────────

class TestEntrenadores:

    def test_crear_entrenador(self):
        svc = TrainerService()
        t = svc.create_trainer("Carlos", "Entrenador", "3001234567",
                               "carlos@gym.com", especialidad="yoga")
        assert t.nombre == "Carlos"
        assert t.especialidad == "yoga"
        assert t.disponible is True

    def test_asignar_horario_disponible(self):
        svc = TrainerService()
        t = svc.create_trainer("Ana", "Entrenadora", "3009876543",
                               "ana@gym.com", especialidad="cardio")
        ok, msg = svc.asignar_horario(t.id_trabajador, id_horario=1)
        assert ok is True

    def test_entrenadores_disponibles(self):
        svc = TrainerService()
        svc.create_trainer("Pedro", "Entrenador", "300111", "pedro@gym.com")
        svc.create_trainer("María", "Entrenadora", "300222", "maria@gym.com")
        assert len(svc.get_disponibles()) == 2

    def test_seleccionar_por_plan(self):
        svc = TrainerService()
        svc.create_trainer("Yoga Coach", "Entrenador", "300x", "y@gym.com",
                           especialidad="yoga")
        svc.create_trainer("Cardio Coach", "Entrenador", "300z", "z@gym.com",
                           especialidad="cardio")
        resultado = svc.seleccionar_por_plan("yoga")
        assert len(resultado) == 1
        assert resultado[0].especialidad == "yoga"

    def test_persistencia_entrenador(self):
        svc = TrainerService()
        svc.create_trainer("Luis", "Entrenador", "111", "luis@gym.com")
        svc2 = TrainerService()
        assert len(svc2.get_trainers()) == 1


# ─── 5. TRABAJADORES Y EMPLEADOS ─────────────────────────────────────────────

class TestTrabajadoresEmpleados:

    def test_alta_trabajador(self):
        svc = WorkerService()
        w = svc.create_worker("Javier", "Recepción", "3001", "j@gym.com",
                              experiencia="2 años", modalidad="presencial",
                              revision_medica=True)
        assert w.nombre == "Javier"
        assert w.revision_medica is True

    def test_registro_empleado(self):
        svc = WorkerService()
        e = svc.register_employee("Sofía", "Contabilidad", "3002", "s@gym.com",
                                  experiencia="3 años", modalidad="remoto",
                                  revision_medica=True,
                                  fecha_ingreso="2025-01-15",
                                  tipo_contrato="indefinido")
        assert e.tipo_contrato == "indefinido"
        assert e.fecha_ingreso == "2025-01-15"

    def test_filtrar_solo_empleados(self):
        svc = WorkerService()
        svc.create_worker("Guardia", "Seguridad", "3003", "g@gym.com")
        svc.register_employee("Contador", "Finanzas", "3004", "c@gym.com",
                              fecha_ingreso="2025-01-01")
        empleados = svc.get_employees()
        assert len(empleados) == 1
        assert empleados[0].nombre == "Contador"

    def test_persistencia_workers(self):
        svc = WorkerService()
        svc.create_worker("Portero", "Portería", "3005", "p@gym.com")
        svc2 = WorkerService()
        assert len(svc2.get_workers()) == 1


# ─── 6. NOTIFICACIONES ───────────────────────────────────────────────────────

class TestNotificaciones:

    def test_notificacion_pago_confirmado(self):
        svc = NotificationService()
        msg = svc.notificar_pago("Juan", 50000, "tarjeta")
        assert "Juan" in msg
        assert "50000" in msg

    def test_notificacion_vencimiento_proximo(self):
        from datetime import datetime, timedelta
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        hoy = datetime.now()
        u.membership = {
            "fechaInicio": (hoy - timedelta(days=25)).strftime("%Y-%m-%d"),
            "fechaFin": (hoy + timedelta(days=3)).strftime("%Y-%m-%d"),
            "estado": "activa"
        }
        svc = NotificationService()
        mensajes = svc.verificar_vencimiento([u])
        assert len(mensajes) == 1
        assert "vence" in mensajes[0].lower()

    def test_notificacion_membresia_vencida(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = {
            "fechaInicio": "2000-01-01",
            "fechaFin": "2000-12-31",
            "estado": "vencida"
        }
        svc = NotificationService()
        mensajes = svc.verificar_vencimiento([u])
        assert len(mensajes) == 1
        assert "vencido" in mensajes[0].lower() or "venció" in mensajes[0].lower() or "vencida" in mensajes[0].lower()

    def test_sin_membresia_no_genera_notificacion(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = None
        svc = NotificationService()
        mensajes = svc.verificar_vencimiento([u])
        assert mensajes == []

    def test_persistencia_notificaciones(self):
        svc = NotificationService()
        svc.notificar_pago("Carlos", 30000, "efectivo")
        svc2 = NotificationService()
        assert len(svc2.get_notifications()) == 1
