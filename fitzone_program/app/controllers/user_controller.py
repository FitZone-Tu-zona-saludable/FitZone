from __future__ import annotations

from app.models.enums import Role, UserStatus
from app.services.user_service import UserService


class UserController:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def create_user(self, name: str, email: str, password: str, phone: str | None = None, role: Role = Role.USER):
        return self.user_service.create_user(name, email, password, phone, role)

    def get_user_by_id(self, user_id: str):
        return self.user_service.get_user_by_id(user_id)

    def list_users(self):
        return self.user_service.list_users()

    def update_user(self, user_id: str, name: str | None = None, email: str | None = None, phone: str | None = None):
        return self.user_service.update_user(user_id, name, email, phone)

    def change_user_status(self, user_id: str, status: UserStatus):
        return self.user_service.change_user_status(user_id, status)

    def delete_user(self, user_id: str):
        self.user_service.delete_user(user_id)
        return {"message": "Usuario eliminado correctamente."}
