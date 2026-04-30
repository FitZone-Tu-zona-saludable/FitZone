from datetime import datetime


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class SatisfactionSurvey:
    _fields = ('id_encuesta', 'id_cliente', 'nombre_cliente', 'puntaje_entrenador', 'puntaje_instalaciones', 'comentario', 'id_entrenador', 'nombre_entrenador', 'fecha')

    """Encuesta de satisfacción (Sprint 4 - Andrés).
    Campos: puntaje_entrenador / puntaje_instalaciones (frontend).
    Aliases: calificacion_entrenador / calificacion_instalaciones (tests sprint4).
    """

    def __init__(self, id_encuesta, id_cliente, nombre_cliente,
                 puntaje_entrenador=0, puntaje_instalaciones=0,
                 comentario="", id_entrenador=None, nombre_entrenador="",
                 fecha=None):
        self.id_encuesta           = id_encuesta
        self.id_cliente            = id_cliente
        self.nombre_cliente        = nombre_cliente
        self.puntaje_entrenador    = int(puntaje_entrenador)
        self.puntaje_instalaciones = int(puntaje_instalaciones)
        self.comentario            = comentario
        self.id_entrenador         = id_entrenador
        self.nombre_entrenador     = nombre_entrenador
        self.fecha                 = fecha or datetime.now().strftime("%Y-%m-%d")

    # Aliases para tests sprint4
    @property
    def calificacion_entrenador(self):
        return self.puntaje_entrenador

    @property
    def calificacion_instalaciones(self):
        return self.puntaje_instalaciones

    @property
    def sugerencias(self):
        return self.comentario

    @property
    def promedio(self):
        return round((self.puntaje_entrenador + self.puntaje_instalaciones) / 2, 2)

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
            "fecha":                 self.fecha,
        }
