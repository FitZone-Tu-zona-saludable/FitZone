from PySide6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from frontend.views.schedule_admin_view import ScheduleAdminView
from frontend.views.schedule_consult_view import ScheduleConsultView
from frontend.views.schedule_reassign_view import ScheduleReassignView


class SchedulePage(QWidget):
    def __init__(self, role="user"):
        super().__init__()
        self.role = role
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.consult_view = ScheduleConsultView()
        self.tabs.addTab(self.consult_view, "Consultar")

        if self.role == "admin":
            self.admin_view = ScheduleAdminView()
            self.reassign_view = ScheduleReassignView()
            self.tabs.addTab(self.admin_view, "Administrar")
            self.tabs.addTab(self.reassign_view, "Reasignar")
        else:
            info = QLabel("Como cliente solo puedes consultar horarios disponibles.")
            info.setObjectName("Muted")
            layout.addWidget(info)

        layout.addWidget(self.tabs)

    def on_activate(self):
        for view in (self.consult_view, getattr(self, "admin_view", None), getattr(self, "reassign_view", None)):
            if view and hasattr(view, "on_activate"):
                view.on_activate()
