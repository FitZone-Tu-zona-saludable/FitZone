from frontend.services.app_context import trainer_service


class TrainerController:
    def __init__(self):
        self.service = trainer_service

    def list_trainers(self):
        return [trainer.to_dict() for trainer in self.service.get_trainers()]

    def add_trainer(self, nombre, especialidad, experiencia, disponibilidad):
        self.service.create_trainer(
            nombre,
            "Entrenador",
            "",
            "",
            especialidad,
            experiencia,
            disponibilidad,
        )
        return True

    def edit_trainer(self, trainer_id, nombre=None, especialidad=None,
                     experiencia=None, disponibilidad=None):
        changes = {}
        if nombre:
            changes["nombre"] = nombre
        if especialidad:
            changes["especialidad"] = especialidad
        if experiencia:
            changes["experiencia"] = experiencia
        if disponibilidad:
            changes["modalidad"] = disponibilidad
        return self.service.update_trainer(trainer_id, **changes)

    def delete_trainer(self, trainer_id):
        return self.service.delete_trainer(trainer_id)

    def set_availability(self, trainer_id, disponible):
        return self.service.set_availability(trainer_id, disponible)
