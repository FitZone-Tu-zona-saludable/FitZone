# app_context.py — conecta al AuthService real del src
from src.services.auth_service import AuthService
from src.services.schedule_service import ScheduleService
from src.services.trainer_service import TrainerService
from src.services.worker_service import WorkerService

# Instancia global del AuthService (maneja usuarios, logs, pagos)
auth_service = AuthService()

# Controladores de dominio
schedule_service = ScheduleService()
trainer_service  = TrainerService()
worker_service   = WorkerService()

# Compatibilidad con api_service.py y auth_service.py del frontend
class _UserControllerAdapter:
    def login_user(self, email, password):
        user = auth_service.login(email, password)
        if user:
            return {"success": True, "data": {
                "id": user.id_cliente,
                "name": user.nombre,
                "email": user.correo,
                "role": user.role,
                "membership": user.membership,
                "payments": user.payments,
            }}
        return {"success": False, "message": "Credenciales incorrectas."}

    def register_user(self, name, email, password, role="usuario"):
        for u in auth_service.get_users():
            if u.get_email() == email:
                return {"success": False, "message": "El correo ya está registrado."}
        auth_service.create_user(name, email, password, role)
        return {"success": True, "message": "Usuario registrado correctamente."}

    def list_users(self):
        return auth_service.get_users()


class _MembershipControllerAdapter:
    PLANS = [
        {"id": 1, "name": "Básico",     "price": 50000,  "duration_days": 30,  "description": "Acceso en horario regular"},
        {"id": 2, "name": "Estándar",   "price": 80000,  "duration_days": 30,  "description": "Acceso completo + clases grupales"},
        {"id": 3, "name": "Premium",    "price": 120000, "duration_days": 30,  "description": "Acceso 24/7 + entrenador personal"},
        {"id": 4, "name": "Trimestral", "price": 200000, "duration_days": 90,  "description": "Plan 3 meses con descuento"},
        {"id": 5, "name": "Anual",      "price": 600000, "duration_days": 365, "description": "Plan anual — mejor precio"},
    ]

    def list_membership_plans(self):
        return {"success": True, "data": self.PLANS}

    def select_membership(self, user_id, plan_id):
        plan = next((p for p in self.PLANS if p["id"] == plan_id), None)
        if not plan:
            return {"success": False, "message": "Plan no encontrado."}
        for u in auth_service.get_users():
            if u.id_cliente == user_id:
                u.membership = plan
                auth_service.save_users()
                return {"success": True, "data": plan}
        return {"success": False, "message": "Usuario no encontrado."}

    def list_user_memberships(self, user_id):
        for u in auth_service.get_users():
            if u.id_cliente == user_id:
                return [u.membership] if u.membership else []
        return []


class _PaymentControllerAdapter:
    def register_payment(self, user_id, membership_id, amount, method, reference):
        for u in auth_service.get_users():
            if u.id_cliente == user_id:
                auth_service.add_payment(u.get_email(), amount, method)
                return {"success": True, "data": {"amount": amount, "method": method}}
        return {"success": False, "message": "Usuario no encontrado."}

    def list_payments(self):
        all_payments = []
        for u in auth_service.get_users():
            for p in u.payments:
                all_payments.append({**p, "user_id": u.id_cliente})
        return all_payments

    def verify_payment(self, payment_id):
        return {"success": True}


user_controller       = _UserControllerAdapter()
membership_controller = _MembershipControllerAdapter()
payment_controller    = _PaymentControllerAdapter()
