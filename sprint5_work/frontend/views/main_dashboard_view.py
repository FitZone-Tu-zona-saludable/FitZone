# main_dashboard_view.py
# Dashboard principal de FitZone — Sprint 5 (cierre visual)
# Sprint 5 - Alex: Pulir pantallas finales para que el sistema sea consistente y fácil de usar

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from frontend.services.state_service import state
from frontend.resources.theme import COLORS


class MainDashboardView(QWidget):
    """
    Dashboard de inicio pulido para el Sprint 5.
    Muestra un resumen visual de estado del sistema y accesos rápidos.
    """

    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate = navigate_callback
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # ── Cabecera de bienvenida ────────────────────────────────────
        user = state.get("user", {})
        nombre = user.get("name", "Usuario") if user else "Usuario"
        rol    = user.get("role", "").capitalize() if user else ""

        header = QHBoxLayout()
        greet = QLabel(f"Bienvenido, {nombre}")
        greet.setObjectName("H1")
        role_lbl = QLabel(f"  · {rol}")
        role_lbl.setObjectName("Muted")
        role_lbl.setAlignment(Qt.AlignBottom)
        header.addWidget(greet)
        header.addWidget(role_lbl)
        header.addStretch()
        layout.addLayout(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(sep)

        # ── Título accesos rápidos ────────────────────────────────────
        lbl_quick = QLabel("Accesos rápidos")
        lbl_quick.setObjectName("H2")
        layout.addWidget(lbl_quick)

        # ── Grid de tarjetas de módulo ────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(16)

        modules = [
            ("📋", "Asistencia",        "attendance",    COLORS["primary"]),
            ("🗓", "Horarios",           "schedule",      COLORS["info"]),
            ("💰", "Contabilidad",       "accounting",    COLORS["warning"]),
            ("👔", "Empleados",          "employees",     COLORS["text_muted"]),
            ("⚠️", "Incidencias",        "incidents",     COLORS["danger"]),
            ("⭐", "Evaluación",         "performance",   COLORS["primary"]),
            ("🔔", "Notificaciones",     "notifications", COLORS["success"]),
            ("📊", "Reportes",           "reports",       COLORS["primary"]),
            ("💼", "Pago Empleados",     "payments",      COLORS["warning"]),
            ("📝", "Encuestas",          "survey",        COLORS["info"]),
        ]

        for idx, (icon, label, key, color) in enumerate(modules):
            card = self._module_card(icon, label, key, color)
            grid.addWidget(card, idx // 4, idx % 4)

        layout.addLayout(grid)
        layout.addStretch()

        # ── Footer ───────────────────────────────────────────────────
        footer = QLabel("FitZone v1.0 · Sprint 5 · Python + PySide6 + MVC")
        footer.setObjectName("Muted")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def _module_card(self, icon, label, key, color):
        """Crea una tarjeta de módulo clicable."""
        frame = QFrame()
        frame.setObjectName("Card")
        frame.setCursor(Qt.PointingHandCursor)
        frame.setFixedHeight(110)

        v = QVBoxLayout(frame)
        v.setAlignment(Qt.AlignCenter)

        ico_lbl = QLabel(icon)
        ico_lbl.setFont(QFont("Segoe UI", 24))
        ico_lbl.setAlignment(Qt.AlignCenter)

        txt_lbl = QLabel(label)
        txt_lbl.setAlignment(Qt.AlignCenter)
        txt_lbl.setStyleSheet(f"color: {color}; font-weight: 600;")

        v.addWidget(ico_lbl)
        v.addWidget(txt_lbl)

        # Hover style
        frame.setStyleSheet(f"""
            QFrame#Card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QFrame#Card:hover {{
                border: 1px solid {color};
                background-color: {COLORS['surface_hi']};
            }}
        """)

        if self.navigate:
            frame.mousePressEvent = lambda e, k=key: self.navigate(k)

        return frame
