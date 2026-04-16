from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from frontend.frontend.views.schedule_view import ScheduleView
from frontend.frontend.views.membership_list_view import MembershipListView
from frontend.frontend.views.membership_select_view import MembershipSelectView
from frontend.frontend.views.payment_verification_view import PaymentVerificationView
from frontend.frontend.views.payment_register_view import PaymentRegisterView
from frontend.frontend.views.logs_view import LogsView
from frontend.frontend.services.state_service import state


class MainPage(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle('FitZone')
        self.resize(1000, 600)
        self.payment_register_view = PaymentRegisterView()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        menu_layout = QVBoxLayout()
        user = state.get('user') or {}
        title = QLabel(f"FITZONE\n{user.get('username', '')} ({self.role})")
        title.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(title)

        self.stack = QStackedWidget()
        self.schedules_view = ScheduleView()
        self.memberships_view = MembershipListView()
        self.membership_select_view = MembershipSelectView()
        self.payment_verification_view = PaymentVerificationView()
        self.logs_view = LogsView()

        self.stack.addWidget(self.schedules_view)
        self.stack.addWidget(self.memberships_view)
        self.stack.addWidget(self.membership_select_view)
        self.stack.addWidget(self.payment_register_view)
        self.stack.addWidget(self.payment_verification_view)
        self.stack.addWidget(self.logs_view)

        buttons = []
        btn_schedule = QPushButton('Horarios')
        btn_schedule.clicked.connect(lambda: self.navigate(self.schedules_view))
        buttons.append(btn_schedule)

        if self.role == 'client':
            btn_memberships = QPushButton('Tarifas y membresias')
            btn_memberships.clicked.connect(lambda: self.navigate(self.memberships_view))
            buttons.append(btn_memberships)

            btn_payment = QPushButton('Registrar pago')
            btn_payment.clicked.connect(lambda: self.refresh_payment_view())
            buttons.append(btn_payment)

        if self.role in ['admin', 'seguridad']:
            btn_verify = QPushButton('Verificar pagos')
            btn_verify.clicked.connect(lambda: self.refresh_verify_view())
            buttons.append(btn_verify)

            btn_logs = QPushButton('Bitacora')
            btn_logs.clicked.connect(lambda: self.refresh_logs_view())
            buttons.append(btn_logs)

        for btn in buttons:
            btn.setFixedHeight(40)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        self.memberships_view.open_selection = self.go_to_membership_selection
        self.membership_select_view.btn_back.clicked.connect(lambda: self.navigate(self.memberships_view))
        self.membership_select_view.btn_confirm.clicked.connect(lambda: self.payment_register_view.amount_input.setText(str((state.get('selected_membership') or {}).get('price', ''))))

        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.stack, 4)
        self.navigate(self.schedules_view)

    def navigate(self, widget):
        self.stack.setCurrentWidget(widget)

    def go_to_membership_selection(self, membership):
        self.membership_select_view.set_membership(membership)
        self.navigate(self.membership_select_view)

    def refresh_payment_view(self):
        self.stack.removeWidget(self.payment_register_view)
        self.payment_register_view.deleteLater()
        self.payment_register_view = PaymentRegisterView()
        self.stack.insertWidget(3, self.payment_register_view)
        self.navigate(self.payment_register_view)

    def refresh_verify_view(self):
        self.payment_verification_view.load_data()
        self.navigate(self.payment_verification_view)

    def refresh_logs_view(self):
        self.logs_view.refresh()
        self.navigate(self.logs_view)
