# membership_controller.py
# Controlador para manejar la lógica de membresías en FitZone
# Ahora conectado al servicio real del backend (membership_service)
# Documentado línea por línea en español

from src.services.membership_service import MembershipService

class MembershipController:
    """
    Controlador para gestionar membresías.
    Contiene métodos para listar, seleccionar y consultar membresías de usuario.
    """

    def __init__(self):
        # Inicializa el servicio de membresías del backend
        self.service = MembershipService()

    def load_memberships(self):
        """
        Devuelve la lista completa de membresías disponibles desde el servicio real.
        """
        return self.service.list_memberships()

    def load_user_memberships(self, user_id):
        """
        Devuelve las membresías activas de un usuario específico.
        """
        return self.service.get_user_memberships(user_id)

    def select_membership(self, user_id, membership_id):
        """
        Registra la selección de una membresía para un usuario.
        """
        result = self.service.select_membership(user_id, membership_id)
        return result