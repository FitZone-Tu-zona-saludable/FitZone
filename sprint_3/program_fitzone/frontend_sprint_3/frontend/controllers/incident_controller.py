# incident_controller.py
# Controlador de incidencias del personal — Sprint 3 (Alex)

from src.services.incident_service import IncidentService


class IncidentController:
    """Intermediario MVC entre la vista de incidencias y el servicio real."""

    def __init__(self):
        self.service = IncidentService()

    def list_incidents(self):
        return [i.to_dict() for i in self.service.get_all()]

    def create_incident(self, id_trabajador, nombre_trabajador, tipo, causa):
        i = self.service.create(id_trabajador, nombre_trabajador, tipo, causa)
        return {"success": True, "data": i.to_dict()}

    def get_by_worker(self, id_trabajador):
        return [i.to_dict() for i in self.service.get_by_worker(id_trabajador)]
