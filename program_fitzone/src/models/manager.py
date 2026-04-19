from src.models.worker import Worker


class Manager(Worker):
    def __init__(self, id_trabajador, nombre, telefono, correo):
        super().__init__(id_trabajador, nombre, "Gerente", telefono, correo)

    def generar_reporte(self):
        return "Reporte generado"
