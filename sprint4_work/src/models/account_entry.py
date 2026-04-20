# account_entry.py
# Modelo de entrada contable (pagos, cobros, saldos)
# Autor: Andrés - Sprint 3

from datetime import datetime


class AccountEntry:
    """Registro contable: pago recibido, cobro pendiente o saldo por pagar."""

    TIPOS = ["ingreso", "cobro_pendiente", "saldo_por_pagar", "descuento"]

    def __init__(self, id_entrada, concepto, tipo, monto, estado="pendiente",
                 referencia="", fecha=None):
        self.id_entrada = id_entrada
        self.concepto = concepto
        self.tipo = tipo if tipo in self.TIPOS else "ingreso"
        self.monto = monto
        self.estado = estado        # "pendiente", "pagado", "cancelado"
        self.referencia = referencia
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id_entrada": self.id_entrada,
            "concepto": self.concepto,
            "tipo": self.tipo,
            "monto": self.monto,
            "estado": self.estado,
            "referencia": self.referencia,
            "fecha": self.fecha
        }
