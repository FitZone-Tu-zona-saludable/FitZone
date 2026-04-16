class User:
    def __init__(self, user_id=None, user_name='', user_email='', user_password='', user_role='client', user_status='active'):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__user_email = user_email
        self.__user_password = user_password
        self.__user_role = user_role
        self.__user_status = user_status

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_user_email(self):
        return self.__user_email

    def set_user_email(self, user_email):
        self.__user_email = user_email

    def get_user_password(self):
        return self.__user_password

    def set_user_password(self, user_password):
        self.__user_password = user_password

    def get_user_role(self):
        return self.__user_role

    def set_user_role(self, user_role):
        self.__user_role = user_role

    def get_user_status(self):
        return self.__user_status

    def set_user_status(self, user_status):
        self.__user_status = user_status
