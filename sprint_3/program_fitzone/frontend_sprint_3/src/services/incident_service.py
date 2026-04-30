# incident_service.py
# Servicio CRUD de incidencias del personal
# Autor: Andrés - Sprint 3

import json
import os
from src.models.incident import Incident


class IncidentService:
    """Gestiona incidencias del personal (inasistencias, permisos, etc.)."""

    def __init__(self):
        self.incidents = []
        self.file = "data/incidents.json"
        self._id_counter = 1
        self.load()

    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.incidents = []
            for d in data:
                i = Incident(
                    d["id_incidencia"], d["id_trabajador"], d["nombre_trabajador"],
                    d.get("tipo", "inasistencia"), d.get("causa", ""), d.get("fecha")
                )
                self.incidents.append(i)
                if d["id_incidencia"] >= self._id_counter:
                    self._id_counter = d["id_incidencia"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([i.to_dict() for i in self.incidents], f, indent=4)

    def create(self, id_trabajador, nombre_trabajador, tipo, causa):
        i = Incident(self._id_counter, id_trabajador, nombre_trabajador, tipo, causa)
        self.incidents.append(i)
        self._id_counter += 1
        self.save()
        return i

    def get_all(self):
        return self.incidents

    def get_by_worker(self, id_trabajador):
        return [i for i in self.incidents if i.id_trabajador == id_trabajador]
