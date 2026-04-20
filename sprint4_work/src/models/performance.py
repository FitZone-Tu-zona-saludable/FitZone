# performance.py
# Modelo para la evaluación de desempeño de usuarios
# Autor: Andrés - Sprint 3

from datetime import datetime


class Performance:
    """Evaluación de desempeño de un cliente realizada por un entrenador."""

    def __init__(self, id_eval, id_cliente, nombre_cliente,
                 id_entrenador, nombre_entrenador,
                 puntaje=0, observaciones="", fecha=None):
        self.id_eval = id_eval
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.id_entrenador = id_entrenador
        self.nombre_entrenador = nombre_entrenador
        self.puntaje = puntaje              # 1-10
        self.observaciones = observaciones
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id_eval": self.id_eval,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "id_entrenador": self.id_entrenador,
            "nombre_entrenador": self.nombre_entrenador,
            "puntaje": self.puntaje,
            "observaciones": self.observaciones,
            "fecha": self.fecha
        }
