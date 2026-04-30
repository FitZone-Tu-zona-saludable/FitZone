from src.models.worker import Worker


class Trainer(Worker):
    def __init__(self, id_trabajador, nombre, cargo, telefono, correo,
                 especialidad="", experiencia="", modalidad="presencial", revision_medica=False):
        super().__init__(id_trabajador, nombre, cargo, telefono, correo,
                         experiencia, modalidad, revision_medica)
        self.especialidad = especialidad
        self.horarios = []       # lista de ids de Schedule asignados
        self.disponible = True

    def asignar_horario(self, id_horario):
        if self.disponible:
            self.horarios.append(id_horario)
            return True
        return False

    def liberar(self):
        self.disponible = True

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "especialidad": self.especialidad,
            "horarios": self.horarios,
            "disponible": self.disponible
        })
        return base
