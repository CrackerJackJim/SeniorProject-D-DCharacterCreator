from database.core import fetch_one, execute

print(">>> USING THIS create_character FUNCTION <<<")


def compute_prof_bonus(level: int) -> int:
    return 2 + (level - 1) // 4


async def create_character(
    account_id, name, gender,
    level,
    race_id, class_id, subclass_id,
    background_id, alignment_id,
    str_score, dex_score, con_score,
    int_score, wis_score, cha_score,
    experience=0,
    proficiency_bonus=None
):
    print(">>> create_character CALLED WITH:", experience, proficiency_bonus)

    # Convert empty strings or "None" to actual SQL NULL
    def clean_fk(value):
        return None if value in ("", "None", None, "") else value

    subclass_id = clean_fk(subclass_id)
    background_id = clean_fk(background_id)
    alignment_id = clean_fk(alignment_id)

    # Normalize gender
    valid_genders = ("Male", "Female", "Unspecified")
    if gender not in valid_genders:
        gender = "Unspecified"

    # Compute proficiency bonus if not provided
    if proficiency_bonus is None:
        proficiency_bonus = compute_prof_bonus(level)

    # Debug print
    print("DEBUG INSERT VALUES:", {
        "account_id": account_id,
        "name": name,
        "gender": gender,
        "level": level,
        "race_id": race_id,
        "class_id": class_id,
        "subclass_id": subclass_id,
        "background_id": background_id,
        "alignment_id": alignment_id,
        "experience": experience,
        "proficiency_bonus": proficiency_bonus
    })

    # INSERT into characters — column order matches schema
    char_id = await execute("""
        INSERT INTO characters (
            AccountID, Name, Gender,
            Level,
            RaceID, ClassID, SubclassID, BackgroundID, AlignmentID,
            Experience, ProficiencyBonus
        ) VALUES (
            %s, %s, %s,
            %s,
            %s, %s, %s, %s, %s,
            %s, %s
        )
    """, (
        account_id, name, gender,
        level,
        race_id, class_id, subclass_id, background_id, alignment_id,
        experience, proficiency_bonus
    ))

    print(">>> NEW CHARACTER ID:", char_id)

    # Insert ability scores
    await execute("""
        INSERT INTO abilityscores (
            CharacterID,
            StrScore, StrMod,
            DexScore, DexMod,
            ConScore, ConMod,
            IntScore, IntMod,
            WisScore, WisMod,
            ChaScore, ChaMod
        ) VALUES (
            %s, %s, %s,
            %s, %s,
            %s, %s,
            %s, %s,
            %s, %s,
            %s, %s
        )
    """, (
        char_id,
        str_score, (str_score - 10) // 2,
        dex_score, (dex_score - 10) // 2,
        con_score, (con_score - 10) // 2,
        int_score, (int_score - 10) // 2,
        wis_score, (wis_score - 10) // 2,
        cha_score, (cha_score - 10) // 2
    ))

    return char_id