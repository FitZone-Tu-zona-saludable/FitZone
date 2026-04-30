from PySide6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from frontend.views.trainer_admin_view import TrainerAdminView
from frontend.views.trainer_select_view import TrainerSelectView


class TrainerPage(QWidget):
    def __init__(self, role="user"):
        super().__init__()
        self.role = role
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.select_view = TrainerSelectView()
        self.tabs.addTab(self.select_view, "Seleccionar")

        if self.role == "admin":
            self.admin_view = TrainerAdminView()
            self.tabs.addTab(self.admin_view, "Administrar")
        else:
            info = QLabel("Aquí puedes comparar entrenadores y escoger uno para tu membresía.")
            info.setObjectName("Muted")
            layout.addWidget(info)

        layout.addWidget(self.tabs)

    def on_activate(self):
        for view in (self.select_view, getattr(self, "admin_view", None)):
            if view and hasattr(view, "on_activate"):
                view.on_activate()
