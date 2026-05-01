from src.services.json_storage import load_json_list, save_json_list
from src.models.incident import Incident


class IncidentService:
    """Gestión de incidencias del personal (Sprint 3 - Andrés).
    Soporta ambas APIs: create() para el frontend y registrar_incidencia() para los tests.
    """

    def __init__(self):
        self.incidents = []
        self.file = "data/incidents.json"
        self._id_counter = 1
        self.load()

    def load(self):
        data = load_json_list(self.file)
        self.incidents = []
        for d in data:
                i = Incident(
                    d["id_incidencia"], d["id_trabajador"], d["nombre_trabajador"],
                    d.get("tipo", "inasistencia"), d.get("causa", ""),
                    d.get("fecha"), d.get("resuelta", False),
                    d.get("observaciones", "")
                )
                self.incidents.append(i)
                if d["id_incidencia"] >= self._id_counter:
                    self._id_counter = d["id_incidencia"] + 1

    def save(self):
        save_json_list(self.file, [i.to_dict() for i in self.incidents])

    # API frontend (sprint5)
    def create(self, id_trabajador, nombre_trabajador, tipo, causa):
        i = Incident(self._id_counter, id_trabajador, nombre_trabajador, tipo, causa)
        self.incidents.append(i)
        self._id_counter += 1
        self.save()
        return i

    # API tests (sprint3/4)
    def registrar_incidencia(self, id_trabajador, nombre_trabajador,
                             tipo, causa, observaciones=""):
        inc = Incident(self._id_counter, id_trabajador, nombre_trabajador,
                       tipo, causa, observaciones=observaciones)
        self.incidents.append(inc)
        self._id_counter += 1
        self.save()
        return inc

    def resolver_incidencia(self, id_incidencia):
        for i in self.incidents:
            if i.id_incidencia == id_incidencia:
                i.resolver()
                self.save()
                return True, "Incidencia resuelta"
        return False, "Incidencia no encontrada"

    def get_all(self):
        return self.incidents

    def get_by_worker(self, id_trabajador):
        return [i for i in self.incidents if i.id_trabajador == id_trabajador]

    def get_by_trabajador(self, id_trabajador):
        return self.get_by_worker(id_trabajador)

    def get_pendientes(self):
        return [i for i in self.incidents if not i.resuelta]

    def get_by_id(self, id_incidencia):
        for i in self.incidents:
            if i.id_incidencia == id_incidencia:
                return i
        return None

    def get_by_tipo(self, tipo):
        return [i for i in self.incidents if i.tipo == tipo]
