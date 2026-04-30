from frontend.services.app_context import schedule_service
from frontend.services.state_service import state


class ScheduleController:
    def __init__(self):
        self.service = schedule_service

    def list_schedules(self):
        return [schedule.to_dict() for schedule in self.service.get_schedules()]

    def list_with_availability(self):
        """Lista horarios con cupos_disponibles e indicador de inscripcion."""
        user = state.get("user")
        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id_cliente", None)
        return self.service.list_with_availability(user_id=user_id)

    def add_schedule(self, fecha, hora, entrenador, cupos, tipo):
        hora_parts = hora.split(":")
        hora_fin = f"{int(hora_parts[0]) + 1:02d}:{hora_parts[1]}"
        self.service.create_schedule(
            fecha, hora, hora_fin, tipo, cupos, id_entrenador=entrenador
        )
        return True

    def edit_schedule(self, schedule_id, fecha=None, hora=None,
                      entrenador=None, cupos=None, tipo=None):
        return self.service.update_schedule(
            schedule_id,
            fecha=fecha,
            hora_inicio=hora,
            tipo=tipo,
            cupos=cupos,
            id_entrenador=entrenador,
        )

    def delete_schedule(self, schedule_id):
        return self.service.delete_schedule(schedule_id)

    # ── Inscripción de usuarios ───────────────────────────────────────────────
    def enroll_current_user(self, id_horario):
        """Inscribe al usuario activo en la sesión en el horario indicado."""
        user = state.get("user")
        if not user:
            return {"success": False, "message": "No hay sesión activa"}
        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id_cliente", None)
        return self.service.enroll_user(id_horario, user_id)

    def unenroll_current_user(self, id_horario):
        """Cancela la inscripción del usuario activo en el horario indicado."""
        user = state.get("user")
        if not user:
            return {"success": False, "message": "No hay sesión activa"}
        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id_cliente", None)
        return self.service.unenroll_user(id_horario, user_id)

    def get_my_schedules(self):
        """Retorna los horarios en los que está inscrito el usuario activo."""
        user = state.get("user")
        if not user:
            return []
        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id_cliente", None)
        return [s.to_dict() for s in self.service.get_user_schedules(user_id)]
