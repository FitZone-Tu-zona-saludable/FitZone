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
                d.get("id_entrenador"),
                d.get("enrolled_users", []),    # retrocompatible con JSON antiguo
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

    # ─── INSCRIPCIÓN DE USUARIOS ───────────────────────────────────────────
    def enroll_user(self, id_horario, user_id):
        """Inscribe a user_id en el horario. Valida cupos y duplicados."""
        s = self.get_by_id(id_horario)
        if not s:
            return {"success": False, "message": "Horario no encontrado"}
        if s.esta_lleno:
            return {
                "success": False,
                "message": f"Sin cupos disponibles (capacidad: {s.cupos})",
            }
        if s.is_enrolled(user_id):
            return {"success": False, "message": "Ya estás inscrito en este horario"}
        s.enrolled_users.append(str(user_id))
        self.save_schedules()
        return {
            "success": True,
            "message": (
                f"Inscripción exitosa en {s.tipo} del {s.fecha}. "
                f"Cupos restantes: {s.cupos_disponibles}"
            ),
            "cupos_disponibles": s.cupos_disponibles,
        }

    def unenroll_user(self, id_horario, user_id):
        """Cancela la inscripción de user_id en el horario."""
        s = self.get_by_id(id_horario)
        if not s:
            return {"success": False, "message": "Horario no encontrado"}
        uid_str = str(user_id)
        if uid_str not in [str(u) for u in s.enrolled_users]:
            return {"success": False, "message": "No tienes inscripción en este horario"}
        s.enrolled_users = [u for u in s.enrolled_users if str(u) != uid_str]
        self.save_schedules()
        return {"success": True, "message": "Inscripción cancelada correctamente"}

    def get_user_schedules(self, user_id):
        """Retorna los horarios en los que está inscrito user_id."""
        uid_str = str(user_id)
        return [s for s in self.schedules
                if uid_str in [str(u) for u in s.enrolled_users]]

    def list_with_availability(self, user_id=None):
        """
        Lista todos los horarios con información de disponibilidad.
        Si se pasa user_id, agrega el campo 'inscrito' a cada entrada.
        """
        result = []
        for s in self.schedules:
            d = s.to_dict()
            d["cupos_disponibles"] = s.cupos_disponibles
            d["esta_lleno"] = s.esta_lleno
            if user_id is not None:
                d["inscrito"] = s.is_enrolled(user_id)
            result.append(d)
        return result

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
