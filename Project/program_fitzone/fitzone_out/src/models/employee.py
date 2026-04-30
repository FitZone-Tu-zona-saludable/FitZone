from src.models.worker import Worker
from src.models.model_accessors import encapsulated_model


@encapsulated_model
class Employee(Worker):
    """Empleado formal del gimnasio con datos laborales y salariales."""

    _fields = (
        "fecha_ingreso",
        "tipo_contrato",
        "estado_laboral",
        "salario",
        "descuento",
    )

    ESTADO_ACTIVO = "activo"
    ESTADO_INACTIVO = "inactivo"
    ESTADO_INCAPACITADO = "incapacitado"

    def __init__(self, id_trabajador, nombre, cargo, telefono, correo,
                 experiencia="", modalidad="presencial", revision_medica=False,
                 datos_laborales=None, documento=""):
        """
        Crea un empleado manteniendo una firma corta para cumplir SonarQube.

        Los datos especificos del contrato y salario se reciben agrupados en
        ``datos_laborales`` para evitar constructores con demasiados parametros.
        """
        super().__init__(id_trabajador, nombre, cargo, telefono, correo,
                         experiencia, modalidad, revision_medica, documento)
        datos_laborales = datos_laborales or {}
        self.fecha_ingreso = datos_laborales.get("fecha_ingreso", "")
        self.tipo_contrato = datos_laborales.get("tipo_contrato", "indefinido")
        self.estado_laboral = datos_laborales.get("estado_laboral", self.ESTADO_ACTIVO)
        self.salario = float(datos_laborales.get("salario", 0.0))
        self.descuento = float(datos_laborales.get("descuento", 0.0))

    @property
    def salario_neto(self):
        """Salario descontando el porcentaje de descuento."""
        return round(self.salario * (1 - self.descuento / 100), 2)

    def actualizar_estado(self, estado):
        estados_validos = [
            self.ESTADO_ACTIVO,
            self.ESTADO_INACTIVO,
            self.ESTADO_INCAPACITADO,
        ]
        if estado in estados_validos:
            self.estado_laboral = estado
            return True
        return False

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "fecha_ingreso": self.fecha_ingreso,
            "tipo_contrato": self.tipo_contrato,
            "estado_laboral": self.estado_laboral,
            "salario": self.salario,
            "descuento": self.descuento,
        })
        return base
