import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.auth_service import AuthService


@pytest.fixture(autouse=True)
def isolated_data(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    monkeypatch.chdir(tmp_path)
    yield


def test_create_user_isolated_from_real_persistence():
    auth = AuthService(seed_defaults=False)
    created = auth.create_user("Romel", "romel@mail.com", "1234", "admin")

    users = auth.get_users()

    assert created.get_email() == "romel@mail.com"
    assert len(users) == 1
    assert users[0].get_email() == "romel@mail.com"


def test_create_user_rejects_duplicate_email():
    auth = AuthService(seed_defaults=False)
    auth.create_user("Romel", "romel@mail.com", "1234", "admin")

    with pytest.raises(ValueError):
        auth.create_user("Otro Romel", "romel@mail.com", "abcd", "admin")
