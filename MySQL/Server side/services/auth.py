from database.core import fetch_one, execute
from passlib.hash import bcrypt

# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(username: str, email: str, password: str) -> int:
    # Basic validation
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Check if username or email already exists
    existing = fetch_one(
        "SELECT AccountID FROM account WHERE Username = %s OR Email = %s",
        (username, email)
    )
    if existing:
        raise ValueError("Username or email is already in use")

    # Hash password (bcrypt max 72 bytes)
    hashed = bcrypt.hash(password[:72])

    # Insert new account
    execute(
        "INSERT INTO account (Username, Email, PasswordHash) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )

    # Fetch the new AccountID
    row = fetch_one(
        "SELECT AccountID FROM account WHERE Email = %s",
        (email,)
    )

    return row["AccountID"] if row else None

# -----------------------------
# LOGIN USER
# -----------------------------
def login_user(identifier: str, password: str):
    # Fetch user by username or email
    user = fetch_one(
        "SELECT AccountID, Username, Email, PasswordHash FROM account "
        "WHERE Username = %s OR Email = %s",
        (identifier, identifier)
    )

    if not user:
        raise ValueError("Invalid username or email")

    # Verify bcrypt password
    if not bcrypt.verify(password[:72], user["PasswordHash"]):
        raise ValueError("Incorrect password")

    # Return user data in the structure auth_router expects
    return {
        "id": user["AccountID"],
        "username": user["Username"],
        "email": user["Email"]
    }