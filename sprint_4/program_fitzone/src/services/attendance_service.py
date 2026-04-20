import json
import os
from datetime import datetime
from src.models.attendance import Attendance


class AttendanceService:
    """Servicio para registrar y consultar el afiche de asistencia de clientes."""

    def __init__(self):
        self.records = []
        self.file = "data/attendance.json"
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
                a = Attendance(
                    d["id_asistencia"], d["id_cliente"], d["nombre_cliente"],
                    d.get("fecha"), d.get("hora"),
                    d.get("clase_servicio", ""), d.get("observaciones", "")
                )
                self.records.append(a)
                if d["id_asistencia"] >= self._id_counter:
                    self._id_counter = d["id_asistencia"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def registrar_entrada(self, id_cliente, nombre_cliente,
                          clase_servicio="", observaciones=""):
        """Registra la entrada de un cliente con fecha y hora actual."""
        a = Attendance(
            self._id_counter, id_cliente, nombre_cliente,
            clase_servicio=clase_servicio, observaciones=observaciones
        )
        self.records.append(a)
        self._id_counter += 1
        self.save()
        return a

    def actualizar_asistencia(self, id_asistencia, **kwargs):
        """Actualiza campos de un registro existente."""
        r = self.get_by_id(id_asistencia)
        if not r:
            return False
        for key, val in kwargs.items():
            if hasattr(r, key):
                setattr(r, key, val)
        self.save()
        return True

    def get_by_id(self, id_asistencia):
        for r in self.records:
            if r.id_asistencia == id_asistencia:
                return r
        return None

    def get_all(self):
        return self.records

    def get_by_cliente(self, id_cliente):
        return [r for r in self.records if r.id_cliente == id_cliente]

    def get_by_fecha(self, fecha):
        return [r for r in self.records if r.fecha == fecha]

    def get_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_by_fecha(today)
