Multi-User-Authentication-System-using-JSON-Storage
A Python-based CLI application that allows multiple users to securely register and log in. The system uses JSON for data storage and implements password hashing for security. It simulates a real-world authentication system with proper validation and error handling.
# 🔐 Multi-User Authentication System (CLI)

🎯 Objective

# This project is a Python-based Command Line Interface (CLI) application that allows multiple users to register and log in securely using JSON-based storage. It simulates a real-world authentication system.

---

🚀 Features

🔹 Core Features

* 👤 User Registration (Username, Email, Password)
* 🔐 Secure Login System
* 💾 JSON-based Data Storage
* ⚠️ Input Validation & Error Handling
 🔹 Security Features

* 🔑 Password Hashing (SHA-256)
* 🚫 No plain-text password storage
* 🔍 Unique username and email validation
* 🔒 Case-sensitive authentication

---

⚙️ Functional Modules

* Register User
* Login User
* Exit System

---

 💡 Advanced Features

* Modular code structure (separate functions/files)
* Exception handling for runtime errors
* Duplicate account prevention

---

🌟 Bonus Features

* 🔄 Password reset functionality
* ❌ Account deletion
* ⛔ Login attempt limit
* 📧 Email validation using Regex
* 👑 Role-based users (Admin/User)

---

🛠 Technologies Used

* Python 3
* JSON (Data Storage)
* hashlib (Password Hashing)
* CLI (Command Line Interface)

---

▶️ How to Run

1. Install Python

2. Clone the repository:

   ```bash
   git clone https://github.com/your-username/authentication-system.git
   ```

3. Navigate to project folder:

   ```bash
   cd authentication-system
   ```

4. Run the program:

   ```bash
   python main.py
   ```

---

 📂 Project Structure

```id="9vpx8p"
authentication-system/
│── main.py
│── auth.py
│── utils.py
│── users.json
│── README.md
```

---

📊 Sample Data (users.json)

```json
[
  {
    "username": "admin",
    "email": "admin@gmail.com",
    "password": "hashed_password_here"
  }
]
```
---
🔐 Password Security
All passwords are encrypted using SHA-256 hashing to ensure secure storage.
---

---

