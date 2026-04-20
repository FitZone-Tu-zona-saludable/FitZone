"""
Sprint 4 – Pruebas de las actividades de Andrés Valdés
Cubre: liquidación y pago de empleados (nómina), encuestas de satisfacción
       y generación de reportes administrativos consolidados.
RF23, RF26, RF27.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.payroll_service import PayrollService
from src.services.survey_service import SurveyService
from src.services.report_service import ReportService
from src.services.auth_service import AuthService
from src.services.accounting_service import AccountingService
from src.services.attendance_service import AttendanceService
from src.services.evaluation_service import EvaluationService
from src.services.incident_service import IncidentService
from src.services.worker_service import WorkerService
from src.models.payroll_record import PayrollRecord
from src.models.satisfaction_survey import SatisfactionSurvey


# ─── FIXTURE ─────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def archivos_temporales(tmp_path, monkeypatch):
    """Redirige todos los JSON a un directorio temporal para no tocar data/."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    yield


# ═════════════════════════════════════════════════════════════════════════════
# 1. LIQUIDACIÓN Y PAGO DE EMPLEADOS (NÓMINA)
# ═════════════════════════════════════════════════════════════════════════════

class TestNomina:

    def test_liquidar_empleado_basico(self):
        svc = PayrollService()
        r, msg = svc.liquidar_empleado(
            id_empleado=1, nombre_empleado="Carlos",
            tipo_contrato="indefinido", horas_trabajadas=160,
            salario_base=2400000, descuento=10,
            periodo="2025-04"
        )
        assert r is not None
        assert r.periodo == "2025-04"
        assert r.estado == PayrollRecord.ESTADO_PENDIENTE

    def test_calculo_bruto_correcto(self):
        svc = PayrollService()
        # salario_base=2400000, horas=240 → valor_hora=10000, bruto=240*10000=2400000
        r, _ = svc.liquidar_empleado(1, "Ana", "indefinido", 240, 2400000, 0, "2025-04")
        assert r.bruto == pytest.approx(2400000.0, rel=1e-4)

    def test_calculo_neto_con_descuento(self):
        svc = PayrollService()
        # salario=2400000, horas=240, descuento=20% → neto=2400000*0.8=1920000
        r, _ = svc.liquidar_empleado(1, "Luis", "indefinido", 240, 2400000, 20, "2025-04")
        assert r.neto == pytest.approx(1920000.0, rel=1e-4)

    def test_horas_proporcionales(self):
        svc = PayrollService()
        # salario_base=2400000 /240 = 10000/hora. 120 horas → bruto=1200000
        r, _ = svc.liquidar_empleado(1, "Pedro", "indefinido", 120, 2400000, 0, "2025-04")
        assert r.bruto == pytest.approx(1200000.0, rel=1e-4)

    def test_horas_negativas_rechazadas(self):
        svc = PayrollService()
        r, msg = svc.liquidar_empleado(1, "X", "indefinido", -10, 1000000, 0, "2025-04")
        assert r is None
        assert "negativa" in msg.lower()

    def test_descuento_invalido_rechazado(self):
        svc = PayrollService()
        r, msg = svc.liquidar_empleado(1, "X", "indefinido", 160, 1000000, 110, "2025-04")
        assert r is None

    def test_confirmar_pago(self):
        svc = PayrollService()
        r, _ = svc.liquidar_empleado(1, "Marta", "indefinido", 200, 2000000, 5, "2025-04")
        ok, msg = svc.confirmar_pago(r.id_pago)
        assert ok is True
        assert svc.get_by_id(r.id_pago).estado == PayrollRecord.ESTADO_PAGADO

    def test_confirmar_pago_duplicado_falla(self):
        svc = PayrollService()
        r, _ = svc.liquidar_empleado(1, "Marta", "indefinido", 200, 2000000, 5, "2025-04")
        svc.confirmar_pago(r.id_pago)
        ok, msg = svc.confirmar_pago(r.id_pago)
        assert ok is False

    def test_historial_por_empleado(self):
        svc = PayrollService()
        svc.liquidar_empleado(1, "Juan", "indefinido", 160, 1500000, 0, "2025-03")
        svc.liquidar_empleado(1, "Juan", "indefinido", 200, 1500000, 0, "2025-04")
        svc.liquidar_empleado(2, "Ana",  "indefinido", 160, 2000000, 0, "2025-04")
        historial = svc.get_by_empleado(1)
        assert len(historial) == 2

    def test_filtro_por_periodo(self):
        svc = PayrollService()
        svc.liquidar_empleado(1, "Juan", "indefinido", 160, 1500000, 0, "2025-03")
        svc.liquidar_empleado(2, "Ana",  "indefinido", 160, 2000000, 0, "2025-04")
        assert len(svc.get_by_periodo("2025-04")) == 1

    def test_totales_pagado_y_pendiente(self):
        svc = PayrollService()
        r1, _ = svc.liquidar_empleado(1, "A", "indefinido", 240, 2400000, 0, "2025-04")
        r2, _ = svc.liquidar_empleado(2, "B", "indefinido", 240, 1200000, 0, "2025-04")
        svc.confirmar_pago(r1.id_pago)
        assert svc.total_pagado()    == pytest.approx(r1.neto, rel=1e-4)
        assert svc.total_pendiente() == pytest.approx(r2.neto, rel=1e-4)

    def test_liquidar_desde_empleado(self):
        ws = WorkerService()
        e = ws.register_employee("Rosa", "Cardio", "300", "r@g.com",
                                  salario=1800000, descuento=8,
                                  tipo_contrato="indefinido")
        svc = PayrollService()
        r, msg = svc.liquidar_desde_empleado(e, horas_trabajadas=240, periodo="2025-04")
        assert r is not None
        assert r.salario_base == 1800000
        assert r.descuento == 8

    def test_persistencia_nomina(self):
        svc = PayrollService()
        svc.liquidar_empleado(1, "Test", "indefinido", 160, 1000000, 0, "2025-04")
        svc2 = PayrollService()
        assert len(svc2.get_all()) == 1

    def test_empleado_sin_horas_neto_cero(self):
        svc = PayrollService()
        r, _ = svc.liquidar_empleado(1, "X", "indefinido", 0, 2400000, 0, "2025-04")
        assert r is not None
        assert r.neto == 0.0


