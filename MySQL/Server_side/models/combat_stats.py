from sqlalchemy import Column, Integer, ForeignKey
from Server_side.db import Base

class CombatStats(Base):
    __tablename__ = "combat_stats"

    CharacterID = Column(Integer, ForeignKey("characters.CharacterID", ondelete="CASCADE"), primary_key=True)

    MaxHP = Column(Integer, nullable=False, default=10)
    CurrentHP = Column(Integer, nullable=False, default=10)
    TempHP = Column(Integer, nullable=False, default=0)

    HitDiceType = Column(Integer, nullable=False, default=0)
    HitDiceTotal = Column(Integer, nullable=False, default=1)
    HitDiceRemaining = Column(Integer, nullable=False, default=1)

    ArmorClass = Column(Integer, nullable=False, default=10)
    Initiative = Column(Integer, nullable=False, default=0)
    Speed = Column(Integer, nullable=False, default=30)