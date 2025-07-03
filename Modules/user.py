import uuid

class User:
    def __init__(self, username, password, first_name=None, last_name=None, user_id=None):
        if not username or len(username) < 5:
            raise ValueError("Username must be at least 5 characters long.")
        self._user_id = user_id or str(uuid.uuid4())
        self._username = username
        self._password = password  # should already be hashed
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
    def set_password(self, hashed_password):
        if not hashed_password:
            raise ValueError("Password cannot be empty.")
        self._password = hashed_password

    def set_username(self, username):
        if not username or len(username) < 5:
            raise ValueError("Username must be at least 5 characters long.")
        self._username = username

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    # Dictionary representation for CSV storage
    def to_dict(self):
        return {
            "user_id": self._user_id,
            "first_name": self._first_name or "",
            "last_name": self._last_name or "",
            "username": self._username,
            "password": self._password
        }
