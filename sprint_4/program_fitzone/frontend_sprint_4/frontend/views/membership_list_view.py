# membership_list_view.py
# Vista para listar membresías disponibles en FitZone
# Ahora conectada al controlador real MembershipController
# Documentado línea por línea en español

from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from frontend.controllers.membership_controller import MembershipController


class MembershipListView(QWidget):
    """
    Vista para listar membresías disponibles.
    Permite al usuario consultar las tarifas y seleccionar una membresía.
    """

    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Controlador real de membresías
        self.controller = MembershipController()

        # Callback para abrir selección (se asigna desde MainPage)
        self.open_selection = None

        # Cargar datos iniciales
        self.load_data()

    def load_data(self):
        """
        Carga las membresías desde el controlador y las muestra en la interfaz.
        """
        self.clear_layout()
        data = self.controller.load_memberships()

        if not data:
            self.layout.addWidget(QLabel("No hay membresías disponibles"))
            return

        self.layout.addWidget(QLabel("Tarifas disponibles"))
        for m in data:
            # Formateo seguro de los datos
            price = m.get("price", 0.0)
            duration = m.get("duration", "")
            benefits = m.get("benefits", "")

            label_text = (
                f"{m.get('name', 'Sin nombre')} - ${price:.2f} - {duration} días\n"
                f"Beneficios: {benefits}"
            )
            label = QLabel(label_text)
            label.setWordWrap(True)

            # Botón para seleccionar membresía
            btn = QPushButton("Seleccionar")
            btn.clicked.connect(partial(self.on_select, m))

            self.layout.addWidget(label)
            self.layout.addWidget(btn)

    def on_select(self, membership):
        """
        Acción al seleccionar una membresía.
        Llama al callback definido en MainPage.
        """
        if callable(self.open_selection):
            self.open_selection(membership)

    def clear_layout(self):
        """
        Limpia el layout eliminando widgets previos.
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()