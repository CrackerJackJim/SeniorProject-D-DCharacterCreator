# assets/apply_features.py

from sqlalchemy import insert, select
from Server_side.models import CharacterFeatures, CharacterSubclasses
from Server_side.assets.classes import FIGHTER_FEATURES
from Server_side.assets.subclasses import CHAMPION_FEATURES

async def apply_fighter_features(session, character_id: int, new_level: int, features_out: list[str]):
    if new_level in FIGHTER_FEATURES:
        for feat in FIGHTER_FEATURES[new_level]:
            features_out.append(feat)

            await session.execute(
                insert(CharacterFeatures).values(
                    CharacterID=character_id,
                    Source="Class",
                    SourceName="Fighter",
                    LevelGained=new_level,
                    FeatureName=feat
                )
            )


async def apply_subclass_features(session, character_id: int, new_level: int, features_out: list[str]):
    result = await session.execute(
        select(CharacterSubclasses).where(CharacterSubclasses.CharacterID == character_id)
    )
    subclasses = result.scalars().all()

    for subclass in subclasses:
        subclass_id = subclass.SubclassID

        # Champion only for now; adjust ID to match your DB
        if subclass_id == 1:
            if new_level in CHAMPION_FEATURES:
                for feat in CHAMPION_FEATURES[new_level]:
                    features_out.append(feat)

                    await session.execute(
                        insert(CharacterFeatures).values(
                            CharacterID=character_id,
                            Source="Subclass",
                            SourceName="Champion",
                            LevelGained=new_level,
                            FeatureName=feat
                        )
                    )