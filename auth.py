import hashlib
import secrets
from datetime import datetime

from storage import save_users
from validators import validate_username, validate_email, validate_password_strength


MAX_LOGIN_ATTEMPTS = 3
HASH_ITERATIONS = 200_000


# -------------------------------
# Password Hashing
# -------------------------------

def hash_password(password, salt=None):
    """
    Hash password using PBKDF2-HMAC-SHA256.
    This is more secure than simple SHA-256 because it uses:
    - Salt
    - Many hashing iterations
    """

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS
    ).hex()

    return password_hash, salt


def verify_password(password, stored_hash, salt):
    """
    Verify user password against stored password hash.
    """

    password_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(password_hash, stored_hash)


# -------------------------------
# User Search Helpers
# -------------------------------

def find_user_by_username(users, username):
    for user in users:
        if user["username"] == username:
            return user
    return None


def find_user_by_email(users, email):
    for user in users:
        if user["email"] == email:
            return user
    return None


def find_user_by_identifier(users, identifier):
    """
    Allows login using either username or email.
    Authentication is case-sensitive.
    """

    user = find_user_by_username(users, identifier)

    if user:
        return user

    return find_user_by_email(users, identifier)


def username_exists(users, username):
    return find_user_by_username(users, username) is not None


def email_exists(users, email):
    return find_user_by_email(users, email) is not None


# -------------------------------
# Registration
# -------------------------------

def register_user(users):
    print("\n========== Register ==========")

    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ")

    if not validate_username(username):
        print("Invalid username.")
        print("Username must be 3-20 characters and contain only letters, numbers, or underscores.")
        return

    if not validate_email(email):
        print("Invalid email format.")
        return

    is_strong, message = validate_password_strength(password)

    if not is_strong:
        print(message)
        return

    if username_exists(users, username):
        print("Username already exists.")
        return

    if email_exists(users, email):
        print("Email already exists.")
        return

    password_hash, salt = hash_password(password)

    role = "Admin" if len(users) == 0 else "User"

    new_user = {
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "salt": salt,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    users.append(new_user)
    save_users(users)

    print("Registration successful.")
    print(f"Your role is: {role}")


# -------------------------------
# Login
# -------------------------------

def login_user(users, login_attempts):
    print("\n========== Login ==========")

    identifier = input("Enter username or email: ").strip()

    if login_attempts.get(identifier, 0) >= MAX_LOGIN_ATTEMPTS:
        print("Too many failed login attempts.")
        print("This account is temporarily blocked during this session.")
        return

    password = input("Enter password: ")

    user = find_user_by_identifier(users, identifier)

    if user and verify_password(password, user["password_hash"], user["salt"]):
        login_attempts[identifier] = 0

        print("\nLogin successful.")
        print(f"Welcome, {user['username']}!")
        print(f"Role: {user['role']}")

        user_dashboard(users, user)
        return

    login_attempts[identifier] = login_attempts.get(identifier, 0) + 1
    remaining_attempts = MAX_LOGIN_ATTEMPTS - login_attempts[identifier]

    print("Invalid username/email or password.")

    if remaining_attempts > 0:
        print(f"Remaining attempts: {remaining_attempts}")
    else:
        print("Maximum login attempts reached.")


# -------------------------------
# Password Reset
# -------------------------------

def reset_password(users):
    print("\n========== Reset Password ==========")

    identifier = input("Enter username or email: ").strip()
    current_password = input("Enter current password: ")

    user = find_user_by_identifier(users, identifier)

    if not user:
        print("User not found.")
        return

    if not verify_password(current_password, user["password_hash"], user["salt"]):
        print("Current password is incorrect.")
        return

    new_password = input("Enter new password: ")

    is_strong, message = validate_password_strength(new_password)

    if not is_strong:
        print(message)
        return

    new_hash, new_salt = hash_password(new_password)

    user["password_hash"] = new_hash
    user["salt"] = new_salt

    save_users(users)

    print("Password reset successful.")


# -------------------------------
# Account Deletion
# -------------------------------

def delete_account(users):
    print("\n========== Delete Account ==========")

    identifier = input("Enter username or email: ").strip()
    password = input("Enter password: ")

    user = find_user_by_identifier(users, identifier)

    if not user:
        print("User not found.")
        return

    if not verify_password(password, user["password_hash"], user["salt"]):
        print("Incorrect password. Account deletion cancelled.")
        return

    confirm = input(f"Type DELETE to confirm deleting account '{user['username']}': ")

    if confirm != "DELETE":
        print("Account deletion cancelled.")
        return

    users.remove(user)
    save_users(users)

    print("Account deleted successfully.")


# -------------------------------
# User Dashboard
# -------------------------------

def user_dashboard(users, current_user):
    while True:
        print("\n========== User Dashboard ==========")
        print(f"Logged in as: {current_user['username']}")
        print(f"Role: {current_user['role']}")
        print("1. View Account Details")
        print("2. Change Password")
        print("3. Delete My Account")

        if current_user["role"] == "Admin":
            print("4. View All Users")
            print("5. Logout")
        else:
            print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n========== Account Details ==========")
            print(f"Username: {current_user['username']}")
            print(f"Email: {current_user['email']}")
            print(f"Role: {current_user['role']}")
            print(f"Created At: {current_user['created_at']}")

        elif choice == "2":
            old_password = input("Enter current password: ")

            if not verify_password(old_password, current_user["password_hash"], current_user["salt"]):
                print("Incorrect current password.")
                continue

            new_password = input("Enter new password: ")

            is_strong, message = validate_password_strength(new_password)

            if not is_strong:
                print(message)
                continue

            new_hash, new_salt = hash_password(new_password)

            current_user["password_hash"] = new_hash
            current_user["salt"] = new_salt

            save_users(users)

            print("Password changed successfully.")

        elif choice == "3":
            password = input("Enter password to confirm account deletion: ")

            if not verify_password(password, current_user["password_hash"], current_user["salt"]):
                print("Incorrect password.")
                continue

            confirm = input("Type DELETE to permanently delete your account: ")

            if confirm != "DELETE":
                print("Account deletion cancelled.")
                continue

            users.remove(current_user)
            save_users(users)

            print("Your account has been deleted.")
            break

        elif choice == "4" and current_user["role"] == "Admin":
            print("\n========== All Users ==========")

            if not users:
                print("No users found.")
            else:
                for index, user in enumerate(users, start=1):
                    print(f"{index}. {user['username']} | {user['email']} | {user['role']}")

        elif choice == "5" and current_user["role"] == "Admin":
            print("Logged out successfully.")
            break

        elif choice == "4" and current_user["role"] != "Admin":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")