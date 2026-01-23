from fastapi import APIRouter, HTTPException
from services.character_recalc import recalc_character
from services.characters import get_characters_for_user, get_character
from models.auth_models import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter()


# -----------------------------
# LIST CHARACTERS FOR USER
# -----------------------------
@router.get("/characters/{user_id}")
def list_characters(user_id: int):
    chars = get_characters_for_user(user_id)
    return {"characters": chars}


# -----------------------------
# GET SINGLE CHARACTER
# -----------------------------
@router.get("/character/{char_id}")
def get_single_character(char_id: int):
    char = get_character(char_id)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char


# -----------------------------
# RECALCULATE CHARACTER
# -----------------------------
@router.post("/characters/{char_id}/recalc")
def recalc(char_id: int):
    try:
        result = recalc_character(char_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))