from datetime import datetime


from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Notification:
    _fields = ('tipo', 'mensaje', 'destinatario', 'destinatario_tipo', 'fecha')

    # ── Tipos existentes (clientes) ──
    PAGO_CONFIRMADO = "pago_confirmado"
    MEMBRESIA_POR_VENCER = "membresia_por_vencer"
    MEMBRESIA_VENCIDA = "membresia_vencida"

    # ── Tipos Sprint 3 (trabajadores) ──
    PAGO_TRABAJADOR = "pago_trabajador"
    VENCIMIENTO_MEMBRESIA_CLIENTE = "vencimiento_membresia_cliente"

    def __init__(self, tipo, mensaje, destinatario="", destinatario_tipo="cliente"):
        self.tipo = tipo
        self.mensaje = mensaje
        self.destinatario = destinatario
        self.destinatario_tipo = destinatario_tipo   # "cliente" o "trabajador"
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Fábricas cliente ──────────────────────────────────────────────
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

    # ── Fábricas trabajador (Sprint 3 - Andrés) ──────────────────────
    @staticmethod
    def crear_pago_trabajador(nombre_trabajador, periodo, monto):
        """Notifica al trabajador que su pago de nómina fue registrado."""
        mensaje = (
            f"Hola {nombre_trabajador}, tu pago de nómina del período {periodo} "
            f"por ${monto} ha sido registrado. Revisa tu cuenta."
        )
        n = Notification(Notification.PAGO_TRABAJADOR, mensaje,
                         nombre_trabajador, "trabajador")
        return n

    @staticmethod
    def crear_aviso_vencimiento_membresia(nombre_trabajador, nombre_cliente, dias):
        """Avisa al trabajador (recepcionista/entrenador) sobre membresía próxima a vencer."""
        mensaje = (
            f"Aviso para {nombre_trabajador}: la membresía del cliente "
            f"{nombre_cliente} vence en {dias} día(s). Considera contactarle."
        )
        n = Notification(Notification.VENCIMIENTO_MEMBRESIA_CLIENTE, mensaje,
                         nombre_trabajador, "trabajador")
        return n

    # ── Envío ─────────────────────────────────────────────────────────
    def enviar_cliente(self):
        return f"[{self.tipo.upper()}] → {self.destinatario}: {self.mensaje}"

    def enviar_trabajador(self):
        return f"[TRABAJADOR][{self.tipo.upper()}] → {self.destinatario}: {self.mensaje}"

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "mensaje": self.mensaje,
            "destinatario": self.destinatario,
            "destinatario_tipo": self.destinatario_tipo,
            "fecha": self.fecha
        }

