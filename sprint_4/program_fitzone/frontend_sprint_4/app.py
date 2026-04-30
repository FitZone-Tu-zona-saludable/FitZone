# app.py — Punto de entrada principal de FitZone
# Integra: Alex (frontend/views), Romel (data/JSON), tercer compañero (src/)

import sys
from PySide6.QtWidgets import QApplication
from frontend.views.login_view import LoginView


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QLineEdit {
            color: black;
            background-color: white;
            padding: 6px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
        }
    """)
    window = LoginView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
