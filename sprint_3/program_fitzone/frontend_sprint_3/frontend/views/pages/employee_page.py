# employee_page.py
# Vista de registro y administración de empleados/trabajadores en FitZone
# Ahora conectada al controlador real EmployeeController
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QComboBox
from PySide6.QtCore import Qt

# Importamos el controlador que conecta con el backend
from frontend.controllers.employee_controller import EmployeeController


class EmployeePage(QWidget):
    """
    Vista para registrar y administrar empleados/trabajadores.
    Contiene un formulario con datos personales, cargo, experiencia, modalidad y revisión médica.
    """

    def __init__(self):
        super().__init__()

        # Inicializamos el controlador para interactuar con el backend
        self.controller = EmployeeController()

        # Configuración inicial de la ventana
        self.setWindowTitle("Registro de Empleados - FitZone")
        self.resize(600, 400)

        # Construcción de la interfaz
        self.init_ui()

    def init_ui(self):
        """
        Construye la interfaz gráfica del formulario de empleados.
        """
        layout = QVBoxLayout()

        # Título principal
        title = QLabel("Registro de Empleados")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(title)

        # Formulario de datos
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo")
        self.name_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                      "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        form_layout.addRow("Nombre completo:", self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        self.email_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                       "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        form_layout.addRow("Correo electrónico:", self.email_input)

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Cargo")
        self.role_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                      "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        form_layout.addRow("Cargo:", self.role_input)

        self.experience_input = QLineEdit()
        self.experience_input.setPlaceholderText("Experiencia (años)")
        self.experience_input.setStyleSheet("color: black; background-color: white; padding: 6px; "
                                            "border: 1px solid #ccc; border-radius: 5px; font-size: 14px;")
        form_layout.addRow("Experiencia (años):", self.experience_input)

        self.modality_input = QComboBox()
        self.modality_input.addItems(["Tiempo completo", "Medio tiempo", "Contrato"])
        form_layout.addRow("Modalidad:", self.modality_input)

        self.medical_input = QComboBox()
        self.medical_input.addItems(["Aprobada", "Pendiente", "No aprobada"])
        form_layout.addRow("Revisión médica:", self.medical_input)

        layout.addLayout(form_layout)

        # Botón para registrar empleado
        btn_register = QPushButton("Registrar empleado")
        btn_register.setStyleSheet("background-color: #27ae60; color: white; padding: 6px; border-radius: 5px;")
        btn_register.clicked.connect(self.register_employee)
        layout.addWidget(btn_register)

        # Asignar layout principal
        self.setLayout(layout)

    def register_employee(self):
        """
        Acción para registrar un nuevo empleado usando el controlador real.
        """
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_input.text().strip()
        experience = self.experience_input.text().strip()
        modality = self.modality_input.currentText()
        medical = self.medical_input.currentText()

        if not name or not email or not role or not experience:
            QMessageBox.warning(self, "Aviso", "Completa todos los campos obligatorios.")
            return

        # Llamamos al controlador para registrar el empleado en el backend
        result = self.controller.add_employee(name, role, modality, email)

        if result:
            QMessageBox.information(
                self,
                "Registro exitoso",
                f"Empleado {name} registrado correctamente.\nCargo: {role}\nExperiencia: {experience} años\nModalidad: {modality}\nRevisión médica: {medical}"
            )
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el empleado en el sistema.")