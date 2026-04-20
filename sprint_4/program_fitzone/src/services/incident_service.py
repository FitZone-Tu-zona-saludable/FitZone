import json
import os
from src.models.incident import Incident


class IncidentService:
    """Registro y gestión de incidencias del personal (inasistencias, causas)."""

    def __init__(self):
        self.incidents = []
        self.file = "data/incidents.json"
        self._id_counter = 1
        self.load()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.incidents = []
            for d in data:
                inc = Incident(
                    d["id_incidencia"], d["id_trabajador"], d["nombre_trabajador"],
                    d["tipo"], d["causa"], d.get("fecha"),
                    d.get("resuelta", False), d.get("observaciones", "")
                )
                self.incidents.append(inc)
                if d["id_incidencia"] >= self._id_counter:
                    self._id_counter = d["id_incidencia"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([i.to_dict() for i in self.incidents], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def registrar_incidencia(self, id_trabajador, nombre_trabajador,
                             tipo, causa, observaciones=""):
        """Registra una incidencia del personal con fecha automática."""
        inc = Incident(
            self._id_counter, id_trabajador, nombre_trabajador,
            tipo, causa, observaciones=observaciones
        )
        self.incidents.append(inc)
        self._id_counter += 1
        self.save()
        return inc

    def resolver_incidencia(self, id_incidencia):
        inc = self.get_by_id(id_incidencia)
        if not inc:
            return False, "Incidencia no encontrada"
        inc.resolver()
        self.save()
        return True, "Incidencia marcada como resuelta"

    def get_by_id(self, id_incidencia):
        for i in self.incidents:
            if i.id_incidencia == id_incidencia:
                return i
        return None

    def get_all(self):
        return self.incidents

    def get_by_trabajador(self, id_trabajador):
        return [i for i in self.incidents if i.id_trabajador == id_trabajador]

    def get_pendientes(self):
        return [i for i in self.incidents if not i.resuelta]

    def get_by_tipo(self, tipo):
        return [i for i in self.incidents if i.tipo == tipo]
