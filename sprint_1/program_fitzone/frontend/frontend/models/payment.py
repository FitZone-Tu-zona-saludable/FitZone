# =========================
# models/payment.py
# =========================

"""
===========================================================
MODELO: PAYMENT
===========================================================

ES:
Representa un pago realizado dentro del sistema del gimnasio.

Responsabilidades:
- Almacenar información del pago
- Validar datos básicos
- Facilitar conversión a diccionario

EN:
Represents a payment in the gym system.

Responsibilities:
- Store payment data
- Validate basic data
- Convert to dictionary format
===========================================================
"""


class Payment:
    """
    ===========================================================
    CLASE: Payment
    ===========================================================

    Modelo de datos para pagos.

    Atributos:
    - payment_id: Identificador único del pago
    - user_id: ID del usuario que realiza el pago
    - membership_id: ID de la membresía asociada
    - amount: Valor del pago
    - method: Método de pago (efectivo, tarjeta, nequi, etc.)
    - date: Fecha del pago
    - status: Estado del pago (pendiente, aprobado, rechazado)
    ===========================================================
    """

    def __init__(self, payment_id, user_id, membership_id, amount, method, date, status):
        """
        Inicializa un pago con validaciones básicas.
        """

        # =========================
        # VALIDACIONES
        # =========================
        if not payment_id:
            raise ValueError("payment_id es requerido")

        if not user_id:
            raise ValueError("user_id es requerido")

        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        if not method:
            raise ValueError("El método de pago es requerido")

        if not date:
            raise ValueError("La fecha es requerida")

        # =========================
        # ASIGNACIÓN DE ATRIBUTOS
        # =========================
        self.payment_id = payment_id
        self.user_id = user_id
        self.membership_id = membership_id
        self.amount = amount
        self.method = method
        self.date = date
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
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "membership_id": self.membership_id,
            "amount": self.amount,
            "method": self.method,
            "date": self.date,
            "status": self.status
        }

    # ===========================================================
    # MÉTODO: __str__
    # ===========================================================
    def __str__(self):
        """
        Representación legible del pago.
        """

        return f"Pago {self.payment_id} - ${self.amount} ({self.method})"

    # ===========================================================
    # MÉTODO: is_completed
    # ===========================================================
    def is_completed(self):
        """
        Retorna True si el pago está aprobado/completado.
        """

        return self.status.lower() in ["aprobado", "completado", "pagado"]

    # ===========================================================
    # MÉTODO: is_pending
    # ===========================================================
    def is_pending(self):
        """
        Retorna True si el pago está pendiente.
        """

        return self.status.lower() == "pendiente"