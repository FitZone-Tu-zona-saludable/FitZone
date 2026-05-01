# auth_controller.py
# Adaptador de autenticación — usa app_context con JSON local

from frontend.services.app_context import user_controller
from frontend.services.state_service import state


def authenticate(email, password):
    """Inicia sesión. Si es exitoso, guarda el usuario en el estado global."""
    result = user_controller.login_user(email, password)
    if isinstance(result, dict) and result.get('success'):
        state['user'] = result.get('data')
    return result


def register_user(name, email, password, role='usuario'):
    """Registra un nuevo usuario."""
    return user_controller.register_user(name, email, password, role)
