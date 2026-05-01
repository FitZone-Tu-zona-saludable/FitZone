import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.mark.parametrize(
    "module_name",
    [
        "frontend.views.login_view",
        "frontend.views.main_dashboard_view",
        "frontend.views.membership_list_view",
        "frontend.views.membership_select_view",
        "frontend.views.payment_register_view",
        "frontend.views.payment_verification_view",
        "frontend.views.security_view",
        "frontend.views.schedule_consult_view",
        "frontend.views.schedule_admin_view",
        "frontend.views.trainer_select_view",
        "frontend.views.trainer_admin_view",
        "frontend.views.staff_register_view",
        "frontend.views.pages.schedule_page",
        "frontend.views.pages.trainer_page",
        "frontend.views.pages.employee_page",
        "frontend.views.pages.sprint5_page",
    ],
)
def test_frontend_modules_import_without_missing_dependencies(module_name):
    pytest.importorskip("PySide6")
    module = importlib.import_module(module_name)
    assert module is not None
