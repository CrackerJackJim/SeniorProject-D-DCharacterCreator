from sqlalchemy import Column, Integer, String, ForeignKey
from Server_side.db import Base

class CharacterFeatures(Base):
    __tablename__ = "character_features"

    FeatureID = Column(Integer, primary_key=True, autoincrement=True)
    CharacterID = Column(Integer, ForeignKey("characters.CharacterID", ondelete="CASCADE"), nullable=False)

    Source = Column(String(50), nullable=False)          # e.g., "Class", "Subclass"
    SourceName = Column(String(100), nullable=False)     # e.g., "Fighter", "Champion"
    LevelGained = Column(Integer, nullable=False)        # Level when feature unlocked
    FeatureName = Column(String(255), nullable=False)    # e.g., "Second Wind"