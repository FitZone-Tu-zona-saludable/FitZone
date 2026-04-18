class Report:
    def __init__(self, tipo, contenido):
        self.tipo = tipo
        self.contenido = contenido

    def generar(self):
        return "Reporte generado"
