"""
Sprint 3 – Pruebas de las actividades de Andrés Valdés
Cubre: asistencia, contabilidad, estado laboral de empleados,
       incidencias, notificaciones al trabajador, evaluaciones de usuarios
       y reasignación de horarios/entrenadores.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.attendance_service import AttendanceService
from src.services.accounting_service import AccountingService
from src.services.incident_service import IncidentService
from src.services.evaluation_service import EvaluationService
from src.services.notification_service import NotificationService
from src.services.worker_service import WorkerService
from src.services.trainer_service import TrainerService
from src.services.schedule_service import ScheduleService
from src.services.auth_service import AuthService
from src.models.account_record import AccountRecord
from src.models.incident import Incident
from src.models.employee import Employee


# ─── FIXTURE ─────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def archivos_temporales(tmp_path, monkeypatch):
    """Redirige todos los JSON a un directorio temporal."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    yield


# ─── 1. ASISTENCIA ───────────────────────────────────────────────────────────

class TestAsistencia:

    def test_registrar_entrada(self):
        svc = AttendanceService()
        a = svc.registrar_entrada(1, "Juan Pérez", "yoga", "puntual")
        assert a.nombre_cliente == "Juan Pérez"
        assert a.clase_servicio == "yoga"

    def test_multiples_registros(self):
        svc = AttendanceService()
        svc.registrar_entrada(1, "Juan", "yoga")
        svc.registrar_entrada(2, "María", "cardio")
        assert len(svc.get_all()) == 2

    def test_filtro_por_cliente(self):
        svc = AttendanceService()
        svc.registrar_entrada(1, "Juan", "yoga")
        svc.registrar_entrada(1, "Juan", "cardio")
        svc.registrar_entrada(2, "María", "pilates")
        assert len(svc.get_by_cliente(1)) == 2

    def test_registro_hoy_aparece_en_get_today(self):
        from datetime import datetime
        svc = AttendanceService()
        svc.registrar_entrada(5, "Carlos", "fuerza")
        hoy = datetime.now().strftime("%Y-%m-%d")
        resultado = svc.get_by_fecha(hoy)
        assert len(resultado) == 1

    def test_persistencia_asistencia(self):
        svc = AttendanceService()
        svc.registrar_entrada(1, "Juan", "yoga")
        svc2 = AttendanceService()
        assert len(svc2.get_all()) == 1

    def test_actualizar_asistencia(self):
        svc = AttendanceService()
        a = svc.registrar_entrada(1, "Juan", "yoga")
        svc.actualizar_asistencia(a.id_asistencia, observaciones="llegó tarde")
        actualizado = svc.get_by_id(a.id_asistencia)
        assert actualizado.observaciones == "llegó tarde"


# ─── 2. CONTABILIDAD ─────────────────────────────────────────────────────────

class TestContabilidad:

    def test_registrar_cobro(self):
        svc = AccountingService()
        r = svc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        assert r.monto == 80000.0
        assert r.estado == AccountRecord.ESTADO_PENDIENTE

    def test_confirmar_pago(self):
        svc = AccountingService()
        r = svc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        ok, msg = svc.confirmar_pago(r.id_registro)
        assert ok is True
        assert svc.get_by_id(r.id_registro).estado == AccountRecord.ESTADO_PAGADO

    def test_total_recaudado(self):
        svc = AccountingService()
        r1 = svc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        r2 = svc.registrar_cobro(2, "María", "inscripción", 20000)
        svc.confirmar_pago(r1.id_registro)
        assert svc.total_recaudado() == 80000.0

    def test_total_pendiente(self):
        svc = AccountingService()
        svc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        svc.registrar_cobro(2, "María", "clase", 30000)
        assert svc.total_pendiente() == 110000.0

    def test_verificar_vencimientos_marca_vencidos(self):
        svc = AccountingService()
        svc.registrar_cobro(1, "Juan", "mensualidad", 50000,
                             fecha_vencimiento="2000-01-01")
        vencidos = svc.verificar_vencimientos()
        assert len(vencidos) == 1
        assert vencidos[0].estado == AccountRecord.ESTADO_VENCIDO

    def test_filtros_por_estado(self):
        svc = AccountingService()
        r1 = svc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        svc.registrar_cobro(2, "María", "clase", 30000)
        svc.confirmar_pago(r1.id_registro)
        assert len(svc.get_pagados()) == 1
        assert len(svc.get_pendientes()) == 1

    def test_persistencia_contabilidad(self):
        svc = AccountingService()
        svc.registrar_cobro(1, "Test", "concepto", 10000)
        svc2 = AccountingService()
        assert len(svc2.get_all()) == 1


# ─── 3. EMPLEADOS – estado laboral, salario neto ─────────────────────────────

