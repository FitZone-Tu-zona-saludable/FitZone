import json
import os
from src.models.satisfaction_survey import SatisfactionSurvey


class SurveyService:
    """Almacenamiento y consulta de encuestas de satisfacción (Sprint 4 - Andrés)."""

    def __init__(self):
        self.surveys = []
        self.file = "data/surveys.json"
        self._id_counter = 1
        self.load()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
            self.surveys = []
            for d in data:
                s = SatisfactionSurvey(
                    d["id_encuesta"], d["id_cliente"], d["nombre_cliente"],
                    d["calificacion_entrenador"], d["calificacion_instalaciones"],
                    d.get("sugerencias", ""), d.get("fecha")
                )
                self.surveys.append(s)
                if d["id_encuesta"] >= self._id_counter:
                    self._id_counter = d["id_encuesta"] + 1

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.file, "w") as f:
            json.dump([s.to_dict() for s in self.surveys], f, indent=4, ensure_ascii=False)

    # ─── LÓGICA DE NEGOCIO ───────────────────────────────────────────
    def registrar_encuesta(self, id_cliente, nombre_cliente,
                           calificacion_entrenador, calificacion_instalaciones,
                           sugerencias=""):
        """
        Registra una encuesta de satisfacción.
        Valida que los criterios estén entre 1 y 5.
        """
        for val in [calificacion_entrenador, calificacion_instalaciones]:
            if not (1 <= val <= 5):
                return None, "Las calificaciones deben estar entre 1 y 5"

        s = SatisfactionSurvey(
            self._id_counter, id_cliente, nombre_cliente,
            calificacion_entrenador, calificacion_instalaciones, sugerencias
        )
        self.surveys.append(s)
        self._id_counter += 1
        self.save()
        return s, "Encuesta registrada correctamente"

    # ─── CONSULTAS ───────────────────────────────────────────────────
    def get_all(self):
        return self.surveys

    def get_by_cliente(self, id_cliente):
        return [s for s in self.surveys if s.id_cliente == id_cliente]

    def promedio_entrenador(self):
        """Promedio global de calificación a entrenadores."""
        if not self.surveys:
            return None
        return round(sum(s.calificacion_entrenador for s in self.surveys) / len(self.surveys), 2)

    def promedio_instalaciones(self):
        """Promedio global de calificación a instalaciones."""
        if not self.surveys:
            return None
        return round(
            sum(s.calificacion_instalaciones for s in self.surveys) / len(self.surveys), 2
        )

    def promedio_general(self):
        """Promedio global combinado de todas las encuestas."""
        if not self.surveys:
            return None
        return round(sum(s.promedio for s in self.surveys) / len(self.surveys), 2)

    def get_sugerencias(self):
        """Devuelve lista de sugerencias no vacías."""
        return [s.sugerencias for s in self.surveys if s.sugerencias.strip()]
