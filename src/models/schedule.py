from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Schedule:
    _fields = ('id_horario', 'fecha', 'hora_inicio', 'hora_fin', 'tipo', 'cupos', 'id_entrenador')

    def __init__(self, id_horario, fecha, hora_inicio, hora_fin,
                 tipo, cupos, id_entrenador=None):
        self.id_horario = id_horario
        self.fecha = fecha           # "YYYY-MM-DD"
        self.hora_inicio = hora_inicio   # "HH:MM"
        self.hora_fin = hora_fin         # "HH:MM"
        self.tipo = tipo             # "yoga", "cardio", "fuerza", etc.
        self.cupos = cupos
        self.id_entrenador = id_entrenador

    def to_dict(self):
        return {
            "id_horario": self.id_horario,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "tipo": self.tipo,
            "cupos": self.cupos,
            "id_entrenador": self.id_entrenador
        }
