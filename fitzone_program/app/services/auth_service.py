from __future__ import annotations

from app.models.entities import User
from app.models.enums import AccessAction, AccessResult, Role, UserStatus
from app.repositories.user_repository import UserRepository
from app.services.access_log_service import AccessLogService
from app.services.user_service import UserService
from app.utils.security import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository, user_service: UserService, access_log_service: AccessLogService) -> None:
        self.user_repository = user_repository
        self.user_service = user_service
        self.access_log_service = access_log_service

    def register(self, name: str, email: str, password: str, role: Role = Role.USER, phone: str | None = None, ip_address: str = '127.0.0.1') -> User:
        user = self.user_service.create_user(name=name, email=email, password=password, phone=phone, role=role)
        self.access_log_service.record(user.id, user.email, AccessAction.REGISTER, AccessResult.SUCCESS, ip_address)
        return user

    def login(self, email: str, password: str, ip_address: str = '127.0.0.1') -> User:
        normalized_email = email.lower().strip()
        user = self.user_repository.get_by_email(normalized_email)
        if not user or not verify_password(password, user.password_hash):
            self.access_log_service.record(None, normalized_email, AccessAction.LOGIN, AccessResult.FAILED, ip_address)
            raise ValueError('Credenciales inválidas.')
        if user.status != UserStatus.ACTIVE:
            self.access_log_service.record(user.id, normalized_email, AccessAction.ACCESS_DENIED, AccessResult.FAILED, ip_address)
            raise ValueError('El usuario no está activo.')
        self.access_log_service.record(user.id, normalized_email, AccessAction.LOGIN, AccessResult.SUCCESS, ip_address)
        return user

    def logout(self, user_id: str, ip_address: str = '127.0.0.1') -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado.')
        self.access_log_service.record(user.id, user.email, AccessAction.LOGOUT, AccessResult.SUCCESS, ip_address)