# ═════════════════════════════════════════════════════════════════════════════
# 2. ENCUESTAS DE SATISFACCIÓN
# ═════════════════════════════════════════════════════════════════════════════

class TestEncuestas:

    def test_registrar_encuesta(self):
        svc = SurveyService()
        s, msg = svc.registrar_encuesta(1, "Juan", 4, 5, "Muy buenas instalaciones")
        assert s is not None
        assert s.calificacion_entrenador == 4
        assert s.calificacion_instalaciones == 5

    def test_promedio_encuesta(self):
        svc = SurveyService()
        s, _ = svc.registrar_encuesta(1, "Juan", 4, 2)
        assert s.promedio == pytest.approx(3.0)

    def test_calificacion_fuera_de_rango_rechazada(self):
        svc = SurveyService()
        s, msg = svc.registrar_encuesta(1, "Juan", 6, 3)
        assert s is None
        s2, msg2 = svc.registrar_encuesta(1, "Juan", 0, 3)
        assert s2 is None

    def test_calificacion_minima_valida(self):
        svc = SurveyService()
        s, _ = svc.registrar_encuesta(1, "Juan", 1, 1)
        assert s is not None

    def test_calificacion_maxima_valida(self):
        svc = SurveyService()
        s, _ = svc.registrar_encuesta(1, "Juan", 5, 5)
        assert s is not None

    def test_promedio_global_entrenadores(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "A", 4, 3)
        svc.registrar_encuesta(2, "B", 2, 3)
        assert svc.promedio_entrenador() == pytest.approx(3.0)

    def test_promedio_global_instalaciones(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "A", 3, 4)
        svc.registrar_encuesta(2, "B", 3, 2)
        assert svc.promedio_instalaciones() == pytest.approx(3.0)

    def test_promedio_general(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "A", 4, 4)  # promedio 4.0
        svc.registrar_encuesta(2, "B", 2, 2)  # promedio 2.0
        assert svc.promedio_general() == pytest.approx(3.0)

    def test_sugerencias_almacenadas(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "A", 3, 3, "Más clases de yoga")
        svc.registrar_encuesta(2, "B", 4, 4, "")        # sin sugerencia
        sugerencias = svc.get_sugerencias()
        assert len(sugerencias) == 1
        assert "yoga" in sugerencias[0].lower()

    def test_filtro_por_cliente(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "Juan", 4, 5)
        svc.registrar_encuesta(1, "Juan", 3, 4)
        svc.registrar_encuesta(2, "Ana",  5, 5)
        assert len(svc.get_by_cliente(1)) == 2

    def test_promedio_sin_encuestas_es_none(self):
        svc = SurveyService()
        assert svc.promedio_general() is None
        assert svc.promedio_entrenador() is None
        assert svc.promedio_instalaciones() is None

    def test_persistencia_encuestas(self):
        svc = SurveyService()
        svc.registrar_encuesta(1, "Test", 4, 4, "buena")
        svc2 = SurveyService()
        assert len(svc2.get_all()) == 1


# ═════════════════════════════════════════════════════════════════════════════
# 3. REPORTES ADMINISTRATIVOS
# ═════════════════════════════════════════════════════════════════════════════

