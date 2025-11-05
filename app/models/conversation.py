from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    grammar_correction = Column(Text)
    pronunciation_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="conversations") 