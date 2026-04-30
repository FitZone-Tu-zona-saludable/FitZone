import json
import os
from src.models.schedule import Schedule


class ScheduleService:
    """Servicio CRUD de horarios con persistencia JSON."""

    def __init__(self):
        self.schedules = []
        self.schedule_file = "data/schedules.json"
        self._id_counter = 1
        self.load_schedules()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load_schedules(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, "r") as f:
                data = json.load(f)
            self.schedules = []
            for d in data:
                s = Schedule(
                    d["id_horario"], d["fecha"], d["hora_inicio"],
                    d["hora_fin"], d["tipo"], d["cupos"],
                    d.get("id_entrenador")
                )
                self.schedules.append(s)
                if d["id_horario"] >= self._id_counter:
                    self._id_counter = d["id_horario"] + 1

    def save_schedules(self):
        os.makedirs("data", exist_ok=True)
        with open(self.schedule_file, "w") as f:
            json.dump([s.to_dict() for s in self.schedules], f, indent=4)

    # ─── CRUD ─────────────────────────────────────────────────────────
    def create_schedule(self, fecha, hora_inicio, hora_fin, tipo, cupos, id_entrenador=None):
        s = Schedule(self._id_counter, fecha, hora_inicio, hora_fin,
                     tipo, cupos, id_entrenador)
        self.schedules.append(s)
        self._id_counter += 1
        self.save_schedules()
        return s

    def get_schedules(self):
        return self.schedules

    def get_by_id(self, id_horario):
        for s in self.schedules:
            if s.id_horario == id_horario:
                return s
        return None

    def update_schedule(self, id_horario, fecha=None, hora_inicio=None,
                        hora_fin=None, tipo=None, cupos=None, id_entrenador=None):
        s = self.get_by_id(id_horario)
        if not s:
            return False
        if fecha is not None:
            s.fecha = fecha
        if hora_inicio is not None:
            s.hora_inicio = hora_inicio
        if hora_fin is not None:
            s.hora_fin = hora_fin
        if tipo is not None:
            s.tipo = tipo
        if cupos is not None:
            s.cupos = cupos
        if id_entrenador is not None:
            s.id_entrenador = id_entrenador
        self.save_schedules()
        return True

    def delete_schedule(self, id_horario):
        s = self.get_by_id(id_horario)
        if s:
            self.schedules.remove(s)
            self.save_schedules()
            return True
        return False

    def filter_by_fecha(self, fecha):
        return [s for s in self.schedules if s.fecha == fecha]

    def filter_by_entrenador(self, id_entrenador):
        return [s for s in self.schedules if s.id_entrenador == id_entrenador]
