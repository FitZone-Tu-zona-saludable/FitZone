from src.services.json_storage import load_json_list, save_json_list
from datetime import datetime
from src.models.attendance import Attendance


class AttendanceService:
    """Registro de asistencia de clientes (Sprint 3 - Andrés).
    Soporta: register() para frontend y registrar_entrada() para tests.
    """

    def __init__(self):
        self.attendances = []
        self.file = "data/attendance.json"
        self._id_counter = 1
        self.load()

    def load(self):
        data = load_json_list(self.file)
        self.attendances = []
        for d in data:
                a = Attendance(
                    d["id_asistencia"], d["id_cliente"], d["nombre_cliente"],
                    d.get("fecha"),
                    d.get("clase", d.get("clase_servicio", "")),
                    d.get("servicio", ""),
                    d.get("observaciones", "")
                )
                self.attendances.append(a)
                if d["id_asistencia"] >= self._id_counter:
                    self._id_counter = d["id_asistencia"] + 1

    def save(self):
        save_json_list(self.file, [a.to_dict() for a in self.attendances])

    # API frontend (sprint5)
    def register(self, id_cliente, nombre_cliente, clase="", servicio="",
                 observaciones=""):
        a = Attendance(self._id_counter, id_cliente, nombre_cliente,
                       clase=clase, servicio=servicio,
                       observaciones=observaciones)
        self.attendances.append(a)
        self._id_counter += 1
        self.save()
        return a

    # API tests (sprint3/4)
    def registrar_entrada(self, id_cliente, nombre_cliente,
                          clase_servicio="", observaciones=""):
        return self.register(
            id_cliente,
            nombre_cliente,
            clase=clase_servicio,
            observaciones=observaciones,
        )

    def actualizar_asistencia(self, id_asistencia, **kwargs):
        return self.update(id_asistencia, **kwargs)

    def update(self, id_asistencia, **kwargs):
        for a in self.attendances:
            if a.id_asistencia == id_asistencia:
                for k, v in kwargs.items():
                    if hasattr(a, k):
                        setattr(a, k, v)
                self.save()
                return True
        return False

    def delete(self, id_asistencia):
        for a in self.attendances:
            if a.id_asistencia == id_asistencia:
                self.attendances.remove(a)
                self.save()
                return True
        return False

    def get_all(self):
        return self.attendances

    def get_by_id(self, id_asistencia):
        for a in self.attendances:
            if a.id_asistencia == id_asistencia:
                return a
        return None

    def get_by_cliente(self, id_cliente):
        return [a for a in self.attendances if a.id_cliente == id_cliente]

    def get_by_client(self, id_cliente):
        return self.get_by_cliente(id_cliente)

    def get_by_fecha(self, fecha):
        return [a for a in self.attendances if a.fecha and a.fecha.startswith(fecha)]

    def get_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_by_fecha(today)
