# =========================
# services/data/mock_data.py
# =========================

"""
===========================================================
MOCK DATA
===========================================================

ES:
Datos simulados del sistema.

Responsabilidades:
- Proveer datos de prueba
- Simular backend

EN:
Mock data provider.
===========================================================
"""

# ===========================================================
# MEMBERSHIPS
# ===========================================================

def get_memberships():
    return [
        {"id": 1, "name": "Básica", "price": 50},
        {"id": 2, "name": "Premium", "price": 80},
        {"id": 3, "name": "VIP", "price": 120},
    ]


# ===========================================================
# PAYMENTS
# ===========================================================

def get_payments():
    return [
        {"id": 1, "user": "Juan", "amount": 50, "status": "Pending"},
        {"id": 2, "user": "Ana", "amount": 80, "status": "Pending"},
        {"id": 3, "user": "Carlos", "amount": 120, "status": "Paid"},
    ]


# ===========================================================
# SCHEDULES  ←   ESTA ES LA QUE FALTA
# ===========================================================

def get_schedules():
    return [
        {"id": 1, "day": "Lunes", "time": "6:00 AM - 8:00 AM", "trainer": "Carlos"},
        {"id": 2, "day": "Martes", "time": "8:00 AM - 10:00 AM", "trainer": "Ana"},
        {"id": 3, "day": "Miércoles", "time": "6:00 PM - 8:00 PM", "trainer": "Luis"},
    ]