from copy import deepcopy


DEFAULT_STATE = {
    "user": None,
    "memberships": [],
    "selected_membership": None,
    "payments": [],
}


state = deepcopy(DEFAULT_STATE)


def _serialize_user(user):
    if user is None:
        return None

    if isinstance(user, dict):
        return {
            "id": user.get("id", user.get("user_id")),
            "user_id": user.get("user_id", user.get("id")),
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "role": user.get("role", ""),
            "membership": user.get("membership"),
            "payments": list(user.get("payments", [])),
        }

    return {
        "id": user.id_cliente,
        "user_id": user.id_cliente,
        "name": user.nombre,
        "email": user.correo,
        "role": user.role,
        "membership": user.membership,
        "payments": list(user.payments),
    }


def reset_state():
    state.clear()
    state.update(deepcopy(DEFAULT_STATE))


def set_current_user(user):
    serialized = _serialize_user(user)
    state["user"] = serialized
    state["selected_membership"] = serialized.get("membership") if serialized else None
    state["payments"] = serialized.get("payments", []) if serialized else []
    return serialized


def refresh_current_user(auth_service=None):
    current = state.get("user")
    if not current:
        return None

    if auth_service is None:
        from frontend.services.app_context import auth_service as shared_auth

        auth_service = shared_auth

    user = auth_service.find_by_id(current.get("user_id"))
    if user is None:
        reset_state()
        return None
    return set_current_user(user)


def set_selected_membership(membership):
    state["selected_membership"] = membership
    if state.get("user"):
        state["user"]["membership"] = membership


def set_payments(payments):
    state["payments"] = list(payments)
    if state.get("user"):
        state["user"]["payments"] = list(payments)
