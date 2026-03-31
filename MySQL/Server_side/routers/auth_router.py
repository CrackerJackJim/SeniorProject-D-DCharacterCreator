from fastapi import APIRouter, HTTPException

# FIXED: all imports now use the full Server_side package path
from Server_side.models.auth_models import RegisterRequest, LoginRequest
from Server_side.services.auth import register_user, login_user
from Server_side.database.core import fetch_one, execute

from passlib.hash import argon2


router = APIRouter(tags=["auth"])


# -------------------------------------------------
# REGISTER (ASYNC + ARGON2)
# -------------------------------------------------
@router.post("/register")
async def register(req: RegisterRequest):
    try:
        user_id = await register_user(req.username, req.email, req.password)
        return {"success": True, "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------
# LOGIN (ARGON2 VERIFY IN services.auth.login_user)
# -------------------------------------------------
@router.post("/login")
async def login(req: LoginRequest):
    user = await login_user(req.identifier, req.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }


# -------------------------------------------------
# PASSWORD RESET — VERIFY USER
# -------------------------------------------------
@router.post("/password/verify")
async def verify_user(data: dict):
    username = data.get("username")
    email = data.get("email")

    user = await fetch_one(
        "SELECT AccountID FROM account WHERE Username = %s AND Email = %s",
        (username, email)
    )

    if not user:
        return {"success": False}

    return {"success": True, "user_id": user["AccountID"]}


# -------------------------------------------------
# PASSWORD RESET — UPDATE PASSWORD (ARGON2)
# -------------------------------------------------
@router.post("/password/reset/{user_id}")
async def reset_password(user_id: int, data: dict):
    new_pass = data.get("password")

    if not new_pass or len(new_pass) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long."
        )

    hashed = argon2.hash(new_pass)

    await execute(
        "UPDATE account SET PasswordHash = %s WHERE AccountID = %s",
        (hashed, user_id)
    )

    return {"success": True}