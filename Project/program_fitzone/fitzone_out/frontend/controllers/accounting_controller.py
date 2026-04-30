# accounting_controller.py
# Controlador de contabilidad — Sprint 3 (Alex)

from frontend.services.app_context import accounting_service


class AccountingController:
    """Intermediario MVC entre la vista contable y el servicio real."""

    def __init__(self):
        self.service = accounting_service

    def list_entries(self):
        return [e.to_dict() for e in self.service.get_all()]

    def list_pending(self):
        return [e.to_dict() for e in self.service.get_pending()]

    def add_entry(self, concepto, tipo, monto, referencia=""):
        e = self.service.add_entry(concepto, tipo, monto, referencia)
        return {"success": True, "data": e.to_dict()}

    def mark_paid(self, id_entrada):
        ok = self.service.mark_paid(id_entrada)
        return {"success": ok}

    # ── Totalizaciones ───────────────────────────────────────────────────────
    def total_ingresos(self):
        """Suma todos los ingresos confirmados (entries + records)."""
        return self.service.total_ingresos()

    def total_pendiente(self):
        """Suma todos los montos pendientes."""
        return self.service.total_pendiente()

    def total_por_usuario(self, user_id):
        """Total pagado por un usuario específico."""
        return self.service.total_por_usuario(user_id)

    def reporte_ingresos(self, desde=None, hasta=None):
        """Reporte de ingresos filtrado por rango de fechas (YYYY-MM-DD)."""
        return self.service.reporte_ingresos(desde=desde, hasta=hasta)

    def resumen_contable(self):
        """Resumen general: ingresos, pendientes, vencidos y totales."""
        return {
            "total_ingresos": self.service.total_ingresos(),
            "total_pendiente": self.service.total_pendiente(),
            "total_recaudado": self.service.total_recaudado(),
            "total_vencido": sum(
                r.monto for r in self.service.get_vencidos()
            ),
            "num_registros": len(self.service.get_all()),
        }
