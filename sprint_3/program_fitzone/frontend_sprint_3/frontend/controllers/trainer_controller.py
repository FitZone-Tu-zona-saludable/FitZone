# trainer_controller.py — usa el TrainerService real del src
from src.services.trainer_service import TrainerService

class TrainerController:
    def __init__(self):
        self.service = TrainerService()

    def list_trainers(self):
        return [t.to_dict() for t in self.service.get_trainers()]

    def add_trainer(self, nombre, especialidad, experiencia, disponibilidad):
        self.service.create_trainer(nombre, "Entrenador", "", "", especialidad, experiencia, disponibilidad)
        return True

    def edit_trainer(self, trainer_id, nombre=None, especialidad=None, experiencia=None, disponibilidad=None):
        kwargs = {}
        if nombre:        kwargs["nombre"] = nombre
        if especialidad:  kwargs["especialidad"] = especialidad
        if experiencia:   kwargs["experiencia"] = experiencia
        if disponibilidad: kwargs["modalidad"] = disponibilidad
        return self.service.update_trainer(trainer_id, **kwargs)

    def delete_trainer(self, trainer_id):
        return self.service.delete_trainer(trainer_id)
