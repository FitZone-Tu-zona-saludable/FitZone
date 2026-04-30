# employee_payment_controller.py
# Controlador de pago de empleados — Sprint 4 (Alex)

from src.services.employee_payment_service import EmployeePaymentService


class EmployeePaymentController:
    def __init__(self):
        self.service = EmployeePaymentService()

    def list_payments(self):
        return [p.to_dict() for p in self.service.get_all()]

    def list_pending(self):
        return [p.to_dict() for p in self.service.get_pending()]

    def create_liquidation(self, id_trabajador, nombre, horas,
                           valor_hora, descuentos=0.0, tipo_contrato="indefinido"):
        p = self.service.create_liquidation(
            id_trabajador, nombre, horas, valor_hora, descuentos, tipo_contrato)
        return {"success": True, "data": p.to_dict()}

    def mark_paid(self, id_pago):
        ok = self.service.mark_paid(id_pago)
        return {"success": ok}
