import json
import os
import tempfile
from datetime import datetime

from src.models.client import Client


def _atomic_write_json(path, data):
    """Escribe data como JSON de forma atómica usando archivo temporal."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handler:
            json.dump(data, handler, indent=4, ensure_ascii=False)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


DEFAULT_USERS = [
    ("Romel", "romel@mail.com", "123", "admin"),
    ("Juan", "user@mail.com", "123", "user"),
    ("Seguridad", "seg@mail.com", "123", "seguridad"),
]


class AuthService:
    def __init__(self, user_file="data/users.json", log_file="data/logs.json",
                 seed_defaults=True):
        self.users = []
        self.logs = []
        self.user_file = user_file
        self.log_file = log_file
        self.seed_defaults = seed_defaults
        self.id_counter = 1

        self.load_users()
        self.load_logs()

    # ------------------------------------------------------------------ utils
    def _normalize_email(self, email):
        return str(email or "").strip().lower()

    def _ensure_data_dir(self, path):
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _seed_default_users(self):
        for name, email, password, role in DEFAULT_USERS:
            user = Client(self.id_counter, name, email, password, role)
            self.users.append(user)
            self.id_counter += 1
        self.save_users()

    def find_by_email(self, email):
        normalized = self._normalize_email(email)
        for user in self.users:
            if self._normalize_email(user.get_email()) == normalized:
                return user
        return None

    def find_by_id(self, user_id):
        for user in self.users:
            if user.id_cliente == user_id:
                return user
        return None

    # ------------------------------------------------------------------- logs
    def add_log(self, message):
        self.logs.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
        })
        self.save_logs()

    def load_logs(self):
        self._ensure_data_dir(self.log_file)
        if not os.path.exists(self.log_file):
            self.logs = []
            return

        try:
            with open(self.log_file, "r", encoding="utf-8") as handler:
                self.logs = json.load(handler)
        except (json.JSONDecodeError, OSError):
            self.logs = []

    def save_logs(self):
        self._ensure_data_dir(self.log_file)
        try:
            _atomic_write_json(self.log_file, self.logs)
        except Exception as exc:
            # Los logs no deben bloquear la app; solo reportar en consola
            print(f"[AuthService] Advertencia: no se pudo guardar logs: {exc}")

    # ------------------------------------------------------------------ users
    def load_users(self):
        self._ensure_data_dir(self.user_file)
        self.users = []
        self.id_counter = 1

        if not os.path.exists(self.user_file):
            if self.seed_defaults:
                self._seed_default_users()
            return

        try:
            with open(self.user_file, "r", encoding="utf-8") as handler:
                data = json.load(handler)
        except (json.JSONDecodeError, OSError):
            data = []

        seen_emails = set()
        duplicates_removed = False

        for raw_user in data:
            # Ignorar registros que no tengan los campos mínimos obligatorios
            if not all(k in raw_user for k in ("id", "name", "email", "password", "role")):
                duplicates_removed = True
                continue

            email = self._normalize_email(raw_user.get("email"))
            if not email or email in seen_emails:
                duplicates_removed = True
                continue

            seen_emails.add(email)
            user = Client(
                raw_user["id"],
                raw_user["name"],
                raw_user["email"],
                raw_user["password"],
                raw_user["role"],
            )
            user.payments = raw_user.get("payments", [])
            user.membership = raw_user.get("membership")
            self.users.append(user)

            if raw_user["id"] >= self.id_counter:
                self.id_counter = raw_user["id"] + 1

        if not self.users and self.seed_defaults:
            self._seed_default_users()
            return

        if duplicates_removed:
            self.save_users()

    def save_users(self):
        self._ensure_data_dir(self.user_file)
        payload = []
        for user in self.users:
            payload.append({
                "id": user.id_cliente,
                "name": user.nombre,
                "email": user.correo,
                "password": user.password,
                "role": user.role,
                "payments": user.payments,
                "membership": user.membership,
            })
        _atomic_write_json(self.user_file, payload)

    # --------------------------------------------------------------- permisos
    def has_permission(self, user, action):
        permissions = {
            "admin": [
                "create", "delete", "update",
                "manage_schedules", "manage_trainers", "manage_workers",
                "verify_payments", "view_logs",
            ],
            "user": [],
            "seguridad": ["view_logs"],
        }
        return action in permissions.get(user.get_role(), [])

    # ------------------------------------------------------------- crud users
    def create_user(self, name, email, password, role):
        normalized = self._normalize_email(email)
        if not normalized:
            raise ValueError("El correo es obligatorio.")
        if self.find_by_email(normalized):
            raise ValueError("El correo ya está registrado.")

        user = Client(self.id_counter, name, normalized, password, role)
        self.users.append(user)
        self.id_counter += 1
        self.add_log(f"Usuario creado: {name}")
        self.save_users()
        return user

    def get_users(self):
        return self.users

    def update_user(self, email, name):
        user = self.find_by_email(email)
        if not user:
            return False
        user.nombre = name
        self.add_log(f"Usuario actualizado: {user.get_email()}")
        self.save_users()
        return True

    def delete_user(self, email, actor=None):
        if actor is not None and not self.has_permission(actor, "delete"):
            self.add_log(
                f"Intento no autorizado de eliminar cuenta {email} "
                f"por {actor.get_name()} (rol: {actor.get_role()})"
            )
            return False, "Sin permiso para eliminar cuentas"

        user = self.find_by_email(email)
        if not user:
            return False, "Usuario no encontrado"

        self.users.remove(user)
        self.add_log(
            f"Cuenta eliminada: {user.get_email()} | nombre: {user.get_name()} | "
            f"eliminado por: {actor.get_name() if actor else 'sistema'}"
        )
        self.save_users()
        return True, "Cuenta eliminada correctamente"

    def login(self, email, password):
        user = self.find_by_email(email)
        if user and user.password == password:
            self.add_log(f"{user.get_name()} inició sesión")
            return user

        self.add_log(f"Intento fallido: {self._normalize_email(email)}")
        return None

    # --------------------------------------------------------------- payments
    def add_payment(self, email, value, method, payment_record=None):
        user = self.find_by_email(email)
        if not user:
            return False

        if payment_record is None:
            payment_record = {
                "amount": float(value),
                "value": float(value),
                "method": method,
                "estado": "verificado",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        user.payments.append(payment_record)
        self.add_log(f"Pago registrado: {user.get_email()}")
        self.save_users()
        return True

    # ----------------------------------------------------------- memberships
    def _get_membership_dates(self, membership):
        try:
            inicio = datetime.strptime(membership["fechaInicio"], "%Y-%m-%d")
            fin = datetime.strptime(membership["fechaFin"], "%Y-%m-%d")
            return inicio, fin
        except (KeyError, TypeError, ValueError):
            return None, None

    def _resolve_membership_status(self, today, inicio, fin):
        if today < inicio:
            return "pendiente"
        if today > fin:
            return "vencida"
        diff_days = (fin - today).days
        return "por_vencer" if diff_days <= 5 else "activa"

    def update_membership_status(self):
        today = datetime.now()

        for user in self.users:
            if not user.membership:
                continue

            inicio, fin = self._get_membership_dates(user.membership)
            if not inicio or not fin:
                continue

            user.membership["estado"] = self._resolve_membership_status(
                today, inicio, fin
            )

        self.save_users()
