from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from app.models.entities import MembershipPlan, UserMembership
from app.models.enums import MembershipPlanStatus, MembershipStatus
from app.repositories.membership_plan_repository import MembershipPlanRepository
from app.repositories.user_membership_repository import UserMembershipRepository
from app.repositories.user_repository import UserRepository
from app.utils.common import new_id, now, today


class MembershipService:
    def __init__(
        self,
        membership_plan_repository: MembershipPlanRepository,
        user_membership_repository: UserMembershipRepository,
        user_repository: UserRepository,
    ) -> None:
        self.membership_plan_repository = membership_plan_repository
        self.user_membership_repository = user_membership_repository
        self.user_repository = user_repository

    def seed_default_plans(self) -> None:
        if self.membership_plan_repository.list_all():
            return
        timestamp = now()
        plans = [
            MembershipPlan(new_id(), "Mensual", Decimal("100000"), 30, "Acceso general al gimnasio", MembershipPlanStatus.ACTIVE, timestamp, timestamp),
            MembershipPlan(new_id(), "Trimestral", Decimal("270000"), 90, "Acceso general + evaluación física", MembershipPlanStatus.ACTIVE, timestamp, timestamp),
            MembershipPlan(new_id(), "Anual", Decimal("950000"), 365, "Acceso total + 2 cortesías mensuales", MembershipPlanStatus.ACTIVE, timestamp, timestamp),
        ]
        for plan in plans:
            self.membership_plan_repository.create(plan)

    def list_plans(self) -> list[MembershipPlan]:
        return self.membership_plan_repository.list_all(only_active=True)

    def assign_membership(self, user_id: str, membership_plan_id: str) -> UserMembership:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("El usuario no existe.")
        plan = self.membership_plan_repository.get_by_id(membership_plan_id)
        if not plan or plan.status != MembershipPlanStatus.ACTIVE:
            raise ValueError("El plan no existe o está inactivo.")
        start = today()
        membership = UserMembership(
            id=new_id(),
            user_id=user_id,
            membership_plan_id=membership_plan_id,
            start_date=start,
            end_date=start + timedelta(days=plan.duration_days),
            status=MembershipStatus.PENDING,
            assigned_at=now(),
        )
        return self.user_membership_repository.create(membership)

    def get_user_memberships(self, user_id: str) -> list[UserMembership]:
        return self.user_membership_repository.list_by_user(user_id)