class TestEmpleados:

    def test_registrar_empleado_con_salario(self):
        svc = WorkerService()
        e = svc.register_employee("Sofía", "Contabilidad", "300", "s@gym.com",
                                   salario=2500000.0, descuento=10.0)
        assert e.salario == 2500000.0
        assert e.descuento == 10.0

    def test_salario_neto_calculado(self):
        svc = WorkerService()
        e = svc.register_employee("Pedro", "Recepción", "301", "p@gym.com",
                                   salario=1000000.0, descuento=20.0)
        assert e.salario_neto == 800000.0

    def test_estado_laboral_inicial_activo(self):
        svc = WorkerService()
        e = svc.register_employee("Ana", "Yoga", "302", "a@gym.com")
        assert e.estado_laboral == Employee.ESTADO_ACTIVO

    def test_actualizar_estado_laboral(self):
        svc = WorkerService()
        e = svc.register_employee("Luis", "Cardio", "303", "l@gym.com")
        ok, msg = svc.actualizar_estado_laboral(e.id_trabajador, Employee.ESTADO_INCAPACITADO)
        assert ok is True
        actualizado = svc.get_by_id(e.id_trabajador)
        assert actualizado.estado_laboral == Employee.ESTADO_INCAPACITADO

    def test_estado_invalido_rechazado(self):
        svc = WorkerService()
        e = svc.register_employee("Carlos", "Pesas", "304", "c@gym.com")
        ok, _ = svc.actualizar_estado_laboral(e.id_trabajador, "jubilado")
        assert ok is False

    def test_info_completa_empleado(self):
        svc = WorkerService()
        e = svc.register_employee("Marta", "Administración", "305", "m@gym.com",
                                   salario=3000000.0, descuento=5.0,
                                   tipo_contrato="indefinido",
                                   fecha_ingreso="2024-01-10")
        info = svc.get_info_completa_empleado(e.id_trabajador)
        assert info is not None
        assert info["salario_neto"] == 2850000.0
        assert info["tipo_contrato"] == "indefinido"

    def test_persistencia_estado_laboral(self):
        svc = WorkerService()
        e = svc.register_employee("Rosa", "Limpieza", "306", "r@gym.com")
        svc.actualizar_estado_laboral(e.id_trabajador, Employee.ESTADO_INACTIVO)
        svc2 = WorkerService()
        e2 = svc2.get_by_id(e.id_trabajador)
        assert e2.estado_laboral == Employee.ESTADO_INACTIVO


# ─── 4. INCIDENCIAS ───────────────────────────────────────────────────────────

class TestIncidencias:

    def test_registrar_incidencia(self):
        svc = IncidentService()
        inc = svc.registrar_incidencia(1, "Carlos", Incident.TIPO_INASISTENCIA,
                                        "Enfermedad")
        assert inc.causa == "Enfermedad"
        assert inc.resuelta is False

    def test_incidencia_tiene_fecha(self):
        from datetime import datetime
        svc = IncidentService()
        inc = svc.registrar_incidencia(1, "Ana", Incident.TIPO_PERMISO, "Médico")
        hoy = datetime.now().strftime("%Y-%m-%d")
        assert inc.fecha == hoy

    def test_resolver_incidencia(self):
        svc = IncidentService()
        inc = svc.registrar_incidencia(1, "Pedro", Incident.TIPO_INASISTENCIA, "Urgencia")
        ok, msg = svc.resolver_incidencia(inc.id_incidencia)
        assert ok is True
        assert svc.get_by_id(inc.id_incidencia).resuelta is True

    def test_filtro_pendientes(self):
        svc = IncidentService()
        inc1 = svc.registrar_incidencia(1, "A", Incident.TIPO_INASISTENCIA, "c1")
        inc2 = svc.registrar_incidencia(2, "B", Incident.TIPO_PERMISO, "c2")
        svc.resolver_incidencia(inc1.id_incidencia)
        pendientes = svc.get_pendientes()
        assert len(pendientes) == 1
        assert pendientes[0].nombre_trabajador == "B"

    def test_filtro_por_trabajador(self):
        svc = IncidentService()
        svc.registrar_incidencia(1, "Carlos", Incident.TIPO_INASISTENCIA, "c1")
        svc.registrar_incidencia(1, "Carlos", Incident.TIPO_PERMISO, "c2")
        svc.registrar_incidencia(2, "María", Incident.TIPO_OTRO, "c3")
        assert len(svc.get_by_trabajador(1)) == 2

    def test_persistencia_incidencias(self):
        svc = IncidentService()
        svc.registrar_incidencia(1, "Test", Incident.TIPO_INASISTENCIA, "prueba")
        svc2 = IncidentService()
        assert len(svc2.get_all()) == 1


# ─── 5. NOTIFICACIONES AL TRABAJADOR ─────────────────────────────────────────

