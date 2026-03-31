from pydantic import BaseModel

class SubclassSelectRequest(BaseModel):
    subclass_id: int  # 1 = Champion (for now)

class SubclassSelectResponse(BaseModel):
    character_id: int
    subclass_id: int
    message: str