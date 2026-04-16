from frontend.frontend.services.app_context import membership_controller, payment_controller
from frontend.frontend.services.state_service import state


def fetch_memberships():
    return membership_controller.list_catalog()['data']


def fetch_payments():
    return payment_controller.list_payments()['data']


def send_membership_selection(data):
    user = state.get('user')
    if not user:
        return {'success': False, 'message': 'Debe iniciar sesion.'}
    return membership_controller.select_membership(
        user_id=user['id'],
        membership_plan=data['name'],
        membership_price=float(data['price']),
        membership_duration=int(data.get('duration', 30)),
        membership_benefits=data.get('benefits', ''),
    )


def register_payment(payment_data):
    user = state.get('user')
    membership = state.get('selected_membership_db')
    if not user or not membership:
        return {'success': False, 'message': 'No hay usuario o membresia seleccionada.'}
    return payment_controller.register_payment(
        user_id=user['id'],
        membership_id=membership['membership_id'],
        payment_amount=float(payment_data['amount']),
        payment_method=payment_data['method'],
        payment_reference=payment_data['reference'],
    )


def verify_payment(payment_id):
    return payment_controller.verify_payment(payment_id)
