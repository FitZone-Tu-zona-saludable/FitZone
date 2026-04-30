# accounting_service.py
# Servicio de contabilidad básica (pagos, saldos, cobros pendientes)
# Autor: Andrés - Sprint 3

import json
import os
from src.models.account_entry import AccountEntry


class AccountingService:
    """Gestiona el módulo contable: ingresos, cobros pendientes y saldos."""

    def __init__(self):
        self.entries = []
        self.file = "data/accounting.json"
        self._id_counter = 1
        self.load()

    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.entries = []
            for d in data:
                e = AccountEntry(
                    d["id_entrada"], d["concepto"], d["tipo"], d["monto"],
                    d.get("estado", "pendiente"), d.get("referencia", ""), d.get("fecha")
                )
                self.entries.append(e)
                if d["id_entrada"] >= self._id_counter:
                    self._id_counter = d["id_entrada"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=4)

    def add_entry(self, concepto, tipo, monto, referencia=""):
        e = AccountEntry(self._id_counter, concepto, tipo, monto, referencia=referencia)
        self.entries.append(e)
        self._id_counter += 1
        self.save()
        return e

    def mark_paid(self, id_entrada):
        for e in self.entries:
            if e.id_entrada == id_entrada:
                e.estado = "pagado"
                self.save()
                return True
        return False

    def get_all(self):
        return self.entries

    def get_pending(self):
        return [e for e in self.entries if e.estado == "pendiente"]

    def get_by_tipo(self, tipo):
        return [e for e in self.entries if e.tipo == tipo]

    def total_ingresos(self):
        return sum(e.monto for e in self.entries
                   if e.tipo == "ingreso" and e.estado == "pagado")

    def total_pendiente(self):
        return sum(e.monto for e in self.entries if e.estado == "pendiente")
