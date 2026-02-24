import re
from database.core import fetch_one, fetch_all, execute
from passlib.hash import argon2

# -----------------------------
# REGISTER USER (ASYNC + STRONG RULES + ARGON2)
# -----------------------------
async def register_user(username: str, email: str, password: str) -> int:
    # Basic username rule
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")

    # Strong password rules
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one symbol")

    # Check if username or email already exists
    existing = await fetch_one(
        "SELECT AccountID FROM account WHERE Username = %s OR Email = %s",
        (username, email)
    )
    if existing:
        raise ValueError("Username or email is already in use")

    # Hash password with Argon2 (no 72‑byte limit)
    hashed = argon2.hash(password)

    # Insert user
    await execute(
        "INSERT INTO account (Username, Email, PasswordHash) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )

    # Fetch new AccountID
    row = await fetch_one(
        "SELECT AccountID FROM account WHERE Email = %s",
        (email,)
    )

    return row["AccountID"] if row else None


# -----------------------------
# LOGIN USER (ASYNC + ARGON2 VERIFY)
# -----------------------------
async def login_user(identifier, password):
    query = """
        SELECT *
        FROM account
        WHERE Username = %s OR Email = %s
    """

    user = await fetch_one(query, (identifier, identifier))

    if not user:
        return None

    # Normalize keys to lowercase
    user = {k.lower(): v for k, v in user.items()}

    # Verify password using Argon2
    stored_hash = user["passwordhash"]
    if not argon2.verify(password, stored_hash):
        return None

    return {
        "id": user["accountid"],
        "username": user["username"],
        "email": user["email"]
    }