# =========================
# models/membership.py
# =========================

"""
===========================================================
MODELO: MEMBERSHIP
===========================================================

ES:
Representa una membresía dentro del sistema del gimnasio.

Responsabilidades:
- Almacenar información de la membresía
- Validar datos básicos
- Facilitar conversión a estructuras (dict)

EN:
Represents a gym membership.

Responsibilities:
- Store membership data
- Basic validation
- Convert to dictionary format
===========================================================
"""


class Membership:
    """
    ===========================================================
    CLASE: Membership
    ===========================================================

    Modelo de datos para una membresía.

    Atributos:
    - membership_id: Identificador único
    - membership_type: Tipo de membresía (mensual, trimestral, etc.)
    - price: Precio de la membresía
    - duration: Duración en días o meses
    - status: Estado (activa, vencida, pendiente)
    ===========================================================
    """

    def __init__(self, membership_id, membership_type, price, duration, status):
        """
        Inicializa una membresía con validaciones básicas.
        """

        # =========================
        # VALIDACIONES
        # =========================
        if not membership_id:
            raise ValueError("membership_id es requerido")

        if price < 0:
            raise ValueError("El precio no puede ser negativo")

        if duration <= 0:
            raise ValueError("La duración debe ser mayor a 0")

        # =========================
        # ASIGNACIÓN DE ATRIBUTOS
        # =========================
        self.membership_id = membership_id
        self.membership_type = membership_type
        self.price = price
        self.duration = duration
        self.status = status

    # ===========================================================
    # MÉTODO: to_dict
    # ===========================================================
    def to_dict(self):
        """
        Convierte el objeto a diccionario.

        Útil para:
        - APIs
        - JSON
        - Debug
        """

        return {
            "membership_id": self.membership_id,
            "membership_type": self.membership_type,
            "price": self.price,
            "duration": self.duration,
            "status": self.status
        }

    # ===========================================================
    # MÉTODO: __str__
    # ===========================================================
    def __str__(self):
        """
        Representación legible del objeto.
        """

        return f"{self.membership_type} - ${self.price} ({self.duration})"

    # ===========================================================
    # MÉTODO: is_active
    # ===========================================================
    def is_active(self):
        """
        Retorna True si la membresía está activa.
        """

        return self.status.lower() == "activa"