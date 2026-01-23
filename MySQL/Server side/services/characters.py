from database.core import fetch_one, fetch_all, execute


# ------------------------------------------------------------
# GET ALL CHARACTERS FOR A USER
# ------------------------------------------------------------
def get_characters_for_user(user_id: int):
    rows = fetch_all(
        """
        SELECT CharacterID, Name, Level, RaceID, ClassID
        FROM characters
        WHERE AccountID = %s
        ORDER BY CharacterID DESC
        """,
        (user_id,)
    )

    characters = []
    for r in rows:
        characters.append({
            "id": r["CharacterID"],
            "name": r["Name"],
            "level": r["Level"],
            "race_id": r["RaceID"],
            "class_id": r["ClassID"]
        })

    return characters


# ------------------------------------------------------------
# GET A SINGLE CHARACTER (FULL BASIC INFO)
# ------------------------------------------------------------
def get_character(character_id: int):
    char = fetch_one(
        """
        SELECT CharacterID, Name, Level, RaceID, ClassID, AccountID
        FROM characters
        WHERE CharacterID = %s
        """,
        (character_id,)
    )

    if not char:
        return None

    # Load ability scores
    abilities = fetch_one(
        """
        SELECT StrScore, DexScore, ConScore, IntScore, WisScore, ChaScore,
               StrMod, DexMod, ConMod, IntMod, WisMod, ChaMod
        FROM abilityscores
        WHERE CharacterID = %s
        """,
        (character_id,)
    )

    # Load combat stats
    combat = fetch_one(
        """
        SELECT MaxHP, HP, ArmorClass, Initiative, PassivePerception,
               HitDiceTotal, HitDiceRemaining
        FROM combatstats
        WHERE CharacterID = %s
        """,
        (character_id,)
    )

    return {
        "id": char["CharacterID"],
        "name": char["Name"],
        "level": char["Level"],
        "race_id": char["RaceID"],
        "class_id": char["ClassID"],
        "account_id": char["AccountID"],
        "ability_scores": abilities,
        "combat_stats": combat
    }