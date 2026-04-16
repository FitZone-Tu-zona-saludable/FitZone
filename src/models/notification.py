class Notification:
    def __init__(self, tipo, mensaje):
        self.tipo = tipo
        self.mensaje = mensaje

    def enviar_cliente(self):
        return f"Notificación enviada: {self.mensaje}"