class TestReportes:

    def test_reporte_clientes_estructura(self):
        auth = AuthService()
        filas = ReportService.reporte_clientes(auth)
        assert isinstance(filas, list)
        assert len(filas) > 0
        for fila in filas:
            assert "id_cliente" in fila
            assert "nombre" in fila
            assert "correo" in fila
            assert "rol" in fila

    def test_reporte_membresias_sin_membresias(self):
        auth = AuthService()
        filas = ReportService.reporte_membresias(auth)
        assert isinstance(filas, list)
        for fila in filas:
            assert "nombre" in fila
            assert "estado" in fila

    def test_reporte_membresias_con_membresia(self):
        auth = AuthService()
        u = auth.login("user@mail.com", "123")
        u.membership = {
            "tipo": "PREMIUM", "fechaInicio": "2025-01-01",
            "fechaFin": "2025-12-31", "estado": "activa"
        }
        auth.save_users()
        filas = ReportService.reporte_membresias(auth)
        prems = [f for f in filas if f["tipo"] == "PREMIUM"]
        assert len(prems) == 1

    def test_reporte_contable_estructura(self):
        acc = AccountingService()
        acc.registrar_cobro(1, "Juan", "mensualidad", 80000)
        r2 = acc.registrar_cobro(2, "Ana", "inscripción", 20000)
        acc.confirmar_pago(r2.id_registro)
        rep = ReportService.reporte_contable(acc)
        assert "total_recaudado" in rep
        assert "total_pendiente" in rep
        assert "detalle" in rep
        assert rep["total_recaudado"] == pytest.approx(20000.0)
        assert rep["total_pendiente"] == pytest.approx(80000.0)

    def test_reporte_actividad_estructura(self):
        att  = AttendanceService()
        ev   = EvaluationService()
        inc  = IncidentService()
        att.registrar_entrada(1, "Juan", "yoga")
        ev.evaluar_usuario(1, "T", 2, "Juan", 8, 8, 8)
        from src.models.incident import Incident
        inc.registrar_incidencia(1, "Carlos", Incident.TIPO_INASISTENCIA, "Fiebre")
        rep = ReportService.reporte_actividad(att, ev, inc)
        assert rep["total_asistencias"]  == 1
        assert rep["total_evaluaciones"] == 1
        assert rep["total_incidencias"]  == 1
        assert rep["incidencias_pendientes"] == 1

    def test_reporte_nomina_estructura(self):
        ps = PayrollService()
        r, _ = ps.liquidar_empleado(1, "Carlos", "indefinido", 160, 2000000, 0, "2025-04")
        ps.confirmar_pago(r.id_pago)
        rep = ReportService.reporte_nomina(ps)
        assert "total_pagado" in rep
        assert "total_pendiente" in rep
        assert "detalle" in rep
        assert rep["total_pagado"] == pytest.approx(r.neto, rel=1e-4)

    def test_reporte_encuestas_estructura(self):
        sv = SurveyService()
        sv.registrar_encuesta(1, "A", 4, 5, "excelente")
        sv.registrar_encuesta(2, "B", 3, 4)
        rep = ReportService.reporte_encuestas(sv)
        assert "total_encuestas"        in rep
        assert "promedio_entrenador"    in rep
        assert "promedio_instalaciones" in rep
        assert "promedio_general"       in rep
        assert "sugerencias"            in rep
        assert rep["total_encuestas"]   == 2

    def test_exportar_reporte_json(self, tmp_path):
        sv  = SurveyService()
        sv.registrar_encuesta(1, "A", 5, 5)
        datos = ReportService.reporte_encuestas(sv)
        ruta = str(tmp_path / "reporte_test.json")
        resultado = ReportService.exportar_json(datos, ruta)
        assert os.path.exists(resultado)
        import json
        with open(resultado, "r", encoding="utf-8") as f:
            cargado = json.load(f)
        assert cargado["total_encuestas"] == 1

    def test_reporte_usa_datos_reales_de_modulos(self):
        """Garantiza que los datos provienen de módulos ya implementados."""
        auth = AuthService()
        acc  = AccountingService()
        att  = AttendanceService()
        ev   = EvaluationService()
        inc  = IncidentService()
        ps   = PayrollService()
        sv   = SurveyService()

        # poblar datos
        acc.registrar_cobro(1, "Test", "mensualidad", 50000)
        att.registrar_entrada(1, "Test", "yoga")
        sv.registrar_encuesta(1, "Test", 4, 4)
        ps.liquidar_empleado(1, "Emp", "indefinido", 100, 1000000, 0, "2025-04")

        rep_cont  = ReportService.reporte_contable(acc)
        rep_act   = ReportService.reporte_actividad(att, ev, inc)
        rep_enc   = ReportService.reporte_encuestas(sv)
        rep_nom   = ReportService.reporte_nomina(ps)

        assert rep_cont["num_registros"]    == 1
        assert rep_act["total_asistencias"] == 1
        assert rep_enc["total_encuestas"]   == 1
        assert rep_nom["num_pagos"]         == 1
