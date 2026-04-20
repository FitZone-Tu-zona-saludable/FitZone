# attendance_service.py
# Servicio CRUD de asistencia con persistencia JSON
# Autor: Andrés - Sprint 3

import json
import os
from src.models.attendance import Attendance


class AttendanceService:
    """Gestiona el registro y consulta de asistencias de clientes."""

    def __init__(self):
        self.attendances = []
        self.file = "data/attendance.json"
        self._id_counter = 1
        self.load()

    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.attendances = []
            for d in data:
                a = Attendance(
                    d["id_asistencia"], d["id_cliente"], d["nombre_cliente"],
                    d.get("fecha"), d.get("clase", ""), d.get("servicio", "")
                )
                self.attendances.append(a)
                if d["id_asistencia"] >= self._id_counter:
                    self._id_counter = d["id_asistencia"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([a.to_dict() for a in self.attendances], f, indent=4)

    def register(self, id_cliente, nombre_cliente, clase="", servicio=""):
        a = Attendance(self._id_counter, id_cliente, nombre_cliente,
                       clase=clase, servicio=servicio)
        self.attendances.append(a)
        self._id_counter += 1
        self.save()
        return a

    def get_all(self):
        return self.attendances

    def get_by_client(self, id_cliente):
        return [a for a in self.attendances if a.id_cliente == id_cliente]

    def update(self, id_asistencia, **kwargs):
        for a in self.attendances:
            if a.id_asistencia == id_asistencia:
                for k, v in kwargs.items():
                    if hasattr(a, k):
                        setattr(a, k, v)
                self.save()
                return True
        return False

    def delete(self, id_asistencia):
        for a in self.attendances:
            if a.id_asistencia == id_asistencia:
                self.attendances.remove(a)
                self.save()
                return True
        return False
