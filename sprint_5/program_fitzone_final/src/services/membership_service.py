from datetime import datetime, timedelta

from src.services.auth_service import AuthService


PLANS = [
    {
        "id": 1,
        "name": "Básico",
        "price": 50000,
        "duration_days": 30,
        "description": "Acceso a sala general en horario regular.",
    },
    {
        "id": 2,
        "name": "Estándar",
        "price": 80000,
        "duration_days": 30,
        "description": "Acceso completo más clases grupales.",
    },
    {
        "id": 3,
        "name": "Premium",
        "price": 120000,
        "duration_days": 30,
        "description": "Acceso 24/7, clases grupales y entrenador asignable.",
    },
    {
        "id": 4,
        "name": "Trimestral",
        "price": 200000,
        "duration_days": 90,
        "description": "Plan de tres meses con descuento.",
    },
    {
        "id": 5,
        "name": "Anual",
        "price": 600000,
        "duration_days": 365,
        "description": "Cobertura anual con la mejor tarifa.",
    },
]


class MembershipService:
    def __init__(self, auth_service=None):
        self.auth = auth_service or AuthService()

    def _clone_plan(self, plan):
        return {
            "id": plan["id"],
            "name": plan["name"],
            "tipo": plan["name"],
            "price": plan["price"],
            "duration_days": plan["duration_days"],
            "description": plan["description"],
        }

    def list_memberships(self):
        return [self._clone_plan(plan) for plan in PLANS]

    def get_plan(self, plan_id):
        plan = next((item for item in PLANS if item["id"] == plan_id), None)
        return self._clone_plan(plan) if plan else None

    def get_user_memberships(self, user_id):
        user = self.auth.find_by_id(user_id)
        return [user.membership] if user and user.membership else []

    def select_membership(self, user_id, plan_id):
        user = self.auth.find_by_id(user_id)
        if not user:
            return {"success": False, "message": "Usuario no encontrado."}

        plan = self.get_plan(plan_id)
        if not plan:
            return {"success": False, "message": "Plan no encontrado."}

        membership = {
            **plan,
            "fechaInicio": None,
            "fechaFin": None,
            "estado": "pendiente_pago",
            "selected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trainer_id": None,
            "trainer_name": None,
        }
        user.membership = membership
        self.auth.add_log(
            f"Membresía seleccionada: {user.get_email()} -> {plan['name']}"
        )
        self.auth.save_users()
        return {
            "success": True,
            "message": f"Plan {plan['name']} seleccionado correctamente.",
            "data": membership,
        }

    def activate_membership(self, user_id):
        user = self.auth.find_by_id(user_id)
        if not user or not user.membership:
            return {"success": False, "message": "El usuario no tiene membresía seleccionada."}

        today = datetime.now().date()
        duration = int(user.membership.get("duration_days", 0))
        end_date = today + timedelta(days=duration)
        user.membership["fechaInicio"] = today.strftime("%Y-%m-%d")
        user.membership["fechaFin"] = end_date.strftime("%Y-%m-%d")
        user.membership["estado"] = "activa"
        self.auth.save_users()
        return {
            "success": True,
            "message": "Membresía activada correctamente.",
            "data": user.membership,
        }

    def assign_trainer(self, user_id, trainer_id, trainer_name):
        user = self.auth.find_by_id(user_id)
        if not user or not user.membership:
            return {"success": False, "message": "Debes seleccionar una membresía primero."}

        user.membership["trainer_id"] = trainer_id
        user.membership["trainer_name"] = trainer_name
        self.auth.save_users()
        return {
            "success": True,
            "message": f"Entrenador {trainer_name} asignado correctamente.",
            "data": user.membership,
        }
