class Client:
    def __init__(self, id_cliente, nombre, cedula, telefono, correo, estado_membresia):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo
        self.estado_membresia = estado_membresia

        self.payments = []  # relación con pagos

    def get_name(self):
        return self.nombre

    def get_email(self):
        return self.correo

    def get_role(self):
        return "client"

    def registrar(self):
        return "Cliente registrado"

    def iniciar_sesion(self):
        return "Sesión iniciada"

    def eliminar_cuenta(self):
        return "Cuenta eliminada"