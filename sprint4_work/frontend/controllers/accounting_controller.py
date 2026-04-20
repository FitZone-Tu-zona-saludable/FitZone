# accounting_controller.py
# Controlador de contabilidad — Sprint 3 (Alex)

from src.services.accounting_service import AccountingService


class AccountingController:
    """Intermediario MVC entre la vista contable y el servicio real."""

    def __init__(self):
        self.service = AccountingService()

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

    def total_ingresos(self):
        return self.service.total_ingresos()

    def total_pendiente(self):
        return self.service.total_pendiente()
