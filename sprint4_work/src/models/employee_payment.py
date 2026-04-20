# employee_payment.py
# Modelo de pago/liquidación de empleado
# Autor: Andrés - Sprint 4

from datetime import datetime


class EmployeePayment:
    """Liquidación de pago a un empleado considerando horas, contrato y descuentos."""

    def __init__(self, id_pago, id_trabajador, nombre_trabajador,
                 horas_trabajadas=0, valor_hora=0.0, descuentos=0.0,
                 tipo_contrato="indefinido", estado="pendiente", fecha=None):
        self.id_pago           = id_pago
        self.id_trabajador     = id_trabajador
        self.nombre_trabajador = nombre_trabajador
        self.horas_trabajadas  = horas_trabajadas
        self.valor_hora        = valor_hora
        self.descuentos        = descuentos
        self.tipo_contrato     = tipo_contrato
        self.estado            = estado   # "pendiente", "pagado"
        self.fecha             = fecha or datetime.now().strftime("%Y-%m-%d")

    @property
    def bruto(self):
        return self.horas_trabajadas * self.valor_hora

    @property
    def neto(self):
        return max(0.0, self.bruto - self.descuentos)

    def to_dict(self):
        return {
            "id_pago":           self.id_pago,
            "id_trabajador":     self.id_trabajador,
            "nombre_trabajador": self.nombre_trabajador,
            "horas_trabajadas":  self.horas_trabajadas,
            "valor_hora":        self.valor_hora,
            "descuentos":        self.descuentos,
            "bruto":             self.bruto,
            "neto":              self.neto,
            "tipo_contrato":     self.tipo_contrato,
            "estado":            self.estado,
            "fecha":             self.fecha
        }
