from sqlalchemy import Column, Integer, ForeignKey
from Server_side.db import Base

class AbilityScores(Base):
    __tablename__ = "abilityscores"   # <-- IMPORTANT: no underscore in your DB

    CharacterID = Column(Integer, ForeignKey("characters.CharacterID", ondelete="CASCADE"), primary_key=True)

    StrScore = Column(Integer, nullable=False, default=10)
    DexScore = Column(Integer, nullable=False, default=10)
    ConScore = Column(Integer, nullable=False, default=10)
    IntScore = Column(Integer, nullable=False, default=10)
    WisScore = Column(Integer, nullable=False, default=10)
    ChaScore = Column(Integer, nullable=False, default=10)

    StrMod = Column(Integer, nullable=False, default=0)
    DexMod = Column(Integer, nullable=False, default=0)
    ConMod = Column(Integer, nullable=False, default=0)
    IntMod = Column(Integer, nullable=False, default=0)
    WisMod = Column(Integer, nullable=False, default=0)
    ChaMod = Column(Integer, nullable=False, default=0)