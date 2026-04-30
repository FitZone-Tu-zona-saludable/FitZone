import json
import os
from datetime import datetime, timedelta
from src.models.notification import Notification


# Número de días antes del vencimiento para alertar
DIAS_ALERTA_VENCIMIENTO = 5


class NotificationService:
    """Genera y registra notificaciones de pago y membresía."""

    def __init__(self):
        self.notifications = []
        self.notif_file = "data/notifications.json"
        self.load_notifications()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load_notifications(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.notif_file):
            with open(self.notif_file, "r") as f:
                self.notifications = json.load(f)

    def save_notifications(self):
        os.makedirs("data", exist_ok=True)
        with open(self.notif_file, "w") as f:
            json.dump(self.notifications, f, indent=4)

    # ─── REGLAS DE NEGOCIO ───────────────────────────────────────────
    def notificar_pago(self, nombre, valor, metodo):
        """Regla: se notifica cada vez que un pago es confirmado."""
        n = Notification.crear_pago_confirmado(nombre, valor, metodo)
        self.notifications.append(n.to_dict())
        self.save_notifications()
        return n.enviar_cliente()

    def verificar_vencimiento(self, users):
        """
        Regla: si la membresía vence en <= DIAS_ALERTA días, notificar.
        Si ya venció, notificar vencimiento.
        Devuelve lista de mensajes generados.
        """
        mensajes = []
        today = datetime.now()

        for u in users:
            if not u.membership:
                continue

            try:
                fecha_fin = datetime.strptime(u.membership["fechaFin"], "%Y-%m-%d")
            except (KeyError, ValueError):
                continue

            delta = (fecha_fin - today).days

            if delta < 0:
                n = Notification.crear_membresia_vencida(u.get_name())
                self.notifications.append(n.to_dict())
                mensajes.append(n.enviar_cliente())
            elif delta <= DIAS_ALERTA_VENCIMIENTO:
                n = Notification.crear_vencimiento_proximo(u.get_name(), delta)
                self.notifications.append(n.to_dict())
                mensajes.append(n.enviar_cliente())

        if mensajes:
            self.save_notifications()

        return mensajes

    def get_notifications(self):
        return self.notifications
