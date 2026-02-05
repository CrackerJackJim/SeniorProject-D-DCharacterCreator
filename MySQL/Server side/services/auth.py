import bcrypt
from database.core import fetch_one, fetch_all, execute
from passlib.hash import bcrypt as passlib_bcrypt

# -----------------------------
# REGISTER USER (ASYNC + FIXED)
# -----------------------------
async def register_user(username: str, email: str, password: str) -> int:
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # MUST be awaited
    existing = await fetch_one(
        "SELECT AccountID FROM account WHERE Username = %s OR Email = %s",
        (username, email)
    )
    if existing:
        raise ValueError("Username or email is already in use")

    # Hash password
    hashed = passlib_bcrypt.hash(password[:72])

    # MUST be awaited
    await execute(
        "INSERT INTO account (Username, Email, PasswordHash) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )

    # MUST be awaited
    row = await fetch_one(
        "SELECT AccountID FROM account WHERE Email = %s",
        (email,)
    )

    return row["AccountID"] if row else None


# -----------------------------
# LOGIN USER (already async)
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

    user = {k.lower(): v for k, v in user.items()}

    if not bcrypt.checkpw(password.encode(), user["passwordhash"].encode()):
        return None

    return {
        "id": user["accountid"],
        "username": user["username"],
        "email": user["email"]
    }