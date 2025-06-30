import csv
from user import User

USERS_CSV_FILE = "users.csv"

def save_users_to_csv(users_db):
    with open(USERS_CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Corrected header order
        writer.writerow(["user_id", "first_name", "last_name", "username", "password"])
        for user in users_db.values():
            d = user.to_dict()
            # Match the header order
            writer.writerow([
                d["user_id"],
                d.get("first_name", "") or "",
                d.get("last_name", "") or "",
                d["username"],
                d["password"]
            ])

def load_users_from_csv():
    users = {}
    try:
        with open(USERS_CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for r in reader:
                    # Validate required fields
                    user_id = r["user_id"]
                    username = r["username"]
                    password = r["password"]

                    # Optional fields
                    first_name = r.get("first_name") or None
                    last_name = r.get("last_name") or None

                    # Create user
                    user = User(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        user_id=user_id
                    )
                    users[username] = user
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet
    return users

