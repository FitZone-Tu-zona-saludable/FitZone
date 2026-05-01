from datetime import datetime

from src.services.auth_service import AuthService
from src.services.membership_service import MembershipService


class PaymentService:
    """Gestión de pagos de clientes (Sprint 1/2)."""

    def __init__(self, auth_service=None, membership_service=None):
        self.auth = auth_service or AuthService()
        self.memberships = membership_service or MembershipService(self.auth)

    def _next_payment_id(self):
        next_id = 1
        for user in self.auth.get_users():
            for payment in user.payments:
                current = int(payment.get("id", 0))
                if current >= next_id:
                    next_id = current + 1
        return next_id

    def _normalize_payment(self, user, payment):
        membership = user.membership or {}
        amount = float(payment.get("amount", payment.get("value", 0)))
        return {
            "id": int(payment.get("id", 0)),
            "user_id": user.id_cliente,
            "user_name": user.nombre,
            "user_email": user.correo,
            "membership_id": payment.get("membership_id", membership.get("id")),
            "membership_name": payment.get("membership_name", membership.get("name", "Sin plan")),
            "amount": amount,
            "value": amount,
            "method": payment.get("method", "N/A"),
            "reference": payment.get("reference", ""),
            "estado": payment.get("estado", "verificado"),
            "created_at": payment.get("created_at", ""),
            "verified_at": payment.get("verified_at", ""),
        }

    def list_payments(self, user_id=None):
        rows = []
        for user in self.auth.get_users():
            if user_id is not None and user.id_cliente != user_id:
                continue
            for payment in user.payments:
                rows.append(self._normalize_payment(user, payment))

        rows.sort(key=lambda item: (item["created_at"], item["id"]), reverse=True)
        return rows

    def list_user_payments(self, user_id):
        return self.list_payments(user_id=user_id)

    def register_payment(self, payment_data):
        user_id = payment_data.get("user_id")
        membership_id = payment_data.get("membership_id")
        amount = float(payment_data.get("amount", 0))
        method = (payment_data.get("method") or "Efectivo").strip()
        reference = (payment_data.get("reference") or "").strip()

        user = self.auth.find_by_id(user_id)
        if not user:
            return {"success": False, "message": "Usuario no encontrado."}
        if not user.membership:
            return {"success": False, "message": "Primero debes seleccionar una membresía."}
        if membership_id != user.membership.get("id"):
            return {"success": False, "message": "La membresía seleccionada no coincide con la del usuario."}
        if amount <= 0:
            return {"success": False, "message": "El monto debe ser mayor a cero."}

        payment_record = {
            "id": self._next_payment_id(),
            "membership_id": membership_id,
            "membership_name": user.membership.get("name", "Sin plan"),
            "amount": amount,
            "value": amount,
            "method": method,
            "reference": reference,
            "estado": "pendiente_verificacion",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "verified_at": None,
        }
        user.payments.append(payment_record)
        user.membership["estado"] = "pendiente_verificacion"
        self.auth.add_log(
            f"Pago registrado: {user.get_email()} | plan: {user.membership.get('name')} | ref: {reference or 'N/A'}"
        )
        self.auth.save_users()
        return {
            "success": True,
            "message": "Pago registrado y enviado a verificación.",
            "data": self._normalize_payment(user, payment_record),
        }

    def verify_payment(self, payment_id):
        for user in self.auth.get_users():
            for payment in user.payments:
                if int(payment.get("id", 0)) != int(payment_id):
                    continue

                if payment.get("estado") == "verificado":
                    return {"success": False, "message": "El pago ya estaba verificado."}

                payment["estado"] = "verificado"
                payment["verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Activar membresía — este método ya llama a save_users() internamente
                activation = self.memberships.activate_membership(user.id_cliente)
                if not activation.get("success"):
                    # Revertir el cambio de estado si la activación falla
                    payment["estado"] = "pendiente_verificacion"
                    payment["verified_at"] = None
                    return activation

                self.auth.add_log(
                    f"Pago verificado: {user.get_email()} | pago #{payment_id}"
                )
                # activate_membership ya guardó; no llamar save_users() de nuevo
                return {
                    "success": True,
                    "message": "Pago verificado correctamente.",
                    "data": self._normalize_payment(user, payment),
                }

        return {"success": False, "message": "Pago no encontrado."}
