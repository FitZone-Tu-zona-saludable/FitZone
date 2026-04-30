import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.auth_service import AuthService
from src.services.membership_service import MembershipService
from src.services.payment_service import PaymentService
from src.services.security_service import SecurityService


@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)
    yield


def test_membership_payment_flow_uses_authenticated_user_and_activates_membership():
    auth = AuthService()
    membership_service = MembershipService(auth_service=auth)
    payment_service = PaymentService(
        auth_service=auth,
        membership_service=membership_service,
    )

    user = auth.login("user@mail.com", "123")
    selection = membership_service.select_membership(user.id_cliente, 3)
    assert selection["success"] is True
    assert user.membership["estado"] == "pendiente_pago"

    payment = payment_service.register_payment({
        "user_id": user.id_cliente,
        "membership_id": user.membership["id"],
        "amount": user.membership["price"],
        "method": "transferencia",
        "reference": "REF-123",
    })
    assert payment["success"] is True
    assert payment["data"]["estado"] == "pendiente_verificacion"
    assert user.membership["estado"] == "pendiente_verificacion"

    verification = payment_service.verify_payment(payment["data"]["id"])
    assert verification["success"] is True
    assert verification["data"]["estado"] == "verificado"
    assert user.membership["estado"] == "activa"
    assert user.membership["fechaInicio"]
    assert user.membership["fechaFin"]


def test_security_service_normalizes_real_log_structure():
    auth = AuthService()
    auth.login("romel@mail.com", "123")
    auth.login("desconocido@mail.com", "bad-pass")

    logs = SecurityService(auth_service=auth).get_access_logs()

    assert len(logs) >= 2
    assert all("date" in log for log in logs)
    assert all("message" in log for log in logs)
