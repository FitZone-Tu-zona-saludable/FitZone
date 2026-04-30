from src.models.model_accessors import encapsulated_model


@encapsulated_model
class Schedule:
    _fields = (
        'id_horario', 'fecha', 'hora_inicio', 'hora_fin',
        'tipo', 'cupos', 'id_entrenador', 'enrolled_users',
    )

    def __init__(self, id_horario, fecha, hora_inicio, hora_fin,
                 tipo, cupos, id_entrenador=None, enrolled_users=None):
        self.id_horario = id_horario
        self.fecha = fecha              # "YYYY-MM-DD"
        self.hora_inicio = hora_inicio  # "HH:MM"
        self.hora_fin = hora_fin        # "HH:MM"
        self.tipo = tipo                # "Yoga", "Cardio", "Fuerza", etc.
        self.cupos = cupos              # cupos TOTALES del horario
        self.id_entrenador = id_entrenador
        # Lista de IDs (str) de usuarios inscritos
        self.enrolled_users = list(enrolled_users) if enrolled_users else []

    # ── Propiedades de disponibilidad ────────────────────────────────────────
    @property
    def cupos_disponibles(self):
        """Cupos que aún quedan libres."""
        return max(0, self.cupos - len(self.enrolled_users))

    @property
    def esta_lleno(self):
        """True si no quedan cupos."""
        return len(self.enrolled_users) >= self.cupos

    def is_enrolled(self, user_id):
        """Indica si user_id ya está inscrito."""
        return str(user_id) in [str(u) for u in self.enrolled_users]

    def to_dict(self):
        return {
            "id_horario": self.id_horario,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "tipo": self.tipo,
            "cupos": self.cupos,
            "id_entrenador": self.id_entrenador,
            "enrolled_users": self.enrolled_users,  # persiste en JSON
        }
