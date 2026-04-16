from frontend.frontend.services.api_service import fetch_memberships, send_membership_selection
from frontend.frontend.services.app_context import membership_controller as backend_membership_controller
from frontend.frontend.services.state_service import state


def load_memberships():
    data = fetch_memberships()
    state['memberships'] = data
    return data


def select_membership(membership):
    result = send_membership_selection(membership)
    if result.get('success'):
        state['selected_membership'] = membership
        membership_db = backend_membership_controller.get_user_membership(state['user']['id'])
        state['selected_membership_db'] = membership_db['data']
    return result
