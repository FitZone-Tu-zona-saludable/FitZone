# security_controller.py
# Controlador para manejar la lógica de seguridad en FitZone
# Ahora conectado al servicio real del backend (security_service)
# Documentado línea por línea en español

from src.services.security_service import SecurityService

class SecurityController:
    """
    Controlador para gestionar la bitácora de accesos.
    Contiene métodos para listar registros de seguridad.
    """

    def __init__(self):
        # Inicializa el servicio de seguridad del backend
        self.service = SecurityService()

    def load_logs(self):
        """
        Devuelve la lista completa de registros de seguridad desde el servicio real.
        """
        return self.service.get_access_logs()