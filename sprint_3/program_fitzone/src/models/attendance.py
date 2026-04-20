from datetime import datetime


class Attendance:
    """Modelo de asistencia: registra entrada de un cliente a una clase/servicio."""

    def __init__(self, id_asistencia, id_cliente, nombre_cliente,
                 fecha=None, hora=None, clase_servicio="", observaciones=""):
        self.id_asistencia = id_asistencia
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.hora = hora or datetime.now().strftime("%H:%M:%S")
        self.clase_servicio = clase_servicio   # yoga, cardio, fuerza, etc.
        self.observaciones = observaciones

    def to_dict(self):
        return {
            "id_asistencia": self.id_asistencia,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "fecha": self.fecha,
            "hora": self.hora,
            "clase_servicio": self.clase_servicio,
            "observaciones": self.observaciones
        }
