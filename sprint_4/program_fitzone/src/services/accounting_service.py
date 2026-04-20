import json
import os
from datetime import datetime
from src.models.account_record import AccountRecord


class AccountingService:
    """Módulo contable: registra pagos, saldos por pagar y cobros pendientes."""

    def __init__(self):
        self.records = []
        self.file = "data/accounting.json"
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
                r = AccountRecord(
                    d["id_registro"], d["id_cliente"], d["nombre_cliente"],
                    d["concepto"], d["monto"], d.get("estado"),
                    d.get("fecha"), d.get("fecha_vencimiento", "")
                )
                self.records.append(r)
                if d["id_registro"] >= self._id_counter:
                    self._id_counter = d["id_registro"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def registrar_cobro(self, id_cliente, nombre_cliente, concepto,
                        monto, fecha_vencimiento=""):
        """Registra un cobro pendiente."""
        r = AccountRecord(
            self._id_counter, id_cliente, nombre_cliente,
            concepto, monto, AccountRecord.ESTADO_PENDIENTE,
            fecha_vencimiento=fecha_vencimiento
        )
        self.records.append(r)
        self._id_counter += 1
        self.save()
        return r

    def confirmar_pago(self, id_registro):
        """Marca un cobro como pagado."""
        r = self.get_by_id(id_registro)
        if not r:
            return False, "Registro no encontrado"
        r.marcar_pagado()
        self.save()
        return True, f"Pago de {r.nombre_cliente} confirmado (${r.monto})"

    def verificar_vencimientos(self):
        """Marca como vencidos los cobros cuya fecha de vencimiento ya pasó."""
        today = datetime.now().strftime("%Y-%m-%d")
        vencidos = []
        for r in self.records:
            if (r.estado == AccountRecord.ESTADO_PENDIENTE
                    and r.fecha_vencimiento and r.fecha_vencimiento < today):
                r.marcar_vencido()
                vencidos.append(r)
        if vencidos:
            self.save()
        return vencidos

    def get_by_id(self, id_registro):
        for r in self.records:
            if r.id_registro == id_registro:
                return r
        return None

    def get_all(self):
        return self.records

    def get_pendientes(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_PENDIENTE]

    def get_vencidos(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_VENCIDO]

    def get_pagados(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_PAGADO]

    def get_by_cliente(self, id_cliente):
        return [r for r in self.records if r.id_cliente == id_cliente]

    def total_recaudado(self):
        return sum(r.monto for r in self.get_pagados())

    def total_pendiente(self):
        return sum(r.monto for r in self.get_pendientes())
