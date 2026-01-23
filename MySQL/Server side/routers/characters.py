# routers/characters.py
from fastapi import APIRouter, HTTPException
from services.characters import create_character
from database.core import fetch_all, fetch_one
from services.character_recalc import recalc_character
from database.core import execute, fetch_all

router = APIRouter(prefix="/api/characters", tags=["characters"])

@router.post("/create")
async def create_char(data: dict):
    try:
        account_id = int(data.get("account_id"))
        name = data.get("name")
        gender = data.get("gender", "Unspecified")
        level = int(data.get("level", 1))
        mode = data.get("mode", "Beginner")
        version = data.get("version", "5E")
        race_id = int(data.get("race_id"))
        class_id = int(data.get("class_id"))
        subclass_id = data.get("subclass_id")
        background_id = data.get("background_id")
        alignment_id = data.get("alignment_id")

        subclass_id = int(subclass_id) if subclass_id is not None else None
        background_id = int(background_id) if background_id is not None else None
        alignment_id = int(alignment_id) if alignment_id is not None else None

        str_score = int(data.get("str", 10))
        dex_score = int(data.get("dex", 10))
        con_score = int(data.get("con", 10))
        int_score = int(data.get("int", 10))
        wis_score = int(data.get("wis", 10))
        cha_score = int(data.get("cha", 10))

        char_id = create_character(
            account_id, name, gender,
            level, mode, version,
            race_id, class_id, subclass_id,
            background_id, alignment_id,
            str_score, dex_score, con_score,
            int_score, wis_score, cha_score
        )
        return {"success": True, "character_id": char_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list/{account_id}")
async def list_chars(account_id: int):
    chars = fetch_all(
        "SELECT * FROM characters WHERE AccountID = %s",
        (account_id,)
    )
    return {"characters": chars}

@router.get("/{character_id}/sheet")
async def get_sheet(character_id: int):
    char = fetch_one("SELECT * FROM characters WHERE CharacterID = %s", (character_id,))
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    abilities = fetch_one("SELECT * FROM abilityscores WHERE CharacterID = %s", (character_id,))
    combat = fetch_one("SELECT * FROM combatstats WHERE CharacterID = %s", (character_id,))

    return {
        "character": char,
        "abilityscores": abilities,
        "combatstats": combat
    }

@router.post("/{character_id}/recalc")
async def recalc(character_id: int):
    try:
        result = recalc_character(character_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/{character_id}/proficiencies")
async def set_proficiencies(character_id: int, data: dict):
    """
    Body: { "proficiency_ids": [1,2,3,...] }
    """
    prof_ids = data.get("proficiency_ids", [])
    if not isinstance(prof_ids, list):
        raise HTTPException(status_code=400, detail="proficiency_ids must be a list")

    # Clear existing
    execute("DELETE FROM character_proficiency WHERE CharacterID = %s", (character_id,))

    # Insert new
    for pid in prof_ids:
        execute(
            "INSERT INTO character_proficiency (CharacterID, ProficiencyID) VALUES (%s, %s)",
            (character_id, int(pid))
        )

    return {"success": True, "character_id": character_id, "proficiencies": prof_ids}

@router.post("/{character_id}/feats")
async def set_feats(character_id: int, data: dict):
    """
    Body: { "feat_ids": [1,2,3,...] }
    """
    feat_ids = data.get("feat_ids", [])
    if not isinstance(feat_ids, list):
        raise HTTPException(status_code=400, detail="feat_ids must be a list")

    execute("DELETE FROM character_feat WHERE CharacterID = %s", (character_id,))

    for fid in feat_ids:
        execute(
            "INSERT INTO character_feat (CharacterID, FeatID) VALUES (%s, %s)",
            (character_id, int(fid))
        )

    return {"success": True, "character_id": character_id, "feats": feat_ids}


@router.post("/{character_id}/spells")
async def set_spells(character_id: int, data: dict):
    """
    Body: { "spell_ids": [1,2,3,...] }
    """
    spell_ids = data.get("spell_ids", [])
    if not isinstance(spell_ids, list):
        raise HTTPException(status_code=400, detail="spell_ids must be a list")

    execute("DELETE FROM character_spell WHERE CharacterID = %s", (character_id,))

    for sid in spell_ids:
        execute(
            "INSERT INTO character_spell (CharacterID, SpellID) VALUES (%s, %s)",
            (character_id, int(sid))
        )

    return {"success": True, "character_id": character_id, "spells": spell_ids}


@router.post("/{character_id}/equipment")
async def set_equipment(character_id: int, data: dict):
    """
    Body: { "equipment_ids": [1,2,3,...] }
    """
    eq_ids = data.get("equipment_ids", [])
    if not isinstance(eq_ids, list):
        raise HTTPException(status_code=400, detail="equipment_ids must be a list")

    execute("DELETE FROM character_equipment WHERE CharacterID = %s", (character_id,))

    for eid in eq_ids:
        execute(
            "INSERT INTO character_equipment (CharacterID, EquipmentID) VALUES (%s, %s)",
            (character_id, int(eid))
        )

    return {"success": True, "character_id": character_id, "equipment": eq_ids}