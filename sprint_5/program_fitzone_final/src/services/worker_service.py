from src.services.json_storage import load_json_list, save_json_list
from src.models.worker import Worker
from src.models.employee import Employee


class WorkerService:
    """Servicio CRUD de trabajadores y empleados con persistencia JSON."""

    def __init__(self):
        self.workers = []
        self.worker_file = "data/workers.json"
        self._id_counter = 1
        self.load_workers()

    # Persistencia
    def load_workers(self):
        data = load_json_list(self.worker_file)
        self.workers = []
        for d in data:
            if d.get("tipo") == "empleado":
                datos_laborales = {
                    "fecha_ingreso": d.get("fecha_ingreso", ""),
                    "tipo_contrato": d.get("tipo_contrato", "indefinido"),
                    "estado_laboral": d.get("estado_laboral", "activo"),
                    "salario": d.get("salario", 0.0),
                    "descuento": d.get("descuento", 0.0),
                }
                w = Employee(
                    d["id_trabajador"], d["nombre"], d["cargo"],
                    d["telefono"], d["correo"], d.get("experiencia", ""),
                    d.get("modalidad", "presencial"),
                    d.get("revision_medica", False),
                    datos_laborales,
                    d.get("documento", ""),
                )
            else:
                w = Worker(
                    d["id_trabajador"], d["nombre"], d["cargo"],
                    d["telefono"], d["correo"], d.get("experiencia", ""),
                    d.get("modalidad", "presencial"),
                    d.get("revision_medica", False),
                    d.get("documento", ""),
                )
            self.workers.append(w)
            if d["id_trabajador"] >= self._id_counter:
                self._id_counter = d["id_trabajador"] + 1

    def save_workers(self):
        data = []
        for w in self.workers:
            d = w.to_dict()
            d["tipo"] = "empleado" if isinstance(w, Employee) else "trabajador"
            data.append(d)
        save_json_list(self.worker_file, data)

    # Alta trabajador
    def create_worker(self, nombre, cargo, telefono, correo,
                      experiencia="", modalidad="presencial",
                      revision_medica=False, documento=""):
        w = Worker(self._id_counter, nombre, cargo, telefono, correo,
                   experiencia, modalidad, revision_medica, documento)
        self.workers.append(w)
        self._id_counter += 1
        self.save_workers()
        return w

    # Registro empleado
    def register_employee(self, nombre, cargo, telefono, correo,
                          experiencia="", modalidad="presencial",
                          revision_medica=False,
                          fecha_ingreso="", tipo_contrato="indefinido",
                          estado_laboral="activo", salario=0.0,
                          descuento=0.0, documento=""):
        datos_laborales = {
            "fecha_ingreso": fecha_ingreso,
            "tipo_contrato": tipo_contrato,
            "estado_laboral": estado_laboral,
            "salario": salario,
            "descuento": descuento,
        }
        e = Employee(self._id_counter, nombre, cargo, telefono, correo,
                     experiencia, modalidad, revision_medica,
                     datos_laborales, documento)
        self.workers.append(e)
        self._id_counter += 1
        self.save_workers()
        return e

    # Consulta
    def get_workers(self):
        return self.workers

    def get_employees(self):
        return [w for w in self.workers if isinstance(w, Employee)]

    def get_by_id(self, id_trabajador):
        for w in self.workers:
            if w.id_trabajador == id_trabajador:
                return w
        return None

    # Actualizacion Sprint 3 Andres
    def update_worker(self, id_trabajador, **kwargs):
        w = self.get_by_id(id_trabajador)
        if not w:
            return False
        for key, val in kwargs.items():
            if hasattr(w, key):
                setattr(w, key, val)
        self.save_workers()
        return True

    def actualizar_estado_laboral(self, id_trabajador, nuevo_estado):
        """Actualiza estado laboral del empleado: activo, inactivo o incapacitado."""
        w = self.get_by_id(id_trabajador)
        if not w or not isinstance(w, Employee):
            return False, "Empleado no encontrado"
        ok = w.actualizar_estado(nuevo_estado)
        if ok:
            self.save_workers()
            return True, f"Estado actualizado a '{nuevo_estado}'"
        return False, f"Estado '{nuevo_estado}' no valido"

    def get_info_completa_empleado(self, id_trabajador):
        """Devuelve informacion completa del empleado, incluyendo salario neto."""
        w = self.get_by_id(id_trabajador)
        if not w or not isinstance(w, Employee):
            return None
        info = w.to_dict()
        info["salario_neto"] = w.salario_neto
        return info
