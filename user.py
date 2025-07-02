import uuid

class User:
    def __init__(self, username, password, first_name=None, last_name=None, user_id=None):
        self._user_id = user_id or str(uuid.uuid4())
        self._username = username
        self._password = password
        self._first_name = first_name
        self._last_name = last_name

    # Getters
    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    # Setters
    def set_username(self, username):
        if not username or len(username) < 5:
            raise ValueError("Username must be at least 5 characters")
        self._username = username

    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self._password = password

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "username": self._username,
            "password": self._password,
            "first_name": self._first_name,
            "last_name": self._last_name
        }
