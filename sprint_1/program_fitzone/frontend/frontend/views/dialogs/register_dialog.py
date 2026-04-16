from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from frontend.frontend.controllers.auth_controller import create_account


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Crear cuenta')
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(['client', 'admin', 'seguridad'])
        self.role_input.setCurrentText('client')

        layout.addRow('Nombre', self.name_input)
        layout.addRow('Correo', self.email_input)
        layout.addRow('Contrasena', self.password_input)
        layout.addRow('Rol', self.role_input)

        btn = QPushButton('Guardar')
        btn.clicked.connect(self.save)
        layout.addRow(btn)

    def save(self):
        result = create_account(
            self.name_input.text(),
            self.email_input.text(),
            self.password_input.text(),
            self.role_input.currentText(),
        )
        if result.get('success'):
            QMessageBox.information(self, 'OK', 'Usuario registrado correctamente')
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', result.get('message', 'No fue posible registrar'))
