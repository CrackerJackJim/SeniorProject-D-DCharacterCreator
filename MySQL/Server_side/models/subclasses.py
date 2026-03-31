from sqlalchemy import Column, Integer, ForeignKey
from Server_side.db import Base

class CharacterSubclasses(Base):
    __tablename__ = "character_subclasses"

    CharacterID = Column(Integer, ForeignKey("characters.CharacterID", ondelete="CASCADE"), primary_key=True)
    SubclassID = Column(Integer, ForeignKey("subclass.SubclassID", ondelete="CASCADE"), primary_key=True)