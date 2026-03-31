from pydantic import BaseModel
from typing import Optional, List

class LevelUpRequest(BaseModel):
    hp_method: str                # "average", "manual", "auto"
    manual_roll: Optional[int] = None


class LevelUpResponse(BaseModel):
    new_level: int
    hp_gained: int
    new_max_hp: int
    new_current_hp: int
    features_gained: List[str]