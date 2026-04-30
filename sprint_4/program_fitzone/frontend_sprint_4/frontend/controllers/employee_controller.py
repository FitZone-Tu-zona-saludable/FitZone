# employee_controller.py — usa el WorkerService real del src
from src.services.worker_service import WorkerService

class EmployeeController:
    def __init__(self):
        self.service = WorkerService()

    def list_employees(self):
        return [w.to_dict() for w in self.service.get_workers()]

    def add_employee(self, nombre, cargo, turno, contacto):
        self.service.register_employee(nombre, cargo, "", contacto, modalidad=turno)
        return True

    def edit_employee(self, worker_id, **kwargs):
        return self.service.update_worker(worker_id, **kwargs)

    def delete_employee(self, worker_id):
        return self.service.delete_worker(worker_id)
