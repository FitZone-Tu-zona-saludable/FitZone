# satisfaction_survey.py
# Modelo de encuesta de satisfacción sobre entrenadores e instalaciones
# Autor: Andrés - Sprint 4

from datetime import datetime


class SatisfactionSurvey:
    """Encuesta de satisfacción para evaluar entrenadores e instalaciones."""

    def __init__(self, id_encuesta, id_cliente, nombre_cliente,
                 puntaje_entrenador=0, puntaje_instalaciones=0,
                 comentario="", id_entrenador=None, nombre_entrenador="",
                 fecha=None):
        self.id_encuesta          = id_encuesta
        self.id_cliente           = id_cliente
        self.nombre_cliente       = nombre_cliente
        self.puntaje_entrenador   = puntaje_entrenador    # 1-5
        self.puntaje_instalaciones= puntaje_instalaciones # 1-5
        self.comentario           = comentario
        self.id_entrenador        = id_entrenador
        self.nombre_entrenador    = nombre_entrenador
        self.fecha                = fecha or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id_encuesta":           self.id_encuesta,
            "id_cliente":            self.id_cliente,
            "nombre_cliente":        self.nombre_cliente,
            "puntaje_entrenador":    self.puntaje_entrenador,
            "puntaje_instalaciones": self.puntaje_instalaciones,
            "comentario":            self.comentario,
            "id_entrenador":         self.id_entrenador,
            "nombre_entrenador":     self.nombre_entrenador,
            "fecha":                 self.fecha
        }
