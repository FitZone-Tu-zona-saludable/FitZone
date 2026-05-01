from src.services.json_storage import load_json_list, save_json_list
from src.models.trainer import Trainer


class TrainerService:
    """Servicio CRUD de entrenadores con persistencia JSON."""

    def __init__(self):
        self.trainers = []
        self.trainer_file = "data/trainers.json"
        self._id_counter = 1
        self.load_trainers()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load_trainers(self):
        data = load_json_list(self.trainer_file)
        self.trainers = []
        for d in data:
                t = Trainer(
                    d["id_trabajador"], d["nombre"], d["cargo"],
                    d["telefono"], d["correo"], d.get("especialidad", ""),
                    d.get("experiencia", ""), d.get("modalidad", "presencial"),
                    d.get("revision_medica", False), d.get("documento", "")
                )
                t.horarios = d.get("horarios", [])
                t.disponible = d.get("disponible", True)
                self.trainers.append(t)
                if d["id_trabajador"] >= self._id_counter:
                    self._id_counter = d["id_trabajador"] + 1

    def save_trainers(self):
        save_json_list(self.trainer_file, [t.to_dict() for t in self.trainers])

    # ─── CRUD ─────────────────────────────────────────────────────────
    def create_trainer(self, nombre, cargo, telefono, correo, especialidad="",
                       experiencia="", modalidad="presencial",
                       revision_medica=False, documento=""):
        t = Trainer(self._id_counter, nombre, cargo, telefono, correo,
                    especialidad, experiencia, modalidad, revision_medica, documento)
        self.trainers.append(t)
        self._id_counter += 1
        self.save_trainers()
        return t

    def get_trainers(self):
        return self.trainers

    def get_by_id(self, id_trabajador):
        for t in self.trainers:
            if t.id_trabajador == id_trabajador:
                return t
        return None

    def update_trainer(self, id_trabajador, **kwargs):
        t = self.get_by_id(id_trabajador)
        if not t:
            return False
        for key, val in kwargs.items():
            if hasattr(t, key):
                setattr(t, key, val)
        self.save_trainers()
        return True

    def set_availability(self, id_trabajador, disponible):
        return self.update_trainer(id_trabajador, disponible=bool(disponible))

    def delete_trainer(self, id_trabajador):
        t = self.get_by_id(id_trabajador)
        if t:
            self.trainers.remove(t)
            self.save_trainers()
            return True
        return False

    # ─── LÓGICA DE ASIGNACIÓN ────────────────────────────────────────
    def get_disponibles(self):
        """Devuelve entrenadores disponibles (sin horario asignado activo)."""
        return [t for t in self.trainers if t.disponible]

    def asignar_horario(self, id_entrenador, id_horario):
        """Asigna un horario a un entrenador si está disponible."""
        t = self.get_by_id(id_entrenador)
        if not t:
            return False, "Entrenador no encontrado"
        if not t.disponible:
            return False, f"{t.nombre} no está disponible"
        t.asignar_horario(id_horario)
        self.save_trainers()
        return True, f"Horario asignado a {t.nombre}"

    def seleccionar_por_plan(self, tipo_plan):
        """Filtra entrenadores compatibles con el tipo de plan."""
        disponibles = self.get_disponibles()
        compatibles = [
            t for t in disponibles
            if tipo_plan.lower() in t.especialidad.lower()
        ]
        return compatibles if compatibles else disponibles
