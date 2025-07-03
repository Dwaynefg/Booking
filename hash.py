import bcrypt

# Your plain text password
password = "admin"

# Generate bcrypt hash
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password_bytes, salt)

# Print the hash (this is what you need to put in your .env file)
print("Bcrypt hash for 'admin':")
print(hashed.decode('utf-8'))

# Test verification
print("\nVerification test:")
print("Password 'admin' matches hash:", bcrypt.checkpw(password_bytes, hashed))