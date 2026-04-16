from frontend.frontend.services.auth_service import login, register
from frontend.frontend.services.state_service import state


def authenticate(email, password):
    result = login(email, password)
    if isinstance(result, dict) and result.get('success'):
        state['user'] = result.get('data')
    return result


def create_account(name, email, password, role='client'):
    return register(name, email, password, role)
