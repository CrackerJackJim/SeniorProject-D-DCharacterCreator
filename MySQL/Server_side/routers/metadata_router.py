# routers/metadata_router.py
from fastapi import APIRouter
from Server_side.database.core import fetch_all

router = APIRouter(prefix="/meta", tags=["metadata"])

# -----------------------------
# RACES
# -----------------------------
@router.get("/races")
async def get_races():
    return await fetch_all("""
        SELECT 
            RaceID AS id,
            Name AS name,
            Description AS description
        FROM race
        ORDER BY Name;
    """)

# -----------------------------
# CLASSES
# -----------------------------
@router.get("/classes")
async def get_classes():
    return await fetch_all("""
        SELECT 
            ClassID AS id,
            Name AS name
        FROM class
        ORDER BY Name;
    """)

# -----------------------------
# BACKGROUNDS
# -----------------------------
@router.get("/backgrounds")
async def get_backgrounds():
    return await fetch_all("""
        SELECT 
            BackgroundID AS id,
            Name AS name,
            Description AS description
        FROM background
        ORDER BY Name;
    """)

# -----------------------------
# ALIGNMENTS
# -----------------------------
@router.get("/alignments")
async def get_alignments():
    return await fetch_all("""
        SELECT 
            AlignmentID AS id,
            Name AS name,
            Description AS description
        FROM alignment
        ORDER BY Name;
    """)

# -----------------------------
# SUBCLASSES (per class)
# -----------------------------
@router.get("/subclasses/{class_id}")
async def get_subclasses(class_id: int):
    return await fetch_all("""
        SELECT 
            SubclassID AS id,
            Name AS name,
            Description AS description
        FROM subclass
        WHERE ClassID = %s
        ORDER BY Name;
    """, (class_id,))

# -----------------------------
# PROFICIENCIES
# -----------------------------
@router.get("/proficiencies")
async def get_proficiencies():
    return await fetch_all("""
        SELECT 
            ProficiencyID AS id,
            Name AS name,
            Type AS type
        FROM proficiency
        ORDER BY Name;
    """)

# -----------------------------
# EQUIPMENT
# -----------------------------
@router.get("/equipment")
async def get_equipment():
    return await fetch_all("""
        SELECT 
            EquipmentID AS id,
            Name AS name,
            Type AS type,
            Properties AS properties,
            Weight AS weight,
            CostDesc AS cost
        FROM equipment
        ORDER BY Name;
    """)

# -----------------------------
# SPELLS
# -----------------------------
@router.get("/spells")
async def get_spells():
    return await fetch_all("""
        SELECT
            SpellID AS id,
            Name AS name,
            Level AS level,
            School AS school,
            `Range` AS spell_range,
            `Components` AS components,
            `Duration` AS duration,
            CastingTime AS casting_time,
            Description AS description
        FROM spell
        ORDER BY Level, Name;
    """)

# -----------------------------
# FEATS
# -----------------------------
@router.get("/feats")
async def get_feats():
    return await fetch_all("""
        SELECT 
            FeatID AS id,
            Name AS name,
            Description AS description,
            Prerequisite AS prerequisite
        FROM feat
        ORDER BY Name;
    """)