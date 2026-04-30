# survey_service.py
# Servicio de encuestas de satisfacción (entrenadores e instalaciones)
# Autor: Andrés - Sprint 4

import json
import os
from src.models.satisfaction_survey import SatisfactionSurvey


class SurveyService:
    """Gestiona el almacenamiento y consulta de encuestas de satisfacción."""

    def __init__(self):
        self.surveys     = []
        self.file        = "data/surveys.json"
        self._id_counter = 1
        self.load()

    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.surveys = []
            for d in data:
                s = SatisfactionSurvey(
                    d["id_encuesta"], d["id_cliente"], d["nombre_cliente"],
                    d.get("puntaje_entrenador", 0), d.get("puntaje_instalaciones", 0),
                    d.get("comentario", ""), d.get("id_entrenador"),
                    d.get("nombre_entrenador", ""), d.get("fecha")
                )
                self.surveys.append(s)
                if d["id_encuesta"] >= self._id_counter:
                    self._id_counter = d["id_encuesta"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([s.to_dict() for s in self.surveys], f, indent=4)

    def submit(self, id_cliente, nombre_cliente, puntaje_entrenador,
               puntaje_instalaciones, comentario="",
               id_entrenador=None, nombre_entrenador=""):
        s = SatisfactionSurvey(
            self._id_counter, id_cliente, nombre_cliente,
            puntaje_entrenador, puntaje_instalaciones, comentario,
            id_entrenador, nombre_entrenador
        )
        self.surveys.append(s)
        self._id_counter += 1
        self.save()
        return s

    def get_all(self):
        return self.surveys

    def get_by_trainer(self, id_entrenador):
        return [s for s in self.surveys if s.id_entrenador == id_entrenador]

    def avg_trainer_score(self):
        """Promedio de puntaje por entrenador."""
        scores = {}
        counts = {}
        for s in self.surveys:
            if s.id_entrenador:
                key = (s.id_entrenador, s.nombre_entrenador)
                scores[key] = scores.get(key, 0) + s.puntaje_entrenador
                counts[key] = counts.get(key, 0) + 1
        return {k: scores[k]/counts[k] for k in scores}

    def avg_facility_score(self):
        total = sum(s.puntaje_instalaciones for s in self.surveys)
        return total / len(self.surveys) if self.surveys else 0.0
