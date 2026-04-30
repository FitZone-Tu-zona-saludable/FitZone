from datetime import datetime


class Payment:
    def __init__(self, id_pago, id_cliente, valor, metodo, fecha=None):
        self.id_pago = id_pago
        self.id_cliente = id_cliente
        self.valor = valor
        self.metodo = metodo          # "efectivo", "tarjeta", "transferencia"
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "id_cliente": self.id_cliente,
            "valor": self.valor,
            "metodo": self.metodo,
            "fecha": self.fecha
        }
