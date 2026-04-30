# attendance_controller.py
# Controlador de asistencia — Sprint 3 (Alex)
# Conecta las vistas de asistencia con el AttendanceService del backend

from src.services.attendance_service import AttendanceService


class AttendanceController:
    """Intermediario MVC entre la vista de asistencia y el servicio real."""

    def __init__(self):
        self.service = AttendanceService()

    def list_attendance(self):
        """Devuelve todos los registros de asistencia como dicts."""
        return [a.to_dict() for a in self.service.get_all()]

    def register(self, id_cliente, nombre_cliente, clase="", servicio=""):
        """Registra la asistencia de un cliente."""
        a = self.service.register(id_cliente, nombre_cliente, clase, servicio)
        return {"success": True, "data": a.to_dict()}

    def update(self, id_asistencia, **kwargs):
        """Actualiza un registro existente."""
        ok = self.service.update(id_asistencia, **kwargs)
        return {"success": ok}

    def delete(self, id_asistencia):
        """Elimina un registro de asistencia."""
        ok = self.service.delete(id_asistencia)
        return {"success": ok}
