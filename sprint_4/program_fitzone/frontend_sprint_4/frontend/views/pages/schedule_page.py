# schedule_page.py
# Vista de consulta y administración de horarios en FitZone
# Ahora conectada al controlador real ScheduleController
# Documentado línea por línea en español

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from frontend.controllers.schedule_controller import ScheduleController


class SchedulePage(QWidget):
    """
    Vista para consultar y administrar horarios.
    Permite listar horarios existentes y crear/modificar clases o sesiones.
    """

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Horarios - FitZone")
        self.resize(800, 500)

        # Conexión con el controlador real
        self.controller = ScheduleController()

        # Construcción de la interfaz
        self.init_ui()

        # Cargar horarios desde el backend
        self.load_schedules()

    def init_ui(self):
        """
        Construye la interfaz gráfica de la página de horarios.
        """
        layout = QVBoxLayout()

        # Título principal
        title = QLabel("Gestión de Horarios")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(title)

        # Tabla para mostrar horarios
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Fecha", "Hora", "Entrenador", "Cupos", "Tipo de sesión"])
        layout.addWidget(self.table)

        # Botones de acción
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Agregar horario")
        btn_add.setStyleSheet("background-color: #27ae60; color: white; padding: 6px; border-radius: 5px;")
        btn_add.clicked.connect(self.add_schedule)
        btn_layout.addWidget(btn_add)

        btn_edit = QPushButton("Editar horario")
        btn_edit.setStyleSheet("background-color: #2980b9; color: white; padding: 6px; border-radius: 5px;")
        btn_edit.clicked.connect(self.edit_schedule)
        btn_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Eliminar horario")
        btn_delete.setStyleSheet("background-color: #c0392b; color: white; padding: 6px; border-radius: 5px;")
        btn_delete.clicked.connect(self.delete_schedule)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

        # Asignar layout principal
        self.setLayout(layout)

    def load_schedules(self):
        """
        Carga horarios desde el controlador en la tabla.
        """
        data = self.controller.list_schedules()
        self.table.setRowCount(len(data))
        for row, horario in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(horario["fecha"]))
            self.table.setItem(row, 1, QTableWidgetItem(horario["hora"]))
            self.table.setItem(row, 2, QTableWidgetItem(horario["entrenador"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(horario["cupos"])))
            self.table.setItem(row, 4, QTableWidgetItem(horario["tipo"]))

    def add_schedule(self):
        """
        Acción para agregar un nuevo horario usando el controlador real.
        """
        result = self.controller.add_schedule("2026-04-25", "09:00", "Nuevo Entrenador", 10, "Pilates")
        if result:
            QMessageBox.information(self, "Agregar horario", "Horario agregado correctamente.")
            self.load_schedules()
        else:
            QMessageBox.critical(self, "Error", "No se pudo agregar el horario.")

    def edit_schedule(self):
        """
        Acción para editar un horario seleccionado usando el controlador real.
        """
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Editar horario", "Selecciona un horario primero.")
            return

        schedule_id = selected  # En el futuro se usará el ID real del backend
        result = self.controller.edit_schedule(schedule_id, hora="11:00")
        if result:
            QMessageBox.information(self, "Editar horario", "Horario editado correctamente.")
            self.load_schedules()
        else:
            QMessageBox.critical(self, "Error", "No se pudo editar el horario.")

    def delete_schedule(self):
        """
        Acción para eliminar un horario seleccionado usando el controlador real.
        """
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Eliminar horario", "Selecciona un horario primero.")
            return

        schedule_id = selected  # En el futuro se usará el ID real del backend
        result = self.controller.delete_schedule(schedule_id)
        if result:
            QMessageBox.information(self, "Eliminar horario", "Horario eliminado correctamente.")
            self.load_schedules()
        else:
            QMessageBox.critical(self, "Error", "No se pudo eliminar el horario.")