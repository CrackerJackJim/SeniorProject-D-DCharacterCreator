from fastapi import APIRouter
from database import fetch_one, fetch_all, execute

router = APIRouter()

@router.get("/characters/{user_id}")
def get_characters_for_user(user_id: int):
    return db.fetch_all("""
        SELECT *
        FROM characters
        WHERE account_id = %s
    """, (user_id,))

@router.get("/character/{char_id}")
def get_character(char_id: int):
    return db.fetch_one("""
        SELECT *
        FROM characters
        WHERE id = %s
    """, (char_id,))

@router.post("/characters/{char_id}/touch")
def touch_character(char_id: int):
    db.execute("""
        UPDATE characters
        SET last_edited = NOW()
        WHERE id = %scombat = await fetch_one("SELECT * FROM combat_stats WHERE CharacterID = %s", (character_id,))
    """, (char_id,))
    db.commit()
    return {"status": "ok"}