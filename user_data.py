import csv
from user import User

USERS_CSV_FILE = "users.csv"

def save_users_to_csv(users_db):
    with open(USERS_CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "email", "first_name", "last_name"])
        for user in users_db.values():
            writer.writerow([
                user.user_id,
                user.email,
                user.first_name or "",
                user.last_name or ""
            ])

def load_users_from_csv():
    users = {}
    try:
        with open(USERS_CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    user_id=row["user_id"],
                    email=row["email"],
                    first_name=row["first_name"],
                    last_name=row["last_name"]
                )
                users[user.email] = user
    except FileNotFoundError:
        pass
    return users
