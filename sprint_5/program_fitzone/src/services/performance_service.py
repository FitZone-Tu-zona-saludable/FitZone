# performance_service.py
# Servicio de evaluación de desempeño de usuarios
# Autor: Andrés - Sprint 3

from src.services.json_storage import load_json_list, save_json_list
from src.models.performance import Performance


class PerformanceService:
    """Gestiona evaluaciones de desempeño realizadas por entrenadores."""

    def __init__(self):
        self.evaluations = []
        self.file = "data/performance.json"
        self._id_counter = 1
        self.load()

    def load(self):
        data = load_json_list(self.file)
        self.evaluations = []
        for d in data:
                p = Performance(
                    d["id_eval"], d["id_cliente"], d["nombre_cliente"],
                    d["id_entrenador"], d["nombre_entrenador"],
                    d.get("puntaje", 0), d.get("observaciones", ""), d.get("fecha")
                )
                self.evaluations.append(p)
                if d["id_eval"] >= self._id_counter:
                    self._id_counter = d["id_eval"] + 1

    def save(self):
        save_json_list(self.file, [e.to_dict() for e in self.evaluations])

    def create(self, id_cliente, nombre_cliente,
               id_entrenador, nombre_entrenador,
               puntaje, observaciones=""):
        p = Performance(self._id_counter, id_cliente, nombre_cliente,
                        id_entrenador, nombre_entrenador, puntaje, observaciones)
        self.evaluations.append(p)
        self._id_counter += 1
        self.save()
        return p

    def get_all(self):
        return self.evaluations

    def get_by_client(self, id_cliente):
        return [e for e in self.evaluations if e.id_cliente == id_cliente]

    def get_by_trainer(self, id_entrenador):
        return [e for e in self.evaluations if e.id_entrenador == id_entrenador]
