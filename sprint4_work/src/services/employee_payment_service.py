# employee_payment_service.py
# Servicio de liquidación y pago de empleados
# Autor: Andrés - Sprint 4

import json
import os
from src.models.employee_payment import EmployeePayment


class EmployeePaymentService:
    """Gestiona la liquidación y el pago de empleados."""

    def __init__(self):
        self.payments    = []
        self.file        = "data/employee_payments.json"
        self._id_counter = 1
        self.load()

    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.payments = []
            for d in data:
                p = EmployeePayment(
                    d["id_pago"], d["id_trabajador"], d["nombre_trabajador"],
                    d.get("horas_trabajadas", 0), d.get("valor_hora", 0.0),
                    d.get("descuentos", 0.0), d.get("tipo_contrato", "indefinido"),
                    d.get("estado", "pendiente"), d.get("fecha")
                )
                self.payments.append(p)
                if d["id_pago"] >= self._id_counter:
                    self._id_counter = d["id_pago"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([p.to_dict() for p in self.payments], f, indent=4)

    def create_liquidation(self, id_trabajador, nombre_trabajador,
                           horas, valor_hora, descuentos=0.0,
                           tipo_contrato="indefinido"):
        p = EmployeePayment(self._id_counter, id_trabajador, nombre_trabajador,
                            horas, valor_hora, descuentos, tipo_contrato)
        self.payments.append(p)
        self._id_counter += 1
        self.save()
        return p

    def mark_paid(self, id_pago):
        for p in self.payments:
            if p.id_pago == id_pago:
                p.estado = "pagado"
                self.save()
                return True
        return False

    def get_all(self):
        return self.payments

    def get_pending(self):
        return [p for p in self.payments if p.estado == "pendiente"]

    def get_by_worker(self, id_trabajador):
        return [p for p in self.payments if p.id_trabajador == id_trabajador]
