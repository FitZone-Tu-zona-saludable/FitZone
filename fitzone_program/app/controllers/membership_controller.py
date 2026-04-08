from __future__ import annotations

from app.services.membership_service import MembershipService


class MembershipController:
    def __init__(self, membership_service: MembershipService) -> None:
        self.membership_service = membership_service

    def list_plans(self):
        return self.membership_service.list_plans()

    def assign_membership(self, user_id: str, membership_plan_id: str):
        return self.membership_service.assign_membership(user_id, membership_plan_id)

    def get_user_memberships(self, user_id: str):
        return self.membership_service.get_user_memberships(user_id)
