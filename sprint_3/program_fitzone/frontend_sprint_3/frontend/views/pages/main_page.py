# main_page.py
# Página principal de FitZone con menú lateral y vistas dinámicas
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt

# Importa las vistas existentes
from frontend.views.membership_list_view import MembershipListView
from frontend.views.membership_select_view import MembershipSelectView
from frontend.views.payment_verification_view import PaymentVerificationView
from frontend.views.payment_register_view import PaymentRegisterView
from frontend.views.security_view import SecurityView

# Importa las nuevas vistas del Sprint 2
from frontend.views.pages.schedule_page import SchedulePage
from frontend.views.pages.trainer_page import TrainerPage
from frontend.views.pages.employee_page import EmployeePage
from frontend.views.pages.alerts_page import AlertsPage
from frontend.services.alert_service import AlertService
from frontend.views.pages.sprint3_page import Sprint3Page


class MainPage(QWidget):
    """
    Clase principal que contiene el menú lateral y las vistas dinámicas.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitZone")

        # Layout principal horizontal: menú lateral + área de vistas
        main_layout = QHBoxLayout(self)

        # Layout vertical para el menú lateral
        menu_layout = QVBoxLayout()

        # Título en la parte superior del menú
        title_label = QLabel("Panel de Control FitZone")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        menu_layout.addWidget(title_label)

        # Botones del menú lateral (cada uno con estilo para que se vea el texto)
        btn_memberships = QPushButton("Membresías")
        btn_memberships.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_memberships)

        btn_select_membership = QPushButton("Seleccionar Membresía")
        btn_select_membership.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_select_membership)

        btn_register_payment = QPushButton("Registrar Pago")
        btn_register_payment.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_register_payment)

        btn_verify_payment = QPushButton("Verificar Pago")
        btn_verify_payment.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_verify_payment)

        btn_security = QPushButton("Seguridad")
        btn_security.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_security)

        btn_schedule = QPushButton("Horarios")
        btn_schedule.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_schedule)

        btn_trainer = QPushButton("Entrenadores")
        btn_trainer.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_trainer)

        btn_employee = QPushButton("Empleados")
        btn_employee.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_employee)

        btn_alerts = QPushButton("Alertas")
        btn_alerts.setStyleSheet("color: black; font-size: 14px;")
        menu_layout.addWidget(btn_alerts)

        # Widget apilado para cambiar entre vistas dinámicamente
        self.stack = QStackedWidget()

        # Instancia de cada vista
        self.membership_list_view = MembershipListView()
        self.membership_select_view = MembershipSelectView()
        self.payment_register_view = PaymentRegisterView()
        self.payment_verification_view = PaymentVerificationView()
        self.security_view = SecurityView()
        self.schedule_page = SchedulePage()
        self.trainer_page = TrainerPage()
        self.employee_page = EmployeePage()
        self.alerts_page = AlertsPage(AlertService())
