# navigation_service.py
# Servicio para manejar la navegación entre vistas en FitZone
# Documentado línea por línea en español

class NavigationService:
    """
    Servicio para manejar el historial de navegación.
    Permite avanzar y retroceder entre vistas.
    """

    def __init__(self):
        # Lista que guarda el historial de vistas
        self.history = []

    def navigate(self, stack, widget):
        """
        Navega hacia una nueva vista y la guarda en el historial.
        """
        self.history.append(widget)
        stack.setCurrentWidget(widget)

    def back(self, stack):
        """
        Regresa a la vista anterior en el historial.
        """
        if len(self.history) > 1:
            # Elimina la vista actual
            self.history.pop()
            # Obtiene la vista anterior
            previous = self.history[-1]
            stack.setCurrentWidget(previous)