from fastapi import APIRouter, HTTPException
from models.auth_models import RegisterRequest, LoginRequest, LoginResponse
from services.auth import register_user, login_user

# -------------------------------------------------
# ROUTER INSTANCE
# -------------------------------------------------
router = APIRouter(prefix="/api", tags=["auth"])

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
        return {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))