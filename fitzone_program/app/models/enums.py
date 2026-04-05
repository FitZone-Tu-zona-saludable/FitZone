from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SECURITY = "SECURITY"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class MembershipPlanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class MembershipStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"
    OTHER = "OTHER"


class AccessAction(str, Enum):
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    ACCESS_DENIED = "ACCESS_DENIED"


class AccessResult(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
