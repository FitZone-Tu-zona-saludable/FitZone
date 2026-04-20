from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from src.services.attendance_service import AttendanceService
from src.services.accounting_service import AccountingService
from src.services.incident_service import IncidentService
from src.services.evaluation_service import EvaluationService
from src.services.worker_service import WorkerService
from src.services.trainer_service import TrainerService
from src.services.schedule_service import ScheduleService
from src.services.notification_service import NotificationService


class AdminView(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

        # ── Instanciar servicios Sprint 3 ──────────────────────────
        self.attendance_svc  = AttendanceService()
        self.accounting_svc  = AccountingService()
        self.incident_svc    = IncidentService()
        self.eval_svc        = EvaluationService()
        self.worker_svc      = WorkerService()
        self.trainer_svc     = TrainerService()
        self.schedule_svc    = ScheduleService()
        self.notif_svc       = NotificationService()

        self.setWindowTitle("Panel Administrador – FitZone Sprint 3")
        self.setGeometry(200, 100, 900, 620)
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()

        # ── HEADER ─────────────────────────────────────────────────
        header_layout = QHBoxLayout()
        logo = QLabel()
        pixmap = QPixmap("src/assets/logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(40, 60))
        else:
            logo.setText("💪")

        title = QLabel("Panel Administrador – Sprint 3")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # ── TABS ────────────────────────────────────────────────────
        tabs = QTabWidget()

        tabs.addTab(self._tab_usuarios(), "👥 Usuarios")
        tabs.addTab(self._tab_sprint3(), "🏋️ Operación Sprint 3")

        main_layout.addWidget(tabs)

        # ── BOTÓN VOLVER ────────────────────────────────────────────
        btn_back = QPushButton("⬅ Volver")
        btn_back.setStyleSheet(self.button_style("#2d3436"))
        btn_back.clicked.connect(self.volver)
        main_layout.addWidget(btn_back)

        self.setLayout(main_layout)

    # ══════════════════════════════════════════════════════════════
    # TAB USUARIOS (funcionalidad Sprint 2 original)
    # ══════════════════════════════════════════════════════════════
    def _tab_usuarios(self):
        tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Nombre")
        self.name_input.setStyleSheet(self.input_style())
        self.email_input = QLineEdit(); self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet(self.input_style())
        self.password_input = QLineEdit(); self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        for label, color, fn in [
            ("➕ Crear", "#00b894", self.create_user),
            ("✏️ Editar", "#0984e3", self.update_user),
            ("🗑 Eliminar", "#d63031", self.delete_user),
            ("🔄 Refrescar", "#636e72", self.load_users),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(self.button_style(color))
            b.clicked.connect(fn)
            btn_layout.addWidget(b)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "Correo", "Rol"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellClicked.connect(self.select_user)
        layout.addWidget(self.table)

        tab.setLayout(layout)
        self.load_users()
        return tab

    # ══════════════════════════════════════════════════════════════
    # TAB SPRINT 3 – módulos de Andrés
    # ══════════════════════════════════════════════════════════════
    def _tab_sprint3(self):
        tab = QWidget()
        layout = QVBoxLayout()

        lbl = QLabel("Módulos operativos – Sprint 3 (Andrés)")
        lbl.setStyleSheet("font-size: 15px; font-weight: bold; padding: 8px;")
        layout.addWidget(lbl)

        grid1 = QHBoxLayout()
        grid2 = QHBoxLayout()

        modulos = [
            ("📋 Asistencia de Clientes", "#00b894", self._abrir_asistencia),
            ("💰 Contabilidad", "#e17055", self._abrir_contabilidad),
            ("👤 Empleados", "#0984e3", self._abrir_empleados),
            ("⚠️ Incidencias Personal", "#d63031", self._abrir_incidencias),
            ("📅 Horarios / Reasignación", "#6c5ce7", self._abrir_horarios),
            ("⭐ Evaluación Usuarios", "#fdcb6e", self._abrir_evaluaciones),
            ("🔔 Notificaciones Trabajadores", "#00cec9", self._abrir_notificaciones),
        ]
        for i, (label, color, fn) in enumerate(modulos):
            b = QPushButton(label)
            b.setStyleSheet(self.button_style(color) +
                            "QPushButton { min-height: 55px; font-size: 13px; }")
            b.clicked.connect(fn)
            (grid1 if i < 4 else grid2).addWidget(b)

        layout.addLayout(grid1)
        layout.addLayout(grid2)
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    # ── Abrir vistas Sprint 3 ──────────────────────────────────────
    def _abrir_asistencia(self):
        from src.ui.attendance_view import AttendanceView
        self._s3_win = AttendanceView(self.auth, self.attendance_svc)
        self._s3_win.show()

    def _abrir_contabilidad(self):
        from src.ui.accounting_view import AccountingView
        self._s3_win = AccountingView(self.auth, self.accounting_svc)
        self._s3_win.show()

    def _abrir_empleados(self):
        from src.ui.employee_view import EmployeeView
        self._s3_win = EmployeeView(self.worker_svc)
        self._s3_win.show()

    def _abrir_incidencias(self):
        from src.ui.incident_view import IncidentView
        self._s3_win = IncidentView(self.incident_svc, self.worker_svc)
        self._s3_win.show()

    def _abrir_horarios(self):
        from src.ui.schedule_reasign_view import ScheduleReasignView
        self._s3_win = ScheduleReasignView(self.schedule_svc, self.trainer_svc)
        self._s3_win.show()

    def _abrir_evaluaciones(self):
        from src.ui.evaluation_view import EvaluationView
        self._s3_win = EvaluationView(self.eval_svc, self.trainer_svc, self.auth)
        self._s3_win.show()

    def _abrir_notificaciones(self):
        """Muestra las notificaciones enviadas a trabajadores."""
        notifs = self.notif_svc.get_notifications_trabajador()
        if not notifs:
            QMessageBox.information(self, "Notificaciones", "No hay notificaciones para trabajadores aún.")
            return
        texto = "\n\n".join(
            f"[{n.get('fecha','')}] {n.get('tipo','').upper()}\n→ {n.get('destinatario','')}: {n.get('mensaje','')}"
            for n in notifs[-20:]
        )
        from PySide6.QtWidgets import QDialog, QTextEdit
        dlg = QDialog(self)
        dlg.setWindowTitle("Notificaciones – Trabajadores")
        dlg.resize(700, 400)
        v = QVBoxLayout()
        te = QTextEdit(); te.setReadOnly(True); te.setPlainText(texto)
        v.addWidget(te)
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(dlg.close)
        v.addWidget(btn_close)
        dlg.setLayout(v)
        dlg.exec()

    # ── CRUD usuarios (Sprint 2) ───────────────────────────────────
    def input_style(self):
        return "QLineEdit { padding: 8px; border: 1px solid #dcdde1; border-radius: 6px; }"

    def button_style(self, color):
        return (f"QPushButton {{ background-color: {color}; color: white; "
                f"padding: 8px; border-radius: 6px; font-weight: bold; }}"
                f"QPushButton:hover {{ background-color: #2d3436; }}")

    def load_users(self):
        users = self.auth.get_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.get_name()))
            self.table.setItem(row, 1, QTableWidgetItem(user.get_email()))
            self.table.setItem(row, 2, QTableWidgetItem(user.get_role()))

    def select_user(self, row, column):
        self.name_input.setText(self.table.item(row, 0).text())
        self.email_input.setText(self.table.item(row, 1).text())

    def create_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        if name and email and password:
            self.auth.create_user(name, email, password, "user")
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario creado")
        else:
            QMessageBox.warning(self, "Error", "Completa todos los campos")

    def update_user(self):
        email = self.email_input.text()
        name = self.name_input.text()
        if self.auth.update_user(email, name):
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario actualizado")
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

    def delete_user(self):
        email = self.email_input.text()
        if self.auth.delete_user(email):
            self.load_users()
            QMessageBox.information(self, "OK", "Usuario eliminado")
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

    def volver(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
