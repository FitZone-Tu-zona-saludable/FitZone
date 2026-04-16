from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from frontend.frontend.controllers.payment_controller import load_payments, verify_payment


class PaymentVerificationView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.load_data()

    def load_data(self):
        self.clear_layout()
        data = load_payments()
        if not data:
            self.layout.addWidget(QLabel('No hay pagos registrados'))
            return
        for p in data:
            label = QLabel(f"{p['user']} - ${p['amount']} - {p['status']}")
            btn = QPushButton('Verificar')
            btn.setEnabled(str(p.get('status', '')).lower() != 'paid')
            btn.clicked.connect(partial(self.handle_verify, p['id']))
            self.layout.addWidget(label)
            self.layout.addWidget(btn)

    def handle_verify(self, payment_id):
        result = verify_payment(payment_id)
        if result.get('success'):
            QMessageBox.information(self, 'Exito', 'Pago verificado correctamente')
            self.load_data()
        else:
            QMessageBox.warning(self, 'Error', result.get('message', 'No se pudo verificar'))

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
