from __future__ import annotations

from datetime import datetime

from app.config.database import get_connection
from app.models.entities import User
from app.models.enums import Role, UserStatus


class UserRepository:
    def create(self, user: User) -> User:
        with get_connection() as conn:
            conn.execute(
                '''
                INSERT INTO users (id, name, email, password_hash, phone, role, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    user.id,
                    user.name,
                    user.email,
                    user.password_hash,
                    user.phone,
                    user.role.value,
                    user.status.value,
                    user.created_at.isoformat(),
                    user.updated_at.isoformat(),
                ),
            )
        return user

    def get_by_email(self, email: str) -> User | None:
        normalized_email = email.lower().strip()
        with get_connection() as conn:
            row = conn.execute('SELECT * FROM users WHERE email = ?', (normalized_email,)).fetchone()
        return self._to_entity(row) if row else None

    def get_by_id(self, user_id: str) -> User | None:
        with get_connection() as conn:
            row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return self._to_entity(row) if row else None

    def list_all(self) -> list[User]:
        with get_connection() as conn:
            rows = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
        return [self._to_entity(row) for row in rows]

    def update(self, user: User) -> User:
        with get_connection() as conn:
            conn.execute(
                '''
                UPDATE users
                SET name = ?, email = ?, password_hash = ?, phone = ?, role = ?, status = ?, updated_at = ?
                WHERE id = ?
                ''',
                (
                    user.name,
                    user.email,
                    user.password_hash,
                    user.phone,
                    user.role.value,
                    user.status.value,
                    user.updated_at.isoformat(),
                    user.id,
                ),
            )
        return user

    def delete(self, user_id: str) -> None:
        with get_connection() as conn:
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))

    @staticmethod
    def _to_entity(row) -> User:
        return User(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            password_hash=row['password_hash'],
            phone=row['phone'],
            role=Role(row['role']),
            status=UserStatus(row['status']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
        )
