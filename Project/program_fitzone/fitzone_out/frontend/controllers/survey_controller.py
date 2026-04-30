# survey_controller.py
# Controlador de encuestas de satisfacción — Sprint 4 (Alex)

from frontend.services.app_context import survey_service


class SurveyController:
    def __init__(self):
        self.service = survey_service

    def list_surveys(self):
        return [s.to_dict() for s in self.service.get_all()]

    def submit_survey(self, id_cliente, nombre_cliente, puntaje_ent,
                      puntaje_inst, comentario="", id_ent=None, nom_ent=""):
        s = self.service.submit(id_cliente, nombre_cliente, puntaje_ent,
                                puntaje_inst, comentario, id_ent, nom_ent)
        return {"success": True, "data": s.to_dict()}

    def avg_trainer_scores(self):
        return self.service.avg_trainer_score()

    def avg_facility(self):
        return self.service.avg_facility_score()
