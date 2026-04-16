# =========================
# services/state_service.py
# =========================

"""
===========================================================
STATE SERVICE
===========================================================

ES:
Este módulo define el estado global de la aplicación.

Responsabilidades:
- Almacenar información compartida entre vistas
- Mantener datos temporales del usuario
- Evitar acoplamiento entre componentes

IMPORTANTE:
- No contiene lógica de negocio
- Solo almacena datos en memoria

EN:
Global state container for the application.
===========================================================
"""

# ===========================================================
# ESTADO GLOBAL
# ===========================================================

state = {
    "user": None,
    "memberships": [],
    "selected_membership": None,
    "payments": []
}