from datetime import datetime


class Incident:
    """Incidencia de personal: inasistencias, permisos, causas registradas."""

    TIPO_INASISTENCIA = "inasistencia"
    TIPO_PERMISO = "permiso"
    TIPO_INCAPACIDAD = "incapacidad"
    TIPO_OTRO = "otro"

    def __init__(self, id_incidencia, id_trabajador, nombre_trabajador,
                 tipo, causa, fecha=None, resuelta=False, observaciones=""):
        self.id_incidencia = id_incidencia
        self.id_trabajador = id_trabajador
        self.nombre_trabajador = nombre_trabajador
        self.tipo = tipo          # TIPO_* constantes
        self.causa = causa
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.resuelta = resuelta
        self.observaciones = observaciones

    def resolver(self):
        self.resuelta = True

    def to_dict(self):
        return {
            "id_incidencia": self.id_incidencia,
            "id_trabajador": self.id_trabajador,
            "nombre_trabajador": self.nombre_trabajador,
            "tipo": self.tipo,
            "causa": self.causa,
            "fecha": self.fecha,
            "resuelta": self.resuelta,
            "observaciones": self.observaciones
        }
