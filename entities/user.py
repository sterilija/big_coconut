from modules.api.api_manager import ApiManager


class User:
    def __init__(self, email: str, password: str, roles: list, session: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.session = session

    @property
    def creds(self):
        return {"email": self.email, "password": self.password}
