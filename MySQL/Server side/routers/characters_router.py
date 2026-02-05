# routers/characters_router.py
from fastapi import APIRouter, HTTPException
from services.character_service import create_character
from services.character_recalc import recalc_character
from database.core import fetch_all, fetch_one, execute

router = APIRouter(prefix="/api/characters", tags=["characters"])

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def safe_int(value):
    try:
        if value in (None, "", "null", "None"):
            return None
        return int(value)
    except:
        return None

def normalize_fk(value):
    """
    Converts empty, null, or '0' values into None so MySQL accepts them.
    """
    if value in (None, "", "0", 0, "null", "None"):
        return None
    return int(value)

# ---------------------------------------------------------
# CREATE CHARACTER
# ---------------------------------------------------------

@router.post("/create")
async def create_char(data: dict):
    account_id = safe_int(data.get("account_id"))
    if account_id is None:
        raise HTTPException(status_code=400, detail="Missing account_id")

    # Basic fields
    name = data.get("name") or "Unnamed"
    gender = data.get("gender") or "Unspecified"
    level = safe_int(data.get("level")) or 1

    # Required FK
    race_id = normalize_fk(data.get("race_id"))
    class_id = normalize_fk(data.get("class_id"))

    if race_id is None:
        raise HTTPException(status_code=400, detail="Missing or invalid race_id")

    if class_id is None:
        raise HTTPException(status_code=400, detail="Missing or invalid class_id")

    # Optional FK
    background_id = normalize_fk(data.get("background_id"))
    alignment_id = normalize_fk(data.get("alignment_id"))
    subclass_id = normalize_fk(data.get("subclass_id"))

    # Ability scores
    str_score = safe_int(data.get("str")) or 10
    dex_score = safe_int(data.get("dex")) or 10
    con_score = safe_int(data.get("con")) or 10
    int_score = safe_int(data.get("int")) or 10
    wis_score = safe_int(data.get("wis")) or 10
    cha_score = safe_int(data.get("cha")) or 10

    # Experience + proficiency bonus
    experience = safe_int(data.get("experience")) or 0
    proficiency_bonus = safe_int(data.get("proficiency_bonus"))

    try:
        char_id = await create_character(
            account_id, name, gender,
            level,
            race_id, class_id, subclass_id,
            background_id, alignment_id,
            str_score, dex_score, con_score,
            int_score, wis_score, cha_score,
            experience,
            proficiency_bonus
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Character creation failed: {e}")

    return {"success": True, "character_id": char_id}

# ---------------------------------------------------------
# GET ALL CHARACTERS FOR ACCOUNT (cards)
# ---------------------------------------------------------

@router.get("/account/{account_id}")
async def get_characters_for_account(account_id: int):
    query = """
        SELECT CharacterID, Name, RaceID, ClassID, Level
        FROM characters
        WHERE AccountID = %s
    """
    rows = await fetch_all(query, (account_id,))
    return rows

# ---------------------------------------------------------
# GET SINGLE CHARACTER
# ---------------------------------------------------------

@router.get("/{char_id}")
async def get_character(char_id: int):
    query = """
        SELECT *
        FROM characters
        WHERE CharacterID = %s
    """
    row = await fetch_one(query, (char_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Character not found")
    return row

# ---------------------------------------------------------
# SHEET (character + abilities + combat)
# ---------------------------------------------------------

@router.get("/{character_id}/sheet")
async def get_sheet(character_id: int):
    char = await fetch_one("SELECT * FROM characters WHERE CharacterID = %s", (character_id,))
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    abilities = await fetch_one("SELECT * FROM abilityscores WHERE CharacterID = %s", (character_id,))
    combat = await fetch_one("SELECT * FROM combatstats WHERE CharacterID = %s", (character_id,))

    return {
        "character": char,
        "abilityscores": abilities,
        "combatstats": combat
    }

# ---------------------------------------------------------
# RECALC
# ---------------------------------------------------------

@router.post("/{character_id}/recalc")
async def recalc(character_id: int):
    try:
        result = await recalc_character(character_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------
# PROFICIENCIES
# ---------------------------------------------------------

@router.post("/{character_id}/proficiencies")
async def set_proficiencies(character_id: int, data: dict):
    prof_ids = data.get("proficiency_ids", [])
    if not isinstance(prof_ids, list):
        raise HTTPException(status_code=400, detail="proficiency_ids must be a list")

    await execute("DELETE FROM character_proficiency WHERE CharacterID = %s", (character_id,))

    for pid in prof_ids:
        await execute(
            "INSERT INTO character_proficiency (CharacterID, ProficiencyID) VALUES (%s, %s)",
            (character_id, int(pid))
        )

    return {"success": True, "character_id": character_id, "proficiencies": prof_ids}

# ---------------------------------------------------------
# FEATS
# ---------------------------------------------------------

@router.post("/{character_id}/feats")
async def set_feats(character_id: int, data: dict):
    feat_ids = data.get("feat_ids", [])
    if not isinstance(feat_ids, list):
        raise HTTPException(status_code=400, detail="feat_ids must be a list")

    await execute("DELETE FROM character_feat WHERE CharacterID = %s", (character_id,))

    for fid in feat_ids:
        await execute(
            "INSERT INTO character_feat (CharacterID, FeatID) VALUES (%s, %s)",
            (character_id, int(fid))
        )

    return {"success": True, "character_id": character_id, "feats": feat_ids}

# ---------------------------------------------------------
# SPELLS
# ---------------------------------------------------------

@router.post("/{character_id}/spells")
async def set_spells(character_id: int, data: dict):
    spell_ids = data.get("spell_ids", [])
    if not isinstance(spell_ids, list):
        raise HTTPException(status_code=400, detail="spell_ids must be a list")

    await execute("DELETE FROM character_spell WHERE CharacterID = %s", (character_id,))

    for sid in spell_ids:
        await execute(
            "INSERT INTO character_spell (CharacterID, SpellID) VALUES (%s, %s)",
            (character_id, int(sid))
        )

    return {"success": True, "character_id": character_id, "spells": spell_ids}

# ---------------------------------------------------------
# EQUIPMENT
# ---------------------------------------------------------

@router.post("/{character_id}/equipment")
async def set_equipment(character_id: int, data: dict):
    eq_ids = data.get("equipment_ids", [])
    if not isinstance(eq_ids, list):
        raise HTTPException(status_code=400, detail="equipment_ids must be a list")

    await execute("DELETE FROM character_equipment WHERE CharacterID = %s", (character_id,))

    for eid in eq_ids:
        await execute(
            "INSERT INTO character_equipment (CharacterID, EquipmentID) VALUES (%s, %s)",
            (character_id, int(eid))
        )

    return {"success": True, "character_id": character_id, "equipment": eq_ids}

# ---------------------------------------------------------
# DELETE CHARACTER
# ---------------------------------------------------------

@router.delete("/{character_id}/delete")
async def delete_character(character_id: int):
    try:
        await execute("DELETE FROM characters WHERE CharacterID = %s", (character_id,))
        return {"success": True, "deleted_id": character_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {e}")