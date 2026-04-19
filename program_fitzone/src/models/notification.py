from datetime import datetime


class Notification:
    PAGO_CONFIRMADO = "pago_confirmado"
    MEMBRESIA_POR_VENCER = "membresia_por_vencer"
    MEMBRESIA_VENCIDA = "membresia_vencida"

    def __init__(self, tipo, mensaje, destinatario=""):
        self.tipo = tipo
        self.mensaje = mensaje
        self.destinatario = destinatario
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def crear_pago_confirmado(nombre, valor, metodo):
        mensaje = (
            f"Hola {nombre}, tu pago de ${valor} "
            f"por {metodo} ha sido confirmado. ¡Gracias!"
        )
        return Notification(Notification.PAGO_CONFIRMADO, mensaje, nombre)

    @staticmethod
    def crear_vencimiento_proximo(nombre, dias_restantes):
        mensaje = (
            f"Hola {nombre}, tu membresía vence en {dias_restantes} día(s). "
            f"Renueva a tiempo para no perder el acceso."
        )
        return Notification(Notification.MEMBRESIA_POR_VENCER, mensaje, nombre)

    @staticmethod
    def crear_membresia_vencida(nombre):
        mensaje = (
            f"Hola {nombre}, tu membresía ha vencido. "
            f"Comunícate con recepción para renovarla."
        )
        return Notification(Notification.MEMBRESIA_VENCIDA, mensaje, nombre)

    def enviar_cliente(self):
        return f"[{self.tipo.upper()}] → {self.destinatario}: {self.mensaje}"

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "mensaje": self.mensaje,
            "destinatario": self.destinatario,
            "fecha": self.fecha
        }
