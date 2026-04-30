from datetime import datetime


class ReportService:
    """Reportes administrativos (Sprint 4 - Andrés).
    Soporta: instancia con auth/accounting (frontend) y métodos estáticos (tests).
    """

    def __init__(self, auth_service=None, accounting_service=None):
        self.auth    = auth_service
        self.account = accounting_service

    # ── API FRONTEND (instance methods) ──────────────────────────────
    def report_members(self):
        if not self.auth:
            return {}
        users     = self.auth.get_users()
        activas   = [u for u in users if u.membership and
                     isinstance(u.membership, dict) and
                     u.membership.get("estado") == "activa"]
        vencidas  = [u for u in users if u.membership and
                     isinstance(u.membership, dict) and
                     u.membership.get("estado") == "vencida"]
        por_vencer= [u for u in users if u.membership and
                     isinstance(u.membership, dict) and
                     u.membership.get("estado") == "por_vencer"]
        sin_mem   = [u for u in users if not u.membership]
        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_usuarios":   len(users),
            "activas":          len(activas),
            "por_vencer":       len(por_vencer),
            "vencidas":         len(vencidas),
            "sin_membresia":    len(sin_mem),
            "detalle": [
                {
                    "nombre": u.nombre, "correo": u.correo, "rol": u.role,
                    "plan":   (u.membership.get("name", "N/A")
                               if isinstance(u.membership, dict) else str(u.membership or "Sin plan")),
                    "estado": (u.membership.get("estado", "N/A")
                               if isinstance(u.membership, dict) else "N/A"),
                }
                for u in users
            ]
        }

    def report_activity(self):
        if not self.auth:
            return {}
        rows = []
        for u in self.auth.get_users():
            for p in u.payments:
                rows.append({
                    "usuario": u.nombre, "correo": u.correo,
                    "valor": p.get("value", 0), "metodo": p.get("method", "N/A"),
                })
        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_pagos": len(rows), "detalle": rows
        }

    def report_financial_summary(self):
        if not self.account:
            return {"error": "Servicio contable no disponible"}
        ingresos = self.account.total_ingresos()
        pendientes = self.account.total_pendiente()
        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_ingresos":   ingresos,
            "total_pendiente":  pendientes,
            "total_entradas":   len(self.account.get_all()),
        }

    def reporte_financiero_completo(self):
        """
        Reporte detallado de ingresos reales leyendo directamente los pagos
        verificados de users.json (fuente de verdad) y combinándolos con
        los registros de accounting.json.
        """
        if not self.auth:
            return {"error": "Servicio de usuarios no disponible"}

        todos_pagos = []
        for user in self.auth.get_users():
            for p in user.payments:
                if p.get("estado") == "verificado":
                    todos_pagos.append({
                        "usuario": user.nombre,
                        "email": user.correo,
                        "monto": float(p.get("amount", 0)),
                        "metodo": p.get("method", "N/A"),
                        "fecha": p.get("verified_at", ""),
                        "membresia": p.get("membership_name", "Sin plan"),
                        "referencia": p.get("reference", ""),
                    })

        total = sum(p["monto"] for p in todos_pagos)
        contable = self.account.total_ingresos() if self.account else 0

        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_ingresos_pagos": total,
            "total_ingresos_contabilidad": contable,
            "cantidad_pagos": len(todos_pagos),
            "promedio_pago": total / len(todos_pagos) if todos_pagos else 0,
            "pagos": sorted(todos_pagos, key=lambda x: x["fecha"], reverse=True),
        }

    # ── API TESTS (static methods) ────────────────────────────────────
    @staticmethod
    def reporte_membresias(auth_service):
        filas = []
        for u in auth_service.get_users():
            mem = u.membership
            if isinstance(mem, dict):
                filas.append({
                    "id_cliente": u.id_cliente, "nombre": u.get_name(),
                    "correo": u.get_email(),
                    "tipo": mem.get("tipo", mem.get("name", "—")),
                    "fecha_inicio": mem.get("fechaInicio", "—"),
                    "fecha_fin": mem.get("fechaFin", "—"),
                    "estado": mem.get("estado", "desconocido"),
                })
            else:
                filas.append({
                    "id_cliente": u.id_cliente, "nombre": u.get_name(),
                    "correo": u.get_email(),
                    "tipo": str(mem) if mem else "sin membresía",
                    "fecha_inicio": "—", "fecha_fin": "—",
                    "estado": "sin membresía",
                })
        return filas

    @staticmethod
    def reporte_clientes(auth_service):
        filas = []
        for u in auth_service.get_users():
            filas.append({
                "id_cliente": u.id_cliente, "nombre": u.get_name(),
                "correo": u.get_email(), "rol": u.get_role(),
                "num_pagos": len(u.payments) if u.payments else 0,
                "tiene_membresia": bool(u.membership),
            })
        return filas

    @staticmethod
    def reporte_contable(accounting_service):
        registros = accounting_service.get_all()
        return {
            "total_recaudado": accounting_service.total_recaudado(),
            "total_pendiente": accounting_service.total_pendiente(),
            "total_vencido":   sum(getattr(r, "monto", 0) for r in accounting_service.get_vencidos()),
            "num_registros":   len(registros),
            "detalle":         [r.to_dict() for r in registros],
        }

    @staticmethod
    def reporte_actividad(attendance_service, evaluation_service, incident_service):
        return {
            "total_asistencias":      len(attendance_service.get_all()),
            "total_evaluaciones":     len(evaluation_service.get_all()),
            "total_incidencias":      len(incident_service.get_all()),
            "incidencias_pendientes": len(incident_service.get_pendientes()),
        }

    @staticmethod
    def reporte_nomina(payroll_service):
        return {
            "total_pagado":    payroll_service.total_pagado(),
            "total_pendiente": payroll_service.total_pendiente(),
            "num_pagos":       len(payroll_service.get_all()),
            "detalle":         [r.to_dict() for r in payroll_service.get_all()],
        }

    @staticmethod
    def reporte_encuestas(survey_service):
        return {
            "total_encuestas":        len(survey_service.get_all()),
            "promedio_entrenador":    survey_service.promedio_entrenador(),
            "promedio_instalaciones": survey_service.promedio_instalaciones(),
            "promedio_general":       survey_service.promedio_general(),
            "sugerencias":            survey_service.get_sugerencias(),
        }

    @staticmethod
    def exportar_json(datos, ruta_archivo):
        import json
        import os
        import tempfile
        dir_name = os.path.dirname(ruta_archivo) if os.path.dirname(ruta_archivo) else "."
        os.makedirs(dir_name, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            os.replace(tmp_path, ruta_archivo)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
        return ruta_archivo
