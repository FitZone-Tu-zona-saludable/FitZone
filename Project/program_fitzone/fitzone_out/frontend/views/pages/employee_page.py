from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from frontend.views.staff_register_view import StaffRegisterView


class EmployeePage(QWidget):
    def __init__(self, role="admin"):
        super().__init__()
        self.role = role
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        if self.role != "admin":
            message = QLabel("Este módulo es exclusivo de administración.")
            message.setObjectName("Muted")
            layout.addWidget(message)
            return

        self.staff_view = StaffRegisterView()
        layout.addWidget(self.staff_view)

    def on_activate(self):
        staff_view = getattr(self, "staff_view", None)
        if staff_view and hasattr(staff_view, "on_activate"):
            staff_view.on_activate()
