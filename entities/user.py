class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_user(self):
        return self.username, self.email
