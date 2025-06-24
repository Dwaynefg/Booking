import uuid

class User:
    def __init__(self, email, first_name=None, last_name=None, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())  # Generate UUID if not provided
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
