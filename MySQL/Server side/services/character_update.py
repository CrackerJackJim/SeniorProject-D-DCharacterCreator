from typing import Any, Dict
from database.core import get_db, release_db


# ------------------------------------------------------------
# UPDATE FULL CHARACTER SHEET
# ------------------------------------------------------------
def update_character_full(char_id: int, sheet: Dict[str, Any]) -> None:
    conn = get_db()
    try:
        with conn.cursor() as cur:

            # -----------------------------
            # UPDATE characters TABLE
            # -----------------------------
            cur.execute("""
                UPDATE characters
                SET Name=%s,
                    Level=%s,
                    Experience=%s,
                    ProficiencyBonus=%s
                WHERE CharacterID=%s
            """, (
                sheet.get("name"),
                int(sheet.get("level", 1)),
                int(sheet.get("experience", 0)),
                sheet.get("proficiency_bonus"),
                char_id
            ))

            # -----------------------------
            # UPDATE abilityscores TABLE
            # -----------------------------
            scores = sheet.get("scores", {})
            mods = sheet.get("mods", {})

            cur.execute("""
                INSERT INTO abilityscores
                    (CharacterID, StrScore, StrMod, DexScore, DexMod,
                     ConScore, ConMod, IntScore, IntMod, WisScore, WisMod,
                     ChaScore, ChaMod)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    StrScore=VALUES(StrScore), StrMod=VALUES(StrMod),
                    DexScore=VALUES(DexScore), DexMod=VALUES(DexMod),
                    ConScore=VALUES(ConScore), ConMod=VALUES(ConMod),
                    IntScore=VALUES(IntScore), IntMod=VALUES(IntMod),
                    WisScore=VALUES(WisScore), WisMod=VALUES(WisMod),
                    ChaScore=VALUES(ChaScore), ChaMod=VALUES(ChaMod)
            """, (
                char_id,
                int(scores.get("str", 10)), int(mods.get("str", 0)),
                int(scores.get("dex", 10)), int(mods.get("dex", 0)),
                int(scores.get("con", 10)), int(mods.get("con", 0)),
                int(scores.get("int", 10)), int(mods.get("int", 0)),
                int(scores.get("wis", 10)), int(mods.get("wis", 0)),
                int(scores.get("cha", 10)), int(mods.get("cha", 0)),
            ))

            # -----------------------------
            # UPDATE combatstats TABLE
            # -----------------------------
            movement = sheet.get("movement", {}) or {}

            cur.execute("""
                INSERT INTO combatstats
                    (CharacterID, HP, MaxHP, ArmorClass, Speed, Initiative, Money)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    HP=VALUES(HP),
                    MaxHP=VALUES(MaxHP),
                    ArmorClass=VALUES(ArmorClass),
                    Speed=VALUES(Speed),
                    Initiative=VALUES(Initiative),
                    Money=VALUES(Money)
            """, (
                char_id,
                int(sheet.get("max_hp") or 1),
                int(sheet.get("max_hp") or 1),
                sheet.get("ac"),
                movement.get("speed"),
                sheet.get("initiative"),
                sheet.get("money"),
            ))

            # -----------------------------
            # UPDATE equipment TABLE
            # -----------------------------
            cur.execute("DELETE FROM character_equipment WHERE CharacterID=%s", (char_id,))
            for e in sheet.get("equipment", []):
                name = e.get("name")
                if not name:
                    continue

                cur.execute("SELECT EquipmentID FROM equipment WHERE Name=%s", (name,))
                row = cur.fetchone()
                if not row:
                    continue

                equip_id = row["EquipmentID"]
                qty = int(e.get("quantity") or 1)

                cur.execute("""
                    INSERT INTO character_equipment (CharacterID, EquipmentID, Quantity)
                    VALUES (%s,%s,%s)
                """, (char_id, equip_id, qty))

            # -----------------------------
            # UPDATE proficiencies TABLE
            # -----------------------------
            cur.execute("DELETE FROM character_proficiency WHERE CharacterID=%s", (char_id,))
            for p in sheet.get("proficiencies", []):
                name = p.get("name")
                ptype = p.get("type")
                if not name or not ptype:
                    continue

                cur.execute("""
                    SELECT ProficiencyID FROM proficiency
                    WHERE Name=%s AND Type=%s
                """, (name, ptype))
                row = cur.fetchone()
                if not row:
                    continue

                prof_id = row["ProficiencyID"]

                cur.execute("""
                    INSERT INTO character_proficiency (CharacterID, ProficiencyID, Expertise)
                    VALUES (%s,%s,'Normal')
                """, (char_id, prof_id))

            # -----------------------------
            # UPDATE feats TABLE
            # -----------------------------
            cur.execute("DELETE FROM character_feat WHERE CharacterID=%s", (char_id,))
            for f in sheet.get("features", []):
                name = f.get("name")
                if not name:
                    continue

                cur.execute("SELECT FeatID FROM feat WHERE Name=%s", (name,))
                row = cur.fetchone()
                if not row:
                    continue

                feat_id = row["FeatID"]

                cur.execute("""
                    INSERT INTO character_feat (CharacterID, FeatID)
                    VALUES (%s,%s)
                """, (char_id, feat_id))

            # -----------------------------
            # UPDATE spells TABLE
            # -----------------------------
            cur.execute("DELETE FROM character_spell WHERE CharacterID=%s", (char_id,))
            spellcasting = sheet.get("spellcasting", {}) or {}

            for sp in spellcasting.get("spells", []):
                name = sp.get("name")
                level = sp.get("level")
                if not name:
                    continue

                cur.execute("""
                    SELECT SpellID FROM spell
                    WHERE Name=%s AND Level=%s
                """, (name, level))
                row = cur.fetchone()
                if not row:
                    continue

                spell_id = row["SpellID"]

                cur.execute("""
                    INSERT INTO character_spell (CharacterID, SpellID)
                    VALUES (%s,%s)
                """, (char_id, spell_id))

        conn.commit()

    finally:
        release_db(conn)



