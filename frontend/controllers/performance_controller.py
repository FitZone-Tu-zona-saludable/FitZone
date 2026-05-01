# performance_controller.py
# Controlador de evaluación de desempeño — Sprint 3 (Alex)

from frontend.services.app_context import performance_service


class PerformanceController:
    """Intermediario MVC entre la vista de evaluación y el servicio real."""

    def __init__(self):
        self.service = performance_service

    def list_evaluations(self):
        return [e.to_dict() for e in self.service.get_all()]

    def create_evaluation(self, id_cliente, nombre_cliente,
                          id_entrenador, nombre_entrenador,
                          puntaje, observaciones=""):
        p = self.service.create(id_cliente, nombre_cliente,
                                id_entrenador, nombre_entrenador,
                                puntaje, observaciones)
        return {"success": True, "data": p.to_dict()}

    def get_by_client(self, id_cliente):
        return [e.to_dict() for e in self.service.get_by_client(id_cliente)]
