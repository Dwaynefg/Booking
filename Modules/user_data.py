import csv
from pathlib import Path
from .user import User  # Proper relative import

# Define paths - go up one level from Modules to reach the project root
DATA_PATH = Path(__file__).parent.parent / "data"  # This goes up from Modules to project root, then to data
USERS_CSV_FILE = DATA_PATH / "users.csv"

def save_users_to_csv(users_db):
    """Save users database to CSV file"""
    # Ensure data directory exists
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    
    try:
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
        print(f"Successfully saved {len(users_db)} users to {USERS_CSV_FILE}")
    except Exception as e:
        print(f"Error saving users to CSV: {e}")
        raise

def load_users_from_csv():
    """Load users database from CSV file"""
    users = {}
    try:
        # Create data folder if it doesn't exist
        DATA_PATH.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists before reading
        if USERS_CSV_FILE.exists():
            print(f"Loading users from: {USERS_CSV_FILE}")
            with open(USERS_CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row_num, r in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                    try:
                        # Validate required fields
                        if not r.get("username") or not r.get("password"):
                            print(f"Warning: Row {row_num} missing username or password, skipping")
                            continue
                            
                        user = User(
                            username=r["username"].strip(),
                            password=r["password"],
                            first_name=r.get("first_name", "").strip() or None,
                            last_name=r.get("last_name", "").strip() or None,
                            user_id=r.get("user_id", "").strip() or None
                        )
                        users[r["username"].strip()] = user
                        
                    except KeyError as e:
                        print(f"Missing required field in CSV row {row_num}: {e}")
                        continue
                    except ValueError as e:
                        print(f"Invalid data in CSV row {row_num}: {e}")
                        continue
                        
            print(f"Successfully loaded {len(users)} users from CSV")
        else:
            print(f"CSV file not found at {USERS_CSV_FILE}, starting with empty user database")
            
    except Exception as e:
        print(f"Error loading users from CSV: {e}")
        # Don't raise the exception, just return empty dict and let the app continue
        
    return users

def get_csv_file_path():
    """Return the path to the CSV file (useful for debugging)"""
    return USERS_CSV_FILE

def csv_file_exists():
    """Check if the CSV file exists"""
    return USERS_CSV_FILE.exists()