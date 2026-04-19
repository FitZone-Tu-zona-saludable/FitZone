import json
import os
from src.models.user_evaluation import UserEvaluation


class EvaluationService:
    """Módulo para que entrenadores evalúen el desempeño de los usuarios."""

    def __init__(self):
        self.evaluations = []
        self.file = "data/evaluations.json"
        self._id_counter = 1
        self.load()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.evaluations = []
            for d in data:
                e = UserEvaluation(
                    d["id_evaluacion"], d["id_entrenador"], d["nombre_entrenador"],
                    d["id_cliente"], d["nombre_cliente"],
                    d.get("puntualidad", 0), d.get("rendimiento", 0), d.get("actitud", 0),
                    d.get("comentarios", ""), d.get("fecha")
                )
                self.evaluations.append(e)
                if d["id_evaluacion"] >= self._id_counter:
                    self._id_counter = d["id_evaluacion"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([e.to_dict() for e in self.evaluations], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def evaluar_usuario(self, id_entrenador, nombre_entrenador,
                        id_cliente, nombre_cliente,
                        puntualidad, rendimiento, actitud, comentarios=""):
        """Crea una evaluación de desempeño de un usuario."""
        for c in [puntualidad, rendimiento, actitud]:
            if not (0 <= c <= 10):
                return None, "Los criterios deben estar entre 0 y 10"
        e = UserEvaluation(
            self._id_counter, id_entrenador, nombre_entrenador,
            id_cliente, nombre_cliente,
            puntualidad, rendimiento, actitud, comentarios
        )
        self.evaluations.append(e)
        self._id_counter += 1
        self.save()
        return e, "Evaluación registrada correctamente"

    def get_by_cliente(self, id_cliente):
        return [e for e in self.evaluations if e.id_cliente == id_cliente]

    def get_by_entrenador(self, id_entrenador):
        return [e for e in self.evaluations if e.id_entrenador == id_entrenador]

    def get_all(self):
        return self.evaluations

    def promedio_cliente(self, id_cliente):
        """Calcula el promedio general de todas las evaluaciones del cliente."""
        evs = self.get_by_cliente(id_cliente)
        if not evs:
            return None
        return round(sum(e.promedio for e in evs) / len(evs), 2)
