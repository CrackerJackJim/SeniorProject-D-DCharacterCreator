# services/character_recalc.py
from Server_side.database.core import fetch_one, fetch_all, execute
import math
import json
from datetime import datetime

# ------------------------------------------------------------
# BASIC HELPERS
# ------------------------------------------------------------
def ability_mod(score: int) -> int:
    return math.floor((score - 10) / 2)


def proficiency_bonus(level: int) -> int:
    if level >= 17:
        return 6
    if level >= 13:
        return 5
    if level >= 9:
        return 4
    if level >= 5:
        return 3
    return 2


def average_hit_die(hit_dice_type: str) -> int:
    try:
        die = int(hit_dice_type.lower().replace("d", ""))
    except Exception:
        die = 8
    return math.ceil(die / 2) + 1


# ------------------------------------------------------------
# SKILLS & SAVING THROWS (TITLE CASE)
# ------------------------------------------------------------
SKILL_ABILITY = {
    "Acrobatics": "dex",
    "Animal Handling": "wis",
    "Arcana": "int",
    "Athletics": "str",
    "Deception": "cha",
    "History": "int",
    "Insight": "wis",
    "Intimidation": "cha",
    "Investigation": "int",
    "Medicine": "wis",
    "Nature": "int",
    "Perception": "wis",
    "Performance": "cha",
    "Persuasion": "cha",
    "Religion": "int",
    "Sleight of Hand": "dex",
    "Stealth": "dex",
    "Survival": "wis"
}

SAVING_THROW_ABILITY = {
    "Strength": "str",
    "Dexterity": "dex",
    "Constitution": "con",
    "Intelligence": "int",
    "Wisdom": "wis",
    "Charisma": "cha"
}


def compute_skills(mods, profs, prof_bonus):
    skills = {}
    prof_skill_names = [p["name"] for p in profs["Skill"]]

    for skill, ability in SKILL_ABILITY.items():
        base = mods[ability]
        if skill in prof_skill_names:
            base += prof_bonus
        skills[skill] = base

    return skills


def compute_saving_throws(mods, profs, prof_bonus):
    saves = {}
    prof_save_names = [p["name"] for p in profs["SavingThrow"]]

    for save, ability in SAVING_THROW_ABILITY.items():
        base = mods[ability]
        if save in prof_save_names:
            base += prof_bonus
        saves[save] = base

    return saves


def compute_passives(skills):
    return {
        "Perception": 10 + skills["Perception"],
        "Investigation": 10 + skills["Investigation"],
        "Insight": 10 + skills["Insight"]
    }


# ------------------------------------------------------------
# FEATURE LOADING
# ------------------------------------------------------------
def load_features_for_character(char: dict):
    class_id = char["ClassID"]
    subclass_id = char["SubclassID"]
    background_id = char["BackgroundID"]

    class_feats = fetch_all(
        "SELECT FeatureID, Name, Description, SubclassID FROM classfeature WHERE ClassID = %s",
        (class_id,)
    )

    base_features = []
    subclass_features = []

    for f in class_feats:
        feat_obj = {
            "id": f["FeatureID"],
            "name": f["Name"],
            "desc": f["Description"]
        }
        if f["SubclassID"] is None:
            base_features.append(feat_obj)
        elif subclass_id is not None and f["SubclassID"] == subclass_id:
            subclass_features.append(feat_obj)

    background_features = []
    if background_id is not None:
        background_rows = fetch_all(
            "SELECT Name, Description FROM backgroundfeature WHERE BackgroundID = %s",
            (background_id,)
        )
        background_features = [
            {"name": b["Name"], "desc": b["Description"]}
            for b in background_rows
        ]

    return {
        "class_features": base_features,
        "subclass_features": subclass_features,
        "background_features": background_features
    }


# ------------------------------------------------------------
# PERSONALITY
# ------------------------------------------------------------
def load_personality(character_id: int):
    rows = fetch_all(
        "SELECT PersonalityID, Type, Description FROM character_personality WHERE CharacterID = %s",
        (character_id,)
    )

    traits = {
        "Trait": [],
        "Ideal": [],
        "Bond": [],
        "Flaw": []
    }

    for r in rows:
        t = r["Type"]
        if t in traits:
            traits[t].append({
                "id": r["PersonalityID"],
                "description": r["Description"]
            })

    return traits


