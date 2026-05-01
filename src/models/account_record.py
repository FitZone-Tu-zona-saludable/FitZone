from datetime import datetime


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class AccountRecord:
    _fields = ('id_registro', 'id_cliente', 'nombre_cliente', 'concepto', 'monto', 'estado', 'fecha', 'fecha_vencimiento')

    """Registro contable del gimnasio: pagos recibidos, saldos y cobros pendientes."""

    ESTADO_PAGADO = "pagado"
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_VENCIDO = "vencido"

    def __init__(self, id_registro, id_cliente, nombre_cliente,
                 concepto, monto, estado=None, fecha=None, fecha_vencimiento=None):
        self.id_registro = id_registro
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.concepto = concepto                # "mensualidad", "inscripción", "clase extra"
        self.monto = float(monto)
        self.estado = estado or self.ESTADO_PENDIENTE
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.fecha_vencimiento = fecha_vencimiento or ""

    def marcar_pagado(self):
        self.estado = self.ESTADO_PAGADO

    def marcar_vencido(self):
        self.estado = self.ESTADO_VENCIDO

    def to_dict(self):
        return {
            "id_registro": self.id_registro,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "concepto": self.concepto,
            "monto": self.monto,
            "estado": self.estado,
            "fecha": self.fecha,
            "fecha_vencimiento": self.fecha_vencimiento
        }
