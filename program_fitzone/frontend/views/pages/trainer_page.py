# trainer_page.py
# Vista de consulta y administración de entrenadores en FitZone
# Ahora conectada al controlador real TrainerController
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from frontend.controllers.trainer_controller import TrainerController


class TrainerPage(QWidget):
    """
    Vista para consultar y administrar entrenadores.
    Permite listar entrenadores, agregar nuevos, editar datos y eliminarlos.
    """

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Entrenadores - FitZone")
        self.resize(800, 500)

        # Conexión con el controlador real
        self.controller = TrainerController()

        # Construcción de la interfaz
        self.init_ui()

        # Cargar entrenadores desde el backend
        self.load_trainers()

    def init_ui(self):
        """
        Construye la interfaz gráfica de la página de entrenadores.
        """
        layout = QVBoxLayout()

        # Título principal
        title = QLabel("Gestión de Entrenadores")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(title)

        # Tabla para mostrar entrenadores
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Especialidad", "Experiencia (años)", "Disponibilidad"])
        layout.addWidget(self.table)

        # Botones de acción
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Agregar entrenador")
        btn_add.setStyleSheet("background-color: #27ae60; color: white; padding: 6px; border-radius: 5px;")
        btn_add.clicked.connect(self.add_trainer)
        btn_layout.addWidget(btn_add)

        btn_edit = QPushButton("Editar entrenador")
        btn_edit.setStyleSheet("background-color: #2980b9; color: white; padding: 6px; border-radius: 5px;")
        btn_edit.clicked.connect(self.edit_trainer)
        btn_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Eliminar entrenador")
        btn_delete.setStyleSheet("background-color: #c0392b; color: white; padding: 6px; border-radius: 5px;")
        btn_delete.clicked.connect(self.delete_trainer)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

        # Asignar layout principal
        self.setLayout(layout)

    def load_trainers(self):
        """
        Carga entrenadores desde el controlador en la tabla.
        """
        data = self.controller.list_trainers()
        self.table.setRowCount(len(data))
        for row, trainer in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(trainer["nombre"]))
            self.table.setItem(row, 1, QTableWidgetItem(trainer["especialidad"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(trainer["experiencia"])))
            self.table.setItem(row, 3, QTableWidgetItem(trainer["disponibilidad"]))

    def add_trainer(self):
        """
        Acción para agregar un nuevo entrenador usando el controlador real.
        """
        # Aquí deberías abrir un formulario para capturar datos.
        # Por ahora mostramos un mensaje de ejemplo.
        result = self.controller.add_trainer("Nuevo Entrenador", "Especialidad X", 2, "Mañanas")
        if result:
            QMessageBox.information(self, "Agregar entrenador", "Entrenador agregado correctamente.")
            self.load_trainers()
        else:
            QMessageBox.critical(self, "Error", "No se pudo agregar el entrenador.")

    def edit_trainer(self):
        """
        Acción para editar un entrenador seleccionado usando el controlador real.
        """
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Editar entrenador", "Selecciona un entrenador primero.")
            return

        trainer_id = selected  # En el futuro se usará el ID real del backend
        result = self.controller.edit_trainer(trainer_id, nombre="Entrenador Editado")
        if result:
            QMessageBox.information(self, "Editar entrenador", "Entrenador editado correctamente.")
            self.load_trainers()
        else:
            QMessageBox.critical(self, "Error", "No se pudo editar el entrenador.")

    def delete_trainer(self):
        """
        Acción para eliminar un entrenador seleccionado usando el controlador real.
        """
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Eliminar entrenador", "Selecciona un entrenador primero.")
            return

        trainer_id = selected  # En el futuro se usará el ID real del backend
        result = self.controller.delete_trainer(trainer_id)
        if result:
            QMessageBox.information(self, "Eliminar entrenador", "Entrenador eliminado correctamente.")
            self.load_trainers()
        else:
            QMessageBox.critical(self, "Error", "No se pudo eliminar el entrenador.")