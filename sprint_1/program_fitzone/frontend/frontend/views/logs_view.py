from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from frontend.frontend.controllers.access_controller import load_logs


class LogsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        self.refresh()

    def refresh(self):
        logs = load_logs()
        lines = []
        for log in logs:
            lines.append(f"{log['created_at']} | {log['user_email']} | {log['action']} | {log['result']}")
        self.text.setText('\n'.join(lines) if lines else 'Sin registros')
