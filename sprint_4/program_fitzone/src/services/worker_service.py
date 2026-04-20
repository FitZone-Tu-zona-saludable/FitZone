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
                        d.get("tipo_contrato", "indefinido"),
                        d.get("estado_laboral", "activo"),
                        d.get("salario", 0.0),
                        d.get("descuento", 0.0)
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
            json.dump(data, f, indent=4, ensure_ascii=False)

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
                          fecha_ingreso="", tipo_contrato="indefinido",
                          estado_laboral="activo", salario=0.0, descuento=0.0):
        e = Employee(self._id_counter, nombre, cargo, telefono, correo,
                     experiencia, modalidad, revision_medica,
                     fecha_ingreso, tipo_contrato,
                     estado_laboral, salario, descuento)
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

    # ─── ACTUALIZACIÓN (Sprint 3 - Andrés) ──────────────────────────
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
        """Actualiza estado laboral del empleado: activo / inactivo / incapacitado."""
        w = self.get_by_id(id_trabajador)
        if not w or not isinstance(w, Employee):
            return False, "Empleado no encontrado"
        ok = w.actualizar_estado(nuevo_estado)
        if ok:
            self.save_workers()
            return True, f"Estado actualizado a '{nuevo_estado}'"
        return False, f"Estado '{nuevo_estado}' no válido"

    def get_info_completa_empleado(self, id_trabajador):
        """
        Devuelve un diccionario con la información completa del empleado,
        incluyendo descuentos, modalidad de pago y salario neto.
        """
        w = self.get_by_id(id_trabajador)
        if not w or not isinstance(w, Employee):
            return None
        info = w.to_dict()
        info["salario_neto"] = w.salario_neto
        return info

    def delete_worker(self, id_trabajador):
        w = self.get_by_id(id_trabajador)
        if w:
            self.workers.remove(w)
            self.save_workers()
            return True
        return False
