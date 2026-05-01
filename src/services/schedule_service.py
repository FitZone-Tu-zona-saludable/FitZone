from src.services.json_storage import load_json_list, save_json_list
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
        data = load_json_list(self.schedule_file)
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
        save_json_list(self.schedule_file, [s.to_dict() for s in self.schedules])

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

    # ─── REASIGNACIÓN POR EVENTOS EXTERNOS (Sprint 3 - Andrés) ───────
    def modificar_por_evento_externo(self, id_horario, nueva_fecha=None,
                                      nueva_hora_inicio=None, nueva_hora_fin=None,
                                      motivo="evento externo"):
        """
        Modifica un horario por eventos externos (cortes, feriados, emergencias).
        Registra el motivo del cambio y retorna el horario actualizado.
        """
        s = self.get_by_id(id_horario)
        if not s:
            return None, "Horario no encontrado"
        if nueva_fecha:
            s.fecha = nueva_fecha
        if nueva_hora_inicio:
            s.hora_inicio = nueva_hora_inicio
        if nueva_hora_fin:
            s.hora_fin = nueva_hora_fin
        self.save_schedules()
        return s, f"Horario #{id_horario} modificado por: {motivo}"

    def reasignar_entrenador(self, id_horario, id_nuevo_entrenador,
                              trainer_service):
        """
        Reasigna un entrenador disponible a un horario.
        Valida disponibilidad antes de asignar.
        """
        s = self.get_by_id(id_horario)
        if not s:
            return False, "Horario no encontrado"

        nuevo = trainer_service.get_by_id(id_nuevo_entrenador)
        if not nuevo:
            return False, "Entrenador no encontrado"
        if not nuevo.disponible:
            return False, f"{nuevo.nombre} no está disponible para reasignación"

        s.id_entrenador = id_nuevo_entrenador
        self.save_schedules()
        return True, f"Entrenador {nuevo.nombre} asignado al horario #{id_horario}"
