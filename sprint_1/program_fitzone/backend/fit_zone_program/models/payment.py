class Payment:
    def __init__(self, payment_id=None, user_id=None, membership_id=None, payment_amount=0.0,
                 payment_date=None, payment_method='', payment_reference='', payment_status='pending'):
        self.__payment_id = payment_id
        self.__user_id = user_id
        self.__membership_id = membership_id
        self.__payment_amount = payment_amount
        self.__payment_date = payment_date
        self.__payment_method = payment_method
        self.__payment_reference = payment_reference
        self.__payment_status = payment_status

    def get_payment_id(self):
        return self.__payment_id

    def set_payment_id(self, payment_id):
        self.__payment_id = payment_id

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_membership_id(self):
        return self.__membership_id

    def set_membership_id(self, membership_id):
        self.__membership_id = membership_id

    def get_payment_amount(self):
        return self.__payment_amount

    def set_payment_amount(self, payment_amount):
        self.__payment_amount = payment_amount

    def get_payment_date(self):
        return self.__payment_date

    def set_payment_date(self, payment_date):
        self.__payment_date = payment_date

    def get_payment_method(self):
        return self.__payment_method

    def set_payment_method(self, payment_method):
        self.__payment_method = payment_method

    def get_payment_reference(self):
        return self.__payment_reference

    def set_payment_reference(self, payment_reference):
        self.__payment_reference = payment_reference

    def get_payment_status(self):
        return self.__payment_status

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status
