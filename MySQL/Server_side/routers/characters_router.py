from fastapi import APIRouter, HTTPException
from fastapi import Response

from Server_side.services.character_service import create_character
from Server_side.services.character_recalc import recalc_character
from Server_side.database.core import fetch_all, fetch_one, execute

router = APIRouter(prefix="/api/characters", tags=["characters"])

print(">>> RUNNING FILE:", __file__)

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

    name = data.get("name") or "Unnamed"
    gender = data.get("gender") or "Unspecified"
    level = safe_int(data.get("level")) or 1

    race_id = normalize_fk(data.get("race_id"))
    class_id = normalize_fk(data.get("class_id"))

    if race_id is None:
        raise HTTPException(status_code=400, detail="Missing or invalid race_id")
    if class_id is None:
        raise HTTPException(status_code=400, detail="Missing or invalid class_id")

    background_id = normalize_fk(data.get("background_id"))
    alignment_id = normalize_fk(data.get("alignment_id"))
    subclass_id = normalize_fk(data.get("subclass_id"))

    str_score = safe_int(data.get("str")) or 10
    dex_score = safe_int(data.get("dex")) or 10
    con_score = safe_int(data.get("con")) or 10
    int_score = safe_int(data.get("int")) or 10
    wis_score = safe_int(data.get("wis")) or 10
    cha_score = safe_int(data.get("cha")) or 10

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

    # ---------------------------------------------------------
    # PATCH #1 — FORCE FIGHTER HIT DIE = d10
    # ---------------------------------------------------------
    await execute(
        """
        UPDATE combat_stats
        SET HitDiceType = 10
        WHERE CharacterID = %s
        """,
        (char_id,)
    )

    # ---------------------------------------------------------
    # PATCH #2 — SET LEVEL 1 HP CORRECTLY
    # ---------------------------------------------------------

    # Fetch CON score
    con_row = await fetch_one(
        "SELECT ConScore FROM abilityscores WHERE CharacterID = %s",
        (char_id,)
    )
    con_mod = (con_row["ConScore"] - 10) // 2

    # Fighter max hit die = 10
    level1_hp = 10 + con_mod
    if level1_hp < 1:
        level1_hp = 1

    # Set correct level‑1 HP + hit dice
    await execute(
        """
        UPDATE combat_stats
        SET 
            MaxHP = %s,
            CurrentHP = %s,
            HitDiceTotal = 1,
            HitDiceRemaining = 1
        WHERE CharacterID = %s
        """,
        (level1_hp, level1_hp, char_id)
    )

    # Ensure default saving throws row exists
    await execute(
        """
        INSERT INTO charactersavingthrows (CharacterID)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE CharacterID = CharacterID
        """,
        (char_id,)
    )

    # Ensure default skills row exists
    await execute(
        """
        INSERT INTO characterskills (CharacterID)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE CharacterID = CharacterID
        """,
        (char_id,)
    )

    # Ensure default inventory row exists
    await execute(
        """
        INSERT INTO characterinventory (CharacterID)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE CharacterID = CharacterID
        """,
        (char_id,)
    )

    return {"success": True, "character_id": char_id}


# ---------------------------------------------------------
# GET ALL CHARACTERS FOR ACCOUNT
# ---------------------------------------------------------

@router.get("/account/{account_id}")
async def get_characters_for_account(account_id: int):
    query = """
        SELECT 
            c.CharacterID,
            c.Name,
            c.Level,
            c.CreatedAt AS CreatedDate,
            c.UpdatedAt AS LastEdited,

            r.Name  AS RaceName,
            cl.Name AS ClassName,
            b.Name  AS BackgroundName

        FROM characters c
        LEFT JOIN race r ON c.RaceID = r.RaceID
        LEFT JOIN class cl ON c.ClassID = cl.ClassID
        LEFT JOIN background b ON c.BackgroundID = b.BackgroundID

        WHERE c.AccountID = %s
    """
    rows = await fetch_all(query, (account_id,))
    return rows


# ---------------------------------------------------------
# GET SINGLE CHARACTER
# ---------------------------------------------------------

