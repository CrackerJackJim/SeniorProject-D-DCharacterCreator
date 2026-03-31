from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from Server_side.db import Base

class Characters(Base):
    __tablename__ = "characters"

    CharacterID = Column(Integer, primary_key=True, autoincrement=True)
    AccountID = Column(Integer, ForeignKey("account.AccountID", ondelete="CASCADE"), nullable=False)
    Name = Column(String(100), nullable=False)
    Gender = Column(String(50), default="Unspecified")
    Level = Column(Integer, nullable=False, default=1)
    RaceID = Column(Integer, ForeignKey("race.RaceID", ondelete="RESTRICT"), nullable=False)
    ClassID = Column(Integer, ForeignKey("class.ClassID", ondelete="RESTRICT"), nullable=False)
    BackgroundID = Column(Integer, ForeignKey("background.BackgroundID", ondelete="SET NULL"))
    AlignmentID = Column(Integer, ForeignKey("alignment.AlignmentID", ondelete="SET NULL"))
    Experience = Column(Integer, nullable=False, default=0)
    ProficiencyBonus = Column(Integer)
    CreatedAt = Column(DateTime, nullable=False, server_default=func.now())
    UpdatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    PlayerName = Column(String(255))