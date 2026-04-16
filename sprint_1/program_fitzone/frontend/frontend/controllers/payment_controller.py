from frontend.frontend.services.api_service import fetch_payments, verify_payment as api_verify, register_payment as api_register
from frontend.frontend.services.state_service import state


def load_payments():
    data = fetch_payments()
    state['payments'] = data
    return data


def verify_payment(payment_id):
    result = api_verify(payment_id)
    if result.get('success'):
        for p in state.get('payments', []):
            if p['id'] == payment_id:
                p['status'] = 'paid'
    return result


def create_payment(amount, method, reference):
    result = api_register({'amount': amount, 'method': method, 'reference': reference})
    return result
