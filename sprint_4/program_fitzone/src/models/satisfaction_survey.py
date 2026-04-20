from datetime import datetime


class SatisfactionSurvey:
    """Encuesta de satisfacción del cliente sobre entrenadores e instalaciones (Sprint 4 - Andrés)."""

    def __init__(self, id_encuesta, id_cliente, nombre_cliente,
                 calificacion_entrenador, calificacion_instalaciones,
                 sugerencias="", fecha=None):
        self.id_encuesta               = id_encuesta
        self.id_cliente                = id_cliente
        self.nombre_cliente            = nombre_cliente
        # Criterios 1-5
        self.calificacion_entrenador    = int(calificacion_entrenador)
        self.calificacion_instalaciones = int(calificacion_instalaciones)
        self.sugerencias               = sugerencias
        self.fecha                     = fecha or datetime.now().strftime("%Y-%m-%d")

    @property
    def promedio(self):
        return round(
            (self.calificacion_entrenador + self.calificacion_instalaciones) / 2, 2
        )

    def to_dict(self):
        return {
            "id_encuesta":                self.id_encuesta,
            "id_cliente":                 self.id_cliente,
            "nombre_cliente":             self.nombre_cliente,
            "calificacion_entrenador":    self.calificacion_entrenador,
            "calificacion_instalaciones": self.calificacion_instalaciones,
            "sugerencias":                self.sugerencias,
            "fecha":                      self.fecha,
            "promedio":                   self.promedio,
        }
