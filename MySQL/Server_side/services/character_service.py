from Server_side.database.core import fetch_one, execute

print(">>> USING THIS create_character FUNCTION <<<")


def compute_prof_bonus(level: int) -> int:
    return 2 + (level - 1) // 4


def safe_score(value):
    try:
        return int(value)
    except:
        return 10


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

    gender = (gender or "").strip()

    # Compute proficiency bonus if not provided
    if proficiency_bonus is None:
        proficiency_bonus = compute_prof_bonus(level)

    # Normalize ALL ability scores safely
    str_score = safe_score(str_score)
    dex_score = safe_score(dex_score)
    con_score = safe_score(con_score)
    int_score = safe_score(int_score)
    wis_score = safe_score(wis_score)
    cha_score = safe_score(cha_score)

    print("ABILITY SCORES CLEANED:", {
        "STR": str_score,
        "DEX": dex_score,
        "CON": con_score,
        "INT": int_score,
        "WIS": wis_score,
        "CHA": cha_score
    })

    # ---------------------------------------------------------
    # INSERT INTO characters  (char_id is created HERE)
    # ---------------------------------------------------------
    char_id = await execute("""
        INSERT INTO characters (
            AccountID, Name, Gender,
            Level,
            RaceID, ClassID, BackgroundID, AlignmentID,
            Experience, ProficiencyBonus
        ) VALUES (
            %s, %s, %s,
            %s,
            %s, %s, %s, %s,
            %s, %s
        )
    """, (
        account_id, name, gender,
        level,
        race_id, class_id, background_id, alignment_id,
        experience, proficiency_bonus
    ))

    print(">>> NEW CHARACTER ID:", char_id)

    # ---------------------------------------------------------
    # INSERT ABILITY SCORES
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # INSERT COMBAT STATS (Level 1 defaults)
    # ---------------------------------------------------------

    # 1. Fetch class hit die (VARCHAR)
    class_row = await fetch_one(
        "SELECT HitDiceType FROM class WHERE ClassID = %s",
        (class_id,)
    )

    raw_hit_die = class_row["HitDiceType"] if class_row else None

    # 2. Normalize hit die string → integer
    def parse_hit_die(value):
        if not value:
            return None
        value = str(value).strip().lower()
        if value.startswith("d"):
            value = value[1:]
        try:
            return int(value)
        except:
            return None

    hit_dice_type = parse_hit_die(raw_hit_die)
    if hit_dice_type is None:
        hit_dice_type = 8  # safe fallback

    # 3. Compute level 1 HP
    con_mod = (con_score - 10) // 2
    max_hp = hit_dice_type + con_mod
    if max_hp < 1:
        max_hp = 1
    hp = max_hp

    # 4. Insert combat stats (MATCHING YOUR REAL TABLE)
    await execute("""
        INSERT INTO combat_stats (
            CharacterID,
            MaxHP,
            CurrentHP,
            TempHP,
            HitDiceType,
            HitDiceTotal,
            HitDiceRemaining,
            ArmorClass,
            Initiative,
            Speed
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        )
    """, (
        char_id,
        max_hp,        # MaxHP
        hp,            # CurrentHP
        0,             # TempHP
        hit_dice_type, # HitDiceType
        1,             # HitDiceTotal
        1,             # HitDiceRemaining
        10,            # ArmorClass
        0,             # Initiative
        30             # Speed
    ))

    print(">>> COMBAT STATS INSERTED for", char_id, "HD:", hit_dice_type, "HP:", hp)

    return char_id