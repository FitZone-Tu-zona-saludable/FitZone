from __future__ import annotations

from app.models.entities import User
from app.models.enums import Role, UserStatus
from app.repositories.user_repository import UserRepository
from app.utils.common import new_id, now
from app.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, name: str, email: str, password: str, phone: str | None = None, role: Role = Role.USER) -> User:
        normalized_email = email.lower().strip()
        if self.user_repository.get_by_email(normalized_email):
            raise ValueError('El correo ya está registrado.')
        timestamp = now()
        user = User(
            id=new_id(),
            name=name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
            phone=phone.strip() if phone else None,
            role=role,
            status=UserStatus.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.user_repository.list_all()

    def update_user(self, user_id: str, name: str | None = None, email: str | None = None, phone: str | None = None) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado.')

        normalized_email = email.lower().strip() if email else None
        if normalized_email and normalized_email != user.email and self.user_repository.get_by_email(normalized_email):
            raise ValueError('El nuevo correo ya está registrado.')

        user.name = name.strip() if name else user.name
        user.email = normalized_email or user.email
        user.phone = phone.strip() if phone is not None and phone else (None if phone == '' else user.phone)
        user.updated_at = now()
        return self.user_repository.update(user)

    def change_user_status(self, user_id: str, status: UserStatus) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado.')
        user.status = status
        user.updated_at = now()
        return self.user_repository.update(user)

    def delete_user(self, user_id: str) -> None:
        if not self.user_repository.get_by_id(user_id):
            raise ValueError('Usuario no encontrado.')
        self.user_repository.delete(user_id)
