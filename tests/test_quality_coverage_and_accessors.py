"""Pruebas de calidad y cobertura real para modelos y servicios FitZone."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.account_entry import AccountEntry
from src.models.attendance import Attendance
from src.models.employee_payment import EmployeePayment
from src.models.manager import Manager
from src.models.membership import Membership
from src.models.payment import Payment
from src.models.payroll_record import PayrollRecord
from src.models.performance import Performance
from src.models.report import Report
from src.models.satisfaction_survey import SatisfactionSurvey
from src.models.trainer import Trainer
from src.models.worker import Worker
from src.services.accounting_service import AccountingService
from src.services.attendance_service import AttendanceService
from src.services.auth_service import AuthService
from src.services.employee_payment_service import EmployeePaymentService
from src.services.membership_service import MembershipService
from src.services.payment_service import PaymentService
from src.services.performance_service import PerformanceService
from src.services.report_service import ReportService
from src.services.schedule_service import ScheduleService
from src.services.survey_service import SurveyService
from src.services.trainer_service import TrainerService
from src.services.worker_service import WorkerService


@pytest.fixture(autouse=True)
def isolated_json_data(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)
    yield


def assert_accessor(instance, field_name, value):
    setter = getattr(instance, f"set_{field_name}")
    getter = getattr(instance, f"get_{field_name}")
    setter(value)
    assert getter() == value
    assert getattr(instance, field_name) == value
    assert getattr(instance, f"_{field_name}") == value


def test_models_have_compatible_getters_setters_and_to_dict():
    entry = AccountEntry(1, "Mensualidad", "tipo_invalido", 50000, referencia="R1")
    assert entry.tipo == "ingreso"
    assert_accessor(entry, "estado", "pagado")
    assert entry.to_dict()["referencia"] == "R1"

    attendance = Attendance(1, 2, "Juan", fecha="2026-01-01", observaciones="OK")
    assert attendance.hora == ""
    assert attendance.clase_servicio == ""
    assert_accessor(attendance, "observaciones", "Ingreso normal")
    assert attendance.to_dict()["observaciones"] == "Ingreso normal"

    payment = Payment(1, 2, 70000, "tarjeta", "2026-01-01")
    assert_accessor(payment, "metodo", "efectivo")
    assert payment.to_dict()["metodo"] == "efectivo"

    membership = Membership(1, "Premium", "2026-01-01", "2026-02-01")
    membership.actualizar_estado("vencida")
    assert_accessor(membership, "estado", "activa")

    performance = Performance(1, 2, "Juan", 3, "Trainer", 8, "Mejoró")
    assert_accessor(performance, "puntaje", 9)
    assert performance.to_dict()["puntaje"] == 9

    report = Report("clientes", {"total": 1})
    assert_accessor(report, "contenido", {"total": 2})
    assert report.generar() == "Reporte generado"

    manager = Manager(1, "Laura", "300", "l@g.com")
    assert manager.cargo == "Gerente"
    assert manager.generar_reporte() == "Reporte generado"


def test_payroll_employee_payment_trainer_worker_model_edges():
    payroll = PayrollRecord(1, 1, "Ana", "indefinido", 10, 0, 0, "2026-04")
    assert payroll.valor_hora == 0.0
    assert payroll.neto == 0.0
    payroll.marcar_pagado()
    assert payroll.estado == PayrollRecord.ESTADO_PAGADO

    employee_payment = EmployeePayment(1, 2, "Carlos", 10, 20000, 50000)
    assert employee_payment.bruto == 200000
    assert employee_payment.neto == 150000
    assert_accessor(employee_payment, "estado", "pagado")
    assert employee_payment.to_dict()["neto"] == 150000

    trainer = Trainer(1, "T", "Entrenador", "300", "t@g.com", "yoga")
    assert trainer.asignar_horario(1) is True
    trainer.disponible = False
    assert trainer.asignar_horario(2) is False
    trainer.liberar()
    assert trainer.disponible is True

    worker = Worker(1, "W", "Recepción", "300", "w@g.com")
    assert worker.get_name() == "W"
    assert worker.get_cargo() == "Recepción"
    assert_accessor(worker, "telefono", "301")

    survey = SatisfactionSurvey(1, 1, "Cliente", 4, 5, "Bien")
    assert survey.calificacion_entrenador == 4
    assert survey.calificacion_instalaciones == 5
    assert survey.sugerencias == "Bien"
    assert survey.promedio == 4.5


def test_employee_payment_service_crud_and_persistence():
    service = EmployeePaymentService()
    payment = service.create_liquidation(1, "Carlos", 8, 10000, 5000, "prestación")

    assert payment.id_pago == 1
    assert service.get_pending() == [payment]
    assert service.get_by_worker(1) == [payment]
    assert service.mark_paid(payment.id_pago) is True
    assert service.mark_paid(999) is False
    assert service.get_pending() == []

    loaded = EmployeePaymentService()
    assert len(loaded.get_all()) == 1
    assert loaded.get_all()[0].estado == "pagado"


def test_performance_service_crud_filters_and_persistence():
    service = PerformanceService()
    evaluation = service.create(1, "Juan", 2, "Trainer", 9, "Buen avance")

    assert service.get_all() == [evaluation]
    assert service.get_by_client(1) == [evaluation]
    assert service.get_by_trainer(2) == [evaluation]

    loaded = PerformanceService()
    assert len(loaded.get_all()) == 1
    assert loaded.get_all()[0].observaciones == "Buen avance"


def test_accounting_frontend_api_and_negative_paths():
    service = AccountingService()
    entry = service.add_entry("Mensualidad", "ingreso", 80000, "P1")
    pending = service.add_entry("Saldo", "saldo_por_pagar", 30000)

    assert service.get_pending() == [entry, pending]
    assert service.get_by_tipo("ingreso") == [entry]
    assert service.mark_paid(entry.id_entrada) is True
    assert service.mark_paid(999) is False
    assert service.total_ingresos() == 80000
    assert service.total_pendiente() == 30000
    assert service.confirmar_pago(999) == (False, "Registro no encontrado")

    loaded = AccountingService()
    assert len(loaded.entries) == 2


def test_attendance_service_observaciones_delete_and_filters():
    service = AttendanceService()
    attendance = service.registrar_entrada(1, "Juan", "yoga", "Entró tarde")

    assert attendance.observaciones == "Entró tarde"
    assert service.get_by_id(attendance.id_asistencia) == attendance
    assert service.get_by_client(1) == [attendance]
    assert service.update(attendance.id_asistencia, servicio="spa") is True
    assert service.update(999, servicio="spa") is False
    assert service.get_by_fecha(attendance.fecha[:10]) == [attendance]

    loaded = AttendanceService()
    assert loaded.get_all()[0].observaciones == "Entró tarde"
    assert service.delete(attendance.id_asistencia) is True
    assert service.delete(999) is False


def test_auth_service_json_edge_cases_and_crud_branches():
    with open("data/users.json", "w", encoding="utf-8") as handler:
        handler.write("{json invalido")
    auth = AuthService(seed_defaults=False)
    assert auth.get_users() == []

    user = auth.create_user("Ana", "ANA@MAIL.COM", "123", "user")
    assert user.correo == "ana@mail.com"
    assert auth.find_by_id(999) is None
    assert auth.update_user("nadie@mail.com", "Nadie") is False

    assert auth.delete_user("nadie@mail.com") == (False, "Usuario no encontrado")
    ok, message = auth.delete_user("ana@mail.com")
    assert ok is True
    assert "eliminada" in message


def test_auth_service_removes_duplicate_loaded_users():
    duplicated = [
        {"id": 1, "name": "A", "email": "a@mail.com", "password": "1", "role": "user"},
        {"id": 2, "name": "A2", "email": "A@mail.com", "password": "2", "role": "user"},
    ]
    with open("data/users.json", "w", encoding="utf-8") as handler:
        json.dump(duplicated, handler)

    auth = AuthService(seed_defaults=False)
    assert len(auth.get_users()) == 1
    with open("data/users.json", "r", encoding="utf-8") as handler:
        saved = json.load(handler)
    assert len(saved) == 1


def test_membership_and_payment_error_paths_and_assignment():
    auth = AuthService(seed_defaults=False)
    user = auth.create_user("Cliente", "cliente@mail.com", "123", "user")
    memberships = MembershipService(auth)
    payments = PaymentService(auth, memberships)

    assert memberships.get_plan(999) is None
    assert memberships.get_user_memberships(user.id_cliente) == []
    assert memberships.select_membership(999, 1)["success"] is False
    assert memberships.select_membership(user.id_cliente, 999)["success"] is False
    assert memberships.assign_trainer(user.id_cliente, 1, "Trainer")["success"] is False

    assert payments.register_payment({"user_id": 999})["success"] is False
    assert payments.register_payment({"user_id": user.id_cliente})["success"] is False

    selected = memberships.select_membership(user.id_cliente, 1)
    assert selected["success"] is True
    assert memberships.assign_trainer(user.id_cliente, 7, "Trainer 7")["success"] is True
    assert memberships.get_user_memberships(user.id_cliente)[0]["trainer_id"] == 7

    mismatch = payments.register_payment({
        "user_id": user.id_cliente,
        "membership_id": 999,
        "amount": 50000,
    })
    assert mismatch["success"] is False

    invalid_amount = payments.register_payment({
        "user_id": user.id_cliente,
        "membership_id": 1,
        "amount": 0,
    })
    assert invalid_amount["success"] is False
    assert payments.verify_payment(999)["success"] is False


def test_payment_verify_already_verified_branch():
    auth = AuthService(seed_defaults=False)
    user = auth.create_user("Cliente", "cliente@mail.com", "123", "user")
    user.membership = {"id": 1, "name": "Básico", "duration_days": 30, "estado": "activa"}
    user.payments.append({"id": 10, "amount": 50000, "method": "Efectivo", "estado": "verificado"})
    payments = PaymentService(auth, MembershipService(auth))

    result = payments.verify_payment(10)
    assert result["success"] is False
    assert "verificado" in result["message"]


def test_report_service_instance_methods():
    empty_report = ReportService()
    assert empty_report.report_members() == {}
    assert empty_report.report_activity() == {}
    assert empty_report.report_financial_summary()["error"]

    auth = AuthService(seed_defaults=False)
    user = auth.create_user("Cliente", "cliente@mail.com", "123", "user")
    user.membership = {"name": "Básico", "estado": "activa"}
    user.payments.append({"value": 50000, "method": "Efectivo"})

    accounting = AccountingService()
    entry = accounting.add_entry("Pago", "ingreso", 50000)
    accounting.mark_paid(entry.id_entrada)
    accounting.registrar_cobro(user.id_cliente, user.nombre, "mensualidad", 30000)

    report = ReportService(auth, accounting)
    member_report = report.report_members()
    assert member_report["activas"] == 1
    assert member_report["total_usuarios"] == 1

    activity_report = report.report_activity()
    assert activity_report["total_pagos"] == 1

    financial_report = report.report_financial_summary()
    assert financial_report["total_ingresos"] == 50000
    assert financial_report["total_pendiente"] == 30000


def test_schedule_trainer_and_worker_extra_branches():
    schedules = ScheduleService()
    trainers = TrainerService()
    workers = WorkerService()

    schedule = schedules.create_schedule("2026-01-01", "08:00", "09:00", "yoga", 10)
    assert schedules.update_schedule(
        schedule.id_horario,
        fecha="2026-01-02",
        hora_inicio="10:00",
        hora_fin="11:00",
        tipo="cardio",
        cupos=12,
        id_entrenador=1,
    ) is True
    assert schedules.update_schedule(999, fecha="2026-01-03") is False
    assert schedules.filter_by_entrenador(1) == [schedule]

    updated, msg = schedules.modificar_por_evento_externo(
        schedule.id_horario,
        nueva_fecha="2026-01-03",
        nueva_hora_inicio="12:00",
        nueva_hora_fin="13:00",
    )
    assert updated.fecha == "2026-01-03"
    assert "modificado" in msg
    assert schedules.modificar_por_evento_externo(999)[0] is None
    assert schedules.reasignar_entrenador(999, 1, trainers)[0] is False
    assert schedules.reasignar_entrenador(schedule.id_horario, 999, trainers)[0] is False

    trainer = trainers.create_trainer("T", "Entrenador", "300", "t@g.com", "cardio")
    assert trainers.update_trainer(999, nombre="X") is False
    assert trainers.set_availability(trainer.id_trabajador, False) is True
    assert trainers.asignar_horario(999, schedule.id_horario)[0] is False
    assert trainers.asignar_horario(trainer.id_trabajador, schedule.id_horario)[0] is False
    assert trainers.delete_trainer(999) is False
    assert trainers.delete_trainer(trainer.id_trabajador) is True

    worker = workers.create_worker("W", "Recepción", "300", "w@g.com")
    assert workers.update_worker(worker.id_trabajador, telefono="301") is True
    assert workers.update_worker(999, telefono="301") is False
    assert workers.get_info_completa_empleado(worker.id_trabajador) is None
    assert workers.delete_worker(999) is False
    assert workers.delete_worker(worker.id_trabajador) is True


def test_survey_additional_frontend_metrics():
    surveys = SurveyService()
    surveys.submit(1, "A", 4, 5, "Bien", id_entrenador=2, nombre_entrenador="T")
    surveys.submit(2, "B", 2, 3, "", id_entrenador=2, nombre_entrenador="T")

    assert surveys.get_by_trainer(2)
    assert surveys.avg_trainer_score()[(2, "T")] == 3.0
    assert surveys.avg_facility_score() == 4.0


def test_json_services_tolerate_empty_and_invalid_files():
    files_and_factories = [
        ("data/accounting.json", AccountingService, lambda svc: svc.get_all()),
        ("data/attendance.json", AttendanceService, lambda svc: svc.get_all()),
        ("data/employee_payments.json", EmployeePaymentService, lambda svc: svc.get_all()),
        ("data/performance.json", PerformanceService, lambda svc: svc.get_all()),
        ("data/schedules.json", ScheduleService, lambda svc: svc.get_schedules()),
        ("data/surveys.json", SurveyService, lambda svc: svc.get_all()),
        ("data/trainers.json", TrainerService, lambda svc: svc.get_trainers()),
        ("data/workers.json", WorkerService, lambda svc: svc.get_workers()),
    ]

    for file_path, factory, reader in files_and_factories:
        with open(file_path, "w", encoding="utf-8") as handler:
            handler.write("")
        assert reader(factory()) == []

        with open(file_path, "w", encoding="utf-8") as handler:
            handler.write("{json invalido")
        assert reader(factory()) == []
