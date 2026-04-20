import json
import os
from datetime import datetime
from src.models.client import Client


class AuthService:
    def __init__(self):
        self.users = []
        self.logs = []
        self.user_file = "data/users.json"
        self.log_file = "data/logs.json"
        self.id_counter = 1

        self.load_users()
        self.load_logs()

    # ─── LOGS ────────────────────────────────────────────────────────
    def add_log(self, message):
        log = {
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message": message
        }
        self.logs.append(log)
        self.save_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.logs = json.load(f)

    def save_logs(self):
        os.makedirs("data", exist_ok=True)
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=4)

    # ─── USERS ───────────────────────────────────────────────────────
    def load_users(self):
        os.makedirs("data", exist_ok=True)

        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as f:
                data = json.load(f)

            for u in data:
                user = Client(
                    u["id"], u["name"], u["email"], u["password"], u["role"]
                )
                user.payments = u.get("payments", [])
                user.membership = u.get("membership", None)
                self.users.append(user)

                if u["id"] >= self.id_counter:
                    self.id_counter = u["id"] + 1
        else:
            self.create_user("Romel", "romel@mail.com", "123", "admin")
            self.create_user("Juan", "user@mail.com", "123", "user")
            self.create_user("Seguridad", "seg@mail.com", "123", "seguridad")

    def save_users(self):
        data = []
        for u in self.users:
            data.append({
                "id": u.id_cliente,
                "name": u.nombre,
                "email": u.correo,
                "password": u.password,
                "role": u.role,
                "payments": u.payments,
                "membership": u.membership
            })
        with open(self.user_file, "w") as f:
            json.dump(data, f, indent=4)

    # ─── PERMISOS ─────────────────────────────────────────────────────
    def has_permission(self, user, action):
        permissions = {
            "admin": ["create", "delete", "update", "manage_schedules",
                      "manage_trainers", "manage_workers"],
            "user": [],
            "seguridad": ["view_logs"]
        }
        return action in permissions.get(user.get_role(), [])

    # ─── CRUD USUARIOS ────────────────────────────────────────────────
    def create_user(self, name, email, password, role):
        user = Client(self.id_counter, name, email, password, role)
        self.users.append(user)
        self.id_counter += 1
        self.add_log(f"Usuario creado: {name}")
        self.save_users()
        return user

    def get_users(self):
        return self.users

    def update_user(self, email, name):
        for u in self.users:
            if u.get_email() == email:
                u.nombre = name
                self.add_log(f"Usuario actualizado: {email}")
                self.save_users()
                return True
        return False

    def delete_user(self, email, actor=None):
        """
        Elimina la cuenta validando permisos.
        actor: objeto Client quien ejecuta la acción (None = sin validación de rol).
        Deja trazabilidad en logs.
        """
        if actor is not None and not self.has_permission(actor, "delete"):
            self.add_log(
                f"Intento no autorizado de eliminar cuenta {email} "
                f"por {actor.get_name()} (rol: {actor.get_role()})"
            )
            return False, "Sin permiso para eliminar cuentas"

        for u in self.users:
            if u.get_email() == email:
                nombre = u.get_name()
                self.users.remove(u)
                self.add_log(
                    f"Cuenta eliminada: {email} | nombre: {nombre} | "
                    f"eliminado por: {actor.get_name() if actor else 'sistema'}"
                )
                self.save_users()
                return True, "Cuenta eliminada correctamente"

        return False, "Usuario no encontrado"

    def login(self, email, password):
        for u in self.users:
            if u.get_email() == email and u.password == password:
                self.add_log(f"{u.get_name()} inició sesión")
                return u
        self.add_log(f"Intento fallido: {email}")
        return None

    # ─── PAGOS + NOTIFICACIÓN ─────────────────────────────────────────
    def add_payment(self, email, value, method):
        for u in self.users:
            if u.get_email() == email:
                u.payments.append({"value": value, "method": method})
                self.add_log(f"Pago confirmado: {email}")
                self.save_users()
                return True
        return False

    # ─── ESTADO MEMBRESÍA ─────────────────────────────────────────────
    def _get_membership_dates(self, membership):
        try:
            inicio = datetime.strptime(membership["fechaInicio"], "%Y-%m-%d")
            fin = datetime.strptime(membership["fechaFin"], "%Y-%m-%d")
            return inicio, fin
        except (KeyError, ValueError):
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

        for u in self.users:
            if not u.membership:
                continue

            inicio, fin = self._get_membership_dates(u.membership)
            if not inicio or not fin:
                continue

            u.membership["estado"] = self._resolve_membership_status(
                today, inicio, fin
            )

        self.save_users()
