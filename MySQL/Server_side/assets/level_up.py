from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from Server_side.schemas.level_up import LevelUpRequest, LevelUpResponse
import random

from Server_side.models import Characters, AbilityScores, CombatStats
from Server_side.assets.apply_features import apply_fighter_features, apply_subclass_features


def ability_mod(score: int) -> int:
    return (score - 10) // 2


def proficiency_bonus_for_level(level: int) -> int:
    if level >= 17: return 6
    if level >= 13: return 5
    if level >= 9:  return 4
    if level >= 5:  return 3
    return 2


async def level_up_character(
    session: AsyncSession,
    character_id: int,
    payload: LevelUpRequest
) -> LevelUpResponse:

    # 1) Load core data
    char = (await session.execute(
        select(Characters).where(Characters.CharacterID == character_id)
    )).scalar_one_or_none()

    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    abilities = (await session.execute(
        select(AbilityScores).where(AbilityScores.CharacterID == character_id)
    )).scalar_one_or_none()

    stats = (await session.execute(
        select(CombatStats).where(CombatStats.CharacterID == character_id)
    )).scalar_one_or_none()

    if not abilities or not stats:
        raise HTTPException(status_code=400, detail="Missing ability or combat stats")

    old_level = char.Level
    new_level = old_level + 1

    con_mod = ability_mod(abilities.ConScore)

    # 2) HP gain
    if payload.hp_method == "average":
        base = (stats.HitDiceType // 2) + 1
        roll_value = base

    elif payload.hp_method == "manual":
        if payload.manual_roll is None or not (1 <= payload.manual_roll <= stats.HitDiceType):
            raise HTTPException(status_code=400, detail="Invalid manual roll")
        roll_value = payload.manual_roll

    else:  # auto
        roll_value = random.randint(1, stats.HitDiceType)

    hp_gained = max(1, roll_value + con_mod)
    new_max_hp = stats.MaxHP + hp_gained
    new_current_hp = stats.CurrentHP + hp_gained

    # 3) Update character level + proficiency
    new_prof = proficiency_bonus_for_level(new_level)

    await session.execute(
        update(Characters)
        .where(Characters.CharacterID == character_id)
        .values(Level=new_level, ProficiencyBonus=new_prof)
    )

    # 4) Update combat stats
    await session.execute(
        update(CombatStats)
        .where(CombatStats.CharacterID == character_id)
        .values(
            MaxHP=new_max_hp,
            CurrentHP=new_current_hp,
            HitDiceTotal=stats.HitDiceTotal + 1,
            HitDiceRemaining=stats.HitDiceRemaining + 1,
        )
    )

    # 5) Apply class + subclass features (REAL CODE)
    features_gained: list[str] = []

    await apply_fighter_features(session, character_id, new_level, features_gained)
    await apply_subclass_features(session, character_id, new_level, features_gained)

    # 6) Commit all changes
    await session.commit()

    return LevelUpResponse(
        new_level=new_level,
        hp_gained=hp_gained,
        new_max_hp=new_max_hp,
        new_current_hp=new_current_hp,
        features_gained=features_gained,
    )