# ------------------------------------------------------------
# PROFICIENCIES
# ------------------------------------------------------------
def load_character_proficiencies(character_id: int):
    rows = fetch_all(
        """
        SELECT p.ProficiencyID, p.Name, p.Type
        FROM character_proficiency cp
        JOIN proficiency p ON cp.ProficiencyID = p.ProficiencyID
        WHERE cp.CharacterID = %s
        """,
        (character_id,)
    )

    result = {
        "Skill": [],
        "SavingThrow": [],
        "Tool": [],
        "Armor": [],
        "Weapon": [],
        "Language": [],
        "Item": []
    }

    for r in rows:
        t = r["Type"]
        if t in result:
            result[t].append({
                "id": r["ProficiencyID"],
                "name": r["Name"]
            })

    return result


def extend_proficiencies_with_effects(profs, effects):
    prof_effects = effects.get("proficiencies", {})
    for ptype, names in prof_effects.items():
        if ptype not in profs:
            continue
        existing_names = {p["name"] for p in profs[ptype]}
        for name in names:
            if name not in existing_names:
                profs[ptype].append({"id": None, "name": name})
    return profs


# ------------------------------------------------------------
# FEATS + EFFECTS
# ------------------------------------------------------------
def load_character_feats(character_id: int):
    rows = fetch_all(
        """
        SELECT f.FeatID, f.Name, f.Description, f.Prerequisite, f.EffectJson
        FROM character_feat cf
        JOIN feat f ON cf.FeatID = f.FeatID
        WHERE cf.CharacterID = %s
        """,
        (character_id,)
    )

    feats = []
    for r in rows:
        feats.append({
            "id": r["FeatID"],
            "name": r["Name"],
            "description": r["Description"],
            "prerequisite": r["Prerequisite"],
            "effect_json": r["EffectJson"]
        })
    return feats


def parse_feat_effects(feats):
    effects = {
        "ability_scores": {},
        "skills": {},
        "ac_bonus": 0,
        "speed_bonus": 0,
        "proficiencies": {}
    }

    for feat in feats:
        raw = feat.get("effect_json")
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        # ability_scores
        for ability, delta in data.get("ability_scores", {}).items():
            ability = ability.lower()
            effects["ability_scores"][ability] = effects["ability_scores"].get(ability, 0) + int(delta)

        # skills
        for skill, delta in data.get("skills", {}).items():
            effects["skills"][skill] = effects["skills"].get(skill, 0) + int(delta)

        # ac_bonus
        if "ac_bonus" in data:
            effects["ac_bonus"] += int(data["ac_bonus"])

        # speed_bonus
        if "speed_bonus" in data:
            effects["speed_bonus"] += int(data["speed_bonus"])

        # proficiencies
        for ptype, names in data.get("proficiencies", {}).items():
            if ptype not in effects["proficiencies"]:
                effects["proficiencies"][ptype] = []
            for name in names:
                if name not in effects["proficiencies"][ptype]:
                    effects["proficiencies"][ptype].append(name)

    return effects


# ------------------------------------------------------------
# SPELLS
# ------------------------------------------------------------
def load_character_spells(character_id: int):
    rows = fetch_all(
        """
        SELECT s.SpellID, s.Name, s.Level, s.School,
               s.CastingTime, s.Range, s.Components,
               s.Duration, s.Description
        FROM character_spell cs
        JOIN spell s ON cs.SpellID = s.SpellID
        WHERE cs.CharacterID = %s
        """,
        (character_id,)
    )

    return [
        {
            "id": r["SpellID"],
            "name": r["Name"],
            "level": r["Level"],
            "school": r["School"],
            "casting_time": r["CastingTime"],
            "range": r["Range"],
            "components": r["Components"],
            "duration": r["Duration"],
            "description": r["Description"]
        }
        for r in rows
    ]


