import json
import os
from src.models.worker import Worker
from src.models.employee import Employee


class WorkerService:
    """Servicio CRUD de trabajadores y empleados con persistencia JSON."""

    def __init__(self):
        self.workers = []
        self.worker_file = "data/workers.json"
        self._id_counter = 1
        self.load_workers()

    # ─── PERSISTENCIA ────────────────────────────────────────────────
    def load_workers(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.worker_file):
            with open(self.worker_file, "r") as f:
                data = json.load(f)
            self.workers = []
            for d in data:
                if d.get("tipo") == "empleado":
                    w = Employee(
                        d["id_trabajador"], d["nombre"], d["cargo"],
                        d["telefono"], d["correo"], d.get("experiencia", ""),
                        d.get("modalidad", "presencial"),
                        d.get("revision_medica", False),
                        d.get("fecha_ingreso", ""),
                        d.get("tipo_contrato", "indefinido")
                    )
                else:
                    w = Worker(
                        d["id_trabajador"], d["nombre"], d["cargo"],
                        d["telefono"], d["correo"], d.get("experiencia", ""),
                        d.get("modalidad", "presencial"),
                        d.get("revision_medica", False)
                    )
                self.workers.append(w)
                if d["id_trabajador"] >= self._id_counter:
                    self._id_counter = d["id_trabajador"] + 1

    def save_workers(self):
        os.makedirs("data", exist_ok=True)
        data = []
        for w in self.workers:
            d = w.to_dict()
            d["tipo"] = "empleado" if isinstance(w, Employee) else "trabajador"
            data.append(d)
        with open(self.worker_file, "w") as f:
            json.dump(data, f, indent=4)

    # ─── ALTA TRABAJADOR ────────────────────────────────────────────
    def create_worker(self, nombre, cargo, telefono, correo,
                      experiencia="", modalidad="presencial", revision_medica=False):
        w = Worker(self._id_counter, nombre, cargo, telefono, correo,
                   experiencia, modalidad, revision_medica)
        self.workers.append(w)
        self._id_counter += 1
        self.save_workers()
        return w

    # ─── REGISTRO EMPLEADO ──────────────────────────────────────────
    def register_employee(self, nombre, cargo, telefono, correo,
                          experiencia="", modalidad="presencial",
                          revision_medica=False,
                          fecha_ingreso="", tipo_contrato="indefinido"):
        e = Employee(self._id_counter, nombre, cargo, telefono, correo,
                     experiencia, modalidad, revision_medica,
                     fecha_ingreso, tipo_contrato)
        self.workers.append(e)
        self._id_counter += 1
        self.save_workers()
        return e

    # ─── CONSULTA ───────────────────────────────────────────────────
    def get_workers(self):
        return self.workers

    def get_employees(self):
        return [w for w in self.workers if isinstance(w, Employee)]

    def get_by_id(self, id_trabajador):
        for w in self.workers:
            if w.id_trabajador == id_trabajador:
                return w
        return None

    def update_worker(self, id_trabajador, **kwargs):
        w = self.get_by_id(id_trabajador)
        if not w:
            return False
        for key, val in kwargs.items():
            if hasattr(w, key):
                setattr(w, key, val)
        self.save_workers()
        return True

    def delete_worker(self, id_trabajador):
        w = self.get_by_id(id_trabajador)
        if w:
            self.workers.remove(w)
            self.save_workers()
            return True
        return False
