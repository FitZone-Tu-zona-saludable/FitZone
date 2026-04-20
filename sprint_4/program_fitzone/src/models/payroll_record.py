from datetime import datetime


class PayrollRecord:
    """Registro de liquidación y pago de nómina de un empleado (Sprint 4 - Andrés)."""

    ESTADO_PENDIENTE = "pendiente"
    ESTADO_PAGADO    = "pagado"

    def __init__(self, id_pago, id_empleado, nombre_empleado,
                 tipo_contrato, horas_trabajadas, salario_base,
                 descuento, periodo, estado=None, fecha=None,
                 observaciones=""):
        self.id_pago           = id_pago
        self.id_empleado       = id_empleado
        self.nombre_empleado   = nombre_empleado
        self.tipo_contrato     = tipo_contrato
        self.horas_trabajadas  = float(horas_trabajadas)
        self.salario_base      = float(salario_base)
        self.descuento         = float(descuento)        # porcentaje 0-100
        self.periodo           = periodo                 # e.g. "2025-04"
        self.estado            = estado or self.ESTADO_PENDIENTE
        self.fecha             = fecha or datetime.now().strftime("%Y-%m-%d")
        self.observaciones     = observaciones

    # ── Cálculos ──────────────────────────────────────────────────────
    @property
    def valor_hora(self):
        """Salario base dividido entre 240 horas mensuales estándar."""
        if self.salario_base <= 0:
            return 0.0
        return round(self.salario_base / 240, 4)

    @property
    def bruto(self):
        """Pago bruto = valor_hora × horas_trabajadas."""
        return round(self.valor_hora * self.horas_trabajadas, 2)

    @property
    def monto_descuento(self):
        return round(self.bruto * self.descuento / 100, 2)

    @property
    def neto(self):
        """Valor final a pagar después de descuentos."""
        return round(self.bruto - self.monto_descuento, 2)

    def marcar_pagado(self):
        self.estado = self.ESTADO_PAGADO

    def to_dict(self):
        return {
            "id_pago":          self.id_pago,
            "id_empleado":      self.id_empleado,
            "nombre_empleado":  self.nombre_empleado,
            "tipo_contrato":    self.tipo_contrato,
            "horas_trabajadas": self.horas_trabajadas,
            "salario_base":     self.salario_base,
            "descuento":        self.descuento,
            "periodo":          self.periodo,
            "bruto":            self.bruto,
            "monto_descuento":  self.monto_descuento,
            "neto":             self.neto,
            "estado":           self.estado,
            "fecha":            self.fecha,
            "observaciones":    self.observaciones,
        }