# ------------------------------------------------------------
# EQUIPMENT + ARMOR + WEAPONS
# ------------------------------------------------------------
def load_character_equipment(character_id: int):
    rows = fetch_all(
        """
        SELECT e.EquipmentID, e.Name, e.Type, e.Properties,
               e.Weight, e.CostDesc,
               e.DamageDice, e.DamageType
        FROM character_equipment ce
        JOIN equipment e ON ce.EquipmentID = e.EquipmentID
        WHERE ce.CharacterID = %s
        """,
        (character_id,)
    )

    total_weight = 0.0
    items = []

    armor_base_ac = None
    armor_max_dex = None
    shield_bonus = 0
    speed_bonus = 0  # reserved for future use

    for r in rows:
        w = float(r["Weight"]) if r["Weight"] is not None else 0.0
        total_weight += w

        etype = (r["Type"] or "").lower()
        props = (r["Properties"] or "")

        if "armor" in etype:
            if "light" in etype:
                armor_base_ac = 11
                armor_max_dex = None
            elif "medium" in etype:
                armor_base_ac = 12
                armor_max_dex = 2
            elif "heavy" in etype:
                armor_base_ac = 16
                armor_max_dex = 0
        elif "shield" in etype:
            shield_bonus += 2

        items.append({
            "id": r["EquipmentID"],
            "name": r["Name"],
            "type": r["Type"],
            "properties": props,
            "weight": w,
            "cost": r["CostDesc"],
            "damage_dice": r.get("DamageDice") if isinstance(r, dict) else r["DamageDice"] if "DamageDice" in r else None,
            "damage_type": r.get("DamageType") if isinstance(r, dict) else r["DamageType"] if "DamageType" in r else None
        })

    return {
        "items": items,
        "total_weight": total_weight,
        "armor_base_ac": armor_base_ac,
        "armor_max_dex": armor_max_dex,
        "shield_bonus": shield_bonus,
        "speed_bonus": speed_bonus
    }


def build_movement_and_armor_flags(equipment, scores, effects):
    total_weight = equipment["total_weight"]
    str_score = scores["str"]

    base_speed = 30 + effects.get("speed_bonus", 0)

    # Encumbrance thresholds
    light_threshold = str_score * 5
    heavy_threshold = str_score * 10

    if total_weight <= light_threshold:
        encumbrance = "Light"
        speed_penalty = 0
    elif total_weight <= heavy_threshold:
        encumbrance = "Normal"
        speed_penalty = 0
    else:
        encumbrance = "Heavy"
        speed_penalty = -10

    # Armor flags
    stealth_disadvantage = False
    heavy_armor_str_requirement_failed = False

    for item in equipment["items"]:
        etype = (item["type"] or "").lower()
        props = (item["properties"] or "").lower()

        if "armor" in etype:
            if "stealth disadvantage" in props:
                stealth_disadvantage = True

            if "heavy" in etype:
                # Try to parse STR requirement from properties, else default 15
                required_str = 15
                # crude parse: look for "str" and a number
                for token in props.replace(",", " ").split():
                    if token.isdigit():
                        required_str = int(token)
                        break
                if str_score < required_str:
                    heavy_armor_str_requirement_failed = True

    if heavy_armor_str_requirement_failed:
        speed_penalty -= 10

    final_speed = max(0, base_speed + speed_penalty)

    return {
        "speed": final_speed,
        "encumbrance": encumbrance,
        "stealth_disadvantage": stealth_disadvantage,
        "heavy_armor_str_requirement_failed": heavy_armor_str_requirement_failed
    }


def build_combat_profile(equipment, mods, profs, prof_bonus):
    weapons = []
    can_two_weapon_fight = False

    weapon_profs = [p["name"] for p in profs["Weapon"]]

    melee_light_weapons = 0

    for item in equipment["items"]:
        etype = (item["type"] or "").lower()
        props = (item["properties"] or "").lower()

        if "weapon" not in etype:
            continue

        is_ranged = "ranged" in props or "thrown" in props
        is_finesse = "finesse" in props
        is_light = "light" in props

        # Determine ability used
        if is_ranged:
            ability_used = "dex"
        elif is_finesse:
            ability_used = "dex" if mods["dex"] >= mods["str"] else "str"
        else:
            ability_used = "str"

        ability_mod_value = mods[ability_used]

        # Very simple proficiency assumption: if any weapon proficiency exists, treat as proficient
        proficient = len(weapon_profs) > 0
        attack_bonus = ability_mod_value + (prof_bonus if proficient else 0)

        damage_dice = item.get("damage_dice")
        damage_type = item.get("damage_type")
        damage_str = None
        if damage_dice:
            sign = "+" if ability_mod_value >= 0 else "-"
            damage_str = f"{damage_dice} {sign} {abs(ability_mod_value)}"
        else:
            damage_str = None

        weapons.append({
            "id": item["id"],
            "name": item["name"],
            "attack_bonus": attack_bonus,
            "damage": damage_str,
            "damage_dice": damage_dice,
            "damage_type": damage_type,
            "ability_used": ability_used.upper(),
            "properties": [p.strip() for p in (item["properties"] or "").split(",") if p.strip()]
        })

        if not is_ranged and is_light:
            melee_light_weapons += 1

    if melee_light_weapons >= 2:
        can_two_weapon_fight = True

    return {
        "weapons": weapons,
        "can_two_weapon_fight": can_two_weapon_fight
    }


