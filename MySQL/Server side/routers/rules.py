# routers/rules.py
from fastapi import APIRouter, HTTPException
from database.core import fetch_all, fetch_one

router = APIRouter(prefix="/api/rules", tags=["rules"])

# -----------------------------
# RACES + RACE ABILITIES
# -----------------------------
@router.get("/races")
async def get_races():
    races = fetch_all("SELECT RaceID, Name, Description FROM race")

    result = []
    for r in races:
        abilities = fetch_all(
            "SELECT AbilityName, ValueOrDesc FROM raceability WHERE RaceID = %s",
            (r["RaceID"],)
        )

        # Convert ability bonuses into structured fields
        ability_bonuses = {}
        features = []

        for a in abilities:
            name = a["AbilityName"]
            val = a["ValueOrDesc"]

            # If it's a numeric ability bonus like "STR +2"
            if name.lower() in ["str", "dex", "con", "int", "wis", "cha"]:
                try:
                    ability_bonuses[name.lower()] = int(val)
                except:
                    features.append({"name": name, "desc": val})
            else:
                features.append({"name": name, "desc": val})

        result.append({
            "id": r["RaceID"],
            "name": r["Name"],
            "description": r["Description"],
            "ability_bonuses": ability_bonuses,
            "features": features
        })

    return result


# -----------------------------
# CLASSES + SUBCLASSES + FEATURES
# -----------------------------
@router.get("/classes")
async def get_classes():
    classes = fetch_all("SELECT ClassID, Name, HitDiceType, Spellcasting FROM class")

    result = []
    for c in classes:
        subclasses = fetch_all(
            "SELECT SubclassID, Name, Description FROM subclass WHERE ClassID = %s",
            (c["ClassID"],)
        )

        features = fetch_all(
            "SELECT FeatureID, Name, Description, SubclassID FROM classfeature WHERE ClassID = %s",
            (c["ClassID"],)
        )

        # Group features by subclass
        subclass_features = {}
        base_features = []

        for f in features:
            if f["SubclassID"] is None:
                base_features.append({
                    "id": f["FeatureID"],
                    "name": f["Name"],
                    "desc": f["Description"]
                })
            else:
                sid = f["SubclassID"]
                if sid not in subclass_features:
                    subclass_features[sid] = []
                subclass_features[sid].append({
                    "id": f["FeatureID"],
                    "name": f["Name"],
                    "desc": f["Description"]
                })

        # Attach features to subclasses
        subclass_list = []
        for sc in subclasses:
            subclass_list.append({
                "id": sc["SubclassID"],
                "name": sc["Name"],
                "description": sc["Description"],
                "features": subclass_features.get(sc["SubclassID"], [])
            })

        result.append({
            "id": c["ClassID"],
            "name": c["Name"],
            "hit_dice": c["HitDiceType"],
            "spellcasting": bool(c["Spellcasting"]),
            "features": base_features,
            "subclasses": subclass_list
        })

    return result


# -----------------------------
# PROFICIENCIES
# -----------------------------
@router.get("/proficiencies")
async def get_proficiencies():
    rows = fetch_all("SELECT ProficiencyID, Name, Type FROM proficiency")

    result = []
    for p in rows:
        result.append({
            "id": p["ProficiencyID"],
            "name": p["Name"],
            "type": p["Type"]  # Skill, SavingThrow, Tool, Armor, Weapon, Language, Item
        })

    return result


# -----------------------------
# FEATS
# -----------------------------
@router.get("/feats")
async def get_feats():
    feats = fetch_all("SELECT FeatID, Name, Description, Prerequisite FROM feat")

    return [
        {
            "id": f["FeatID"],
            "name": f["Name"],
            "description": f["Description"],
            "prerequisite": f["Prerequisite"]
        }
        for f in feats
    ]


# -----------------------------
# SPELLS
# -----------------------------
@router.get("/spells")
async def get_spells():
    spells = fetch_all("""
        SELECT SpellID, Name, Level, School, CastingTime, Range,
               Components, Duration, Description
        FROM spell
    """)

    result = []
    for s in spells:
        result.append({
            "id": s["SpellID"],
            "name": s["Name"],
            "level": s["Level"],
            "school": s["School"],
            "casting_time": s["CastingTime"],
            "range": s["Range"],
            "components": s["Components"],
            "duration": s["Duration"],
            "description": s["Description"]
        })

    return result


# -----------------------------
# EQUIPMENT
# -----------------------------
@router.get("/equipment")
async def get_equipment():
    items = fetch_all("""
        SELECT EquipmentID, Name, Type, Properties, Weight, CostDesc
        FROM equipment
    """)

    result = []
    for e in items:
        result.append({
            "id": e["EquipmentID"],
            "name": e["Name"],
            "type": e["Type"],  # Weapon, Armor, Gear, etc.
            "properties": e["Properties"],
            "weight": float(e["Weight"]) if e["Weight"] is not None else None,
            "cost": e["CostDesc"]
        })

    return result


@router.get("/spellcasting/{class_id}")
async def get_spellcasting_progression(class_id: int):
    rows = fetch_all(
        """
        SELECT Level, Slots1, Slots2, Slots3, Slots4, Slots5,
               Slots6, Slots7, Slots8, Slots9
        FROM class_spellcasting
        WHERE ClassID = %s
        ORDER BY Level ASC
        """,
        (class_id,)
    )

    return [
        {
            "level": r["Level"],
            "slots": {
                1: r["Slots1"],
                2: r["Slots2"],
                3: r["Slots3"],
                4: r["Slots4"],
                5: r["Slots5"],
                6: r["Slots6"],
                7: r["Slots7"],
                8: r["Slots8"],
                9: r["Slots9"],
            }
        }
        for r in rows
    ]


# -----------------------------
# BACKGROUNDS + FEATURES
# -----------------------------
@router.get("/backgrounds")
async def get_backgrounds():
    backgrounds = fetch_all("SELECT BackgroundID, Name, Description FROM background")

    result = []
    for b in backgrounds:
        features = fetch_all(
            "SELECT Name, Description FROM backgroundfeature WHERE BackgroundID = %s",
            (b["BackgroundID"],)
        )

        result.append({
            "id": b["BackgroundID"],
            "name": b["Name"],
            "description": b["Description"],
            "features": [{"name": f["Name"], "desc": f["Description"]} for f in features]
        })

    return result


# -----------------------------
# ALIGNMENTS
# -----------------------------
@router.get("/alignments")
async def get_alignments():
    aligns = fetch_all("SELECT AlignmentID, Name, Description FROM alignment")

    return [
        {
            "id": a["AlignmentID"],
            "name": a["Name"],
            "description": a["Description"]
        }
        for a in aligns
    ]