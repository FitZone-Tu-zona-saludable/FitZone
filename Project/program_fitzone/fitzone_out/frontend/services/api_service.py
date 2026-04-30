from frontend.services.app_context import membership_controller, payment_controller
from frontend.services.state_service import state


def fetch_memberships():
    return membership_controller.list_membership_plans()


def send_membership_selection(data):
    user = state.get('user')
    if not user:
        return {'success': False, 'message': 'No hay usuario autenticado.'}
    return membership_controller.select_membership(user['user_id'], data['id'])


def fetch_user_memberships():
    user = state.get('user')
    if not user:
        return []
    return membership_controller.list_user_memberships(user['user_id'])


def register_payment(payment_data):
    user = state.get('user')
    if not user:
        return {'success': False, 'message': 'No hay usuario autenticado.'}
    return payment_controller.register_payment(
        user['user_id'],
        payment_data['membership_id'],
        payment_data['amount'],
        payment_data['method'],
        payment_data['reference'],
    )


def fetch_payments():
    return payment_controller.list_payments()


def verify_payment(payment_id):
    return payment_controller.verify_payment(payment_id)
