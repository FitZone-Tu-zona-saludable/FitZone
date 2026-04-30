# frontend/main.py
# Función de arranque del frontend de FitZone
# Documentado línea por línea en español

import sys
from PySide6.QtWidgets import QApplication
from frontend.views.login_view import LoginView


def run_frontend():
    """
    Inicializa la aplicación Qt para el frontend de FitZone.
    Aplica un estilo global a los campos de texto (QLineEdit)
    para asegurar que el texto digitado sea visible.
    """

    # Crear la aplicación Qt con los argumentos del sistema
    app = QApplication(sys.argv)

    # Estilo global para todos los QLineEdit
    # Esto asegura que el texto digitado se vea negro sobre fondo blanco
    app.setStyleSheet("""
        QLineEdit {
            color: black;                  /* Texto negro */
            background-color: white;       /* Fondo blanco */
            padding: 6px;                  /* Espaciado interno */
            border: 1px solid #ccc;        /* Borde gris */
            border-radius: 5px;            /* Bordes redondeados */
            font-size: 14px;               /* Tamaño de letra */
        }
    """)

    # Crear y mostrar la ventana de login del frontend
    window = LoginView()
    window.show()

    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec())