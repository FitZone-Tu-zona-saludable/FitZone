from frontend.frontend.services.app_context import user_controller, access_controller


def login(email, password):
    result = user_controller.authenticate_user(email, password)
    access_controller.log_access(email, 'login', 'success' if result.get('success') else 'failed')
    if result.get('success'):
        user = result['user']
        return {
            'success': True,
            'data': {
                'id': user['user_id'],
                'username': user['user_name'],
                'email': user['user_email'],
                'role': user['user_role'],
            },
            'role': user['user_role'],
            'message': result['message'],
        }
    return {'success': False, 'data': None, 'message': result['message']}


def register(name, email, password, role='client'):
    result = user_controller.register_user(name, email, password, role)
    return result
