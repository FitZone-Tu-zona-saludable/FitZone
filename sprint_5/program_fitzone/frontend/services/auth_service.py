from frontend.services.app_context import user_controller


def login(email, password):
    return user_controller.login_user(email, password)


def register(name, email, password, role='usuario'):
    return user_controller.register_user(name, email, password, role)
