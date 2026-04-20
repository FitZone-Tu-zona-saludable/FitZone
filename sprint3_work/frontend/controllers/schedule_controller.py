# schedule_controller.py — usa el ScheduleService real del src
from src.services.schedule_service import ScheduleService

class ScheduleController:
    def __init__(self):
        self.service = ScheduleService()

    def list_schedules(self):
        return [s.to_dict() for s in self.service.get_schedules()]

    def add_schedule(self, fecha, hora, entrenador, cupos, tipo):
        # hora_fin calculada como 1h después por defecto
        hora_parts = hora.split(":")
        hora_fin = f"{int(hora_parts[0])+1:02d}:{hora_parts[1]}"
        self.service.create_schedule(fecha, hora, hora_fin, tipo, cupos)
        return True

    def edit_schedule(self, schedule_id, fecha=None, hora=None, entrenador=None, cupos=None, tipo=None):
        return self.service.update_schedule(schedule_id, fecha=fecha, hora_inicio=hora, tipo=tipo, cupos=cupos)

    def delete_schedule(self, schedule_id):
        return self.service.delete_schedule(schedule_id)
