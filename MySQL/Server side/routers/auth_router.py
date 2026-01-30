from fastapi import APIRouter, HTTPException
from models.auth_models import RegisterRequest, LoginRequest, LoginResponse
from services.auth import register_user, login_user
from database import fetch_one, execute
from passlib.hash import bcrypt

router = APIRouter(tags=["auth"])

# -------------------------------------------------
# REGISTER
# -------------------------------------------------
@router.post("/register")
def register(req: RegisterRequest):
    try:
        user_id = register_user(req.username, req.email, req.password)
        return {"success": True, "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    try:
        user = login_user(req.identifier, req.password)
        print("DEBUG LOGIN RESPONSE:", user)
        return {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------------------------------
# PASSWORD RESET — VERIFY USER
# -------------------------------------------------
@router.post("/password/verify")
def verify_user(data: dict):
    username = data.get("username")
    email = data.get("email")

    user = fetch_one(
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
def reset_password(user_id: int, data: dict):
    new_pass = data.get("password")

    # -------------------------------------------------
    # MATCH REGISTRATION PASSWORD RULES
    # -------------------------------------------------
    if not new_pass or len(new_pass) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long."
        )

    # Add any additional rules you enforce during registration:
    # if " " in new_pass:
    #     raise HTTPException(status_code=400, detail="Password cannot contain spaces.")

    # -------------------------------------------------
    # HASH USING SAME SYSTEM AS REGISTER/LOGIN
    # -------------------------------------------------
    hashed = bcrypt.hash(new_pass[:72])

    execute(
        "UPDATE account SET PasswordHash = %s WHERE AccountID = %s",
        (hashed, user_id)
    )

    return {"success": True}