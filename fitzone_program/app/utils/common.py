from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4


def new_id() -> str:
    return str(uuid4())


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


def today() -> date:
    return date.today()


def money(value: str | float | int | Decimal) -> Decimal:
    return Decimal(str(value))
