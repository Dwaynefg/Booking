import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH").encode('utf-8')

def verify_admin(username_input, password_input):
    if username_input == ADMIN_USERNAME:
        return bcrypt.checkpw(password_input.encode('utf-8'), ADMIN_PASSWORD_HASH)
    return False
