import json
import os
from src.services.json_storage import load_json_list, save_json_list
from datetime import datetime
from src.models.account_entry import AccountEntry
from src.models.account_record import AccountRecord


class AccountingService:
    """Módulo contable — soporta la API del frontend (AccountEntry) y la de los tests (AccountRecord).
    Sprint 3 - Andrés.
    """

    def __init__(self):
        self.entries = []        # AccountEntry — usado por frontend
        self.records = []        # AccountRecord — usado por tests sprint4
        self.file = "data/accounting.json"
        self._id_counter = 1
        self._rec_counter = 1
        self.load()

    def load(self):
        data = load_json_list(self.file)
        self.entries = []
        self.records = []
        for d in data:
            # Detect which format
            if "id_entrada" in d:
                e = AccountEntry(
                    d["id_entrada"], d["concepto"], d["tipo"], d["monto"],
                    d.get("estado", "pendiente"), d.get("referencia", ""), d.get("fecha")
                )
                self.entries.append(e)
                if d["id_entrada"] >= self._id_counter:
                    self._id_counter = d["id_entrada"] + 1
            elif "id_registro" in d:
                r = AccountRecord(
                    d["id_registro"], d["id_cliente"], d["nombre_cliente"],
                    d["concepto"], d["monto"], d.get("estado"),
                    d.get("fecha"), d.get("fecha_vencimiento", "")
                )
                self.records.append(r)
                if d["id_registro"] >= self._rec_counter:
                    self._rec_counter = d["id_registro"] + 1

    def save(self):
        all_data = [e.to_dict() for e in self.entries] + [r.to_dict() for r in self.records]
        save_json_list(self.file, all_data)

    # ── API FRONTEND (AccountEntry) ───────────────────────────────────
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

    def get_pending(self):
        return [e for e in self.entries if e.estado == "pendiente"]

    def get_by_tipo(self, tipo):
        return [e for e in self.entries if e.tipo == tipo]

    def total_ingresos(self):
        return sum(e.monto for e in self.entries
                   if e.tipo == "ingreso" and e.estado == "pagado")

    def total_pendiente(self):
        total_entries = sum(e.monto for e in self.entries if e.estado == "pendiente")
        total_records = sum(r.monto for r in self.records if r.estado == AccountRecord.ESTADO_PENDIENTE)
        return total_entries + total_records

    # ── API TESTS sprint4 (AccountRecord) ────────────────────────────
    def registrar_cobro(self, id_cliente, nombre_cliente, concepto,
                        monto, fecha_vencimiento=""):
        r = AccountRecord(
            self._rec_counter, id_cliente, nombre_cliente,
            concepto, monto, AccountRecord.ESTADO_PENDIENTE,
            fecha_vencimiento=fecha_vencimiento
        )
        self.records.append(r)
        self._rec_counter += 1
        self.save()
        return r

    def confirmar_pago(self, id_registro):
        r = self.get_by_id(id_registro)
        if not r:
            return False, "Registro no encontrado"
        r.marcar_pagado()
        self.save()
        return True, f"Pago de {r.nombre_cliente} confirmado (${r.monto})"

    def verificar_vencimientos(self):
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

    def get_by_cliente(self, id_cliente):
        return [r for r in self.records if r.id_cliente == id_cliente]

    def get_pagados(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_PAGADO]

    def get_vencidos(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_VENCIDO]

    def get_pendientes(self):
        return [r for r in self.records if r.estado == AccountRecord.ESTADO_PENDIENTE]

    def total_recaudado(self):
        return sum(r.monto for r in self.get_pagados())

    # ── UNIFIED get_all ───────────────────────────────────────────────
    def get_all(self):
        return self.entries + self.records
