from src.models.worker import Worker


class Trainer(Worker):
    def __init__(self, id_trabajador, nombre, telefono, correo, especialidad):
        super().__init__(id_trabajador, nombre, "Entrenador", telefono, correo)
        self.especialidad = especialidad
        self.disponible = True

    def asignar_horario(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
