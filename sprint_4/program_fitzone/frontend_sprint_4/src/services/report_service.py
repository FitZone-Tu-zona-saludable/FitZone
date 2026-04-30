# report_service.py
# Servicio de generación de reportes de membresías, clientes y actividad
# Autor: Andrés - Sprint 4

from datetime import datetime


class ReportService:
    """Consolida información operativa y contable para la gerencia."""

    def __init__(self, auth_service, accounting_service=None):
        self.auth    = auth_service
        self.account = accounting_service

    # ─── RF23: Generar reportes ────────────────────────────────────
    def report_members(self):
        """Reporte de membresías activas, por vencer y vencidas."""
        users    = self.auth.get_users()
        activas  = [u for u in users if u.membership and
                    u.membership.get("estado") == "activa"]
        vencidas = [u for u in users if u.membership and
                    u.membership.get("estado") == "vencida"]
        por_vencer=[u for u in users if u.membership and
                    u.membership.get("estado") == "por_vencer"]
        sin_mem  = [u for u in users if not u.membership]

        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_usuarios":   len(users),
            "activas":          len(activas),
            "por_vencer":       len(por_vencer),
            "vencidas":         len(vencidas),
            "sin_membresia":    len(sin_mem),
            "detalle": [
                {
                    "nombre": u.nombre,
                    "correo": u.correo,
                    "rol":    u.role,
                    "plan":   u.membership.get("name", "N/A") if u.membership else "Sin plan",
                    "estado": u.membership.get("estado", "N/A") if u.membership else "N/A"
                }
                for u in users
            ]
        }

    def report_activity(self):
        """Reporte de actividad general: pagos registrados por usuario."""
        users = self.auth.get_users()
        rows  = []
        for u in users:
            for p in u.payments:
                rows.append({
                    "usuario": u.nombre,
                    "correo":  u.correo,
                    "valor":   p.get("value", 0),
                    "metodo":  p.get("method", "N/A"),
                })
        return {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_pagos":      len(rows),
            "detalle":          rows
        }

    def report_financial_summary(self):
        """Resumen contable para gerencia (si accounting_service disponible)."""
        if not self.account:
            return {"error": "Servicio contable no disponible"}
        entries = self.account.get_all()
        ingresos  = sum(e.monto for e in entries
                        if e.tipo == "ingreso" and e.estado == "pagado")
        pendientes= sum(e.monto for e in entries if e.estado == "pendiente")
        return {
            "fecha_generacion":  datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_ingresos":    ingresos,
            "total_pendiente":   pendientes,
            "total_entradas":    len(entries),
        }
