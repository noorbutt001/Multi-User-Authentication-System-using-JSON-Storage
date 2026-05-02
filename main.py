from auth import register_user, login_user, reset_password, delete_account
from storage import load_users


def main():
    users = load_users()
    login_attempts = {}

    while True:
        print("\n========== Multi-User Authentication System ==========")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Delete Account")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user(users)

        elif choice == "2":
            login_user(users, login_attempts)

        elif choice == "3":
            reset_password(users)

        elif choice == "4":
            delete_account(users)

        elif choice == "5":
            print("Thank you for using the authentication system.")
            break

        else:
            print("Invalid choice. Please select between 1 and 5.")


if __name__ == "__main__":
    main()