# ------------------------------------------------------------
# SPELLCASTING SUPPORT (DATA-DRIVEN)
# ------------------------------------------------------------
def load_spellcasting_progression(class_id: int, level: int):
    row = fetch_one(
        """
        SELECT Slots1, Slots2, Slots3, Slots4, Slots5,
               Slots6, Slots7, Slots8, Slots9
        FROM class_spellcasting
        WHERE ClassID = %s AND Level = %s
        """,
        (class_id, level)
    )

    if not row:
        return None

    return {
        1: row["Slots1"],
        2: row["Slots2"],
        3: row["Slots3"],
        4: row["Slots4"],
        5: row["Slots5"],
        6: row["Slots6"],
        7: row["Slots7"],
        8: row["Slots8"],
        9: row["Slots9"],
    }


def get_spellcasting_ability(class_id: int):
    row = fetch_one(
        "SELECT SpellcastingAbility FROM class WHERE ClassID = %s",
        (class_id,)
    )
    if not row or not row["SpellcastingAbility"]:
        return None
    return row["SpellcastingAbility"].lower()


# ------------------------------------------------------------
# MAIN RECALC ENGINE
# ------------------------------------------------------------
def recalc_character(character_id: int):
    # -----------------------------
    # LOAD CHARACTER CORE DATA
    # -----------------------------
    char = fetch_one("SELECT * FROM characters WHERE CharacterID = %s", (character_id,))
    if not char:
        raise ValueError("Character not found")

    level = char["Level"]
    class_id = char["ClassID"]
    race_id = char["RaceID"]

    # -----------------------------
    # LOAD ABILITY SCORES
    # -----------------------------
    ab = fetch_one("SELECT * FROM abilityscores WHERE CharacterID = %s", (character_id,))
    if not ab:
        raise ValueError("Ability scores missing")

    scores = {
        "str": ab["StrScore"],
        "dex": ab["DexScore"],
        "con": ab["ConScore"],
        "int": ab["IntScore"],
        "wis": ab["WisScore"],
        "cha": ab["ChaScore"]
    }
    # -----------------------------
    # LOAD FEATS + EFFECTS (ABILITY SCORE BONUSES)
    # -----------------------------
    feats = load_character_feats(character_id)
    effects = parse_feat_effects(feats)

    for ability, delta in effects.get("ability_scores", {}).items():
        if ability in scores:
            scores[ability] += int(delta)

    # -----------------------------
    # RECOMPUTE ABILITY MODIFIERS
    # -----------------------------
    mods = {k: ability_mod(v) for k, v in scores.items()}

    # -----------------------------
    # CLASS HIT DICE + HP
    # -----------------------------
    cls = fetch_one("SELECT HitDiceType FROM class WHERE ClassID = %s", (class_id,))
    if not cls:
        raise ValueError("Class not found")

    hit_die = cls["HitDiceType"] or "d8"

    first_level_hp = int(hit_die.replace("d", "")) + mods["con"]
    if first_level_hp < 1:
        first_level_hp = 1

    if level == 1:
        max_hp = first_level_hp
    else:
        avg = average_hit_die(hit_die)
        max_hp = first_level_hp + (level - 1) * (avg + mods["con"])

    if max_hp < 1:
        max_hp = 1

    # -----------------------------
    # PROFICIENCY BONUS
    # -----------------------------
    prof_bonus = proficiency_bonus(level)

    # -----------------------------
    # LOAD FEATURES, PERSONALITY, PROFS, SPELLS, EQUIPMENT
    # -----------------------------
    features = load_features_for_character(char)
    personality = load_personality(character_id)
    profs = load_character_proficiencies(character_id)
    # extend proficiencies with feat effects before skills/saves
    profs = extend_proficiencies_with_effects(profs, effects)
    spells = load_character_spells(character_id)
    equipment = load_character_equipment(character_id)

    # -----------------------------
    # SKILLS, SAVING THROWS, PASSIVES (WITH FEAT SKILL BONUSES)
    # -----------------------------
    skills = compute_skills(mods, profs, prof_bonus)
    # apply feat skill bonuses
    for skill_name, bonus in effects.get("skills", {}).items():
        if skill_name in skills:
            skills[skill_name] += int(bonus)
    saving_throws = compute_saving_throws(mods, profs, prof_bonus)
    passives = compute_passives(skills)

    # -----------------------------
    # INITIATIVE
    # -----------------------------
    initiative = mods["dex"]

    # -----------------------------
    # MOVEMENT & ARMOR FLAGS
    # -----------------------------
    movement = build_movement_and_armor_flags(equipment, scores, effects)

    # -----------------------------
    # COMBAT PROFILE (WEAPONS)
    # -----------------------------
    combat_profile = build_combat_profile(equipment, mods, profs, prof_bonus)

    # -----------------------------
    # FINAL ARMOR CLASS (WITH FEAT AC BONUS)
    # -----------------------------
    armor_base = equipment["armor_base_ac"]
    armor_max_dex = equipment["armor_max_dex"]
    shield_bonus = equipment["shield_bonus"]
    ac_bonus = effects.get("ac_bonus", 0)

    if armor_base is None:
        final_ac = 10 + mods["dex"] + shield_bonus + ac_bonus
    else:
        if armor_max_dex is None:
            dex_contrib = mods["dex"]
        else:
            dex_contrib = min(mods["dex"], armor_max_dex)
        final_ac = armor_base + dex_contrib + shield_bonus + ac_bonus

    # -----------------------------
    # SPELLCASTING (DATA-DRIVEN)
    # -----------------------------
    spellcasting_ability = get_spellcasting_ability(class_id)

    if spellcasting_ability:
        ability_mod_value = mods[spellcasting_ability]
        spell_save_dc = 8 + prof_bonus + ability_mod_value
        spell_attack_bonus = prof_bonus + ability_mod_value
        slots = load_spellcasting_progression(class_id, level)
    else:
        spell_save_dc = None
        spell_attack_bonus = None
        slots = None

    # -----------------------------
    # UPDATE DATABASE: ABILITY SCORES
    # -----------------------------
    execute(
        """
        UPDATE abilityscores
        SET StrScore=%s, StrMod=%s,
            DexScore=%s, DexMod=%s,
            ConScore=%s, ConMod=%s,
            IntScore=%s, IntMod=%s,
            WisScore=%s, WisMod=%s,
            ChaScore=%s, ChaMod=%s
        WHERE CharacterID=%s
        """,
        (
            scores["str"], mods["str"],
            scores["dex"], mods["dex"],
            scores["con"], mods["con"],
            scores["int"], mods["int"],
            scores["wis"], mods["wis"],
            scores["cha"], mods["cha"],
            character_id
        )
    )

    # -----------------------------
    # UPDATE DATABASE: CHARACTERS
    # -----------------------------
    execute(
        """
        UPDATE characters
        SET ProficiencyBonus=%s,
            UpdatedAt=%s
        WHERE CharacterID=%s
        """,
        (prof_bonus, datetime.utcnow(), character_id)
    )

    # -----------------------------
    # UPDATE DATABASE: COMBAT STATS
    # -----------------------------
    execute(
        """
        UPDATE combatstats
        SET MaxHP=%s,
            HP=%s,
            HitDiceTotal=%s,
            HitDiceRemaining=%s,
            ArmorClass=%s,
            Initiative=%s,
            PassivePerception=%s
        WHERE CharacterID=%s
        """,
        (
            max_hp,
            max_hp,
            f"{level}{hit_die}",
            f"{level}{hit_die}",
            final_ac,
            initiative,
            passives["Perception"],
            character_id
        )
    )

    # -----------------------------
    # UPDATE DATABASE: SPELL SLOTS
    # -----------------------------
    if slots:
        execute("DELETE FROM spellslot WHERE CharacterID = %s", (character_id,))
        for lvl, count in slots.items():
            if count and count > 0:
                execute(
                    """
                    INSERT INTO spellslot (CharacterID, SpellLevel, SlotsTotal, SlotsRemaining)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (character_id, lvl, count, count)
                )

    # -----------------------------
    # RETURN FULL SHEET OBJECT
    # -----------------------------
    return {
        "success": True,
        "character_id": character_id,
        "updated": {
            "scores": scores,
            "mods": mods,
            "max_hp": max_hp,
            "prof_bonus": prof_bonus,
            "ac": final_ac,
            "initiative": initiative,
            "skills": skills,
            "saving_throws": saving_throws,
            "passives": passives,
            "features": features,
            "personality": personality,
            "proficiencies": profs,
            "feats": feats,
            "spells": spells,
            "equipment": equipment,
            "movement": movement,
            "combat_profile": combat_profile,
            "spellcasting": {
                "ability": spellcasting_ability,
                "spell_save_dc": spell_save_dc,
                "spell_attack_bonus": spell_attack_bonus,
                "slots": slots
            },
            "applied_effects": effects
        }
    }