from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Client:
    _fields = ('id_cliente', 'nombre', 'correo', 'password', 'role', 'payments', 'membership')

    def __init__(self, id_cliente, nombre, correo, password, role):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.role = role
        self.payments = []
        self.membership = None

    def get_name(self):
        return self.nombre

    def get_email(self):
        return self.correo

    def get_role(self):
        return self.role
