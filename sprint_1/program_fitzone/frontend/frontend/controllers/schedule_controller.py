# =========================
# controllers/schedule_controller.py
# =========================

"""
===========================================================
SCHEDULE CONTROLLER
===========================================================

ES:
Controlador de horarios.

Responsabilidades:
- Obtener horarios desde datos simulados
- Servir datos a la vista

EN:
Handles schedule data retrieval.
===========================================================
"""

# IMPORT CORREGIDO (IMPORTANTE)
from frontend.frontend.services.data.mock_data import get_schedules


def load_schedules():
    """
    Retorna la lista de horarios disponibles.
    """
    return get_schedules()