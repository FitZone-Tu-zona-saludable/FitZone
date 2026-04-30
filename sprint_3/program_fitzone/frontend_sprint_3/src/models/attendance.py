# attendance.py
# Modelo de asistencia de clientes al gimnasio
# Autor: Andrés - Sprint 3

from datetime import datetime


class Attendance:
    """Registro de asistencia de un cliente a una sesión/clase."""

    def __init__(self, id_asistencia, id_cliente, nombre_cliente,
                 fecha=None, clase="", servicio=""):
        self.id_asistencia = id_asistencia
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clase = clase          # nombre de la clase o sesión
        self.servicio = servicio    # servicio adicional tomado

    def to_dict(self):
        return {
            "id_asistencia": self.id_asistencia,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "fecha": self.fecha,
            "clase": self.clase,
            "servicio": self.servicio
        }
