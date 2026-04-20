from src.models.worker import Worker


class Employee(Worker):
    """Empleado formal del gimnasio (contrato, datos laborales)."""

    ESTADO_ACTIVO = "activo"
    ESTADO_INACTIVO = "inactivo"
    ESTADO_INCAPACITADO = "incapacitado"

    def __init__(self, id_trabajador, nombre, cargo, telefono, correo,
                 experiencia="", modalidad="presencial", revision_medica=False,
                 fecha_ingreso="", tipo_contrato="indefinido",
                 estado_laboral="activo", salario=0.0, descuento=0.0):
        super().__init__(id_trabajador, nombre, cargo, telefono, correo,
                         experiencia, modalidad, revision_medica)
        self.fecha_ingreso = fecha_ingreso
        self.tipo_contrato = tipo_contrato
        # Sprint 3 - Andrés: estado laboral, información salarial y descuentos
        self.estado_laboral = estado_laboral   # activo / inactivo / incapacitado
        self.salario = float(salario)
        self.descuento = float(descuento)      # porcentaje de descuento (0-100)

    @property
    def salario_neto(self):
        """Salario descontando el porcentaje de descuento."""
        return round(self.salario * (1 - self.descuento / 100), 2)

    def actualizar_estado(self, estado):
        estados_validos = [self.ESTADO_ACTIVO, self.ESTADO_INACTIVO, self.ESTADO_INCAPACITADO]
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
            "descuento": self.descuento
        })
        return base