@router.get("/{char_id}")
async def get_character(char_id: int):
    row = await fetch_one("SELECT * FROM characters WHERE CharacterID = %s", (char_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Character not found")
    return row


# ---------------------------------------------------------
# UPDATE CHARACTER (FULL SHEET SAVE)
# ---------------------------------------------------------

@router.post("/{char_id}/update")
async def update_character(char_id: int, data: dict):

    print(">>> RUNNING FILE:", __file__)
    print("Updating character", char_id)
    print("RAW DATA RECEIVED:", data)

    overview = data.get("overview") or {}
    abilities = data.get("abilities") or {}
    combat = data.get("combat") or {}
    saving_throws = data.get("saving_throws") or {}
    skills = data.get("skills") or {}
    inventory = data.get("inventory") or {}

    # -----------------------------
    # UPDATE characters table
    # -----------------------------
    await execute(
        """
        UPDATE characters SET
            Name = %s,
            PlayerName = %s,
            Gender = %s,
            Level = %s,
            AlignmentID = %s,
            Experience = %s
        WHERE CharacterID = %s
        """,
        (
            overview.get("name"),
            overview.get("player_name"),
            overview.get("gender"),
            safe_int(overview.get("level")),
            normalize_fk(overview.get("alignment")),
            safe_int(overview.get("xp")),
            char_id,
        ),
    )
    
    # -----------------------------
    # UPDATE abilityscores
    # -----------------------------
    await execute(
        """
        UPDATE abilityscores SET
            StrScore = %s,
            DexScore = %s,
            ConScore = %s,
            IntScore = %s,
            WisScore = %s,
            ChaScore = %s
        WHERE CharacterID = %s
        """,
        (
            abilities.get("strength"),
            abilities.get("dexterity"),
            abilities.get("constitution"),
            abilities.get("intelligence"),
            abilities.get("wisdom"),
            abilities.get("charisma"),
            char_id,
        ),
    )

    # -----------------------------
    # UPSERT combatstats (WITH TempHP)
    # -----------------------------
    await execute(
        """
        INSERT INTO combat_stats (
            CharacterID,
            ArmorClass,
            CurrentHP,
            MaxHP,
            TempHP,
            Initiative,
            Speed,
            SpeedClimb,
            SpeedSwim,
            SpeedFly,
            HitDiceTotal,
            HitDiceRemaining,
            PassivePerception,
            PassiveInvestigation,
            PassiveInsight,
            DeathSuccess1,
            DeathSuccess2,
            DeathSuccess3,
            DeathFail1,
            DeathFail2,
            DeathFail3,
            Resistances,
            Immunities,
            Vulnerabilities,
            Conditions,
            ProficiencyBonus,
            Money
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            ArmorClass = VALUES(ArmorClass),
            CurrentHP = VALUES(CurrentHP),
            MaxHP = VALUES(MaxHP),
            TempHP = VALUES(TempHP),
            Initiative = VALUES(Initiative),
            Speed = VALUES(Speed),
            SpeedClimb = VALUES(SpeedClimb),
            SpeedSwim = VALUES(SpeedSwim),
            SpeedFly = VALUES(SpeedFly),
            HitDiceTotal = VALUES(HitDiceTotal),
            HitDiceRemaining = VALUES(HitDiceRemaining),
            PassivePerception = VALUES(PassivePerception),
            PassiveInvestigation = VALUES(PassiveInvestigation),
            PassiveInsight = VALUES(PassiveInsight),
            DeathSuccess1 = VALUES(DeathSuccess1),
            DeathSuccess2 = VALUES(DeathSuccess2),
            DeathSuccess3 = VALUES(DeathSuccess3),
            DeathFail1 = VALUES(DeathFail1),
            DeathFail2 = VALUES(DeathFail2),
            DeathFail3 = VALUES(DeathFail3),
            Resistances = VALUES(Resistances),
            Immunities = VALUES(Immunities),
            Vulnerabilities = VALUES(Vulnerabilities),
            Conditions = VALUES(Conditions),
            ProficiencyBonus = VALUES(ProficiencyBonus),
            Money = VALUES(Money)
        """,
        (
            char_id,
            safe_int(combat.get("ac")),
            safe_int(combat.get("hp")) or 1,
            safe_int(combat.get("max_hp")) or 1,
            safe_int(combat.get("temp_hp")) or 0,
            safe_int(combat.get("initiative")),
            safe_int(combat.get("speed")),
            safe_int(combat.get("speed_climb")) or 0,
            safe_int(combat.get("speed_swim")) or 0,
            safe_int(combat.get("speed_fly")) or 0,
            safe_int(combat.get("hit_dice_total")) or 0,
            safe_int(combat.get("hit_dice_remaining")) or 0,
            safe_int(combat.get("passive_perception")) or 0,
            safe_int(combat.get("passive_investigation")) or 0,
            safe_int(combat.get("passive_insight")) or 0,
            int(bool(combat.get("death_success_1"))),
            int(bool(combat.get("death_success_2"))),
            int(bool(combat.get("death_success_3"))),
            int(bool(combat.get("death_fail_1"))),
            int(bool(combat.get("death_fail_2"))),
            int(bool(combat.get("death_fail_3"))),
            combat.get("resistances"),
            combat.get("immunities"),
            combat.get("vulnerabilities"),
            combat.get("conditions"),
            safe_int(combat.get("proficiency_bonus")) or 0,
            str(combat.get("money") or "0"),
        ),
    )

    # -----------------------------
    # UPSERT saving throws
    # -----------------------------
    st = saving_throws or {}
    await execute(
        """
        INSERT INTO charactersavingthrows (
            CharacterID,
            StrProf, StrValue,
            DexProf, DexValue,
            ConProf, ConValue,
            IntProf, IntValue,
            WisProf, WisValue,
            ChaProf, ChaValue
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            StrProf = VALUES(StrProf),
            StrValue = VALUES(StrValue),
            DexProf = VALUES(DexProf),
            DexValue = VALUES(DexValue),
            ConProf = VALUES(ConProf),
            ConValue = VALUES(ConValue),
            IntProf = VALUES(IntProf),
            IntValue = VALUES(IntValue),
            WisProf = VALUES(WisProf),
            WisValue = VALUES(WisValue),
            ChaProf = VALUES(ChaProf),
            ChaValue = VALUES(ChaValue)
        """,
        (
            char_id,
            int(bool(st.get("str", {}).get("proficient"))),
            st.get("str", {}).get("value"),
            int(bool(st.get("dex", {}).get("proficient"))),
            st.get("dex", {}).get("value"),
            int(bool(st.get("con", {}).get("proficient"))),
            st.get("con", {}).get("value"),
            int(bool(st.get("int", {}).get("proficient"))),
            st.get("int", {}).get("value"),
            int(bool(st.get("wis", {}).get("proficient"))),
            st.get("wis", {}).get("value"),
            int(bool(st.get("cha", {}).get("proficient"))),
            st.get("cha", {}).get("value"),
        ),
    )

    # -----------------------------
    # UPDATE skills
    # -----------------------------
    sk = skills if isinstance(skills, dict) else {}

    def s(name: str):
        return sk.get(name)

    await execute(
        """
        UPDATE characterskills SET
            AcrobaticsValue        = %s,
            AnimalHandlingValue    = %s,
            ArcanaValue            = %s,
            AthleticsValue         = %s,
            DeceptionValue         = %s,
            HistoryValue           = %s,
            InsightValue           = %s,
            IntimidationValue      = %s,
            InvestigationValue     = %s,
            MedicineValue          = %s,
            NatureValue            = %s,
            PerceptionValue        = %s,
            PerformanceValue       = %s,
            PersuasionValue        = %s,
            ReligionValue          = %s,
            SleightOfHandValue     = %s,
            StealthValue           = %s,
            SurvivalValue          = %s
        WHERE CharacterID = %s
        """,
        (
            s("acrobatics"),
            s("animal_handling"),
            s("arcana"),
            s("athletics"),
            s("deception"),
            s("history"),
            s("insight"),
            s("intimidation"),
            s("investigation"),
            s("medicine"),
            s("nature"),
            s("perception"),
            s("performance"),
            s("persuasion"),
            s("religion"),
            s("sleight_of_hand"),
            s("stealth"),
            s("survival"),
            char_id,
        )
    )

    # -----------------------------
    # UPSERT inventory
    # -----------------------------
    await execute(
        """
        INSERT INTO characterinventory (
            CharacterID,
            CP, SP, EP, GP, PP,
            Armor, Weapons, Tools, MiscItems
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            CP = VALUES(CP),
            SP = VALUES(SP),
            EP = VALUES(EP),
            GP = VALUES(GP),
            PP = VALUES(PP),
            Armor = VALUES(Armor),
            Weapons = VALUES(Weapons),
            Tools = VALUES(Tools),
            MiscItems = VALUES(MiscItems)
        """,
        (
            char_id,
            inventory.get("cp"),
            inventory.get("sp"),
            inventory.get("ep"),
            inventory.get("gp"),
            inventory.get("pp"),
            inventory.get("armor"),
            inventory.get("weapons"),
            inventory.get("tools"),
            inventory.get("misc_items"),
        )
    )

    # -----------------------------
    # UPSERT spells
    # -----------------------------
    spells = data.get("spells") or {}

    await execute(
        """
        INSERT INTO characterspells (
            CharacterID,
            SpellcastingAbility,
            SpellSaveDC,
            SpellAttackBonus,

            L1SlotsTotal, L1SlotsRemaining,
            L2SlotsTotal, L2SlotsRemaining,
            L3SlotsTotal, L3SlotsRemaining,
            L4SlotsTotal, L4SlotsRemaining,
            L5SlotsTotal, L5SlotsRemaining,
            L6SlotsTotal, L6SlotsRemaining,
            L7SlotsTotal, L7SlotsRemaining,
            L8SlotsTotal, L8SlotsRemaining,
            L9SlotsTotal, L9SlotsRemaining,

            KnownSpells,
            PreparedSpells
        )
        VALUES (%s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s)
        ON DUPLICATE KEY UPDATE
            SpellcastingAbility = VALUES(SpellcastingAbility),
            SpellSaveDC = VALUES(SpellSaveDC),
            SpellAttackBonus = VALUES(SpellAttackBonus),

            L1SlotsTotal = VALUES(L1SlotsTotal),
            L1SlotsRemaining = VALUES(L1SlotsRemaining),
            L2SlotsTotal = VALUES(L2SlotsTotal),
            L2SlotsRemaining = VALUES(L2SlotsRemaining),
            L3SlotsTotal = VALUES(L3SlotsTotal),
            L3SlotsRemaining = VALUES(L3SlotsRemaining),
            L4SlotsTotal = VALUES(L4SlotsTotal),
            L4SlotsRemaining = VALUES(L4SlotsRemaining),
            L5SlotsTotal = VALUES(L5SlotsTotal),
            L5SlotsRemaining = VALUES(L5SlotsRemaining),
            L6SlotsTotal = VALUES(L6SlotsTotal),
            L6SlotsRemaining = VALUES(L6SlotsRemaining),
            L7SlotsTotal = VALUES(L7SlotsTotal),
            L7SlotsRemaining = VALUES(L7SlotsRemaining),
            L8SlotsTotal = VALUES(L8SlotsTotal),
            L8SlotsRemaining = VALUES(L8SlotsRemaining),
            L9SlotsTotal = VALUES(L9SlotsTotal),
            L9SlotsRemaining = VALUES(L9SlotsRemaining),

            KnownSpells = VALUES(KnownSpells),
            PreparedSpells = VALUES(PreparedSpells)
        """,
        (
            char_id,
            spells.get("ability"),
            spells.get("save_dc"),
            spells.get("attack_bonus"),

            spells.get("l1_total"), spells.get("l1_remaining"),
            spells.get("l2_total"), spells.get("l2_remaining"),
            spells.get("l3_total"), spells.get("l3_remaining"),
            spells.get("l4_total"), spells.get("l4_remaining"),
            spells.get("l5_total"), spells.get("l5_remaining"),
            spells.get("l6_total"), spells.get("l6_remaining"),
            spells.get("l7_total"), spells.get("l7_remaining"),
            spells.get("l8_total"), spells.get("l8_remaining"),
            spells.get("l9_total"), spells.get("l9_remaining"),

            spells.get("known_spells"),
            spells.get("prepared_spells"),
        )
    )

    # -----------------------------
    # UPSERT feats & traits
    # -----------------------------
    traits = data.get("traits") or {}

    await execute(
        """
        INSERT INTO charactertraits (
            CharacterID,
            Feats,
            RaceFeatures,
            ClassFeatures,
            BackgroundFeatures,
            ProficienciesLanguages,
            PersonalityTraits,
            Ideals,
            Bonds,
            Flaws,
            Backstory
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            Feats = VALUES(Feats),
            RaceFeatures = VALUES(RaceFeatures),
            ClassFeatures = VALUES(ClassFeatures),
            BackgroundFeatures = VALUES(BackgroundFeatures),
            ProficienciesLanguages = VALUES(ProficienciesLanguages),
            PersonalityTraits = VALUES(PersonalityTraits),
            Ideals = VALUES(Ideals),
            Bonds = VALUES(Bonds),
            Flaws = VALUES(Flaws),
            Backstory = VALUES(Backstory)
        """,
        (
            char_id,
            traits.get("feats"),
            traits.get("race_features"),
            traits.get("class_features"),
            traits.get("background_features"),
            traits.get("proficiencies_languages"),
            traits.get("personality_traits"),
            traits.get("ideals"),
            traits.get("bonds"),
            traits.get("flaws"),
            traits.get("backstory"),
        )
    )

    return {"success": True, "character_id": char_id}


# ---------------------------------------------------------
# SHEET (character + abilities + combat + saves + skills + inventory)
# ---------------------------------------------------------

@router.get("/{character_id}/sheet")
async def get_sheet(character_id: int, response: Response):
    response.headers["Cache-Control"] = "no-store"

    # Debug check
    print("SHEET LOADER DB CHECK:", await fetch_one(
        "SELECT SubclassID FROM characters WHERE CharacterID = %s",
        (character_id,)
    ))

    # ---------------------------------------------------------
    # EXPLICIT CHARACTER SELECT (NO c.* ANYWHERE)
    # ---------------------------------------------------------
    char = await fetch_one(
        """
        SELECT 
            c.CharacterID,
            c.AccountID,
            c.Name,
            c.Gender,
            c.Level,
            c.RaceID,
            c.ClassID,
            c.BackgroundID,
            c.AlignmentID,
            c.Experience,
            c.ProficiencyBonus,
            c.ProfileIconURL,
            c.CreatedAt,
            c.UpdatedAt,
            c.PlayerName,
            c.SubclassID,          
            r.Name  AS RaceName,
            cl.Name AS ClassName,
            b.Name  AS BackgroundName
        FROM characters c
        LEFT JOIN race r ON c.RaceID = r.RaceID
        LEFT JOIN class cl ON c.ClassID = cl.ClassID
        LEFT JOIN background b ON c.BackgroundID = b.BackgroundID
        WHERE c.CharacterID = %s
        """,
        (character_id,)
    )

    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    # ---------------------------------------------------------
    # REMAINING TABLES (unchanged)
    # ---------------------------------------------------------
    abilities = await fetch_one("SELECT * FROM abilityscores WHERE CharacterID = %s", (character_id,))
    combat = await fetch_one("SELECT * FROM combat_stats WHERE CharacterID = %s", (character_id,))
    saving_throws = await fetch_one("SELECT * FROM charactersavingthrows WHERE CharacterID = %s", (character_id,))
    skills = await fetch_one("SELECT * FROM characterskills WHERE CharacterID = %s", (character_id,))
    inventory = await fetch_one("SELECT * FROM characterinventory WHERE CharacterID = %s", (character_id,))
    spells = await fetch_one("SELECT * FROM characterspells WHERE CharacterID = %s", (character_id,))
    traits = await fetch_one("SELECT * FROM charactertraits WHERE CharacterID = %s", (character_id,))

    if not skills:
        await execute("INSERT INTO characterskills (CharacterID) VALUES (%s)", (character_id,))
        skills = await fetch_one("SELECT * FROM characterskills WHERE CharacterID = %s", (character_id,))

    # ---------------------------------------------------------
    # AVAILABLE SUBCLASSES (LEVEL‑GATED)
    # ---------------------------------------------------------
    if char["ClassName"] == "Fighter" and char["Level"] < 3:
        subclasses = []  # No subclass until level 3
    else:
        subclasses = await fetch_all(
            "SELECT * FROM subclass WHERE ClassID = %s",
            (char["ClassID"],)
        )

    return {
        "character": char,
        "abilityscores": abilities,
        "combatstats": combat,
        "savingthrows": saving_throws,
        "skills": skills,
        "inventory": inventory,
        "spells": spells,
        "traits": traits,
        "available_subclasses": subclasses
    }


# ---------------------------------------------------------
# RECALC / PROFICIENCIES / FEATS / SPELLS / EQUIPMENT / DELETE / TOUCH
# ---------------------------------------------------------

@router.post("/{character_id}/recalc")
async def recalc(character_id: int):
    try:
        result = await recalc_character(character_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.delete("/{character_id}/delete")
async def delete_character(character_id: int):
    try:
        await execute("DELETE FROM characters WHERE CharacterID = %s", (character_id,))
        return {"success": True, "deleted_id": character_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Delete failed: {e}")


@router.post("/{character_id}/touch")
async def touch_character(character_id: int):
    try:
        await execute(
            "UPDATE characters SET UpdatedAt = NOW() WHERE CharacterID = %s",
            (character_id,)
        )
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Touch failed: {e}")
    

@router.post("/{character_id}/subclass/select")
async def select_subclass(character_id: int, data: dict):
    subclass_id = data.get("subclass_id")

    if subclass_id is None:
        raise HTTPException(status_code=400, detail="Missing subclass_id")

    await execute(
        "UPDATE characters SET SubclassID = %s WHERE CharacterID = %s",
        (subclass_id, character_id)
    )

    result = await fetch_one(
        "SELECT SubclassID FROM characters WHERE CharacterID = %s",
        (character_id,)
    )
    print("DEBUG SUBCLASS AFTER UPDATE:", result)

    return {"success": True}


@router.post("/{character_id}/level_up")
async def level_up(character_id: int, data: dict):
    manual_roll = safe_int(data.get("manual_roll"))
    if manual_roll is None:
        raise HTTPException(status_code=400, detail="Missing manual_roll")

    # Fetch character level
    char = await fetch_one(
        "SELECT Level FROM characters WHERE CharacterID = %s",
        (character_id,)
    )

    # Fetch CON score (DO NOT RESET ABILITY SCORES)
    abilities = await fetch_one(
        "SELECT ConScore FROM abilityscores WHERE CharacterID = %s",
        (character_id,)
    )

    # Fetch combat stats
    combat = await fetch_one(
        "SELECT MaxHP, CurrentHP, HitDiceTotal, HitDiceRemaining FROM combat_stats WHERE CharacterID = %s",
        (character_id,)
    )

    if not char or not abilities or not combat:
        raise HTTPException(status_code=404, detail="Character not found")

    # Calculate CON modifier
    con_mod = (abilities["ConScore"] - 10) // 2

    # HP gained from level-up
    gained_hp = manual_roll + con_mod
    if gained_hp < 1:
        gained_hp = 1

    # New values
    new_level = char["Level"] + 1
    new_max_hp = combat["MaxHP"] + gained_hp
    new_current_hp = combat["CurrentHP"] + gained_hp
    new_hitdice_total = combat["HitDiceTotal"] + 1
    new_hitdice_remaining = combat["HitDiceRemaining"] + 1

    # Update character level
    await execute(
        "UPDATE characters SET Level = %s WHERE CharacterID = %s",
        (new_level, character_id)
    )

    # Update combat stats
    await execute(
        """
        UPDATE combat_stats
        SET 
            MaxHP = %s,
            CurrentHP = %s,
            HitDiceTotal = %s,
            HitDiceRemaining = %s
        WHERE CharacterID = %s
        """,
        (
            new_max_hp,
            new_current_hp,
            new_hitdice_total,
            new_hitdice_remaining,
            character_id
        )
    )

    # Return updated HP so frontend can update without losing ability scores
    return {
        "success": True,
        "new_level": new_level,
        "new_max_hp": new_max_hp,
        "new_current_hp": new_current_hp
    }