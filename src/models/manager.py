from src.models.worker import Worker


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Manager(Worker):
    _fields = ()

    def __init__(self, id_trabajador, nombre, telefono, correo):
        super().__init__(id_trabajador, nombre, "Gerente", telefono, correo)

    def generar_reporte(self):
        return "Reporte generado"
