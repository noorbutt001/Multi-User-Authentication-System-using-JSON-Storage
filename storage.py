import json
import os


DB_FILE = "users.json"


def load_users():
    """
    Load users from users.json.
    If the file does not exist, create it with an empty list.
    """

    if not os.path.exists(DB_FILE):
        save_users([])
        return []

    try:
        with open(DB_FILE, "r") as file:
            users = json.load(file)

            if not isinstance(users, list):
                print("Invalid database format. Resetting users.json.")
                save_users([])
                return []

            return users

    except json.JSONDecodeError:
        print("Database file is corrupted. Resetting users.json.")
        save_users([])
        return []


def save_users(users):
    """
    Save users to users.json.
    """

    with open(DB_FILE, "w") as file:
        json.dump(users, file, indent=4)