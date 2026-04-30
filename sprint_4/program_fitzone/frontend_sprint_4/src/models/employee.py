from src.models.worker import Worker


class Employee(Worker):
    """Empleado formal del gimnasio (contrato, datos laborales)."""

    def __init__(self, id_trabajador, nombre, cargo, telefono, correo,
                 experiencia="", modalidad="presencial", revision_medica=False,
                 fecha_ingreso="", tipo_contrato="indefinido"):
        super().__init__(id_trabajador, nombre, cargo, telefono, correo,
                         experiencia, modalidad, revision_medica)
        self.fecha_ingreso = fecha_ingreso
        self.tipo_contrato = tipo_contrato

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "fecha_ingreso": self.fecha_ingreso,
            "tipo_contrato": self.tipo_contrato
        })
        return base
