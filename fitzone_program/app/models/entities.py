from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from app.models.enums import (
    AccessAction,
    AccessResult,
    MembershipPlanStatus,
    MembershipStatus,
    PaymentMethod,
    PaymentStatus,
    Role,
    UserStatus,
)


@dataclass(slots=True)
class User:
    id: str
    name: str
    email: str
    password_hash: str
    phone: Optional[str]
    role: Role
    status: UserStatus
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class MembershipPlan:
    id: str
    name: str
    price: Decimal
    duration_days: int
    benefits: str
    status: MembershipPlanStatus
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class UserMembership:
    id: str
    user_id: str
    membership_plan_id: str
    start_date: date
    end_date: date
    status: MembershipStatus
    assigned_at: datetime


@dataclass(slots=True)
class Payment:
    id: str
    user_id: str
    user_membership_id: str
    amount: Decimal
    payment_date: datetime
    method: PaymentMethod
    reference: str
    status: PaymentStatus
    created_at: datetime


@dataclass(slots=True)
class AccessLog:
    id: str
    user_id: Optional[str]
    email_attempted: str
    action: AccessAction
    result: AccessResult
    ip_address: str
    created_at: datetime
