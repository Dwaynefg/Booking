import csv
from user import User

USERS_CSV_FILE = "users.csv"

def save_users_to_csv(users_db):
    with open(USERS_CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Note header updated from email to password
        writer.writerow(["s_no", "user_id", "password", "username", "first_name", "last_name"])
        
        for index, user in enumerate(users_db.values(), start=1):
            data = user.to_dict()
            writer.writerow([
                index,
                data["user_id"],
                data["password"],
                data["username"] or "",
                data["first_name"] or "",
                data["last_name"] or ""
            ])

def load_users_from_csv():
    users = {}
    try:
        with open(USERS_CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    user_id=row["user_id"],
                    first_name=row.get("first_name", None),
                    last_name=row.get("last_name", None),
                    username=row.get("username", None),
                    password=row["password"]
                )
                users[user.get_password()] = user  # Using password as key (you may want to use username or another key)
    except FileNotFoundError:
        pass
    return users
