from src.services.json_storage import load_json_list, save_json_list
from src.models.satisfaction_survey import SatisfactionSurvey


class SurveyService:
    """Encuestas de satisfacción (Sprint 4 - Andrés).
    Soporta: submit() para frontend y registrar_encuesta() para tests.
    """

    def __init__(self):
        self.surveys = []
        self.file = "data/surveys.json"
        self._id_counter = 1
        self.load()

    def load(self):
        data = load_json_list(self.file)
        self.surveys = []
        for d in data:
                s = SatisfactionSurvey(
                    d["id_encuesta"], d["id_cliente"], d["nombre_cliente"],
                    d.get("puntaje_entrenador", d.get("calificacion_entrenador", 0)),
                    d.get("puntaje_instalaciones", d.get("calificacion_instalaciones", 0)),
                    d.get("comentario", d.get("sugerencias", "")),
                    d.get("id_entrenador"),
                    d.get("nombre_entrenador", ""),
                    d.get("fecha")
                )
                self.surveys.append(s)
                if d["id_encuesta"] >= self._id_counter:
                    self._id_counter = d["id_encuesta"] + 1

    def save(self):
        save_json_list(self.file, [s.to_dict() for s in self.surveys])

    # API frontend (sprint5)
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

    # API tests (sprint4)
    def registrar_encuesta(self, id_cliente, nombre_cliente,
                           calificacion_entrenador, calificacion_instalaciones,
                           sugerencias=""):
        for val in [calificacion_entrenador, calificacion_instalaciones]:
            if not (1 <= val <= 5):
                return None, "Las calificaciones deben estar entre 1 y 5"
        s = self.submit(id_cliente, nombre_cliente,
                        calificacion_entrenador, calificacion_instalaciones, sugerencias)
        return s, "Encuesta registrada correctamente"

    def get_all(self):
        return self.surveys

    def get_by_cliente(self, id_cliente):
        return [s for s in self.surveys if s.id_cliente == id_cliente]

    def get_by_trainer(self, id_entrenador):
        return [s for s in self.surveys if s.id_entrenador == id_entrenador]

    def promedio_entrenador(self):
        if not self.surveys:
            return None
        return round(sum(s.puntaje_entrenador for s in self.surveys) / len(self.surveys), 2)

    def promedio_instalaciones(self):
        if not self.surveys:
            return None
        return round(sum(s.puntaje_instalaciones for s in self.surveys) / len(self.surveys), 2)

    def promedio_general(self):
        if not self.surveys:
            return None
        total = sum((s.puntaje_entrenador + s.puntaje_instalaciones) / 2
                    for s in self.surveys)
        return round(total / len(self.surveys), 2)

    def get_sugerencias(self):
        return [s.comentario for s in self.surveys if s.comentario and s.comentario.strip()]

    def avg_trainer_score(self):
        scores, counts = {}, {}
        for s in self.surveys:
            if s.id_entrenador:
                key = (s.id_entrenador, s.nombre_entrenador)
                scores[key] = scores.get(key, 0) + s.puntaje_entrenador
                counts[key] = counts.get(key, 0) + 1
        return {k: scores[k] / counts[k] for k in scores}

    def avg_facility_score(self):
        total = sum(s.puntaje_instalaciones for s in self.surveys)
        return total / len(self.surveys) if self.surveys else 0.0
