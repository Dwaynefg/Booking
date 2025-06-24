import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

# Get credentials from environment
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH").encode("utf-8")

def verify_admin(username_input, password_input):
    if username_input != ADMIN_USERNAME:
        return False
    return bcrypt.checkpw(password_input.encode("utf-8"), ADMIN_PASSWORD_HASH)

# === Simulate test input ===
input_username = input("Enter admin username: ")
input_password = input("Enter admin password: ")

# === Test verification ===
if verify_admin(input_username, input_password):
    print("✅ Admin login successful!")
else:
    print("❌ Admin login failed. Invalid credentials.")
