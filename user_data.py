import csv
from pathlib import Path
from user import User

# Define paths
DATA_PATH = Path(__file__).parent / "data"
USERS_CSV_FILE = DATA_PATH / "users.csv"  # Now points to data/users.csv

def save_users_to_csv(users_db):
    # Ensure data directory exists
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    
    with open(USERS_CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "first_name", "last_name", "username", "password"])
        for user in users_db.values():
            d = user.to_dict()
            writer.writerow([
                d["user_id"],
                d.get("first_name", ""),
                d.get("last_name", ""),
                d["username"],
                d["password"]
            ])

def load_users_from_csv():
    users = {}
    try:
        # Create data folder if it doesn't exist
        DATA_PATH.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists before reading
        if USERS_CSV_FILE.exists():
            with open(USERS_CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for r in reader:
                    try:
                        user = User(
                            username=r["username"],
                            password=r["password"],
                            first_name=r.get("first_name"),
                            last_name=r.get("last_name"),
                            user_id=r["user_id"]
                        )
                        users[r["username"]] = user
                    except KeyError as e:
                        print(f"Missing required field in CSV: {e}")
                        continue
    except Exception as e:
        print(f"Error loading users: {e}")
    return users