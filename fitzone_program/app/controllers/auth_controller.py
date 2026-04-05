from __future__ import annotations

from app.models.enums import Role
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    def register(self, name: str, email: str, password: str, role: Role = Role.USER, phone: str | None = None):
        return self.auth_service.register(name, email, password, role=role, phone=phone)

    def login(self, email: str, password: str):
        return self.auth_service.login(email, password)

    def logout(self, user_id: str):
        self.auth_service.logout(user_id)
        return {"message": "Sesión cerrada correctamente."}
