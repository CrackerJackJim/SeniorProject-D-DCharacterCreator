from fastapi import APIRouter, HTTPException
from models.auth_models import RegisterRequest, LoginRequest
from services.auth import register_user, login_user
from database.core import fetch_one, execute
from passlib.hash import bcrypt

router = APIRouter(tags=["auth"])

# -------------------------------------------------
# REGISTER (ASYNC + FIXED)
# -------------------------------------------------
@router.post("/register")
async def register(req: RegisterRequest):
    try:
        user_id = await register_user(req.username, req.email, req.password)
        return {"success": True, "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------------------------------
# LOGIN
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
# PASSWORD RESET — UPDATE PASSWORD
# -------------------------------------------------
@router.post("/password/reset/{user_id}")
async def reset_password(user_id: int, data: dict):
    new_pass = data.get("password")

    if not new_pass or len(new_pass) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long."
        )

    hashed = bcrypt.hash(new_pass[:72])

    await execute(
        "UPDATE account SET PasswordHash = %s WHERE AccountID = %s",
        (hashed, user_id)
    )

    return {"success": True}