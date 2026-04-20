import json
import os
from datetime import datetime
from src.models.payroll_record import PayrollRecord
from src.models.employee import Employee


class PayrollService:
    """Liquidación y pago de empleados con historial persistido (Sprint 4 - Andrés)."""

    def __init__(self):
        self.records = []
        self.file = "data/payroll.json"
        self._id_counter = 1
        self.load()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.records = []
            for d in data:
                r = PayrollRecord(
                    d["id_pago"], d["id_empleado"], d["nombre_empleado"],
                    d["tipo_contrato"], d["horas_trabajadas"], d["salario_base"],
                    d["descuento"], d["periodo"],
                    d.get("estado"), d.get("fecha"), d.get("observaciones", "")
                )
                self.records.append(r)
                if d["id_pago"] >= self._id_counter:
                    self._id_counter = d["id_pago"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def liquidar_empleado(self, id_empleado, nombre_empleado, tipo_contrato,
                          horas_trabajadas, salario_base, descuento,
                          periodo, observaciones=""):
        """
        Genera el registro de liquidación para un empleado.
        Valida que las horas sean > 0 y el salario >= 0.
        """
        if horas_trabajadas < 0:
            return None, "Las horas trabajadas no pueden ser negativas"
        if salario_base < 0:
            return None, "El salario base no puede ser negativo"
        if not (0 <= descuento <= 100):
            return None, "El descuento debe estar entre 0 y 100"

        r = PayrollRecord(
            self._id_counter, id_empleado, nombre_empleado,
            tipo_contrato, horas_trabajadas, salario_base,
            descuento, periodo, observaciones=observaciones
        )
        self.records.append(r)
        self._id_counter += 1
        self.save()
        return r, "Liquidación registrada correctamente"

    def liquidar_desde_empleado(self, empleado: Employee, horas_trabajadas,
                                 periodo, observaciones=""):
        """
        Atajo: toma los datos de un objeto Employee para liquidar.
        """
        return self.liquidar_empleado(
            empleado.id_trabajador, empleado.nombre,
            empleado.tipo_contrato, horas_trabajadas,
            empleado.salario, empleado.descuento,
            periodo, observaciones
        )

    def confirmar_pago(self, id_pago):
        """Marca el registro de nómina como pagado."""
        r = self.get_by_id(id_pago)
        if not r:
            return False, "Registro no encontrado"
        if r.estado == PayrollRecord.ESTADO_PAGADO:
            return False, "El pago ya fue confirmado anteriormente"
        r.marcar_pagado()
        self.save()
        return True, f"Pago de {r.nombre_empleado} confirmado: ${r.neto:,.2f}"

    # ─── CONSULTAS ───────────────────────────────────────────────────
    def get_by_id(self, id_pago):
        for r in self.records:
            if r.id_pago == id_pago:
                return r
        return None

    def get_all(self):
        return self.records

    def get_by_empleado(self, id_empleado):
        """Historial de pagos de un empleado."""
        return [r for r in self.records if r.id_empleado == id_empleado]

    def get_by_periodo(self, periodo):
        return [r for r in self.records if r.periodo == periodo]

    def get_pendientes(self):
        return [r for r in self.records if r.estado == PayrollRecord.ESTADO_PENDIENTE]

    def get_pagados(self):
        return [r for r in self.records if r.estado == PayrollRecord.ESTADO_PAGADO]

    def total_pagado(self):
        return round(sum(r.neto for r in self.get_pagados()), 2)

    def total_pendiente(self):
        return round(sum(r.neto for r in self.get_pendientes()), 2)
