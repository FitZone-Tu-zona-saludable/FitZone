from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
from frontend.frontend.controllers.payment_controller import create_payment
from frontend.frontend.services.state_service import state


class PaymentRegisterView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout(self)
        self.amount_input = QLineEdit()
        self.method_input = QLineEdit('efectivo')
        self.reference_input = QLineEdit()
        layout.addRow('Monto', self.amount_input)
        layout.addRow('Metodo', self.method_input)
        layout.addRow('Referencia', self.reference_input)
        btn = QPushButton('Registrar pago')
        btn.clicked.connect(self.register_payment)
        layout.addRow(btn)
        membership = state.get('selected_membership')
        if membership:
            self.amount_input.setText(str(membership.get('price', '')))

    def register_payment(self):
        result = create_payment(self.amount_input.text(), self.method_input.text(), self.reference_input.text())
        if result.get('success'):
            QMessageBox.information(self, 'Exito', 'Pago registrado en estado pendiente')
        else:
            QMessageBox.warning(self, 'Error', result.get('message', 'No se pudo registrar el pago'))
