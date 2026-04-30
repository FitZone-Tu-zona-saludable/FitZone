from datetime import datetime


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Attendance:
    _fields = ('id_asistencia', 'id_cliente', 'nombre_cliente', 'fecha', 'clase', 'servicio', 'observaciones')

    """Registro de asistencia de clientes (Sprint 3 - Andrés)."""

    def __init__(self, id_asistencia, id_cliente, nombre_cliente,
                 fecha=None, clase="", servicio="", observaciones=""):
        self.id_asistencia  = id_asistencia
        self.id_cliente     = id_cliente
        self.nombre_cliente = nombre_cliente
        self.fecha          = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clase          = clase
        self.servicio       = servicio
        self.observaciones  = observaciones

    @property
    def hora(self):
        """Compatibilidad con código que lea .hora"""
        if " " in self.fecha:
            return self.fecha.split(" ")[1]
        return ""

    @property
    def clase_servicio(self):
        """Alias para compatibilidad con sprint4 tests."""
        return self.clase or self.servicio

    def to_dict(self):
        return {
            "id_asistencia":  self.id_asistencia,
            "id_cliente":     self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "fecha":          self.fecha,
            "clase":          self.clase,
            "servicio":       self.servicio,
            "observaciones":  self.observaciones,
        }
