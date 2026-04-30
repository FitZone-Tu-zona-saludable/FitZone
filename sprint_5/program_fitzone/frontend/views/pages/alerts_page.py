from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from frontend.controllers.payment_controller import PaymentController
from frontend.controllers.security_controller import SecurityController
from frontend.services.state_service import state
from frontend.views.components.alerts import AlertBanner
from frontend.views.components.widgets import Card, PageHeader


class AlertsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.payment_controller = PaymentController()
        self.security_controller = SecurityController()
        self._build_ui()
        self.reload()

    def _build_ui(self):
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(24, 24, 24, 24)
        self.root.setSpacing(16)

        self.root.addWidget(PageHeader(
            "Alertas del sistema",
            "Resumen contextual de pagos, membresías y eventos de seguridad.",
        ))

        self.summary_card = Card()
        self.summary_text = QLabel()
        self.summary_text.setObjectName("Muted")
        self.summary_card.layout.addWidget(self.summary_text)
        self.root.addWidget(self.summary_card)

        self.alerts_slot = QVBoxLayout()
        self.root.addLayout(self.alerts_slot)

    def _clear_alerts(self):
        while self.alerts_slot.count():
            item = self.alerts_slot.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def reload(self):
        self._clear_alerts()
        user = state.get("user") or {}
        membership = user.get("membership") or {}
        payments = user.get("payments", [])
        role = user.get("role", "")

        alerts = []

        membership_state = membership.get("estado")
        if membership_state == "pendiente_pago":
            alerts.append(AlertBanner(
                "Tienes una membresía seleccionada, pero aún falta registrar el pago.",
                kind="warning",
            ))
        elif membership_state == "pendiente_verificacion":
            alerts.append(AlertBanner(
                "Tu pago ya fue registrado y está pendiente de verificación administrativa.",
                kind="info",
            ))
        elif membership_state == "por_vencer":
            alerts.append(AlertBanner(
                "Tu membresía está por vencer. Considera renovarla pronto.",
                kind="warning",
            ))
        elif membership_state == "vencida":
            alerts.append(AlertBanner(
                "Tu membresía venció. Debes seleccionar un nuevo plan y registrar pago.",
                kind="danger",
            ))

        if payments:
            last_payment = payments[-1]
            if last_payment.get("estado") == "verificado":
                alerts.append(AlertBanner(
                    f"Último pago verificado correctamente. Ref: {last_payment.get('reference', 'N/A')}",
                    kind="success",
                ))

        if role in {"admin", "seguridad"}:
            recent_logs = self.security_controller.load_logs()[-10:]
            failed_logins = [
                log for log in recent_logs
                if "Intento fallido" in log.get("message", "")
            ]
            pending_payments = [
                payment for payment in self.payment_controller.load_payments()
                if payment.get("estado") != "verificado"
            ]

            if failed_logins:
                alerts.append(AlertBanner(
                    f"Se detectaron {len(failed_logins)} intento(s) fallido(s) de acceso recientemente.",
                    kind="danger",
                ))
            if pending_payments:
                alerts.append(AlertBanner(
                    f"Hay {len(pending_payments)} pago(s) pendientes por verificar.",
                    kind="warning",
                ))

        if not alerts:
            alerts.append(AlertBanner(
                "No hay alertas críticas por ahora.",
                kind="success",
                dismissible=False,
            ))

        for alert in alerts:
            self.alerts_slot.addWidget(alert)

        self.summary_text.setText(
            f"Rol actual: {role or 'sin sesión'} · "
            f"Alertas visibles: {len(alerts)}"
        )

    def on_activate(self):
        self.reload()
