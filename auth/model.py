class AuthenticatedUser:
    def __init__(self, user_id: str, email: str, role: str, token: str):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.token = token
