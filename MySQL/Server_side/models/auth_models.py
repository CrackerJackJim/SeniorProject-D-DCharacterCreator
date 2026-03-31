from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    identifier: str  # username OR email
    password: str

class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr