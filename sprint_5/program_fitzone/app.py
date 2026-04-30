# app.py — Punto de entrada principal de FitZone (sistema completo)
import sys
from PySide6.QtWidgets import QApplication
from frontend.resources.theme import apply_theme
from frontend.views.login_view import LoginView


def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    window = LoginView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
