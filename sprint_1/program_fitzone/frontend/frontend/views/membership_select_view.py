from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from frontend.frontend.controllers.membership_controller import select_membership


class MembershipSelectView(QWidget):
    def __init__(self):
        super().__init__()
        self.membership = None
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        title = QLabel('Detalle de Membresia')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.label_name = QLabel('')
        self.label_price = QLabel('')
        self.label_duration = QLabel('')
        self.label_benefits = QLabel('')
        for label in [self.label_name, self.label_price, self.label_duration, self.label_benefits]:
            layout.addWidget(label)
        self.btn_confirm = QPushButton('Confirmar')
        self.btn_confirm.clicked.connect(self.confirm_selection)
        layout.addWidget(self.btn_confirm)
        self.btn_back = QPushButton('Volver')
        layout.addWidget(self.btn_back)

    def set_membership(self, membership):
        self.membership = membership
        if not membership:
            return
        self.label_name.setText(f"Plan: {membership.get('name', '')}")
        self.label_price.setText(f"Precio: ${membership.get('price', 0)}")
        self.label_duration.setText(f"Duracion: {membership.get('duration', 0)} dias")
        self.label_benefits.setText(f"Beneficios: {membership.get('benefits', '')}")

    def confirm_selection(self):
        if not self.membership:
            QMessageBox.warning(self, 'Aviso', 'No hay membresia seleccionada')
            return
        result = select_membership(self.membership)
        if result.get('success'):
            QMessageBox.information(self, 'Exito', 'Membresia seleccionada correctamente')
        else:
            QMessageBox.warning(self, 'Error', result.get('message', 'No se pudo seleccionar'))
