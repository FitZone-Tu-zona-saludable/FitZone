import json
import os
from datetime import datetime


class ReportService:
    """
    Generación de reportes administrativos consolidados (Sprint 4 - Andrés).
    Consolida datos de módulos ya implementados en sprints anteriores.
    """

    # ─── REPORTE MEMBRESÍAS ──────────────────────────────────────────
    @staticmethod
    def reporte_membresias(auth_service):
        """
        Reporte de membresías: estado, tipo, fechas de cada cliente.
        Devuelve lista de dicts listos para mostrar / exportar.
        """
        filas = []
        for u in auth_service.get_users():
            mem = u.membership
            if isinstance(mem, dict):
                filas.append({
                    "id_cliente":   u.id_cliente,
                    "nombre":       u.get_name(),
                    "correo":       u.get_email(),
                    "tipo":         mem.get("tipo", "—"),
                    "fecha_inicio": mem.get("fechaInicio", "—"),
                    "fecha_fin":    mem.get("fechaFin", "—"),
                    "estado":       mem.get("estado", "desconocido"),
                })
            else:
                filas.append({
                    "id_cliente":   u.id_cliente,
                    "nombre":       u.get_name(),
                    "correo":       u.get_email(),
                    "tipo":         str(mem) if mem else "sin membresía",
                    "fecha_inicio": "—",
                    "fecha_fin":    "—",
                    "estado":       "sin membresía",
                })
        return filas

    # ─── REPORTE CLIENTES ────────────────────────────────────────────
    @staticmethod
    def reporte_clientes(auth_service):
        """
        Reporte de datos de contacto y actividad de clientes.
        """
        filas = []
        for u in auth_service.get_users():
            filas.append({
                "id_cliente": u.id_cliente,
                "nombre":     u.get_name(),
                "correo":     u.get_email(),
                "rol":        u.get_role(),
                "num_pagos":  len(u.payments) if u.payments else 0,
                "tiene_membresia": bool(u.membership),
            })
        return filas

    # ─── REPORTE CONTABLE ────────────────────────────────────────────
    @staticmethod
    def reporte_contable(accounting_service):
        """
        Consolida información contable: totales por estado y listado completo.
        """
        registros = accounting_service.get_all()
        return {
            "total_recaudado": accounting_service.total_recaudado(),
            "total_pendiente": accounting_service.total_pendiente(),
            "total_vencido":   sum(r.monto for r in accounting_service.get_vencidos()),
            "num_registros":   len(registros),
            "detalle":         [r.to_dict() for r in registros],
        }

    # ─── REPORTE ACTIVIDAD GENERAL ───────────────────────────────────
    @staticmethod
    def reporte_actividad(attendance_service, evaluation_service, incident_service):
        """
        Consolida asistencias, evaluaciones e incidencias para la gerencia.
        """
        return {
            "total_asistencias":  len(attendance_service.get_all()),
            "total_evaluaciones": len(evaluation_service.get_all()),
            "total_incidencias":  len(incident_service.get_all()),
            "incidencias_pendientes": len(incident_service.get_pendientes()),
        }

    # ─── REPORTE NÓMINA ──────────────────────────────────────────────
    @staticmethod
    def reporte_nomina(payroll_service):
        """
        Reporte de nómina: totales y detalle de pagos.
        """
        return {
            "total_pagado":    payroll_service.total_pagado(),
            "total_pendiente": payroll_service.total_pendiente(),
            "num_pagos":       len(payroll_service.get_all()),
            "detalle":         [r.to_dict() for r in payroll_service.get_all()],
        }

    # ─── REPORTE ENCUESTAS ───────────────────────────────────────────
    @staticmethod
    def reporte_encuestas(survey_service):
        """
        Reporte de satisfacción: promedios y listado de sugerencias.
        """
        return {
            "total_encuestas":        len(survey_service.get_all()),
            "promedio_entrenador":    survey_service.promedio_entrenador(),
            "promedio_instalaciones": survey_service.promedio_instalaciones(),
            "promedio_general":       survey_service.promedio_general(),
            "sugerencias":            survey_service.get_sugerencias(),
        }

    # ─── EXPORTAR COMO JSON ──────────────────────────────────────────
    @staticmethod
    def exportar_json(datos, ruta_archivo):
        """
        Guarda un reporte como archivo JSON para uso posterior en la interfaz.
        """
        os.makedirs(os.path.dirname(ruta_archivo) if os.path.dirname(ruta_archivo) else ".", exist_ok=True)
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return ruta_archivo
