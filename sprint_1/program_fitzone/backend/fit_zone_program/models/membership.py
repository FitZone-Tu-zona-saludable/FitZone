class Membership:
    def __init__(self, membership_id=None, user_id=None, membership_plan='', membership_price=0.0,
                 membership_duration=0, membership_benefits='', membership_status='active'):
        self.__membership_id = membership_id
        self.__user_id = user_id
        self.__membership_plan = membership_plan
        self.__membership_price = membership_price
        self.__membership_duration = membership_duration
        self.__membership_benefits = membership_benefits
        self.__membership_status = membership_status

    def get_membership_id(self):
        return self.__membership_id

    def set_membership_id(self, membership_id):
        self.__membership_id = membership_id

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_membership_plan(self):
        return self.__membership_plan

    def set_membership_plan(self, membership_plan):
        self.__membership_plan = membership_plan

    def get_membership_price(self):
        return self.__membership_price

    def set_membership_price(self, membership_price):
        self.__membership_price = membership_price

    def get_membership_duration(self):
        return self.__membership_duration

    def set_membership_duration(self, membership_duration):
        self.__membership_duration = membership_duration

    def get_membership_benefits(self):
        return self.__membership_benefits

    def set_membership_benefits(self, membership_benefits):
        self.__membership_benefits = membership_benefits

    def get_membership_status(self):
        return self.__membership_status

    def set_membership_status(self, membership_status):
        self.__membership_status = membership_status
