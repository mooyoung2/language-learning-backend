from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # 학습 정보
    target_language = Column(String, default="영어")
    level = Column(String, default="A1")  # A1, A2, B1, B2, C1, C2
    
    # 통계
    total_study_time = Column(Integer, default=0)  # 분 단위
    total_conversations = Column(Integer, default=0)
    total_words_learned = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)  # 연속 학습일
    
    # 날짜
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # 관계
    conversations = relationship("Conversation", back_populates="user")
    vocabularies = relationship("Vocabulary", back_populates="user")