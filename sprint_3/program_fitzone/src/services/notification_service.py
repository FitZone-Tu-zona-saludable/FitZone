import json
import os
from datetime import datetime, timedelta
from src.models.notification import Notification


# Número de días antes del vencimiento para alertar
DIAS_ALERTA_VENCIMIENTO = 5


class NotificationService:
    """Genera y registra notificaciones de pago y membresía (clientes y trabajadores)."""

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
            json.dump(self.notifications, f, indent=4, ensure_ascii=False)

    # ─── NOTIFICACIONES CLIENTE ──────────────────────────────────────
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

    # ─── NOTIFICACIONES TRABAJADOR (Sprint 3 - Andrés) ───────────────
    def notificar_pago_trabajador(self, nombre_trabajador, periodo, monto):
        """Notifica al trabajador cuando se registra su pago de nómina."""
        n = Notification.crear_pago_trabajador(nombre_trabajador, periodo, monto)
        self.notifications.append(n.to_dict())
        self.save_notifications()
        return n.enviar_trabajador()

    def notificar_vencimiento_a_trabajador(self, nombre_trabajador, nombre_cliente, dias):
        """Alerta a un trabajador sobre la membresía próxima a vencer de un cliente."""
        n = Notification.crear_aviso_vencimiento_membresia(
            nombre_trabajador, nombre_cliente, dias
        )
        self.notifications.append(n.to_dict())
        self.save_notifications()
        return n.enviar_trabajador()

    def verificar_vencimientos_para_trabajadores(self, users, trabajadores):
        """
        Para cada membresía próxima a vencer, notifica a todos los trabajadores
        activos (recepcionistas/entrenadores) para que puedan hacer seguimiento.
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
            if 0 <= delta <= DIAS_ALERTA_VENCIMIENTO:
                for trabajador in trabajadores:
                    msg = self.notificar_vencimiento_a_trabajador(
                        trabajador.nombre, u.get_name(), delta
                    )
                    mensajes.append(msg)

        return mensajes

    def get_notifications(self):
        return self.notifications

    def get_notifications_trabajador(self):
        return [n for n in self.notifications if n.get("destinatario_tipo") == "trabajador"]

    def get_notifications_cliente(self):
        return [n for n in self.notifications
                if n.get("destinatario_tipo", "cliente") == "cliente"]

