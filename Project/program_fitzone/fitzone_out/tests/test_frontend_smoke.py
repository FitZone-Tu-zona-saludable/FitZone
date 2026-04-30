import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from frontend.services.state_service import reset_state, state


@pytest.fixture
def qt_app():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    yield app


def test_login_view_builds(qt_app):
    from frontend.views.login_view import LoginView

    view = LoginView()
    assert view.windowTitle() == "FitZone - Login"
    view.close()


@pytest.mark.parametrize("role", ["user", "admin", "seguridad"])
def test_sprint5_page_builds_per_role(qt_app, role):
    from frontend.views.pages.sprint5_page import Sprint5Page

    reset_state()
    state["user"] = {
        "id": 1,
        "user_id": 1,
        "name": "Tester",
        "email": "tester@fitzone.com",
        "role": role,
        "membership": None,
        "payments": [],
    }

    page = Sprint5Page(role=role)
    assert page.role == role
    assert page.stack.count() >= 1
    page.close()


@pytest.mark.parametrize(
    ("role", "allowed_keys", "forbidden_keys"),
    [
        (
            "user",
            {"memberships", "select_membership", "register_payment", "schedules", "trainers"},
            {"verify_payment", "security", "employees", "reports"},
        ),
        (
            "admin",
            {"verify_payment", "security", "employees", "reports", "emp_payments"},
            set(),
        ),
        (
            "seguridad",
            {"security", "alerts"},
            {"memberships", "register_payment", "employees", "reports"},
        ),
    ],
)
def test_sprint5_page_limits_navigation_by_role(qt_app, role, allowed_keys, forbidden_keys):
    from frontend.views.pages.sprint5_page import Sprint5Page

    reset_state()
    state["user"] = {
        "id": 1,
        "user_id": 1,
        "name": "Tester",
        "email": "tester@fitzone.com",
        "role": role,
        "membership": None,
        "payments": [],
    }

    page = Sprint5Page(role=role)
    visible_keys = set(page.nav_buttons.keys())

    assert allowed_keys.issubset(visible_keys)
    assert forbidden_keys.isdisjoint(visible_keys)
    page.close()
