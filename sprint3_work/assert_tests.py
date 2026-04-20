from src.services.auth_service import AuthService

auth = AuthService()
auth.create_user("Romel", "romel@mail.com", "1234", "admin")

users = auth.get_users()

assert len(users) == 1
assert users[0].get_email() == "romel@mail.com"

print(" Assert tests passed")
