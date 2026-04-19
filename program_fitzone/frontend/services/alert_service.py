# alert_service.py
# Servicio centralizado para manejar alertas en FitZone
# Documentado línea por línea en español

from PySide6.QtWidgets import QMessageBox


class AlertService:
    """
    Servicio para mostrar alertas en la aplicación.
    Centraliza los mensajes de información, advertencia y error.
    """

    @staticmethod
    def info(parent, title, message):
        """
        Muestra un mensaje informativo.
        """
        QMessageBox.information(parent, title, message)

    @staticmethod
    def warning(parent, title, message):
        """
        Muestra un mensaje de advertencia.
        """
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def error(parent, title, message):
        """
        Muestra un mensaje de error.
        """
        QMessageBox.critical(parent, title, message)