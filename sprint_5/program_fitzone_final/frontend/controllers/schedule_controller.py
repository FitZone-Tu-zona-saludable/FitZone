from frontend.services.app_context import schedule_service


class ScheduleController:
    def __init__(self):
        self.service = schedule_service

    def list_schedules(self):
        return [schedule.to_dict() for schedule in self.service.get_schedules()]

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
