from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Membership:
    _fields = ('id_membresia', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado')

    def __init__(self, id_membresia, tipo, fecha_inicio, fecha_fin):
        self.id_membresia = id_membresia
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = "activa"

    def actualizar_estado(self, estado):
        self.estado = estado
