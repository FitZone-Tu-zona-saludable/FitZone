from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from frontend.views.staff_register_view import StaffRegisterView

class EmployeePage(QWidget):
    def __init__(self, role="admin"):
        super().__init__()  
        # Inicializa la clase base QWidget para que EmployeePage sea una ventana de Qt.
        
        self.role = role  
        # Guarda el rol del usuario (por defecto "admin") como atributo de la instancia.
        # Esto permite condicionar qué interfaz se muestra según el rol.

        self._build_ui()  
        # Llama al método interno que construye la interfaz gráfica.

    def _build_ui(self):
        layout = QVBoxLayout(self)  
        # Crea un layout vertical que organizará los widgets dentro de la ventana.

        if self.role != "admin":  
            # Si el rol NO es administrador...
            message = QLabel("Este módulo es exclusivo de administración.")  
            # Muestra un mensaje informativo restringiendo el acceso.
            
            message.setObjectName("Muted")  
            # Asigna un identificador al QLabel (útil para aplicar estilos vía CSS/Qt StyleSheets).
            
            layout.addWidget(message)  
            # Agrega el mensaje al layout.
            
            return  
            # Termina la construcción de la interfaz (no carga el formulario de empleados).

        self.staff_view = StaffRegisterView()  
        # Si el rol es "admin", crea la vista de registro de personal (otra clase importada).
        
        layout.addWidget(self.staff_view)  
        # Inserta esa vista dentro del layout principal.

    def on_activate(self):
        staff_view = getattr(self, "staff_view", None)  
        # Obtiene el atributo staff_view si existe, de lo contrario devuelve None.
        
        if staff_view and hasattr(staff_view, "on_activate"):  
            # Verifica que staff_view exista y que tenga el método on_activate.
            
            staff_view.on_activate()  
            # Llama al método on_activate de StaffRegisterView (ej. refrescar datos).