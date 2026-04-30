# incident.py
# Modelo de incidencias del personal (inasistencias, causas)
# Autor: Andrés - Sprint 3

from datetime import datetime


class Incident:
    """Incidencia registrada para un trabajador (inasistencia, llegada tarde, etc.)."""

    TIPOS = ["inasistencia", "llegada_tarde", "permiso", "incapacidad", "otro"]

    def __init__(self, id_incidencia, id_trabajador, nombre_trabajador,
                 tipo="inasistencia", causa="", fecha=None):
        self.id_incidencia = id_incidencia
        self.id_trabajador = id_trabajador
        self.nombre_trabajador = nombre_trabajador
        self.tipo = tipo if tipo in self.TIPOS else "otro"
        self.causa = causa
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id_incidencia": self.id_incidencia,
            "id_trabajador": self.id_trabajador,
            "nombre_trabajador": self.nombre_trabajador,
            "tipo": self.tipo,
            "causa": self.causa,
            "fecha": self.fecha
        }
