# worker_notifications_view.py
# Vista de notificaciones dirigidas al trabajador
# Sprint 3 - Alex (RF5: Notificar pago a trabajador / RF8: Notificar vencimiento membresía a trabajador)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from frontend.resources.theme import COLORS
from src.services.notification_service import NotificationService
from src.services.auth_service import AuthService


class WorkerNotificationsView(QWidget):
    """Centro de notificaciones para trabajadores: pagos y vencimientos de membresía."""

    def __init__(self):
        super().__init__()
        self.notif_service = NotificationService()
        self.auth_service  = AuthService()
        self._build_ui()
        self._load_notifications()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("🔔  Centro de Notificaciones — Trabajador")
        title.setObjectName("H1")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Notificaciones de pago confirmado y alertas de vencimiento de membresía.")
        sub.setObjectName("Muted")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # ── Acciones rápidas ─────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_check = QPushButton("🔍  Verificar vencimientos")
        btn_check.setObjectName("Primary")
        btn_check.clicked.connect(self._check_expiry)
        btn_refresh = QPushButton("🔄  Actualizar")
        btn_refresh.clicked.connect(self._load_notifications)
        btn_row.addWidget(btn_check)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # ── Área de scroll para las notificaciones ───────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.notif_layout = QVBoxLayout(self.container)
        self.notif_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def _load_notifications(self):
        # Limpiar layout
        while self.notif_layout.count():
            item = self.notif_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        notifications = self.notif_service.get_notifications()
        if not notifications:
            lbl = QLabel("No hay notificaciones registradas.")
            lbl.setObjectName("Muted")
            lbl.setAlignment(Qt.AlignCenter)
            self.notif_layout.addWidget(lbl)
            return

        # Mostrar las últimas 20 notificaciones (más recientes primero)
        for n in reversed(notifications[-20:]):
            card = self._make_notif_card(n)
            self.notif_layout.addWidget(card)

    def _make_notif_card(self, notif):
        """Crea una tarjeta visual para una notificación."""
        tipo = notif.get("tipo", "")
        # Determinar color e ícono según tipo
        if tipo == "pago_confirmado":
            color = COLORS["success"]
            icono = "✅"
            obj_name = "AlertSuccess"
        elif tipo == "membresia_por_vencer":
            color = COLORS["warning"]
            icono = "⚠️"
            obj_name = "AlertWarning"
        elif tipo == "membresia_vencida":
            color = COLORS["danger"]
            icono = "❌"
            obj_name = "AlertDanger"
        else:
            color = COLORS["info"]
            icono = "ℹ️"
            obj_name = "Card"

        frame = QFrame()
        frame.setObjectName(obj_name)
        v = QVBoxLayout(frame)
        v.setContentsMargins(14, 10, 14, 10)

        header = QHBoxLayout()
        lbl_tipo = QLabel(f"{icono}  {tipo.upper().replace('_', ' ')}")
        lbl_tipo.setStyleSheet(f"font-weight: bold; color: {color};")
        lbl_fecha = QLabel(notif.get("fecha", ""))
        lbl_fecha.setObjectName("Muted")
        lbl_fecha.setAlignment(Qt.AlignRight)
        header.addWidget(lbl_tipo)
        header.addStretch()
        header.addWidget(lbl_fecha)
        v.addLayout(header)

        lbl_msg = QLabel(notif.get("mensaje", ""))
        lbl_msg.setWordWrap(True)
        v.addWidget(lbl_msg)

        dest = notif.get("destinatario", "")
        if dest:
            lbl_dest = QLabel(f"Para: {dest}")
            lbl_dest.setObjectName("Muted")
            v.addWidget(lbl_dest)

        return frame

    def _check_expiry(self):
        """Verifica vencimientos y genera nuevas notificaciones."""
        users = self.auth_service.get_users()
        mensajes = self.notif_service.verificar_vencimiento(users)
        if mensajes:
            QMessageBox.information(
                self, "Alertas generadas",
                f"Se generaron {len(mensajes)} alerta(s) de vencimiento."
            )
        else:
            QMessageBox.information(
                self, "Sin alertas",
                "No hay membresías próximas a vencer."
            )
        self._load_notifications()
