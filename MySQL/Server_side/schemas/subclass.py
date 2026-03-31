# Server_side/schemas/subclass.py

from pydantic import BaseModel

class SubclassSelectRequest(BaseModel):
    subclass_id: int


class SubclassSelectResponse(BaseModel):
    character_id: int
    subclass_id: int
    message: str