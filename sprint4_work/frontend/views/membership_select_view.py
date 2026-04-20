# membership_select_view.py
# Vista para mostrar el detalle de una membresía seleccionada en FitZone
# Ahora conectada al controlador real MembershipController
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from frontend.controllers.membership_controller import MembershipController


class MembershipSelectView(QWidget):
    """
    Vista para mostrar el detalle de una membresía seleccionada.
    Permite confirmar la selección y registrar la membresía en el backend.
    """

    def __init__(self):
        super().__init__()

        # Controlador real de membresías
        self.controller = MembershipController()

        # Membresía seleccionada
        self.membership = None

        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Título
        title = QLabel('Detalle de Membresía')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Etiquetas para mostrar datos
        self.label_name = QLabel('')
        self.label_price = QLabel('')
        self.label_benefits = QLabel('')
        self.label_benefits.setWordWrap(True)

        layout.addWidget(self.label_name)
        layout.addWidget(self.label_price)
        layout.addWidget(self.label_benefits)

        # Botón de confirmación
        self.btn_confirm = QPushButton('Confirmar')
        self.btn_confirm.clicked.connect(self.confirm_selection)
        layout.addWidget(self.btn_confirm, alignment=Qt.AlignCenter)

        # Botón de volver (callback asignado desde MainPage)
        self.btn_back = QPushButton('Volver')
        layout.addWidget(self.btn_back, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def set_membership(self, membership):
        """
        Asigna la membresía seleccionada y muestra sus datos en la interfaz.
        """
        self.membership = membership
        if not membership:
            self.label_name.setText('Sin datos')
            self.label_price.setText('')
            self.label_benefits.setText('')
            return

        self.label_name.setText(membership.get('name', ''))
        self.label_price.setText(f"Precio: ${membership.get('price', 0)}")
        self.label_benefits.setText(f"Beneficios: {membership.get('benefits', '')}")

    def confirm_selection(self):
        """
        Confirma la selección de la membresía usando el controlador real.
        """
        if not self.membership:
            QMessageBox.warning(self, 'Aviso', 'No hay membresía seleccionada')
            return

        # Aquí deberíamos pasar también el user_id real
        result = self.controller.select_membership(user_id=1, membership_id=self.membership.get('id'))

        if result and result.get('success'):
            QMessageBox.information(
                self,
                'Éxito',
                f"Membresía seleccionada correctamente. ID asignado: {result['membership_id']}"
            )
        else:
            QMessageBox.critical(self, 'Error', result.get('message', 'No se pudo seleccionar la membresía'))