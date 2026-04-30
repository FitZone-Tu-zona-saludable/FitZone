from src.models.model_accessors import encapsulated_model
@encapsulated_model
class Report:
    _fields = ('tipo', 'contenido')

    def __init__(self, tipo, contenido):
        self.tipo = tipo
        self.contenido = contenido

    def generar(self):
        return "Reporte generado"