# ------------------------------------------------------------
# LOAD FULL CHARACTER SHEET
# ------------------------------------------------------------
def get_full_character_sheet(char_id: int) -> Dict[str, Any]:
    conn = get_db()
    try:
        with conn.cursor() as cur:

            # -----------------------------
            # characters
            # -----------------------------
            cur.execute("""
                SELECT c.CharacterID, c.Name, c.Level, c.Experience, c.ProficiencyBonus,
                       r.Name AS RaceName, cl.Name AS ClassName,
                       b.Name AS BackgroundName, a.Name AS AlignmentName
                FROM characters c
                LEFT JOIN race r ON c.RaceID = r.RaceID
                LEFT JOIN class cl ON c.ClassID = cl.ClassID
                LEFT JOIN background b ON c.BackgroundID = b.BackgroundID
                LEFT JOIN alignment a ON c.AlignmentID = a.AlignmentID
                WHERE c.CharacterID=%s
            """, (char_id,))
            base = cur.fetchone()
            if not base:
                raise ValueError("Character not found")

            # -----------------------------
            # abilityscores
            # -----------------------------
            cur.execute("SELECT * FROM abilityscores WHERE CharacterID=%s", (char_id,))
            ab = cur.fetchone() or {}

            # -----------------------------
            # combatstats
            # -----------------------------
            cur.execute("SELECT * FROM combatstats WHERE CharacterID=%s", (char_id,))
            cs = cur.fetchone() or {}

            # -----------------------------
            # equipment
            # -----------------------------
            cur.execute("""
                SELECT e.Name, ce.Quantity
                FROM character_equipment ce
                JOIN equipment e ON ce.EquipmentID = e.EquipmentID
                WHERE ce.CharacterID=%s
            """, (char_id,))
            equipment = list(cur.fetchall())

            # -----------------------------
            # proficiencies
            # -----------------------------
            cur.execute("""
                SELECT p.Name, p.Type
                FROM character_proficiency cp
                JOIN proficiency p ON cp.ProficiencyID = p.ProficiencyID
                WHERE cp.CharacterID=%s
            """, (char_id,))
            profs = list(cur.fetchall())

            # -----------------------------
            # feats
            # -----------------------------
            cur.execute("""
                SELECT f.Name
                FROM character_feat cf
                JOIN feat f ON cf.FeatID = f.FeatID
                WHERE cf.CharacterID=%s
            """, (char_id,))
            feats = list(cur.fetchall())

            # -----------------------------
            # spells
            # -----------------------------
            cur.execute("""
                SELECT s.Name, s.Level, s.School
                FROM character_spell cs
                JOIN spell s ON cs.SpellID = s.SpellID
                WHERE cs.CharacterID=%s
            """, (char_id,))
            spells = list(cur.fetchall())

        # Build final sheet object
        return {
            "id": base["CharacterID"],
            "name": base["Name"],
            "level": base["Level"],
            "experience": base["Experience"],
            "proficiency_bonus": base["ProficiencyBonus"],
            "race_name": base["RaceName"],
            "class_name": base["ClassName"],
            "background_name": base["BackgroundName"],
            "alignment_name": base["AlignmentName"],

            "scores": {
                "str": ab.get("StrScore"),
                "dex": ab.get("DexScore"),
                "con": ab.get("ConScore"),
                "int": ab.get("IntScore"),
                "wis": ab.get("WisScore"),
                "cha": ab.get("ChaScore"),
            },

            "mods": {
                "str": ab.get("StrMod"),
                "dex": ab.get("DexMod"),
                "con": ab.get("ConMod"),
                "int": ab.get("IntMod"),
                "wis": ab.get("WisMod"),
                "cha": ab.get("ChaMod"),
            },

            "movement": {
                "speed": cs.get("Speed")
            },

            "max_hp": cs.get("MaxHP"),
            "ac": cs.get("ArmorClass"),
            "initiative": cs.get("Initiative"),
            "money": cs.get("Money"),

            "equipment": [
                {"name": e["Name"], "quantity": e["Quantity"], "description": ""}
                for e in equipment
            ],

            "proficiencies": [
                {"name": p["Name"], "type": p["Type"]}
                for p in profs
            ],

            "features": [
                {"name": f["Name"], "description": ""}
                for f in feats
            ],

            "spellcasting": {
                "spells": [
                    {"name": s["Name"], "level": s["Level"], "school": s["School"]}
                    for s in spells
                ]
            },

            "skills": [],
            "combat_profile": {"weapons": []}
        }

    finally:
        release_db(conn)