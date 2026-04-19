# payment_register_view.py
# Vista para registrar pagos en FitZone
# Ahora conectada al controlador real PaymentController y al servicio de alertas
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QLabel, QPushButton, QMessageBox
from frontend.controllers.membership_controller import MembershipController
from frontend.controllers.payment_controller import PaymentController
from frontend.services.alert_service import AlertService


class PaymentRegisterView(QWidget):
    """
    Vista para registrar pagos asociados a una membresía.
    Permite seleccionar la membresía, ingresar datos del pago y guardarlo en el backend.
    """

    def __init__(self):
        super().__init__()

        # Controladores reales
        self.membership_controller = MembershipController()
        self.payment_controller = PaymentController()

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Campos de entrada
        self.membership_combo = QComboBox()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Monto')
        self.amount_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                        "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")

        self.method_input = QLineEdit()
        self.method_input.setPlaceholderText('Método de pago')
        self.method_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                        "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")

        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText('Referencia')
        self.reference_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                           "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")

        # Construcción de la interfaz
        self.layout.addWidget(QLabel('Registrar pago'))
        self.layout.addWidget(self.membership_combo)
        self.layout.addWidget(self.amount_input)
        self.layout.addWidget(self.method_input)
        self.layout.addWidget(self.reference_input)

        # Botón para guardar pago
        btn = QPushButton('Guardar pago')
        btn.clicked.connect(self.save_payment)
        btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border-radius: 5px;")
        self.layout.addWidget(btn)

        # Cargar membresías del usuario
        self.reload_memberships()

    def reload_memberships(self):
        """
        Carga las membresías activas del usuario en el combo.
        """
        self.membership_combo.clear()
        memberships = self.membership_controller.load_user_memberships(user_id=1)  # Aquí se pasa el ID real del usuario
        for m in memberships:
            self.membership_combo.addItem(
                f"{m['name']} - ${m['price']} ({m['status']})",
                m['id']
            )

    def save_payment(self):
        """
        Registra un nuevo pago usando el controlador real y muestra alertas.
        """
        membership_id = self.membership_combo.currentData()
        if membership_id is None:
            AlertService.warning(self, 'Aviso', 'Primero debes seleccionar una membresía.')
            return

        try:
            amount = float(self.amount_input.text().strip())
        except ValueError:
            AlertService.error(self, 'Error', 'Ingresa un monto válido.')
            return

        payment_data = {
            'membership_id': membership_id,
            'amount': amount,
            'method': self.method_input.text().strip() or 'Efectivo',
            'reference': self.reference_input.text().strip() or 'SIN-REF',
        }

        result = self.payment_controller.register_payment(payment_data)

        if result and result.get('success'):
            AlertService.info(self, 'Éxito', result.get('message', 'Pago registrado correctamente.'))
            # Limpiar campos
            self.amount_input.clear()
            self.method_input.clear()
            self.reference_input.clear()
        else:
            AlertService.error(self, 'Error', result.get('message', 'No se pudo registrar el pago.'))