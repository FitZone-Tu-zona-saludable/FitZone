from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Worker:
    _fields = ('id_trabajador', 'nombre', 'cargo', 'telefono', 'correo', 'experiencia', 'modalidad', 'revision_medica', 'documento')

    def __init__(self, id_trabajador, nombre, cargo, telefono, correo,
                 experiencia="", modalidad="presencial", revision_medica=False,
                 documento=""):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.cargo = cargo
        self.telefono = telefono
        self.correo = correo
        self.experiencia = experiencia
        self.modalidad = modalidad
        self.revision_medica = revision_medica
        self.documento = documento

    def get_name(self):
        return self.nombre

    def get_cargo(self):
        return self.cargo

    def to_dict(self):
        return {
            "id_trabajador": self.id_trabajador,
            "nombre": self.nombre,
            "cargo": self.cargo,
            "telefono": self.telefono,
            "correo": self.correo,
            "experiencia": self.experiencia,
            "modalidad": self.modalidad,
            "revision_medica": self.revision_medica,
            "documento": self.documento,
        }
