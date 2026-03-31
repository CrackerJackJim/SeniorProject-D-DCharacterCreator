from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

# Correct absolute import
from Server_side.db import get_session

from Server_side.models import CharacterSubclasses, Characters
from Server_side.schemas.subclass import SubclassSelectRequest, SubclassSelectResponse
from Server_side.schemas.level_up import LevelUpRequest, LevelUpResponse
from Server_side.assets.level_up import level_up_character


# ---------------------------------------------------------
# SUBCLASS ROUTES
# ---------------------------------------------------------
subclass_router = APIRouter(prefix="/api/subclass", tags=["subclass"])


@subclass_router.post("/select/{character_id}", response_model=SubclassSelectResponse)
async def select_subclass(
    character_id: int,
    payload: SubclassSelectRequest,
    session: AsyncSession = Depends(get_session)
):
    char = (await session.execute(
        select(Characters).where(Characters.CharacterID == character_id)
    )).scalar_one_or_none()

    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    if char.Level < 3:
        raise HTTPException(status_code=400, detail="Subclass cannot be selected before level 3")

    existing = (await session.execute(
        select(CharacterSubclasses).where(CharacterSubclasses.CharacterID == character_id)
    )).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Subclass already selected")

    await session.execute(
        insert(CharacterSubclasses).values(
            CharacterID=character_id,
            SubclassID=payload.subclass_id
        )
    )

    await session.commit()

    return SubclassSelectResponse(
        character_id=character_id,
        subclass_id=payload.subclass_id,
        message="Subclass selected successfully"
    )


# ---------------------------------------------------------
# LEVEL UP ROUTE
# ---------------------------------------------------------
levelup_router = APIRouter(prefix="/api", tags=["level_up"])


@levelup_router.post("/characters/{character_id}/level_up", response_model=LevelUpResponse)
async def level_up(character_id: int, payload: LevelUpRequest, session: AsyncSession = Depends(get_session)):
    return await level_up_character(session, character_id, payload)