from datetime import datetime


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class UserEvaluation:
    _fields = ('id_evaluacion', 'id_entrenador', 'nombre_entrenador', 'id_cliente', 'nombre_cliente', 'puntualidad', 'rendimiento', 'actitud', 'comentarios', 'fecha')

    """Evaluación de desempeño de un usuario/cliente realizada por un entrenador."""

    def __init__(self, id_evaluacion, id_entrenador, nombre_entrenador,
                 id_cliente, nombre_cliente,
                 puntualidad=0, rendimiento=0, actitud=0,
                 comentarios="", fecha=None):
        self.id_evaluacion = id_evaluacion
        self.id_entrenador = id_entrenador
        self.nombre_entrenador = nombre_entrenador
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente

        # Criterios (0-10)
        self.puntualidad = puntualidad
        self.rendimiento = rendimiento
        self.actitud = actitud
        self.comentarios = comentarios
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    @property
    def promedio(self):
        criterios = [self.puntualidad, self.rendimiento, self.actitud]
        return round(sum(criterios) / len(criterios), 2)

    def to_dict(self):
        return {
            "id_evaluacion": self.id_evaluacion,
            "id_entrenador": self.id_entrenador,
            "nombre_entrenador": self.nombre_entrenador,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "puntualidad": self.puntualidad,
            "rendimiento": self.rendimiento,
            "actitud": self.actitud,
            "comentarios": self.comentarios,
            "fecha": self.fecha,
            "promedio": self.promedio
        }
