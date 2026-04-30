from frontend.services.app_context import membership_service


class MembershipController:
    def __init__(self):
        self.service = membership_service

    def load_memberships(self):
        return self.service.list_memberships()

    def load_user_memberships(self, user_id):
        return self.service.get_user_memberships(user_id)

    def select_membership(self, user_id, membership_id):
        return self.service.select_membership(user_id, membership_id)
