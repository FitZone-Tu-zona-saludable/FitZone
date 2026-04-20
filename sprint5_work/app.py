# app.py — Punto de entrada principal de FitZone (Sprint 5 - sistema completo)
# Integra: Andrés (backend), Romel (seguridad/pruebas), Alex (frontend/vistas)

import sys
from PySide6.QtWidgets import QApplication
from frontend.resources.theme import apply_theme
from frontend.views.login_view import LoginView


def main():
    app = QApplication(sys.argv)
    apply_theme(app)           # Tema visual consistente Sprint 5
    window = LoginView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
