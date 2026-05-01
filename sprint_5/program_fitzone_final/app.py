# app.py — Punto de entrada principal de FitZone
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox
from frontend.resources.theme import apply_theme
from frontend.views.login_view import LoginView


def _global_exception_handler(exc_type, exc_value, exc_tb):
    """Captura excepciones no manejadas y muestra diálogo en lugar de crashear."""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f"[ERROR CRÍTICO]\n{error_msg}", file=sys.stderr)
    try:
        QMessageBox.critical(
            None,
            "Error inesperado — FitZone",
            f"Ocurrió un error inesperado.\n\n{exc_value}\n\n"
            "Por favor contacte soporte técnico.",
        )
    except Exception:
        pass


def main():
    sys.excepthook = _global_exception_handler

    app = QApplication(sys.argv)
    app.setApplicationName("FitZone")
    apply_theme(app)

    window = LoginView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
