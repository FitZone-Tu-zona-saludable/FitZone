import sys
from PySide6.QtWidgets import QApplication
from app.ui.login_view import LoginView

app = QApplication(sys.argv)

window = LoginView()
window.show()

sys.exit(app.exec())