class TestNotificacionesTrabajador:

    def test_notificar_pago_trabajador(self):
        svc = NotificationService()
        msg = svc.notificar_pago_trabajador("Pedro", "Abril 2025", 2500000)
        assert "Pedro" in msg
        assert "2500000" in msg

    def test_notificar_vencimiento_a_trabajador(self):
        svc = NotificationService()
        msg = svc.notificar_vencimiento_a_trabajador("Recepcionista", "Juan", 3)
        assert "Recepcionista" in msg
        assert "Juan" in msg

    def test_filtrar_notificaciones_trabajador(self):
        svc = NotificationService()
        svc.notificar_pago("Cliente", 50000, "efectivo")          # tipo cliente
        svc.notificar_pago_trabajador("Empleado", "Mayo", 1000000)  # tipo trabajador
        trabajador_notifs = svc.get_notifications_trabajador()
        assert len(trabajador_notifs) == 1

    def test_filtrar_notificaciones_cliente(self):
        svc = NotificationService()
        svc.notificar_pago("Cliente", 50000, "efectivo")
        svc.notificar_pago_trabajador("Empleado", "Mayo", 1000000)
        cliente_notifs = svc.get_notifications_cliente()
        assert len(cliente_notifs) == 1

    def test_verificar_vencimientos_notifica_trabajadores(self):
        from datetime import datetime, timedelta
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        hoy = datetime.now()
        u.membership = {
            "fechaInicio": (hoy - timedelta(days=25)).strftime("%Y-%m-%d"),
            "fechaFin": (hoy + timedelta(days=2)).strftime("%Y-%m-%d"),
            "estado": "activa"
        }
        ws = WorkerService()
        w = ws.create_worker("Recepción", "Recepcionista", "300", "r@gym.com")
        svc = NotificationService()
        mensajes = svc.verificar_vencimientos_para_trabajadores([u], [w])
        assert len(mensajes) == 1
        assert "Recepción" in mensajes[0]


# ─── 6. EVALUACIÓN DE USUARIOS ───────────────────────────────────────────────

class TestEvaluaciones:

    def test_evaluar_usuario(self):
        svc = EvaluationService()
        ev, msg = svc.evaluar_usuario(1, "Trainer", 2, "Juan",
                                       puntualidad=8, rendimiento=9, actitud=7)
        assert ev is not None
        assert ev.promedio == pytest.approx(8.0)

    def test_criterios_fuera_de_rango(self):
        svc = EvaluationService()
        ev, msg = svc.evaluar_usuario(1, "Trainer", 2, "Juan",
                                       puntualidad=11, rendimiento=9, actitud=7)
        assert ev is None

    def test_promedio_cliente(self):
        svc = EvaluationService()
        svc.evaluar_usuario(1, "T1", 2, "Juan", 10, 10, 10)
        svc.evaluar_usuario(1, "T1", 2, "Juan", 0, 0, 0)
        prom = svc.promedio_cliente(2)
        assert prom == 5.0

    def test_filtro_por_cliente(self):
        svc = EvaluationService()
        svc.evaluar_usuario(1, "T", 2, "Juan", 8, 8, 8)
        svc.evaluar_usuario(1, "T", 3, "María", 9, 9, 9)
        assert len(svc.get_by_cliente(2)) == 1

    def test_filtro_por_entrenador(self):
        svc = EvaluationService()
        svc.evaluar_usuario(1, "T1", 2, "Juan", 8, 8, 8)
        svc.evaluar_usuario(2, "T2", 3, "María", 9, 9, 9)
        assert len(svc.get_by_entrenador(1)) == 1

    def test_persistencia_evaluaciones(self):
        svc = EvaluationService()
        svc.evaluar_usuario(1, "T", 2, "Juan", 7, 7, 7)
        svc2 = EvaluationService()
        assert len(svc2.get_all()) == 1


# ─── 7. REASIGNACIÓN DE HORARIOS ─────────────────────────────────────────────

class TestReasignacion:

    def test_modificar_horario_por_evento_externo(self):
        svc = ScheduleService()
        h = svc.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 10)
        s, msg = svc.modificar_por_evento_externo(
            h.id_horario, nueva_fecha="2025-06-02", motivo="corte de luz"
        )
        assert s is not None
        assert s.fecha == "2025-06-02"
        assert "corte de luz" in msg

    def test_reasignar_entrenador_disponible(self):
        ss = ScheduleService()
        ts = TrainerService()
        h = ss.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 10)
        t = ts.create_trainer("Ana", "Entrenadora", "300", "a@gym.com",
                               especialidad="yoga")
        ok, msg = ss.reasignar_entrenador(h.id_horario, t.id_trabajador, ts)
        assert ok is True
        assert ss.get_by_id(h.id_horario).id_entrenador == t.id_trabajador

    def test_reasignar_entrenador_no_disponible_falla(self):
        ss = ScheduleService()
        ts = TrainerService()
        h = ss.create_schedule("2025-06-01", "08:00", "09:00", "yoga", 10)
        t = ts.create_trainer("Luis", "Entrenador", "301", "l@gym.com")
        t.disponible = False
        ts.save_trainers()
        ok, msg = ss.reasignar_entrenador(h.id_horario, t.id_trabajador, ts)
        assert ok is False

    def test_modificar_horario_inexistente(self):
        svc = ScheduleService()
        s, msg = svc.modificar_por_evento_externo(999, nueva_fecha="2025-07-01")
        assert s is None
