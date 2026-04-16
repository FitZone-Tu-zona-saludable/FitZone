from frontend.frontend.services.app_context import access_controller


def load_logs():
    return access_controller.list_logs()['data']
